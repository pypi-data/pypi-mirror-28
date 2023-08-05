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
import pygame.mixer

from civil.ui import widget
from civil import properties
from civil.model import scenario
from civil.ui.widget import Widget


class Button(Widget):
    """
    This class defines a simple pushbutton which can can be clicked. It needs a surfaces that
    represent the button. The surface will be loaded by the constructor from a passed file_name.

    This class plays a small sound when the button is clicked.

    Dependinging on the value of propeties.button_enter_leave the button behaves graphically
    different. For a value of 1 the button changes image when the mouse enters/leaves the button,
    and for a value od 0 the image changes then the player clicks the button.
    """

    # define a shared cache
    cache = {}

    def __init__(self, file_name1, file_name2, position=(0, 0), callbacks=None):
        """
        Initializes the widget. Loads the icons from the passed file_name.
        """

        # first call superclass constructor
        Widget.__init__(self, position, callbacks)

        # do we have the wanted image in our cache?
        if file_name1 in Button.cache:
            # yep, use that instead
            self.surface_released = Button.cache[file_name1]
            self.surface_outside = self.surface_released
        else:
            # not in memory, try to load the surfaces
            self.surface_released = pygame.image.load(file_name1).convert()
            self.surface_outside = self.surface_released

            # setup color key
            self.__setupColorkey(self.surface_released)

            # store in the cache for later use
            Button.cache[file_name1] = self.surface_released

        # do we have the wanted image in our cache?
        if file_name2 in Button.cache:
            # yep, use that instead
            self.surface_pressed = Button.cache[file_name2]
            self.surface_inside = self.surface_pressed

        else:
            # not in memory, try to load the surfaces
            self.surface_pressed = pygame.image.load(file_name2).convert()
            self.surface_inside = self.surface_pressed

            # setup color key
            self.__setupColorkey(self.surface_pressed)

            # store in the cache for later use
            Button.cache[file_name2] = self.surface_pressed

        # initial surface is the non-pressed one
        self.surface = self.surface_released

        # set our internal callbacks so that we can trap keys, depending on what mode of operation
        # we want for the button graphics
        if properties.button_enter_leave:
            # use enter/leave
            self.internal = {widget.MOUSEENTEREVENT: self.mouseEnter,
                             widget.MOUSELEAVEEVENT: self.mouseLeave}
        else:
            # use up/down
            self.internal = {widget.MOUSEBUTTONUP: self.mouseUp,
                             widget.MOUSEBUTTONDOWN: self.mouseDown}

    def mouseUp(self, event):
        """
        Internal callback triggered when the mouse is released when it is over a button. This
        sets a new icon for the button.
        """
        # set the new icon
        self.surface = self.surface_released

        # play a sound
        scenario.audio.playSample('button-clicked')

        # we're dirty
        self.dirty = 1

    def mouseDown(self, event):
        """
        Internal callback triggered when the mouse is pressed when it is over a button. This
        sets a new icon for the button.
        """
        # set the new icon
        self.surface = self.surface_pressed

        # we're dirty
        self.dirty = 1

    def mouseEnter(self, event):
        """
        Internal callback triggered when the mouse enters a button. This sets a new icon for the
        button.
        """
        # set the new icon
        self.surface = self.surface_inside

        # we're dirty
        self.dirty = 1

    def mouseLeave(self, event):
        """
        Internal callback triggered when the mouse leaves a button. This sets a new icon for the
        button.
        """
        # set the new icon
        self.surface = self.surface_outside

        # we're dirty
        self.dirty = 1

    def __setupColorkey(self, button):
        """
        Sets up colorkey data if needed for the passed button.
        """

        # do we need colorkeying?
        if properties.button_use_colorkey:
            # yeah, set it
            button.set_colorkey(properties.button_colorkey_color)
