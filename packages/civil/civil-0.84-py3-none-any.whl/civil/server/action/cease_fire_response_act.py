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


class CeaseFireResponseAct(Action):
    """
    This class implements the action 'cease fire response'. It is sent to the player that initiated
    a cease fire question and contains the answer that the other player gave. Based on the answer
    the game is either ended or it continues as normally.
    """

    def __init__(self, player=-1, accepted=0):
        """
        Initializes the instance.
        """
        # call superclass constructor
        Action.__init__(self, "cease_fire_response_act")

        # store the player too
        self.player = player
        self.accepted = accepted

    def getPlayer(self):
        """
        Returns the player the update was created by.
        """
        return self.player

    def wasAccepted(self):
        """
        Returns 1 if the cease fire was accepted and 0 if not.
        """
        return self.accepted

    def extract(self, parameters):
        """
        Extracts the data for the command.
        """
        # parse out the data
        self.player = int(parameters[0])
        self.accepted = int(parameters[1])

    def execute(self):
        """
        Executes the action. Ends the game or continues as normally.
        """

        # are we the same player that sent the request?
        if self.player == scenario.local_player_id:
            # yes, we don't want to do anything here, only the remote player has anything to do
            return

        # this should actually never be sent to the AI player, as it never sends out an cease fire request
        if scenario.local_player_ai:
            # ai player
            print("AI: CeaseFireResponseAct.execute: *** should never happen ***")
            return

        # was the request accepted?
        if self.accepted:
            # yes, the game should end here and now
            scenario.messages.add("Your cease fire offer was accepted, ending the game")

            # the game is not being played anymore, we can stop immediately
            scenario.playing = constants.GAME_ENDED
            scenario.end_game_type = constants.CEASE_FIRE

        else:
            # not accepted
            scenario.messages.add("Your cease fire offer was rejected")

    def toString(self):
        """
        Returns a string representation of the command, suitable for sending over a socket.
        """
        # create a string and return
        return "%s %d %d\n" % (self.getName(), self.player, self.accepted)

    def __str__(self):
        """
        Convenience wrapper for toString() suitable for using when debugging and printing the
        command to the screen. Will just call toString().
        """
        return self.toString()
