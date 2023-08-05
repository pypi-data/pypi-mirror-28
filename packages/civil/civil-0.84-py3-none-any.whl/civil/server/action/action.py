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


class Action:
    """
    This class is a base class for all available types of actions that can be sent from the server to
    the clients. Actions are used to send information about something that has happened in a turn
    to the clients. Each action instance contains some small update to a unit or some other part of
    the client's datastructures.
    
    Every action contains a name which is a short lowercase string that identifies it. The name is
    unique only among classes, not instances. The name can be used to recognize the update when in
    deep debug mode.

    By default all actions are sent to all players, but by using setReceiver() some action can be
    sent to only one player.
    """

    def __init__(self, name):
        """
        Initializes the instance. Stores the name.
        """
        # store the name
        self.name = name

        # by default both players get this
        self.receiver = constants.BOTH

    def getName(self):
        """
        Returns the name of the action. This is a string that can be used to identify the class.
        """
        return self.name

    def getReceiver(self):
        """
        Returns the receiver of the action. This should be a player id or constants.BOTH for both


 """
        return self.receiver

    def setReceiver(self, receiver):
        """
        Sets a new receiver for the action. This is mainly used by the server when it creates
        actions. It determines which player gets the action. The default is that both player get
        it.
        """
        self.receiver = receiver

    def extract(self, parameters):
        """
        Extracts all data from the data coming from the network. This method is used whenever
        the instance has been written to the socket and an instance needs to be recreated from textual
        data.  This method should be overridden to perform whatever is needed. The 'parameters' is a
        list of all the parameters passed with the packet.
        """
        pass

    def execute(self):
        """
        This method applies the action to the client data structures. Usually it means changing
        some data for one a unit. It must be overridden by subclasses.
        """

        raise NotImplementedError("Action.execute: this method must be overridden")
