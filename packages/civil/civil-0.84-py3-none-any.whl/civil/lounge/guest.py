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

from civil.net.connection import Connection


class Guest:
    """
    This class 

 """

    def __init__(self, socket):
        """
        Initializes the guest with the passed data. The 'socket' is an open socket to the guest.
        """
        # set bogus data
        self.name = 'unknown'

        # store the socket as a connection
        self.connection = Connection(socket=socket)

    def getName(self):
        """
        Returns the name of the guest.
        """
        return self.name

    def setName(self, name):
        """
        Sets a new name for the guest.
        """
        self.name = name

    def send(self, line):
        """
        Sends the line of data to the guest.
        """
        self.connection.send(line)

    def getConnection(self):
        """
        Returns the network connection to the guest.
        """
        return self.connection

    def fileno(self):
        """
        Returns a integer referring to the internal connection.
        """
        return self.connection.fileno()
