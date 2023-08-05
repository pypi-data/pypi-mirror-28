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

from civil.server.engine.executor.assault_exec import AssaultExec
from civil.server.engine.executor.change_combat_policy_exec import ChangeCombatPolicyExec
from civil.server.engine.executor.change_mode_exec import ChangeModeExec
from civil.server.engine.executor.move_exec import MoveExec
from civil.server.engine.executor.move_fast_exec import MoveFastExec
from civil.server.engine.executor.retreat_exec import RetreatExec
from civil.server.engine.executor.rotate_exec import RotateExec
from civil.server.engine.executor.rout_exec import RoutExec
from civil.server.engine.executor.skirmish_exec import SkirmishExec
from civil.server.engine.executor.wait_exec import WaitExec

# our map of creators
creators = {'assault': AssaultExec,
            'changecombatpolicy': ChangeCombatPolicyExec,
            'changemode': ChangeModeExec,
            'move': MoveExec,
            'movefast': MoveFastExec,
            'retreat': RetreatExec,
            'rotate': RotateExec,
            'rout': RoutExec,
            'skirmish': SkirmishExec,
            'wait': WaitExec
            }


def create(unit, plan):
    """
    Creates a new plan executor from the passed plan. Based on the plan type a new executor is


 """

    # get the plan type
    type = plan.getName()

    # do we have such a plan?
    if type not in creators:
        # unknown plan type
        raise RuntimeError("factory.create: unknown plan type: '%s'" % type)

    # create a executor based on the plan type
    executor = creators[type](unit, plan)

    return executor
