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

import os
import re

import pygame
from pygame.locals import *

from civil import properties
from civil.model import scenario
from civil.playfield.layer import Layer


class TerrainLayer(Layer):
    """
    This class defines the main terrain layer of the game. It is the lowest layer that is painted
    first and contains all the terrain hexes. All other layers are painted upon this. This class
    knows what all icons look like, and will load the icons for all used hexes in the game.

    This class reads the Map class and blits out all the hexes in it.
    """

    def __init__(self, name):
        """
        Initializes the layer.
        """
        # call superclass constructor
        Layer.__init__(self, name)

        # the icons we have.
        self.icons = {}

        # load the icons
        self.loadIcons()

        # This contains a copy of the current terrain
        self.copiedTerrain = None
        self.invalidateTerrain()

        # Remember size of the backup copy in case of resolution change
        self.gui_width = -1
        self.gui_height = -1

    def updateForResolutionChange(self, oldwidth, oldheight, width, height):
        """
        This method is overridden from Layer. It makes sure the terrain cache is invalidated as
        the resolution has changed. If the new size however is smaller then the cache is simply just
        shrunk a little bit, as the start of the data is perfectly ok.
        """
        # call superclass first
        Layer.updateForResolutionChange(self, oldwidth, oldheight, width, height)

        # precaution to avoid extra work. this should never actually happen
        if oldwidth == width and oldheight == height:
            # oops, raising an exception here to notify that this should be fixed
            raise RuntimeError("oldwidth == width and oldheight == height")

        # copy a subsurface if the new size is smaller than the old size
        if width < oldwidth and height < oldheight:
            # do the copy
            self.copiedTerrain = self.copiedTerrain.subsurface((0, 0, self.width, self.height))

            # now, to avoid having the cache be regenerated anyway in paint() we store the gui
            # dimensions here too, this lets the method know that the cache is valid
            self.gui_width = width
            self.gui_height = height

        else:
            # new size is larger, invalidate the cache
            self.invalidateTerrain()

    def invalidateTerrain(self):
        """

        """
        # Invalid values so terrain will be created first time paint()
        # is called
        self.gui_offset_x = -1
        self.gui_offset_y = -1

    def paintCopy(self, offset_x, offset_y):
        """
        Creates a pristine copy of the terrain so that paint()
        can simply blit directly from there instead of repainting.
        """

        # Paint the whole terrain
        st = pygame.time.get_ticks()
        self.paintTerrain(offset_x, offset_y)

        # paint all extra features
        self.paintFeatures(offset_x, offset_y)

        if scenario.playfield.debug_gfx:
            et = pygame.time.get_ticks()
            print("Paint speed: %d" % (et - st))

        width = scenario.sdl.getWidth()
        height = scenario.sdl.getHeight()
        if self.copiedTerrain:

            # Check if the resolution has changed
            if width != self.gui_width or height != self.gui_height:
                # This may give some garbage collector chance to run?
                self.copiedTerrain = None

        if not self.copiedTerrain:
            # Create the backup surface
            self.copiedTerrain = pygame.Surface((width, height), HWSURFACE)
            self.gui_width = width
            self.gui_height = height

        # Copy it
        self.copiedTerrain.blit(scenario.sdl.getSurface(), (0, 0))
        self.gui_offset_x = offset_x
        self.gui_offset_y = offset_y

        if scenario.playfield.debug_gfx:
            et = pygame.time.get_ticks()
            print("Paint total speed: %d" % (et - st))

    def paint(self, offset_x, offset_y, dirtyrect=None):
        """
        Paints the layer. Loops over all hexes in the Map instance and paints their icons. The
        parameters 'offset_x' and 'offset_y' are the number of hexes the map has been scrolled down or
        to the right. They must be taken into account when painting.
        """

        # If the map has been moved, we must recreate it
        if offset_x != self.gui_offset_x or offset_y != self.gui_offset_y:
            self.paintCopy(offset_x, offset_y)

        # No need to take dirtyrect into account, master painter
        # has set a clip if necessary...
        scenario.sdl.blit(self.copiedTerrain, (0, 0))
        return

    def paintTerrain(self, offset_x, offset_y, dirtyrect=None):
        """

        Args:
            offset_x: 
            offset_y: 
            dirtyrect: 
        """
        # get a list of the hexes
        print("* paintTerrain()")
        hexes = scenario.map.getHexes()

        size_hex = properties.hex_size

        # get the tuple with the visible sizes and extract the x- and y-dimensions
        visible_x, visible_y = scenario.playfield.getVisibleSizeClamped()

        # optimization. avoids dots
        delta_y = self.delta_y
        delta_x = self.delta_x
        delta_x_half = delta_x / 2
        icons = self.icons

        # TODO: we need to convert the pixels in dirtyrect to nice hex offsets so that we know which
        # range to paint. seems to not be too trivial?

        # loop over the hexes in the map. The +1 is so that we paint one more that the normally
        # visible size. This in turn is because we start and finish painting outside the screen
        visible_x = int(visible_x)
        visible_y = int(visible_y)
        for y in range(visible_y):
            for x in range(visible_x):
                # get the hex for that position
                # TODO offset_x, y can be floating point numbers
                offset_x = int(offset_x)
                offset_y = int(offset_y)
                hex = hexes[y + offset_y][x + offset_x]

                # now determine weather we have a odd or even offset and the current row. This is a
                # little bit ugly, but it works. Some artifacts remain on the edges though
                if (offset_y + y) % 2 == 0:
                    # the icon is painted as far left as possible
                    coordinates = (x * delta_x - delta_x_half, y * delta_y - (size_hex - delta_y))

                else:
                    # the icon is indented half a hex to the right.
                    coordinates = (x * delta_x, y * delta_y - (size_hex - delta_y))

                # get the terrain
                iconid = hex.getIconId()

                # now perform the actual raw blit of the icon
                scenario.sdl.blit(icons[iconid], coordinates)

                # Debugging, draws hex lines
                if scenario.playfield.debug_gfx:
                    (cx, cy) = coordinates
                    self.paintDebugging(hex, cx, cy)

    def paintDebugging(self, hex, cx, cy):
        """
        Paints debugging in the map. This will paint a hexagonal grid around the hexes and also
        draw the height for each triangle i a hex.
        """
        # draw the grid
        scenario.sdl.drawLines([((178, 178, 178), (cx + 24, cy), (cx + 48, cy + 12)),
                                ((178, 178, 178), (cx + 24, cy), (cx, cy + 12)),
                                ((178, 178, 178), (cx, cy + 12), (cx, cy + 36))
                                ])

    def paintFeatures(self, offset_x, offset_y):
        """
         """

        # get all features that the map contains
        features = scenario.map.getAllFeatures()

        # do we even have any? no need to waste any cycles if it's empty
        if features == {}:
            # nope, it's empty, get lost
            return

        # get the tuple with the visible sizes (in hexes)
        visible_x, visible_y = scenario.playfield.getVisibleSize()

        # precalculate the min and max possible x and y values
        min_x = offset_x * self.delta_x
        min_y = offset_y * self.delta_y
        max_x = (offset_x + visible_x) * self.delta_x
        max_y = (offset_y + visible_y) * self.delta_y

        print("Minmax paintFeatures")
        print((min_x, min_y, max_x, max_y))

        # no loop over all feature type lists
        for featurelist in list(features.values()):
            # loop over all the single features
            for x, y, id, icon in featurelist:
                # get the size of the icon
                width = icon.get_width()
                height = icon.get_height()

                # we have all data now, is this feature inside the currently visible part of the
                # map?
                if min_x - width <= x < max_x and min_y - height <= y <= max_y:
                    # it's inside, so now do the offset-corrected blit
                    scenario.sdl.blit(icon, (x - min_x, y - min_y))

    def loadIcons(self):
        """
        Loads all needed icons. Iterates through the map and checks which icons are actually used
        and loads them. The icons are stored internally in a map.

        This method will first get the names of all icons that are available and cache them
        teporarily. Then it will iterate through the map and get the terrain ids of all actually
        *used* terrains and using the map load the correct icon.
        """

        # get a list of all files in the icons directory
        allFiles = os.listdir(properties.path_terrains)

        # create the regular expression for matching the id in the name
        iconExp = re.compile('^t-.+([0-9]{3}).png$')

        # temporary map for mapping terrain id to file_name
        names = {}

        # loop over all files in the directory
        for file in allFiles:
            # attempt to match the expression
            match = iconExp.search(file)

            # did it match?
            if match:
                # yep, set it in the temporary dictionary
                names[int(match.group(1))] = os.path.join(properties.path_terrains, file)

        # get the map
        map = scenario.map
        size_x, size_y = map.getSize()

        # loop over the map
        for y in range(size_y):
            for x in range(size_x):
                # get the terrain for the hex
                iconid = map.getHex(x, y).getIconId()

                # do we not have an icon for that terrain?
                if iconid not in self.icons:
                    # no such terrain yet loaded, load it
                    try:
                        icon = pygame.image.load(names[iconid])
                    except:
                        # failed to load it
                        print("TerrainLayer.loadIcons: failed to load: %d, %s" % (iconid, names[iconid]))
                        raise

                    # set the transparent color
                    icon.set_colorkey((255, 255, 255), RLEACCEL)

                    # store them
                    self.icons[iconid] = icon.convert()
