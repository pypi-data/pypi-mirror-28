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

from pygame.locals import *

from civil.state import state
from civil.model import scenario


class ArmyStatus(state.State):
    """
    This class is a state that is used to drive the army status dialog. This class just brings the
    layer to the top and takes care of relaying mouse presses to it. It also close the dialog (hides
    the layer) when needed.
    
    This state manages events, and forwards all clicks to the playfield layer that paints the
    browser. When closed this state resumes the previous state.
    """

    def __init__(self, caller):
        """
        Initializes the instance. Sets default values for all needed member.
        """

        # call superclass constructor
        state.State.__init__(self)

        # set default cursor
        self.setDefaultCursor()

        # set defaults
        self.name = "army_status"

        # store the calling state
        self.caller = caller

        # set the keymap too
        self.keymap[(K_ESCAPE, KMOD_NONE)] = self.close

        # find the layer
        self.army_status_layer = scenario.playfield.getLayer("army_status")

        # update the shown info
        self.army_status_layer.updateUnits()

        # and make it visible
        scenario.playfield.setVisible(self.army_status_layer)

    def handleLeftMousePressed(self, event):
        """
        Handles a click with the left mouse button. This method checks weather the 'Close' button
        was clicked, and if it was then closes the help browser. Lets the layer handle the click if
        it wasn't in the button. Restores the previous state when closed.
        """

        # get event position
        xev, yev = event.pos

        # was ok pressed? ask the layer about it
        if self.army_status_layer.isOkPressed(xev, yev):
            # yep, closed, so close and return whatever state we had before
            return self.close()

        # no 'Close' clicked, see if there's something else that needs to be take care of
        if self.army_status_layer.handleLeftMousePressed(xev, yev):
            # we need an update now of the playfield
            scenario.playfield.needRepaint()

    def close(self):
        """
        Closes the state without doing anything. Hides the dialog and repaints the
        playfield. This method is used from the keybindings.
        """

        # find the layer and hide it
        scenario.playfield.setVisible(self.army_status_layer, 0)

        # return the previous state
        return self.caller
