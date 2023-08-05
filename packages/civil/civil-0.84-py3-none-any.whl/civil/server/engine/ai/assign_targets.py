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
from civil.server.action.add_plan_act import AddPlanAct
from civil.constants import HOLDFIRE, DEFENSIVEFIRE
from civil.plan.skirmish import Skirmish
from civil.server.engine.ai.module import Module


class AssignTargets(Module):
    """
    This class defines a module that when executed checks units that have no target assigned to
    them and assigns a skirmish target. This reduces the click-load for the players, as the server
    will aid in giving the units targets.

    The code will favour the closest unit that is accessible without rotating, but it will rotate
    the unit if no other target is accessible.

    This module is executed every step.
    """

    def __init__(self):
        """
        Initializes the module. Sets a suitable name.
        """

        # call superclass with the delays
        Module.__init__(self, 'assign targets')

    def execute(self, actiondata):
        """
        Executes the module. Loops over all units and assigns suitable skirmish targets to units
        that have no current target.

        This method will favour targets that are closest and in the same direction as the unit is
        facing. If the unit must turn the target is penalized. If a suitable target is found a
        Skirmish plan is created for the unit.
        """

        # loop over all units we have
        for unit in scenario.info.units.values():
            # does the unit already have some other plan?
            if len(unit.getPlans()) > 0:
                # unit already has plans, so not eligible for skirmish
                continue

            # does it already have a target? no use to assign many targets
            if unit.getTarget() is not None:
                # already has a target
                continue

            # can the unit skirmish in its current mode?
            if not unit.getMode().canSkirmish():
                # unit can't skirmish in it's current mode
                continue

            # get the combat policy
            policy = unit.getCombatPolicy()

            # is the unit not allowed to do anything?
            if policy == HOLDFIRE:
                # do nothing with this unit
                continue

            # check morale, fatigue
            if unit.getMorale().checkSkirmish() == 0 or unit.getFatigue().checkSkirmish() == 0:
                # either the morale is too low or the fatigue is too high, we won't do combat
                print("AssignTargets.execute: morale or fatigue fails, no target for:", unit)
                continue

            if policy == DEFENSIVEFIRE:
                # defensive fire only, check for a suitable attacker
                self.checkDefensiveFire(unit, actiondata)
                continue

            # unit is allowed to fire at will

            # store the unit owner for speed
            owner = unit.getOwner()
            mindistance = 10000000

            # no chosen target yet
            chosentarget = None

            # unit is eligible for skirmish, so find a unit that it should target
            for potentialtarget in scenario.info.units.values():
                # is it a unit of the opposite side
                if potentialtarget.getOwner() == owner:
                    # same side, no target
                    continue

                # it can be a potential enemy. do we see it and is it in range?
                if not unit.inRange(potentialtarget) or not unit.seesEnemy(potentialtarget):
                    # not in range or not visible
                    continue

                # get the distance to the unit. The distance is squared, so it's just for comparison
                distance = unit.distance(target=potentialtarget, simple=1)

                # add to the distance if we're not facing the enemy, and thus prefer those that are
                # available without rotating
                if not unit.pointedAt(potentialtarget):
                    # double the distance
                    distance *= 2

                # is the distance less than the currently closest distance?
                if distance < mindistance:
                    # yep, we have a new target candidate
                    mindistance = distance
                    chosentarget = potentialtarget

            # now we've gone through all units, do we have a chosen target?
            if chosentarget is not None:
                # yep, the unit now has a suitable target, create a new 'skirmish' plan and assign it
                plan = Skirmish(unit_id=unit.getId(), targetid=chosentarget.getId())

                # add it to the plans for the unit
                unit.getPlans().append(plan)

                # we need some actions so that all parties know of the new plan
                actiondata.append(AddPlanAct(unit.getId(), plan))

                print("AssignTargets.execute: %s skirmish %s" % (unit.getName(), chosentarget.getName()))

    def checkDefensiveFire(self, unit, actiondata):
        """
        Checks weather there are any suitable enemies that are attacking this unit. If there is
        and they are in range then they are set as targets for the unit.

        This method will favour the unit targetting an attacker that is closest and in the same
        direction as the unit is facing. If the unit must turn the attacker is penalized.
        """

        # store the unit owner for speed
        owner = unit.getOwner()
        mindistance = 10000000

        # no chosen target yet
        chosentarget = None

        # unit is eligible for skirmish, so find a unit that it should target
        for potentialtarget in scenario.info.units.values():
            # is it a unit of the opposite side
            if potentialtarget.getOwner() == owner:
                # same side, no target
                continue

            # des the enemy currently have our unit as a target?
            if potentialtarget.getTarget() != unit:
                # no, so it can't be fired upon either
                continue

            # get the distance to the unit. The distance is squared, so it's just for comparison
            distance = unit.distance(target=potentialtarget, simple=1)

            # add to the distance if we're not facing the enemy, and thus prefer those that are
            # available without rotating
            if not unit.pointedAt(potentialtarget):
                # double the distance
                distance *= 2

            # is the distance less than the currently closest distance?
            if distance < mindistance:
                # yep, we have a new target candidate
                mindistance = distance
                chosentarget = potentialtarget

        # now we've gone through all units, do we have a chosen target?
        if chosentarget is not None:
            # yep, create a new skirmish plan
            plan = Skirmish(unit_id=unit.getId(), targetid=chosentarget.getId())

            # add it to the plans for the unit
            unit.getPlans().append(plan)

            # we need some actions so that all parties know of the new plan
            actiondata.append(AddPlanAct(unit.getId(), plan))

            print("AssignTargets.checkDefensiveFire: %s skirmish with %s" % (unit.getName(),
                                                                             chosentarget.getName()))
