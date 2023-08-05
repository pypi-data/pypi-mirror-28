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

from civil.ui.widget import Widget


class Fader(Widget):
    """
    This class defines a simple surface that works as a fader widget. It covers a part of a dialog
    with asurface that can gradially become less and less transparent, thus fading the part of the
    dialog towards that color.

    Call the setAlpha() method periodically to alter alpha.
    """

    def __init__(self, size=(0, 0), position=(0, 0), alpha=0, color=(0, 0, 0), callbacks=None):
        """
        Initializes the widget. Creates the surface.
        """

        # first call superclass constructor
        Widget.__init__(self, position, callbacks)

        # create the surface
        self.surface = pygame.Surface(size)

        # set the alpha too
        self.surface.set_alpha(alpha, RLEACCEL)

        # store alpha too
        self.alpha = alpha

    def getAlpha(self):
        """
        Returns current alpha value.
        """
        return self.alpha

    def setAlpha(self, alpha):
        """
        Sets a new alpha value for the fader.
        """
        # store new alpha
        self.alpha = alpha

        # set the alpha too
        self.surface.set_alpha(alpha, RLEACCEL)

        # we're dirty now
        self.dirty = 1
