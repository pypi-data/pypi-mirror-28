# coding=utf-8
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>

"""

"""

import pickle
import os
import re
import time

import pygame
from pygame.locals import *

from civil.map import triangles
from civil import properties
from civil.model import scenario
from civil.map.los import ccivil as los_ccivil
from civil.map.map import Map


def sign(x):
    """

    Args:
        x: 

    Returns:

    """
    if x > 0:
        return 1
    if x < 0:
        return -1
    return 0


class MapDisplayable(Map):
    """
    This class...
    """

    def __init__(self, size_x, size_y):
        """
        Creates the map.
        """
        Map.__init__(self, size_x, size_y)

        # a cache of file names and icons
        self.file_name_cache = None
        self.icon_cache = {}

        # store the scaling factor
        self.scale_factor = properties.hex_size / properties.hex_los_size

        # no los map yet
        self.los_map = None

    def checkLos(self, start, end, max_distance=3000.0, los_points=100.0, debug=0):
        """
        Calculates a LOS value from the position 'start' towards 'end' to see if the ending
        position can be seen. If it can not be seen then 0 is returned and if it can be seen then 1
        is returned. The coordinates in the position are supposed to be map coordinates, not hex coordinates.
        """
        # TODO use Python code
        return los_ccivil.tracelos(start, end)

    def traceLos(self, start, end, max_distance=3000.0, los_points=100.0, debug=0):
        """
        Calculates a LOS value from the position 'start' towards 'end' to see if the ending
        position can be seen. If it can not be seen then final seen position is returned and if it
        can be seen then 'end' is returned. The coordinates in the position are supposed to be map
        coordinates, not hex coordinates.
        """
        # TODO use Python code
        return los_ccivil.loslimit(start, end)

    def loadFeatureIcon(self, id, path=properties.path_features):
        """
        Loads an icon with the given id and returns it.
        """

        # do we already have loaded the icon?
        if id in self.icon_cache:
            # yes, return it
            return self.icon_cache[id]

        # not yet loaded the icon, so do we already have a cache?
        if self.file_name_cache is None:
            # no, so get a list of all files in the features directory
            allFiles = os.listdir(path)

            # create the regular expression for matching the id in the name
            iconExp = re.compile('^t-.+([0-9]{3}).png$')

            # init the cache to an empty dict
            self.file_name_cache = {}

            # loop over all files in the directory
            for file in allFiles:
                # attempt to match the expression
                match = iconExp.search(file)

                # did it match?
                if match:
                    # yep, set it in the temporary dictionary
                    self.file_name_cache[int(match.group(1))] = path + file

                    # print "MapDisplayable.loadFeatureIcon: found:", path + file

        # we do have a cache at least now
        try:
            file_name = self.file_name_cache[id]
        except:
            # oops, no such id?
            raise RuntimeError("MapDisplayable.loadFeatureIcon: no feature icon with id %d found" % id)

        # load the icon
        icon = pygame.image.load(file_name)

        # set the transparent color
        icon.set_colorkey((255, 255, 255), RLEACCEL)

        # The try block is because editor doesn't use sdl
        try:
            # convert the icon to a more efficient format
            icon = icon.convert()
        except:
            pass

        # store the icon in our cache
        self.icon_cache[id] = icon

        return icon

    def getLosMap(self):
        """
        Returns the LOS map. This is None if no LOS map has been set or created.
        """
        # just return it
        return self.los_map

    def setLosMap(self, los_map):
        """
        Sets the LOS map. This is a matrix with suitable integers, and has been created by the
        caller. The map is simply stored and later used.
        """
        # just store it
        self.los_map = los_map
        # TODO use Python code
        los_ccivil.setlosmap(los_map, properties.hex_size / properties.hex_los_size)

        # the rest is debugging

        print("MapDisplayable.setLosMap: %d %d" % (len(los_map), len(los_map[0])))

    def createLosMap(self):
        """
        Initializes the  internal LOS map. Creates  a matrix where  each hex is represented  by a
        16x16 part. Each triangle  in the hex is filled in into the  matrix. Encoded in each element
        in the large matrix is terrain and height info.
        """

        width, height = self.getSize()
        delta_x = properties.hex_los_delta_x
        delta_y = properties.hex_los_delta_y
        size_hex = properties.hex_los_size

        # constants for big hexes
        dx = properties.hex_delta_x
        dy = properties.hex_delta_y
        sf = int(dx / delta_x)
        print("map size in hexes", scenario.map.getSize())
        w = (width - 1) * dx + dx / 2
        h = height * dy - (dx - dy)
        print("map size in small pixels", w, h)

        # los map dimensions - they are BIGGER then needed
        map_width = w / sf  # width * delta_x + delta_x / 2
        map_height = h / sf  # height * delta_y + (size_hex - delta_y )

        print("MapDisplayable.createLosMap: los map size: %d,%d" % (map_width, map_height))

        # initialize the los map to a n*m matrix of 0:s. this is ugly, but the only way i know of
        self.los_map = [0] * map_height
        for index in range(map_height):
            self.los_map[index] = [0] * map_width

        # now loop over the entire map matrix 
        for y in range(height):
            for x in range(width):
                # get the hex
                hex = self.getHex(x, y)

                # now determine weather we have a odd or even offset and the current row. This is a
                # little bit ugly, but it works. Some artifacts remain on the edges though
                if y % 2 == 0:
                    # the icon is painted as far left as possible
                    coordinates = (x * delta_x - delta_x / 2, y * delta_y - (size_hex - delta_y))
                else:
                    # the icon is indented half a hex to the right.
                    coordinates = (x * delta_x, y * delta_y - (size_hex - delta_y))

                # loop over all terrains
                for triangle_index in range(6):
                    # get the terrain for this triangle                    
                    ter = ord(hex.getTerrain(triangle_index).getCode()) - 65
                    if len(hex.template.terrains) == 7:
                        terc = ord(hex.getTerrain(6).getCode()) - 65
                    else:
                        terc = ord('~') - 65
                    tern = ord(hex.getTerrain((triangle_index + 1) % 6).getCode()) - 65
                    terp = ord(hex.getTerrain((triangle_index - 1) % 6).getCode()) - 65
                    ters = (ter << 26) | (terc << 20) | (terp << 14) | (tern << 8)

                    # get the proper icon that represents the terrain at the given triangle
                    triangle = triangles.triangle_data[triangle_index]

                    # get the triangle height. the method expects 1..6
                    hheight = hex.getHeight() + hex.template.getDeltaHeight(triangle_index + 1)

                    # now set the data for this triangle
                    self.__setTriangleData(triangle, ters, coordinates, hheight, map_width, map_height)

        # Now compute the "real" terrain types
        # in this moment we have for each los_map pixel the hex_height and the triangle terrain type

        # first blits all bitmap hexes to the temp surface
        tmpsurf = pygame.Surface((w, h), pygame.SWSURFACE, 32)
        for y in range(height):
            for x in range(width):
                if (y % 2) == 0:  # copied from terrain_layer.py
                    coordinates = (x * dx - dx / 2, y * dy - (dx - dy))
                else:
                    coordinates = (x * dx, y * dy - (dx - dy))
                hex = self.getHex(x, y)
                iconid = hex.getIconId()
                icon = self.loadFeatureIcon(iconid, properties.path_terrains)
                tmpsurf.blit(icon, coordinates)

        print("the surface is drawn")
        # should clear the features cache ...
        # for each pixel in the los_map, makes a list (9 pixels) w/ the corresponding
        # pixels in the surface, then passes it to C to get the real terrain type

        t = time.time()
        tmppixline = [0] * w

        # TODO use Python code
        los_ccivil.createlosmap(0, self.los_map, w, h)
        for y in range(h):
            for x in range(w):
                tmppixline[x] = tmpsurf.get_at((x, y))
            # TODO use Python code
            los_ccivil.createlosmap(1, tmppixline, 0, y)

        t1 = time.time()
        print("pix array transfered ", t1 - t)
        t = t1

        # TODO use Python code
        los_ccivil.createlosmap(2, self.los_map, 0, 0)

        t1 = time.time()
        print("C createlosmap ", t1 - t)

        print("now HOPE los_map has good terrain values")

    def saveLosMap(self, file_name):
        """
        Saves the created los map into 'file_name' using pickling.
        """
        # precautionsq
        if self.los_map is None:
            # no image? can't save it
            raise RuntimeError("no los map calculated, can't save")

        # open a file for writing
        file = open(file_name, 'wb')

        print("MapDisplayable.saveLosMap: pickling the los map, hang on...")

        start_time = time.time()

        # los created all done, so save it in a binary form
        pickle.dump(self.los_map, file, 1)

        # we're done
        file.close()

        end_time = time.time()

        print("MapDisplayable.saveLosMap: los map pickled:", end_time - start_time)

    def __setTriangleData(self, triangle, ttypes, coordinates, height, w, h):
        """
        This method initializes the part of the los  map that the given triangle covers. Sets the
        type and height info in each position, encoded like this:

        byte 3: unused
        byte 2: unused
        byte 1: terrain type
        byte 0: height divided by 5, ie. a value of 100 means 500m up
        """

        base_x, base_y = coordinates

        # now loop over the entire map matrix 
        for y in range(properties.hex_los_size):
            for x in range(properties.hex_los_size):
                # should this pixel be set for this triangle
                if triangle[y][x] == 1:
                    # create the values to be stored.
                    # value = ( ord (code) << 8 ) + ((height / 5) & 0xff)
                    # and store
                    xx = base_x + x
                    yy = base_y + y

                    # make sure we stay within the surface
                    if xx >= 0 and yy >= 0 and xx < w and yy < h:
                        self.los_map[yy][xx] = ttypes | ((height / 5) & 0xff)
