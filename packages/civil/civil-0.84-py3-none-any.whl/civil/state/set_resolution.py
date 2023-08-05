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


class SetResolution(state.State):
    """
    This class is a state that is used to drive the dialog layer SetResolution. It takes care of
    events and forwards mouse presses to the layer for handling.
    """

    def __init__(self, oldstate):
        """
        Initializes the instance. Sets default values for all needed member.
        """

        # call superclass constructor
        state.State.__init__(self)

        # store the old state
        self.oldstate = oldstate

        # set default cursor
        self.setDefaultCursor()

        # set defaults
        self.name = "set_resolution"

        # set the keymap too
        self.keymap[(K_ESCAPE, KMOD_NONE)] = self.close

        # find the question layer
        self.layer = scenario.playfield.getLayer("set_resolution")

        # Center it
        self.layer.center()

        # and make it visible
        scenario.playfield.setVisible(self.layer)

    def handleLeftMousePressed(self, event):
        """
        Handles a click with the left mouse button. This method checks weather the 'Ok' button was
        clicked, and if it was then gets the new resolution and attempts to set it as the new global
        screen resolution.

        Returns the old state that was active before this state was activated.
        """

        # get event position
        xev, yev = event.pos

        # was ok pressed? Let the layer handle the keypress
        if self.layer.isOkPressed(xev, yev):
            # Remember old size
            oldwidth = scenario.sdl.getWidth()
            oldheight = scenario.sdl.getHeight()

            # get the new selected resolution
            width, height = self.layer.getResolution()

            if width != oldwidth or height != oldheight:
                # let the player know what we're doing
                scenario.messages.add("Setting resolution to %d x %d" % (width, height))

                # set the new size
                scenario.sdl.setSize(width, height)

                # let the playfield and all layers know of the new resolution
                scenario.playfield.updateForResolutionChange(oldwidth, oldheight, width, height)

                # repaint the playfield
                scenario.playfield.needRepaint()

            # we're done, hide the layer
            scenario.playfield.setVisible(self.layer, 0)

            # return the old state
            return self.oldstate

        # no 'Ok' clicked, see if there' something else that needs to be take care of
        self.layer.handleLeftMousePressed(xev, yev)

    def close(self):
        """
        Closes the state without doing anything. Hides the dialog and repaints the playfield.
        """

        # find the layer and hide it
        scenario.playfield.setVisible(self.layer, 0)

        # return the previous state
        return self.oldstate
