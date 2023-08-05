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


class ChatLayer(Layer):
    """
    This class defines a layer that plugs into the PlayField. It provides code for showing a dialog
    with info about a given weapon. The info includes all info that can be retrieved from the Weapon
    class. The user can using this dialog get a good idea as to what a weapon can do.

    To set the weapon this layer should show call 'setWeapon()'. This layer should be added among
    the last to the playfield, so that it is drawn on top over  everything else.

    TODO: combine this layer with the help layer to share code?

    """

    def __init__(self, name):
        """
        Initializes the layer.
        """
        # call superclass constructor
        Layer.__init__(self, name)

        # no label yet
        self.label = None

        # load the font for the text
        self.font = pygame.font.Font(properties.layer_chat_font,
                                     properties.layer_chat_font_size)

        # set starting y coordinate
        self.y = scenario.sdl.getHeight()

        # subtract the height of the icons and the text size. Also make sure there is some slight
        # gap between the frame and the panel. Looks better?
        self.height = 0
        self.height += Layer.top.get_height()
        self.height += Layer.bot.get_height()
        self.height += self.font.get_height()
        self.y -= self.height + 10

        # set horizontal coordinates
        self.width = scenario.sdl.getWidth() - Layer.left.get_width() - Layer.right.get_width() - 10
        self.x = Layer.left.get_width() + 5

    def setMessage(self, message):
        """
        Sets the message that should be displayed in the box. This is the message written by the
        player. The input is handled by the Chat state. This method will render a new label.
        """

        # do we have a message yet?
        if message == "":
            # nope, set it to nothing
            self.label = None
            return

        # create the label
        self.label = self.font.render(message, 1, properties.layer_chat_color)

    def paint(self, offset_x, offset_y, dirtyrect=None):
        """
        Paints the layer. Loops and blits out all labels. The offsets are used so that we know how
        much the map has been scrolled.
        """

        # get starting position and size
        x = self.x
        y = self.y
        width = self.width
        height = self.height

        # fill a part of the background with black so that we have something to paint on
        scenario.sdl.fill((0, 0, 0), (x - 1, y - 1, width + 2, height + 2))

        # paint the border first
        self.paintBorder(x, y, width, height)

        # do we have a label yet?
        if self.label is None:
            # no label, go away
            return

        # add the borders before we paint the label
        x += Layer.left.get_width() + 5
        y += Layer.topleft.get_height()

        # now blit out the label
        scenario.sdl.blit(self.label, (x, y))
