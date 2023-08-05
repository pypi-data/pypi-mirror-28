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

from civil.server.action.change_combat_policy_act import ChangeCombatPolicyAct
from civil.server.engine.executor.executor import Executor


class ChangeCombatPolicyExec(Executor):
    """
    This class implements an executor for the plan 'ChangeCombatPolicy'. It contains the actual code for
    executing changing the combat policy for the unit. Changing it really needs no extra data or
    delays, so it is immediately assigned.
    """

    def __init__(self, unit, plan):
        """
        Initializes the instance.
        """
        # call superclass constructor
        Executor.__init__(self, unit, plan)

    def execute(self):
        """
        Executes the plan. Simply just sets the new policy and sends out the action.
        """

        # assign the new policy to the unit
        self.unit.setCombatPolicy(self.plan.getPolicy())

        # this plan is finished now
        self.finished = 1

        # create action for the changed policy
        return ChangeCombatPolicyAct(self.unit.getId(), self.plan.getPolicy())
