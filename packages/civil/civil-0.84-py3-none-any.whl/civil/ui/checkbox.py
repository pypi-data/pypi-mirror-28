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

from civil.ui import widget
from civil import properties
from civil.model import scenario
from civil.ui.widget import Widget


class CheckBox(Widget):
    """
    This class defines a checkbox which can be in a checked or unchecked state. The two needed
    images will be loaded by the constructor from the passed file names.

    This class plays a small sound when the checkbox is toggled.
    """

    # a shared font
    font = None

    def __init__(self, text, checkedname, uncheckedname, checked=0, position=(0, 0),
                 callbacks=None, color=properties.checkbox_font_color, background=(0, 0, 0)):
        """
        Initializes the widget. Loads the icons from the passed file_namea.
        """

        # first call superclass constructor
        Widget.__init__(self, position, callbacks)

        # do we have a font already?
        if CheckBox.font is None:
            # no, so create it 
            CheckBox.font = pygame.font.Font(properties.checkbox_font_name, properties.checkbox_font_size)

        # load the icons
        self.checked = pygame.image.load(checkedname).convert()
        self.unchecked = pygame.image.load(uncheckedname).convert()

        # make sure they have the transparent color set (always white)
        self.checked.set_colorkey((255, 255, 255), RLEACCEL)
        self.unchecked.set_colorkey((255, 255, 255), RLEACCEL)

        # store the default state
        self.state = checked

        # create the surface
        self.renderedtext = CheckBox.font.render(text, 1, color)

        # store the needed data so that we can set the text later
        self.color = color
        self.background = background

        # set the surface too, so that isInside() has something to check
        self.surface = self.checked

        # store the text
        if text is None:
            self.text = ""
        else:
            self.text = text

        # set our internal callbacks so that we can trap changes
        self.internal = {widget.MOUSEBUTTONUP: self.toggle}

    def isChecked(self):
        """
        Returns 1 if the checkbox is checked and 0 if it is not checked.
        """
        return self.state

    def setChecked(self, checked=1):
        """
        Sets the checkbox as unchecked if the parameter is 0, and to checked for all other
        values.
        """
        if checked == 0:
            self.state = 0
        else:
            self.state = 1

        # we're dirty now
        self.dirty = 1

    def toggle(self, event):
        """
        Toggles the state of a checkbox.
        """
        if self.state == 0:
            self.state = 1
        else:
            self.state = 0

        # play a sound
        scenario.audio.playSample('checkbox-toggled')

        # we're dirty now
        self.dirty = 1

    def paint(self, destination, force=0):
        """
        Method that paints the editfield. This method will simply blit out the surface of the widget
        onto the destination surface.
        """
        # are we dirty or not?
        if not self.dirty and not force:
            # not dirty, nothing to do here
            return 0

        # what surface should we use?
        if self.state:
            usedsurface = self.checked
        else:
            usedsurface = self.unchecked

        # we're dirty, blit out the button first
        destination.blit(usedsurface, self.position)

        # get the x and y positions where rendering of the label should start
        labelheight = self.renderedtext.get_height()
        x = self.position[0] + usedsurface.get_width() + 5
        y = self.position[1] + usedsurface.get_height() / 2 - labelheight / 2

        # and then the text label
        destination.blit(self.renderedtext, (x, y))

        self.dirty = 0

        # we did something, make sure the widget manager knows that
        return 1
