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


class HelpBrowser(state.State):
    """
    This class is a state that is used to drive the help browser. The browser is a very simple
    hypertext browser that can show some help text along with a title and some 'see also'
    links. The player can navigate in the text by clicking the links with the mouse.

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
        self.name = "help_browser"

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

        # find the browser layer
        self.browserlayer = scenario.playfield.getLayer("help_browser")

        # start from the topic that the caller wants
        self.browserlayer.setTopic(caller.help_topic)

        # and make it visible
        scenario.playfield.setVisible(self.browserlayer)

        # we want mouse motion events, for highlighting
        self.wantmousemotion = 1

    def handleMouseMotion(self, event):
        """
        Handles highlighting of links, by simply asking the layer.
        """
        self.browserlayer.handleMouseMotion(event.pos[0], event.pos[1])

    def handleLeftMousePressed(self, event):
        """
        Handles a click with the left mouse button. This method checks weather the 'Close' button
        was clicked, and if it was then closes the help browser. Lets the browser layer handle the
        click if it wasn't in the button. Restores the previous state when closed.
        """

        # get event position
        xev, yev = event.pos

        # was ok pressed? Let the layer handle the keypress
        if self.browserlayer.isOkPressed(xev, yev):
            # yep, closed, so close and return whatever state we had before
            return self.close()

        # no 'Close' clicked, see if there's something else that needs to be take care of
        if self.browserlayer.handleLeftMousePressed(xev, yev):
            # we need an update now of the playfield
            scenario.playfield.needRepaint()

    def close(self):
        """
        Closes the state without doing anything. Hides the dialog and repaints the
        playfield. This method is used from the keybindings.
        """

        # find the layer and hide it
        scenario.playfield.setVisible(self.browserlayer, 0)

        # return the previous state
        return self.caller
