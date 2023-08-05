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

from civil.ui.widget import Widget


class Image(Widget):
    """
    This class defines a simple image on the screen. No interaction can be had with it. It needs a
    file name from which the surface is loaded.
    """

    # define a shared cache
    cache = {}

    def __init__(self, file_name, position=(0, 0), callbacks=None, alpha=-1):
        """
        Initializes the widget. Loads the icons from the passed file name.
        """

        # first call superclass constructor
        Widget.__init__(self, position, callbacks)

        # do we have the wanted image in our cache?
        if file_name in Image.cache:
            # yep, use that instead
            self.surface = Image.cache[file_name]

        else:
            # not in memory, try to load the surfaces
            self.surface = pygame.image.load(file_name)

            # store in the cache for later use
            Image.cache[file_name] = self.surface

        # set the color key
        self.surface.set_colorkey((255, 255, 255), RLEACCEL)

        # did we get an alpha value?
        if alpha != -1:
            # yep, convert the image to alpha
            self.surface.set_alpha(alpha, RLEACCEL)

            # convert to a more efficient format
            self.surface = self.surface.convert()
