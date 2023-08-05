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

from civil.model import scenario
from civil.server.action.action import Action


class MoveAct(Action):
    """
    This class implements the action 'move'. This is sent by the server when an unit
    should move to a new position. Facing, mode or other data is not affected in any way, just the
    unit position.
    """

    def __init__(self, unit_id=-1, x=-1, y=-1):
        """
        Initializes the instance.
        """
        # call superclass constructor
        Action.__init__(self, "move_act")

        # store all data
        self.unit_id = unit_id
        self.x = x
        self.y = y

    def extract(self, parameters):
        """
        Extracts the data for the command.
        """
        # parse out the data
        self.unit_id = int(parameters[0])
        self.x = int(parameters[1])
        self.y = int(parameters[2])

    def execute(self):
        """
        Executed the action. Finds the affected unit and updates its position to the new
        position.
        """

        # get the unit with the given id 
        unit = scenario.info.units[self.unit_id]

        # set the new position
        unit.setPosition((self.x, self.y))

        # make sure the world knows of this change
        if not scenario.local_player_ai:
            scenario.dispatcher.emit('units_changed', (unit,))

    def toString(self):
        """
        Returns a string representation of the command, suitable for sending over a socket.
        """
        # create a string and return
        return "%s %d %d %d\n" % (self.getName(), self.unit_id, self.x, self.y)

    def __str__(self):
        """
        Convenience wrapper for toString() suitable for using when debugging and printing the
        command to the screen. Will just call toString().
        """
        return self.toString()
