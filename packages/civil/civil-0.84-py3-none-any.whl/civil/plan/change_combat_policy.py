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


class ChangeCombatPolicy(Plan):
    """
    This class implements the plan 'changecombatpolicy'. This plan is used to set a general combat
    policy for the unit. The combat policy affects how the unit gets automatically assigned
    combat orders. The value is an integer defined in the file unit.py.
    
    Parameters:

    o the numeric id of the unit.
    o the new policy for the unit.
    """

    def __init__(self, unit_id=-1, policy=-1):
        """
        Initializes the instance.
        """
        # call superclass constructor, the turn may not be valid here yet
        Plan.__init__(self, "changecombatpolicy", unit_id)

        # store passed data
        self.unit_id = unit_id

        # store the policy
        self.policy = policy

        # set a nice text depending on the policy id
        self.labeltext = ('holding fire', 'defensive fire only', 'firing at will')[policy]

        # this plan can not be visualized
        self.showonplayfield = 0

    def extract(self, parameters):
        """
        Extracts the data for the rotation and stores in local variables. This method is used
        when the command has been sent over the network.
        """

        # parse out the data
        self.id = int(parameters[0])
        self.unit_id = int(parameters[1])
        self.policy = int(parameters[2])

    def getPolicy(self):
        """
        Returns the new combat policy for the unit.
        """
        return self.policy

    def toString(self):
        """
        Returns a string representation of the command, suitable for sending over a socket.
        """
        # create a string and return
        tmp = "%s %d %d %d\n" % (self.getName(), self.id, self.unit_id, self.policy)

        # return it
        return tmp

    def __str__(self):
        """
        Convenience wrapper for toString() suitable for using when debugging and printing the
        command to the screen. Will just call toString().
        """
        return self.toString()
