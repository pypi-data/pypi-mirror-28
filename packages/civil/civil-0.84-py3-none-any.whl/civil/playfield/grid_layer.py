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


class GridLayer(Layer):
    """
    This class defines a layer that is used for showing a grid on the main map. It is drawn after
    the main terrain and will blit a simple grid upon the map so that the player knows the borders
    of hexes.

    This layer is transparent and will only obscure the positions where the icon borders are.
    """

    def __init__(self, name):
        """
        Initializes the layer.
        """
        # call superclass constructor
        Layer.__init__(self, name)

        # load the icon for the grids
        self.icon = pygame.image.load(properties.layer_grid_icon).convert()

        # set the transparent color for the icon and the surface
        self.icon.set_colorkey((255, 255, 255), RLEACCEL)

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
                # is this an odd or even row?
                if y % 2:
                    # odd
                    scenario.sdl.blit(self.icon, (x * 48 + 24, y * delta_y))
                else:
                    # even
                    scenario.sdl.blit(self.icon, (x * 48, y * delta_y))
