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

from civil.ui.widget import Widget


class Label(Widget):
    """
    This class defines a simple label with a text rendered in a certain font. 

 """

    def __init__(self, font, text, position=(0, 0), callbacks=None,
                 color=(255, 255, 255), background=(0, 0, 0)):
        """
        Initializes the widget. Renders the font using the passed data.
        """

        # first call superclass constructor
        Widget.__init__(self, position, callbacks)

        # create the surface
        self.surface = font.render(text, 1, color)

        # store the needed data so that we can set the text later
        self.font = font
        self.color = color
        self.background = background

        # store our text too
        self.text = text

    def setText(self, text):
        """
        Sets a new text for the label. Renders the new label using the font and colors passed in
        the constructor.
        """

        # create the surface
        self.surface = self.font.render(text, 1, self.color)

        # store the new text
        self.text = text

        # we're dirty now
        self.dirty = 1

    def getText(self):
        """
        Returns the current text of the label.
        """
        return self.text
