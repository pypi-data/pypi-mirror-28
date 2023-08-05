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


class MinimapLayer(FloatingWindowLayer):
    """
    This class defines a layer that plugs into the PlayField. It provides code for showing a little
    minimap. The minimap contains the full map of the scenario, but with one pixel representing a
    hex or unit.

    When something changes in the data it should also change here.

    This layer is a floating window layer, which means it can be dragged around the map.
    """

    def __init__(self, name):
        """
        Initializes the layer.
        """
        # call superclass constructor
        FloatingWindowLayer.__init__(self, name)

        # init the map
        self.createMap()

        # by default we start the map at the upper left corner
        self.x, self.y = self.getBorderWidth()

        # add some extra spacing, it allows some of the background terrain to show through on the
        # upper and left side of the minimap
        self.x += 5
        self.y += 5

    def createMap(self):
        """
        Creates the minimap. Sets the initial terrain and unit data based on real Map data.
        """
        # get map width and height
        self.width = scenario.map.getsize_x() * 2
        self.height = scenario.map.getsize_y() * 2

        # allocate a surface for ourselves
        self.terrain = pygame.Surface((self.width, self.height), HWSURFACE)
        self.units = pygame.Surface((self.width, self.height), HWSURFACE)

        # make sure the units surface is transparent
        self.units.set_colorkey((0, 0, 0))

        self.populateMap()

    def populateMap(self):
        """
        Populates the minimap with terrain data and units. Called at start and
        at each new turn. (the units move => update needed)
        """
        # get a list of the hexes
        hexes = scenario.map.getHexes()

        # lock the surface
        self.terrain.lock()

        # loop over the hexes in the map
        for y in range(scenario.map.getsize_y()):
            for x in range(scenario.map.getsize_x()):
                # get the hex for that position
                hex = hexes[y][x]

                # get the color for the hex
                color = hex.getColor()

                # create a pixel with the proper color
                self.terrain.set_at((x * 2 + 0, y * 2 + 0), color)
                self.terrain.set_at((x * 2 + 0, y * 2 + 1), color)
                self.terrain.set_at((x * 2 + 1, y * 2 + 0), color)
                self.terrain.set_at((x * 2 + 1, y * 2 + 1), color)

        # we're done, now the surface can be unlocked
        self.terrain.unlock()

        # fill the units surface with black (transparent) so that we start out with an empty surface
        # that's fully transparent
        self.units.fill((0, 0, 0))

        # get a reference to the colors
        colors = properties.layer_minimap_unit_colors

        # lock the surface
        self.units.lock()

        # loop over all units
        for unit in scenario.info.units.values():
            # is the unit visible?
            if not unit.isVisible():
                # not visible, so don't include it either
                continue

            # get its position 
            unitx, unity = unit.getPosition()

            # translate the position so that it is within the screen
            unitx /= 24
            unity /= 18

            # get color for the unit
            color = colors[unit.getOwner()]

            # create a pixel with the proper color
            unitx = int(unitx)
            unity = int(unity)
            self.units.set_at((unitx + 0, unity + 0), color)
            self.units.set_at((unitx + 0, unity + 1), color)
            self.units.set_at((unitx + 1, unity + 0), color)
            self.units.set_at((unitx + 1, unity + 1), color)

        # we're done, now the surface can be unlocked
        self.units.unlock()

    def updateUnits(self):
        """
        Updates the unit layer. Reads data about all units and blits out a pixel for those units
        that the player can see.
        """
        pass

    def paint(self, offset_x, offset_y, dirtyrect=None):
        """
        Paints the layer. Blits out the surfaces for the minimap surrounded by a border. Paints
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
        scenario.sdl.blit(self.terrain, (self.x, self.y))
        scenario.sdl.blit(self.units, (self.x, self.y))

        # and the minimap rectangle. First get the offset needed. we want to paint the rect so that
        # it is starting from the current scrolling offset
        rectx = self.x + offset_x * 2
        recty = self.y + offset_y * 2

        # get the playfield size and draw a rectangle
        visx, visy = scenario.playfield.getVisibleSizeClamped()
        scenario.sdl.drawRect((255, 255, 255), pygame.Rect(rectx, recty, visx * 2, visy * 2), 1)

    def handleContentsClick(self, x, y):
        """
        This callback is activated if the player clicks within the minimap area, ie. inside the
        borders. This callback will get the new offsets for the map scrolling and do the scroll
        """

        # transform the coordinates to be inside the minimap
        x = x - self.x
        y = y - self.y

        # gte the width and height of the map
        mapwidth = self.width / 2
        mapheight = self.height / 2

        # get the clicked position within the minimap. each hex is a 2*2 pixel, so we need to halve
        # the coordinates
        x /= 2
        y /= 2

        # get the visible size in hexes of the map
        vis_x, vis_y = scenario.playfield.getVisibleSize()

        # Click on center of focus, not top-left corner
        x -= vis_x / 2
        y -= vis_y / 2

        # default to assume the rect will fit
        offset_x = x
        offset_y = y

        # is the x offset too big, i.e. the rect won't fit?
        if x + vis_x >= mapwidth:
            # too wide
            offset_x = mapwidth - vis_x

        # is the y offset too big, i.e. the rect won't fit?
        if y + vis_y >= mapheight:
            # too wide
            offset_y = mapheight - vis_y

        if x < 0:
            offset_x = 0

        if y < 0:
            offset_y = 0

        # assign the new offsets
        repaintneeded1 = scenario.playfield.setoffset_x(offset_x)
        repaintneeded2 = scenario.playfield.setoffset_y(offset_y)

        # do we need to repaint?
        if repaintneeded1 or repaintneeded2:
            # repaint the playfield now that it has changed
            scenario.playfield.needRepaint()

        # we were handled all right
        return 1
