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

import string

from civil.model import scenario
from civil.server.action.action import Action
from civil.ui.messages import CHAT1


class ChatAct(Action):
    """
    This class implements the action 'chat'. This will send a message to the other player. The
    message is some text that the player wants to send to the other player. When executed the
    message contained in the object will be added to all other messages to the player, and displayed
    in the playfield.
    """

    def __init__(self, message=""):
        """
        Initializes the instance.
        """
        # call superclass constructor
        Action.__init__(self, "chat_act")

        # store the message and player
        self.message = message

    def extract(self, parameters):
        """
        Extracts the data for the command. The only data is the turn when the chat should take place.
        """
        # parse out the data
        self.message = "".join(parameters)

    def execute(self):
        """
        Adds the message to the panel.
        """

        # this should not be done for the ai
        if scenario.local_player_ai:
            # ai player, send a dummy reply
            scenario.connection.send(ChatAct("Talk less, play more").toString())
            return

        # add the message we have to the messages
        scenario.messages.add(self.message, CHAT1)

    def toString(self):
        """
        Returns a string representation of the command, suitable for sending over a socket.
        """
        # create a string and return
        return "%s %s\n" % (self.getName(), self.message)

    def __str__(self):
        """
        Convenience wrapper for toString() suitable for using when debugging and printing the
        command to the screen. Will just call toString().
        """
        return self.toString()
