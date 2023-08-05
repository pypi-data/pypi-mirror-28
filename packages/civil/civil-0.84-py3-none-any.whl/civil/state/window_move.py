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

from civil.state import state
from civil.model import scenario


class WindowMove(state.State):
    """
    This class is a state that is used when floating windows are moved. Floating windows are layers
    that subclass FloatingWindowLayer. When this state is initialized it is given a layer that
    should me moved according to mouse motions until the left mouse button is released.

    The mouse movements are directly sent to the layer which is moved and then repainted.
    """

    def __init__(self, layer, oldstate):
        """
        Initializes the instance. Gets the layer that should be controlled and the old state that
        should be activated when this state is done.
        """

        # call superclass constructor
        state.State.__init__(self)

        # set default cursor
        self.setDefaultCursor()

        # set defaults
        self.name = "window_move_state"

        # set the keymap to something empty. we don't want to handle anything
        self.keymap = {}

        # store the passed layer. this is what we're moving
        self.layer = layer

        # store the old state. this is the one that gets reactivated when the moving is done
        self.oldstate = oldstate

        # we want mouse motion events
        self.wantmousemotion = 1

        # store the position of the mouse now when the drag starts so that we have a delta for where
        # on the frame the player has grabbed
        startx, starty = self.layer.getPosition()
        x, y = pygame.mouse.get_pos()

        # delta values for the movements
        self.delta_x = x - startx
        self.delta_y = y - starty

    def handleLeftMouseReleased(self, event):
        """
        Handles a the event when the left mouse button is released. This finishes the moving of
        the window and restores a suitable state. If no units are selected this method returns the
        Idle state, and if units were selected then OwnUnit is returned.
        """

        # return the old state we had before this started
        return self.oldstate

    def handleMouseMotion(self, event):
        """
        This method handles the mouse moving around. It is used to be able to track where the
        mouse is right now and highlight the current alternative.
        """

        # Grab all mouse movements, but use only the last one. avoids flicker
        event = self.latestMousemove(event)

        # Eh, this seems to ignore all events and use the current mouse pos?
        # oh well, it can't be wrong, but is perhaps the same as in event?
        x, y = pygame.mouse.get_pos()

        updaterect = self.layer.getRect()

        # update the current ending position in the selection layer
        self.layer.setPosition(x - self.delta_x, y - self.delta_y)

        # The rect to update is the union of the layer's
        # previous position and the current position
        updaterect = updaterect.union(self.layer.getRect())

        # the playfield needs a repaint
        scenario.playfield.needRepaint(updaterect)

        return None
