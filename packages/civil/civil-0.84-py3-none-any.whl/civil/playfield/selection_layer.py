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
import pygame.image
from pygame.locals import *

from civil import properties
from civil.model import scenario
from civil.playfield.layer import Layer


class SelectionLayer(Layer):
    """
    This class defines a layer that is used for showing a selection rectangle. It is no ordinary
    layer, as it is treated specially by the playfield. A selection is shown when the player drags
    the mouse with the left button pressed, thus trying to select many units.

    The layer can repaint a rectangle that tracks the selection. It has methods for setting the
    starting point and to update the opposite corner when the mouse moves.
    """

    def __init__(self, name):
        """
        Initializes the layer.
        """
        # call superclass constructor
        Layer.__init__(self, name)

        # default values
        self.start = None

        # a list of stored surfaces
        self.stored = []

        self.x = -1
        self.y = -1
        self.width = 0
        self.height = 0

    def setStartPosition(self, start):
        """
        Sets the starting position for the selection. This position will not change during the
        entire selection. Only a new selection will change it.
        """
        self.start = start
        self.x, self.y = start
        self.width = 0
        self.height = 0
        self.finished = 0

    def setEndPosition(self, end):
        """
        Updates the ending position. This is position is used as the current ending position when
        repainting the selection box. The starting position is always the one set by
        setStartPosition(). This method should be called when the mouse moves while doing a
        selection.
        """
        x, y = self.start
        w, h = end
        w -= x
        h -= y

        if w < 0:
            x, w = x + w, -w
        if h < 0:
            y, h = y + h, -h

        self.x, self.y = x, y
        self.width, self.height = w, h

    def finishSelection(self):
        """
        This method should be called when the selection is done. It clears internal structures
        and makes sure everyting is tidied up.
        """

        # Finally, always remove the selection rectangle
        self.restoreRectangle()

        self.finished = 1

    def paint(self, offset_x, offset_y, dirtyrect=None):
        """
        Paints the layer. Restores the terrain under the old rectangle and repaints the new one.
        """

        if self.finished:
            return

        # restore the old rects
        self.restoreRectangle()

        # store new rectangle
        self.saveRectangle()

        # paint the new rectangle
        self.paintRectangle()

    def restoreRectangle(self):
        """
        Restores the old rectangle.
        """

        # loop over all stored surfaces with their coordinates
        for x, y, surface in self.stored:
            # blit it out
            scenario.sdl.blit(surface, (x, y))

        # no stored surfaces anymore
        self.stored = []

    def saveRectangle(self):
        """
        Saves the surface under the rectangle that should be painted.
        """

        # get the min and max x,y coordinates 
        x1 = self.x
        y1 = self.y
        width = self.width
        height = self.height
        x2 = x1 + width
        y2 = y1 + height

        # do we have a width and height?
        if width == 0 or height == 0:
            # nope, so nothing to do here
            return

        # create new surfaces that match the edge of the painted rectangle
        left = pygame.Surface((1, height + 1), HWSURFACE)
        right = pygame.Surface((1, height + 1), HWSURFACE)
        top = pygame.Surface((width + 1, 1), HWSURFACE)
        bottom = pygame.Surface((width + 1, 1), HWSURFACE)

        # get the main surface
        main = scenario.sdl.getSurface()

        # lock it
        main.lock()

        # copy data from our main surface
        left.blit(main.subsurface((x1, y1, 1, height + 1)), (0, 0))
        right.blit(main.subsurface((x2, y1, 1, height + 1)), (0, 0))
        top.blit(main.subsurface((x1, y1, width + 1, 1)), (0, 0))
        bottom.blit(main.subsurface((x1, y2, width + 1, 1)), (0, 0))

        # add the surfaces
        self.stored.append((x1, y1, left))
        self.stored.append((x2, y1, right))
        self.stored.append((x1, y1, top))
        self.stored.append((x1, y2, bottom))

        # we're done, unlock
        main.unlock()

    def paintRectangle(self):
        """
        Paints a new rectangle from the start position to the current ending position.
        """

        # get the size of the box
        width = self.width
        height = self.height

        # do we have a width and height?
        if width == 0 or height == 0:
            # nope, so nothing to do here
            return

        # draw the selection rectangle
        scenario.sdl.drawRect(properties.layer_selection_color,
                              (self.x, self.y, width + 1, height + 1), 1)
