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


class Help(state.State):
    """
    This class is a state that is used to show a simple help text on the screen. It will add a new
    layer to the playfield and use it to display a dialog with some help text. The user can click a
    button 'Ok' to return to the previous state pr press 'Escape'.
    """

    def __init__(self, labels, caller):
        """
        Initializes the instance. Sets default values for all needed member.
        """

        # call superclass constructor
        state.State.__init__(self)

        # set default cursor
        self.setDefaultCursor()

        # set defaults
        self.name = "help_state"

        # store the calling state
        self.caller = caller

        # set the keymap too
        self.keymap = {(K_ESCAPE, KMOD_NONE): self.close}

        # build up the admin menu. this is the extra commands that can be triggered from the little
        # admin menu in the unit info window. this should ensure that we can't recursively add more
        # help windows by pressing F1 while the help window is active. we only allow screenshots to
        # be taken
        self.adminmenukeymap = [('save a screenshot', K_F12, KMOD_NONE)]

        # TODO: what about the help texts? are they needed?

        # find the help layer
        self.helplayer = scenario.playfield.getLayer("help")

        # set the labels it should show
        self.helplayer.setLabels(labels)

        # and make it visible
        scenario.playfield.setVisible(self.helplayer)

    def handleLeftMousePressed(self, event):
        """
        Handles a click with the left mouse button. This method checks weather the 'Ok' button was
        clicked, and if it was then terminates this state. If the button was not clicked then
        nothing will be done. Activates the previous state.
        """

        # get event position
        xev, yev = event.pos

        # was ok pressed?
        if not self.helplayer.isOkPressed(xev, yev):
            # nope, go away
            return None

        # find the layer and hide it
        scenario.playfield.setVisible(self.helplayer, 0)

        # return the previous state
        return self.caller

    def close(self):
        """


 """

        # find the layer and hide it
        scenario.playfield.setVisible(self.helplayer, 0)

        # return the previous state
        return self.caller
