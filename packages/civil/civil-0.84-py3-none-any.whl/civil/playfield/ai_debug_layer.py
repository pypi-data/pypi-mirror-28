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

from civil import properties
from civil.model import scenario
from civil.playfield.layer import Layer


class AIDebugLayer(Layer):
    """
    This class defines a layer that is used for debugging the AI. It shows a label at the center of
    the hex. The value of the label is just some text that makes sense when debugging the AI.

    This class can also be used as a base class for other debugging layers that just need to write
    some short label for each hex. To do that just subclass it and override the getHexValue() method
    and defined one that returns the wanted value.
    """

    def __init__(self, name):
        """
        Initializes the layer.
        """
        # call superclass constructor
        Layer.__init__(self, name)

        # store a dict of generated labels
        self.labels = {}

        # load the font for the labels
        self.labelfont = pygame.font.Font(properties.layer_locations_font,
                                          properties.layer_locations_font_size)

    def paint(self, offset_x, offset_y, dirtyrect=None):
        """
        Paints the layer. Simply blits out the already created surface.
        """

        # get the needed deltas
        delta_x = properties.hex_delta_x
        delta_y = properties.hex_delta_y

        # loop over the hexes in the map and create
        for y in range(scenario.sdl.getHeight() / delta_y):
            for x in range(scenario.sdl.getWidth() / delta_x):

                # get the value for this hex
                value = self.getHexValue(x, y)

                # do we have a label for this value?
                if value not in self.labels:
                    # nope, so create one
                    surface = self.labelfont.render("%d" % value, 1, properties.layer_locations_color)

                    # store it for later use
                    self.labels[value] = surface
                else:
                    # get it
                    surface = self.labels[value]

                # is this an odd or even row?
                if y % 2:
                    # odd
                    scenario.sdl.blit(surface, (x * 48 + 24, y * delta_y))
                else:
                    # even
                    scenario.sdl.blit(surface, (x * 48, y * delta_y))

    def getHexValue(self, x, y):
        """
        Returns the value the hex (x,y) should have. This method can be overridden by subclasses
        if needed. The value is currently an integer value. If floats etc are needed then the line
        that renders the table in the paint() method must be changed too.
        """

        # this is an example only, return the sum of the coordinates
        return x + y
