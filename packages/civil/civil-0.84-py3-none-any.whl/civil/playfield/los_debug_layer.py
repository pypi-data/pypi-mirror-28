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

import pygame
from pygame.locals import *

from civil import properties
from civil.model import scenario
from civil.playfield.floating_window_layer import FloatingWindowLayer


class LosDebugLayer(FloatingWindowLayer):
    """
    This class defines a layer that simply visualizes LOS data. It shows the internal LOS data s
    images and thus allows the LOS data to be debugged. It has no use for a normal player, and thus
    this layer should be created only when debugging.

    The layer will show bot the terrain and the height. To toggle these click the map.
    """

    def __init__(self, name):
        """
        Initializes the layer.
        """
        # call superclass constructor
        FloatingWindowLayer.__init__(self, name)

        # grid not shown yet
        self.show_grid = 0

        # init the map
        self.createMap()

        # by default we start the map at the upper left corner
        self.x, self.y = self.getBorderWidth()

        # add some extra spacing, it allows some of the background terrain to show through on the
        # upper and left side of the minimap
        self.x += 5
        self.y += 5

        # no shown line yet
        self.line_start = None
        self.line_mid = None
        self.line_end = None

        # store the scaling factor the scales from world coordinates to los coordinates
        self.scale_factor = properties.hex_size / properties.hex_los_size

        # load the icon for the grids
        self.icon = pygame.image.load(properties.layer_los_debug_icon).convert()

        # set the transparent color for the icon and the surface
        self.icon.set_colorkey((0, 0, 0), RLEACCEL)

    def setLosLines(self, start, end, mid=None):
        """
        Sets the coordinates for the lines that are used to visualize LOS. The passed values are
        all (x,y) pairs and indicate world coordinates, not coordinates local to the LOS map or
        anything. Normal coordinates for units etc.

        A red line will be draw from the starting point towards the mid point. This indicates what
        the unit sees. If mid!=end then a blue line is drawn from mid towards end, to show the parts
        that the unit does not see. If the line of sight goes all the way to the end then mid can be
        set to None (or left at its default value).
        """

        # did we get a start position?
        if start is not None:
            # convert to LOS coordinates
            self.line_start = (start[0] / self.scale_factor, start[1] / self.scale_factor)

        # did we get a end position?
        if end is not None:
            # convert to LOS coordinates
            self.line_end = (end[0] / self.scale_factor, end[1] / self.scale_factor)

        # did we get a mid position?
        if mid is not None:
            # convert to LOS coordinates
            self.line_mid = (mid[0] / self.scale_factor, mid[1] / self.scale_factor)
        else:
            # no mid point, we see all the way
            self.line_mid = None

        # start with an empty output buffer with only the current image blitted into it
        self.output.blit(self.currently_shown, (0, 0))

        # draw the lines and the grid
        self.__drawLines()
        self.__drawGrid()

        # repaint the playfield now that it has changed
        scenario.playfield.needRepaint()

    def createMap(self):
        """
        Creates the minimap. Sets the initial terrain and unit data based on real Map data.
        """
        # get all data
        los_data = scenario.map.getLosMap()

        # get map width and height
        self.width = len(los_data[0])
        self.height = len(los_data)

        # allocate surfaces for ourselves
        self.terrain = pygame.Surface((self.width, self.height), HWSURFACE)
        self.heights = pygame.Surface((self.width, self.height), HWSURFACE)
        self.output = pygame.Surface((self.width, self.height), HWSURFACE)

        # the currently shown surface
        self.currently_shown = self.terrain

        # get the los data from the map

        # lock the image's pixels
        self.terrain.lock()
        self.heights.lock()

        # now loop over the entire map matrix 
        for y in range(self.height):
            for x in range(self.width):
                # get the value in the LOS map and mask out the terrain type (second byte)
                value = los_data[y][x]

                # split out the terrain and height
                tcode = chr((value >> 16) & 0xff)
                height = (value & 0xffff) / 50  # this is real height, can be > 255 !
                if height > 255:
                    height = 255

                # create a grayscale pixel and store in the map
                if tcode in map.terrain.terrainDict:
                    color = map.terrain.terrainDict[tcode].loscolor()
                else:
                    color = (255, 0, 0)
                self.terrain.set_at((x, y), color)
                self.heights.set_at((x, y), (height, height, height))

        # unlock the image's pixels, we're done
        self.terrain.unlock()
        self.heights.unlock()

        # currently we want to show the terrain data
        self.output.blit(self.currently_shown, (0, 0))

        # create the initial lines too
        self.__drawGrid()

    def paint(self, offset_x, offset_y, dirtyrect=None):
        """
        Paints the layer. Blits out the surfaces for the los layer surrounded by a border. Paints
        the window as minimized if the window is minimized.
        """
        # are we minimized?
        if self.isMinimized():
            # yes, paint just the minimized layer, no content, and then go away
            self.paintBorderMinimized(self.x, self.y, self.width)
            return

        # paint the border first
        self.paintBorder(self.x, self.y, self.width, self.height)

        # blit it out
        scenario.sdl.blit(self.output, (self.x, self.y))

    def handleContentsClick(self, x, y):
        """
        This callback is activated if the player clicks within the window area, ie. inside the
        borders. This callback will toggle the shown map, ie. alternate between the terrain map and
        the height map.
        """
        # transform the coordinates to be inside the minimap
        x = x - self.x
        y = y - self.y

        print("LosdebugLayer.handleContentsClick: %d %d" % (x, y))

        # toggle the grid showing bit
        self.show_grid = (1, 0)[self.show_grid]

        # should we toggle the shown image? this is only done every second click
        if self.show_grid == 0:
            # just toggle the shown
            if self.currently_shown == self.terrain:
                # show the heights
                self.currently_shown = self.heights
            else:
                # show terrain
                self.currently_shown = self.terrain

        # copy a clear and empty version of the current surface to our output buffer
        self.output.blit(self.currently_shown, (0, 0))

        # draw the lines and the grid
        self.__drawLines()
        self.__drawGrid()

        # repaint the playfield now that we have changed
        scenario.playfield.needRepaint()

        # we were handled all right
        return 1

    def __drawLines(self):
        """
        Draws the lines for the current LOS ont the output buffer.
        """

        # do we have a "we see this" line?
        if self.line_start is not None:
            # yep, should we draw to the mid or end?
            if self.line_mid is not None:
                # the mid, so draw a green line from the start position as far as we can see
                pygame.draw.line(self.output, (128, 255, 128), self.line_start, self.line_mid)
            else:
                # the end, so draw a green line from the start position all the way
                pygame.draw.line(self.output, (128, 255, 128), self.line_start, self.line_end)

        # do we have a "we don't see this" line?
        if self.line_mid is not None and self.line_end is not None:
            # yes, so draw a red line from the position where los ended up to the ending point
            pygame.draw.line(self.output, (255, 128, 128), self.line_mid, self.line_end)

    def __drawGrid(self):
        """
        Draws a grid on top of the current output image.
        """
        # only draw if the grid should be shown
        if self.show_grid == 0:
            # no grid, we're done
            return

        # map dimensions
        width, height = scenario.map.getSize()
        delta_x = properties.hex_los_delta_x
        delta_y = properties.hex_los_delta_y

        # now loop over the entire map matrix 
        for y in range(height):
            for x in range(width):

                if y % 2 == 0:
                    # the icon is painted as far left as possible
                    coordinates = (x * delta_x - delta_x / 2, y * delta_y - (delta_x - delta_y))
                else:
                    # the icon is indented half a hex to the right.
                    coordinates = (x * delta_x, y * delta_y - (delta_x - delta_y))

                # blit out a grid icon
                self.output.blit(self.icon, coordinates)
