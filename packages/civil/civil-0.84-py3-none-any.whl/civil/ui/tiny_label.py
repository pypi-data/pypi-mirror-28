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

from civil import properties
from civil.ui.widget import Widget


class TinyLabel(Widget):
    """
    This class defines a tiny label with a text rendered in a predefined font, color and
    background. 

 """

    # a shared tiny font, color and background
    font = None
    background = None

    def __init__(self, text, position=(0, 0), callbacks=None, color=properties.tiny_font_color):
        """
        Initializes the widget. Renders the font using the passed data.
        """

        # first call superclass constructor
        Widget.__init__(self, position, callbacks)

        # do we have a font already?
        if TinyLabel.font is None:
            # no, so create it 
            TinyLabel.font = pygame.font.Font(properties.tiny_font_name, properties.tiny_font_size)

            # and the background 
            TinyLabel.background = properties.tiny_font_background

        # create the surface
        self.surface = TinyLabel.font.render(text, 1, color)

        # store our text and color too
        self.text = text
        self.color = color

    def setText(self, text):
        """
        Sets a new text for the label. Renders the new label.
        """

        # create the surface
        self.surface = TinyLabel.font.render(text, 1, self.color)

        # store the new text
        self.text = text

        # we're dirty now
        self.dirty = 1

    def getText(self):
        """
        Returns the current text of the label.
        """
        return self.text
