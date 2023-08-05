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

from civil import constants
from civil.model import scenario
from civil.server.action.action import Action
from civil.ui.messages import CHAT1


class QuitAct(Action):
    """
    This class implements the action 'quit'. Used when a player has quit.

    TODO: should also contain some kind of info for why that game was quit?
    """

    def __init__(self, player=-1):
        """
        Initializes the instance.
        """
        # call superclass constructor
        Action.__init__(self, "quit_act")

        # store the player too
        self.player = player

    def extract(self, parameters):
        """
        Extracts the data for the command.
        """
        # parse out the data
        self.player = int(parameters[0])

    def execute(self):
        """
        Executes the action. Sets a flag that indicates that the game has ended.
        """
        # we're no longer playing a game. this also terminates the AI client as the human player has
        # quit 
        scenario.playing = constants.GAME_ENDED

        # get the type of end game
        endgametype = [constants.REBEL_QUIT, constants.UNION_QUIT][self.player]

        # store the type of end game
        scenario.end_game_type = endgametype

        # this should not be done for the ai
        if scenario.local_player_ai:
            # ai player, go away
            print("AI: QuitAct.execute: human player has quit, so we will too")
            return

        # add the message we have to the messages
        surrendername = ['Rebel', 'Union'][self.player]
        scenario.messages.add("%s player has quit" % surrendername, CHAT1)

    def toString(self):
        """
        Returns a string representation of the command, suitable for sending over a socket.
        """
        # create a string and return
        return "%s %d\n" % (self.getName(), self.player)

    def __str__(self):
        """
        Convenience wrapper for toString() suitable for using when debugging and printing the
        command to the screen. Will just call toString().
        """
        return self.toString()
