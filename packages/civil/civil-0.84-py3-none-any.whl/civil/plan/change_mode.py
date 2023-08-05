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

from civil.plan.plan import Plan


class ChangeMode(Plan):
    """
    This class implements the plan 'changemode'. This plan is sent by clients when a unit has been
    ordered to change it mode. Modes can by the player be changed like this:

    * limbered -> unlimbering -> unlimbered
    * mounted -> dismounting -> dismounted
    * formation -> changing to formation -> column

    And of course the reverse too. This plan will alter the mode of the unit, i.e. basically toggle it.

    Parameters:

    o the numeric id of the unit.
    """

    def __init__(self, unit_id=-1):
        """
        Initializes the instance.
        """
        # call superclass constructor, the turn may not be valid here yet
        Plan.__init__(self, "changemode", unit_id)

        # store passed data
        self.unit_id = unit_id

        # get the unit
        # unit = scenario.info.units[unit_id]

        # a nice text for the label
        self.labeltext = "changing mode"

        # TODO: this doesn't work, as the unit will be invalid here
        # self.labeltext = unit.getMode ().getTitle ()

    def extract(self, parameters):
        """
        Extracts the data for the plan and stores in local variables. This method is used
        when the command has been sent over the network.
        """

        # parse out the data
        self.id = int(parameters[0])
        self.unit_id = int(parameters[1])

    def toString(self):
        """
        Returns a string representation of the command, suitable for sending over a socket.
        """
        # create a string and return
        return "%s %d %d\n" % (self.getName(), self.id, self.unit_id)

    def __str__(self):
        """
        Convenience wrapper for toString() suitable for using when debugging and printing the
        command to the screen. Will just call toString().
        """
        return self.toString()
