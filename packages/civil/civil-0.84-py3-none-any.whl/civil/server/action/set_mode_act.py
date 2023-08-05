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
from civil.server.mode.mode_factory import createMode


class SetModeAct(Action):
    """
    This class implements the action 'setmode'. This is sent by the server when an unit
    gets a new mode.
    """

    def __init__(self, unit_id=-1, mode=""):
        """
        Initializes the instance.
        """
        # call superclass constructor, the turn may not be valid here yet
        Action.__init__(self, "set_mode_act")

        # set values for all data
        self.unit_id = unit_id
        self.mode = mode

    def extract(self, parameters):
        """
        Extracts the data for the move.
        """

        # parse out the data
        self.unit_id = int(parameters[0])
        self.mode = parameters[1]

    def execute(self):
        """
        Executed the action. Finds the affected unit and updates its mode to the new mode.
        """

        # get the unit with the given id 
        unit = scenario.info.units[self.unit_id]

        # create the proper mode instance
        mode = createMode(self.mode)

        # assign it
        unit.setMode(mode)

        # make sure the world knows of this change
        if not scenario.local_player_ai:
            scenario.dispatcher.emit('units_changed', (unit,))

    def toString(self):
        """
        Returns a string representation of the command, suitable for sending over a socket.
        """
        # create a string
        return "%s %d %s\n" % (self.getName(), self.unit_id, self.mode)

    def __str__(self):
        """
        Convenience wrapper for toString() suitable for using when debugging and printing the
        command to the screen. Will just call toString().
        """
        return self.toString()
