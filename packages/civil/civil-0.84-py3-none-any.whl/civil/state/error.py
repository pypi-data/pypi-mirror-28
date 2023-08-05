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

from civil.state import state
from civil import constants
from civil.model import scenario


class Error(state.State):
    """
    This class is a state that is used when the network connection to the other player has somehow
    died. It will ask the player weather an emergency save should be done or not. After the player
    has answered the question the game will exit.

    The emergency save should be just like any other save game, and can be loaded later to resume
    the game.
    
    This state will not transfer into any other state when it's done, instead the game exits.
    """

    def __init__(self):
        """
        Initializes the instance. Sets default values for all needed member.
        """

        # call superclass constructor
        state.State.__init__(self)

        # set default cursor
        self.setDefaultCursor()

        # set defaults
        self.name = "error"

        # Call us once
        self.done = 0
        self.callMeSoon()

    def handleEvent(self, event):
        """
        Event handler, used only once.
        This is really a little kludge. This is only
        called for the server, and only once.
        """

        if self.done:
            return state.State.handleEvent(self, event)

        self.done = 1

        # ask weather the player wants to save the current state
        if self.askQuestion(['General, it seems the connection to the remote',
                             'player has been lost!',
                             ' ',
                             'Do you wish to save the game?']):
            # yes, perform the save
            self.save()

        # we're no longer playing a game
        scenario.playing = constants.GAME_ENDED

        # store the type of end game, which as a crash
        scenario.end_game_type = constants.CRASH

        # keep this state active
        return None

    def save(self):
        """
        Saves the current game in an emergency save file.
        """
        print("Error.save: do nothing")
