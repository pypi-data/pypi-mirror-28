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

from civil.plan.general_move_command import GeneralMoveCommand
from civil.plan.plan import Plan


class Rout(GeneralMoveCommand):
    """
    This class implements the plan 'rout'. It is used when a unit has been routed and is
    retreating to some location.
    
    Parameters:

    o the numeric id of the unit
    o the x- and y-coordinates of the rout destination.
    """

    def __init__(self, unit_id=-1, x=-1, y=-1):
        """
        Initializes the instance.
        """
        # call superclass constructor, the turn may not be valid here yet
        Plan.__init__(self, "rout", unit_id)

        # set illegal values for all data
        self.unit_id = unit_id
        self.target_x = x
        self.target_y = y

        # a nice text for the label
        self.labeltext = "rout"

    def extract(self, parameters):
        """
        Extracts the data for the rout.
        """

        # parse out the data
        self.id = int(parameters[0])
        self.unit_id = int(parameters[1])
        self.target_x = int(parameters[2])
        self.target_y = int(parameters[3])

    def getTarget(self):
        """
        Returns the target position the unit should move to as an (x,y) tuple.
        """
        return self.target_x, self.target_y

    def toString(self):
        """
        Returns a string representation of the command, suitable for sending over a socket.
        """
        # create a string
        return '%s %d %d %d %d\n' % (self.getName(), self.id, self.unit_id, self.target_x, self.target_y)

    def __str__(self):
        """
        Convenience wrapper for toString() suitable for using when debugging and printing the
        command to the screen. Will just call toString().
        """
        return self.toString()
