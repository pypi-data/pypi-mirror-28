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

# import all actions
from civil.server.action.add_plan_act import AddPlanAct
from civil.server.action.cease_fire_act import CeaseFireAct
from civil.server.action.cease_fire_response_act import CeaseFireResponseAct
from civil.server.action.change_combat_policy_act import ChangeCombatPolicyAct
from civil.server.action.change_modifiers_act import ChangeModifiersAct
from civil.server.action.chat_act import ChatAct
from civil.server.action.clear_plans_act import ClearPlansAct
from civil.server.action.clear_target_act import ClearTargetAct
from civil.server.action.damage_act import DamageAct
from civil.server.action.done_act import DoneAct
from civil.server.action.end_game_act import EndGameAct
from civil.server.action.move_act import MoveAct
from civil.server.action.quit_act import QuitAct
from civil.server.action.reinforcements_act import ReinforcementsAct
from civil.server.action.rotate_act import RotateAct
from civil.server.action.set_mode_act import SetModeAct
from civil.server.action.set_target_act import SetTargetAct
from civil.server.action.set_visibility_act import SetVisibilityAct
from civil.server.action.surrender_act import SurrenderAct
from civil.server.action.time_act import TimeAct

# our map of creators
creators = {'add_plan_act': AddPlanAct,
            'cease_fire_act': CeaseFireAct,
            'cease_fire_response_act': CeaseFireResponseAct,
            'change_combat_policy_act': ChangeCombatPolicyAct,
            'change_modifiers_act': ChangeModifiersAct,
            'chat_act': ChatAct,
            'clear_plans_act': ClearPlansAct,
            'clear_target_act': ClearTargetAct,
            'damage_act': DamageAct,
            'done_act': DoneAct,
            'endgame_act': EndGameAct,
            'move_act': MoveAct,
            'quit_act': QuitAct,
            'reinforcements_act': ReinforcementsAct,
            'rotate_act': RotateAct,
            'set_target_act': SetTargetAct,
            'set_mode_act': SetModeAct,
            'set_visibility_act': SetVisibilityAct,
            'surrender_act': SurrenderAct,
            'time_act': TimeAct
            }


def isAction(type):
    """
    Checks weather the given type (string) is an action or not. This can be used by the engine to
    determine weather something is a plan or an action. Return 1 if it is an action and 0 if not.
    """
    # just do a check
    return type in creators


def create(parameters):
    """
    Creates a new action from the passed parameters. The parameter is a list of strings string
    that is supposed to be data for a action. The first word is the type of action, and the other
    are data for that specific upate. Based on the type a new instance is created and returned.
    """

    # get the packet type
    type = parameters[0]

    # do we have such a plan?
    if type not in creators:
        # not an action
        return None

    # create a action based on the type
    action = creators[type]()

    # and let it extract whatever it needs from the parameters it got
    action.extract(parameters[1:])

    return action
