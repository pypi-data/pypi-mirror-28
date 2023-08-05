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


class Player:
    """
    This class defines a player as the server sees one. A player consists of an id that define the
    side the player has along with a connection. The connection is used to receive and send data to/from the
    player. The connection can not be altered once set, but the id can be changed.
    """

    def __init__(self, connection, id, name):
        """
        Creates an instance of the class. Uses the passed data or default values.
        """
        # set the passed name and rank
        self.name = name
        self.id = id
        self.connection = connection

    def getId(self):
        """
        Returns the id of the player.
        """
        return self.id

    def setId(self, id):
        """
        Stores a new id for the player.
        """
        self.id = id

    def getOtherPlayerId(self):
        """
        Returns the id of the other player.
        """

    def getName(self):
        """
        Returns the name of the player. This is a cleartext name suitable for displaying to the


 """
        return self.name

    def setName(self, name):
        """
        Stores a new name for the player.
        """
        self.name = name

    def getConnection(self):
        """
        Returns the connection connected to the player.
        """
        return self.connection
