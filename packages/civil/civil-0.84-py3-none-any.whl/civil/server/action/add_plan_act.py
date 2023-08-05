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

from civil import plan
from civil.model import scenario
from civil.server.action.action import Action


class AddPlanAct(Action):
    """
    This class implements the action 'add plan'. This is sent by the server when an unit
    has finished a plan and it should be removed from the unit's plans. The first plan that the unit
    has (the one that's supposed to be active) is removed.
    """

    def __init__(self, unit_id=-1, plan=None):
        """
        Initializes the instance.
        """
        # call superclass constructor
        Action.__init__(self, "add_plan_act")

        # store all data
        self.unit_id = unit_id

        # store the plan
        self.plan = plan

    def extract(self, parameters):
        """
        Extracts the data for the command.
        """
        # parse out the data
        self.unit_id = int(parameters[0])

        print("AddPlanAct.extract:", parameters[1:])

        # create the plan from the rest of the data
        self.plan = plan.factory.create(parameters[1:])

    def execute(self):
        """
        Executed the action. Finds the affected unit and just removes the first plan it has.
        """

        # get the unit with the given id 
        unit = scenario.info.units[self.unit_id]

        # is it a local unit? only do this to local units
        if unit.getOwner() == scenario.local_player_id:
            # add the new plan
            unit.getPlans().append(self.plan)

    def toString(self):
        """
        Returns a string representation of the command, suitable for sending over a socket.
        """
        # create a string and return
        return "%s %d %s\n" % (self.getName(), self.unit_id, self.plan.toString().strip())

    def __str__(self):
        """
        Convenience wrapper for toString() suitable for using when debugging and printing the
        command to the screen. Will just call toString().
        """
        return self.toString()
