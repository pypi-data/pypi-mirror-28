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


class SurrenderAct(Action):
    """
    This class implements the action 'surrender'. This updated means that the player sending
    it wants to surrender the battle unconditionally and declare the opponent a winner. The server
    will internally handle the surrender and send out an 'EndGame' update to both players.
    """

    def __init__(self, player=-1):
        """
        Initializes the instance.
        """
        # call superclass constructor
        Action.__init__(self, "surrender_act")

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
        Executes the plan. Will terminate the application by setting the flag that indicates that
        the main loop should terminate. Stores the surrendering player data.
        """

        # we're no longer playing a game
        scenario.playing = constants.GAME_ENDED

        # get the type of end game
        endgametype = [constants.REBEL_SURRENDER, constants.UNION_SURRENDER][self.player]

        # store the type of end game
        scenario.end_game_type = endgametype

        # this should not be done for the ai
        if scenario.local_player_ai:
            # ai player, go away
            return

        # add the message we have to the messages
        surrendername = ['Rebel', 'Union'][self.player]
        scenario.messages.add("%s player has surrendered" % surrendername, CHAT1)

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
