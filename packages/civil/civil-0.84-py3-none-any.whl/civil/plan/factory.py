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

# import all plans
from civil.plan.assault import Assault
from civil.plan.change_combat_policy import ChangeCombatPolicy
from civil.plan.change_mode import ChangeMode
from civil.plan.move import Move
from civil.plan.move_fast import MoveFast
from civil.plan.retreat import Retreat
from civil.plan.rotate import Rotate
from civil.plan.rout import Rout
from civil.plan.skirmish import Skirmish
from civil.plan.wait import Wait

# our map of creators
creators = {'assault': Assault,
            'changecombatpolicy': ChangeCombatPolicy,
            'changemode': ChangeMode,
            'move': Move,
            'movefast': MoveFast,
            'retreat': Retreat,
            'rotate': Rotate,
            'rout': Rout,
            'skirmish': Skirmish,
            'wait': Wait
            }


def create(parameters):
    """
    Creates a new plan from the passed parameters. The parameter is a list of strings string that
    is supposed to be data for a plan. The first word is the type of plan, and the other are data
    for that specific plan. Based on the type a new plan is created and returned.
    """

    print("plan: create:", parameters)

    # get the packet type
    plan_type = parameters[0]

    # do we have such a plan?
    if plan_type not in creators:
        # unknown plan type
        raise RuntimeError("factory.create: unknown plan type: '" + plan_type + "', params: ", parameters)

    # create a plan based on the type
    plan = creators[plan_type]()

    # and let it extract whatever it needs from the parameters it got
    plan.extract(parameters[1:])

    return plan
