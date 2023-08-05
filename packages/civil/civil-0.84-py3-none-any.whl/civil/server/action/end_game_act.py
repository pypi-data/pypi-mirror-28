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


class EndGameAct(Action):
    """
    This class implements the action 'endgame'. This is sent by the server when the game has been
    ended for some reason. The reason could be that one player has lost, resigned or that the time
    allocated for the battle has run out. This update will set a flag that terminates the main event
    loops for the client and the AI players.

    This command also sets a flag that indicates how the game ended, i.e. which player won, was it a
    surrender etc. The constants are defined in the file constants.py.
    """

    def __init__(self, how=constants.BOTH_DESTROYED):
        """
        Initializes the instance.
        """
        # call superclass constructor
        Action.__init__(self, "endgame_act")

        # store the flag indicating how the game ended
        self.how = how

    def extract(self, parameters):
        """
        Extracts the data for the command. The only data is the turn when the ending should take
        place.
        """
        # parse out the data
        self.how = int(parameters[0])

    def execute(self):
        """
        Executed the command. Sets a flag that will later terminate the main event loop. Also
        sets a flag that indicates how the game ended.
        """

        # set flags
        scenario.playing = constants.GAME_ENDED
        scenario.end_game_type = self.how

    def toString(self):
        """
        Returns a string representation of the command, suitable for sending over a socket.
        """
        # create a string and return
        return "%s %d\n" % (self.getName(), self.how)

    def __str__(self):
        """
        Convenience wrapper for toString() suitable for using when debugging and printing the
        command to the screen. Will just call toString().
        """
        return self.toString()
