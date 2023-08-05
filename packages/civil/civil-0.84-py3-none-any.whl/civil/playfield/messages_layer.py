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

from civil.model import scenario
from civil.playfield.layer import Layer


class MessagesLayer(Layer):
    """
    This class defines a layer that plugs into the PlayField. It can render all messages that the
    player should see as labels in the top right corner of the screen. The labels are drawn as
    transparent with only the actual text as solid color.

    The text font and size are given in the properties file.
    """

    def __init__(self, name):
        """
        Initializes the layer.
        """
        # call superclass constructor
        Layer.__init__(self, name)

        self.y = 10
        self.x = scenario.sdl.getWidth()
        self.width = 0
        self.height = 0

        scenario.dispatcher.registerCallback('messages_changed', self.messagesChanges)

    def messagesChanges(self, parameters):
        """

        Args:
            parameters: 
        """
        # start from y coordinate 10
        y = 10
        newx = self.x
        newy = self.y

        # loop over all pregenerated surface labels we have
        for milliseconds, label in scenario.messages.getLabels():
            # figure out the x coordinate
            x = scenario.sdl.getWidth() - label.get_width() - 10
            newx = min(newx, x)

            # add to the y coord so that we paint a little down
            y += label.get_height() + 2

        self.x = min(self.x, newx)
        self.width = scenario.sdl.getWidth() - self.x
        self.height = max(self.height, y - self.y)

        # repaint the playfield
        scenario.playfield.needRepaint(self.getRect())

    def paint(self, offset_x, offset_y, dirtyrect=None):
        """
        Paints the layer. Loops and blits out all message labels.
        """

        # start from y coordinate 10
        y = 10

        # loop over all pregenerated surface labels we have
        for milliseconds, label in scenario.messages.getLabels():
            # figure out the x coordinate
            x = scenario.sdl.getWidth() - label.get_width() - 10
            self.x = min(self.x, x)

            # now blit out the actual text in the middle of the outline
            scenario.sdl.blit(label, (x, y))

            # add to the y coord so that we paint a little down
            y += label.get_height() + 2

        self.width = scenario.sdl.getWidth() - self.x
        self.height = y - self.y
