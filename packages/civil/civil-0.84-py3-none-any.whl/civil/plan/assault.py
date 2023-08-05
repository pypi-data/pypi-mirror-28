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
from civil.plan.plan import Plan


class Assault(Plan):
    """
    This class implements the plan 'assault'. This plan means that the unit has been ordered to
    do a full scale assault on the target. An assault means that the unit will advance against the
    target while firing at it, and when close enough perform an assault and engage in hand-to-hand
    combat. Bloody stuff.

    Parameters:

    o the numeric id of the attacker unit
    o the numeric id of the target unit
    """

    def __init__(self, unit_id=-1, targetid=-1):
        """
        Initializes the instance.
        """
        # call superclass constructor, the turn may not be valid here yet
        Plan.__init__(self, "assault", unit_id)

        # set illegal values for all data
        self.unit_id = unit_id
        self.targetid = targetid

        # create the label
        self.createLabel()

    def createLabel(self):
        """
        Create the label text.
        """
        # do we have a target yet?
        if self.targetid == -1:
            # nope, set something invalid
            self.labeltext = "assaulting unknown"
            return

        # first get the full unit if we have it
        targetunit = scenario.info.units[self.targetid]

        # a nice text for the label
        self.labeltext = "assaulting %s" % targetunit.getTypeString().lower()

    def extract(self, parameters):
        """
        Extracts the data for the move.
        """

        # parse out the data
        self.id = int(parameters[0])
        self.unit_id = int(parameters[1])
        self.targetid = int(parameters[2])

        # create the label
        self.createLabel()

    def getTargetId(self):
        """
        Returns the id of the target we're assaulting.
        """
        return self.targetid

    def toString(self):
        """
        Returns a string representation of the command, suitable for sending over a socket.
        """
        # create a string and return it
        return '%s %d %d %d\n' % (self.getName(), self.id, self.unit_id, self.targetid)

    def __str__(self):
        """
        Convenience wrapper for toString() suitable for using when debugging and printing the
        command to the screen. Will just call toString().
        """
        return self.toString()
