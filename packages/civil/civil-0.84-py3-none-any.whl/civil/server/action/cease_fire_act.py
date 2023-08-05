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

from civil.server.action.cease_fire_response_act import CeaseFireResponseAct
from civil import constants
from civil.model import scenario
from civil.server.action.action import Action


class CeaseFireAct(Action):
    """
    This class implements the action 'cease fire'. In case of a human player he/she is asked weather
    the cease fire should be accepted or rejected. If the cease fire is accepted then the game ends
    here and now, otherwise it continues. The AI player always accepts.
    """

    def __init__(self, player=-1):
        """
        Initializes the instance.
        """
        # call superclass constructor
        Action.__init__(self, "cease_fire_act")

        # store the player too
        self.player = player

    def getPlayer(self):
        """
        Returns the player the update was created by.
        """
        return self.player

    def extract(self, parameters):
        """
        Extracts the data for the command.
        """
        # parse out the data
        self.player = int(parameters[0])

    def execute(self):
        """
        Executes the action. In case of a human player he/she is asked weather the cease fire
        should be accepted or rejected. If the cease fire is accepted then the game ends here and
        now, otherwise it continues. The AI player always accepts.
        """

        # are we the same player that sent the request?
        if self.player == scenario.local_player_id:
            # yes, we don't want to do anything here, only the remote player has anything to do
            return

        # the AI player should just silently accept the cease fire request
        if scenario.local_player_ai:
            # ai player, accept request
            self.__acceptAI()
            return

        # find the name of the remote player. note that the strings are reversed
        other = ['union', 'rebel'][scenario.local_player_id]

        # add the message we have to the messages
        scenario.messages.add("The %s commander offers you a cease fire" % other)

        # use the current state to ask the player a question
        if scenario.current_state.askQuestion(['The %s commander offers you a cease fire.' % other,
                                               'Will you accept the offer?']) == 0:
            # the player did not accept it, send a negative response
            answer = CeaseFireResponseAct(scenario.local_player_id)

            # show some logging too
            scenario.messages.add("Cease fire offer declined")
        else:
            # the answer to our cease fire question was accepted, create a new action for the positive answer
            answer = CeaseFireResponseAct(scenario.local_player_id, 1)

            # some logging too
            scenario.messages.add("Cease fire offer accepted")

            # the game is not being played anymore, we can stop immediately
            scenario.playing = constants.GAME_ENDED
            scenario.end_game_type = constants.CEASE_FIRE

        # send the answer to the server for dispatching to the other player
        scenario.connection.send(answer.toString())

    def __acceptAI(self):
        """
        Accepts the cease fire request for the AI player.
        """
        # create the positive answer
        answer = CeaseFireResponseAct(scenario.local_player_id, 1)

        # the game is not being played anymore, we can stop immediately
        scenario.playing = constants.GAME_ENDED
        scenario.end_game_type = constants.CEASE_FIRE

        # send the answer to the server for dispatching to the other player
        scenario.connection.send(answer.toString())

        print("AI: CeaseFireAct.__acceptAI: accepted the cease fire request")

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
