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

import random

from civil import constants
from civil.model import scenario
from civil.server.action.damage_act import DamageAct
from civil.server.engine.ai.module import Module


class ResolveMelee(Module):
    """
    This class defines a module that resolves all melee combat that is currently taking
    place. Units meleeing are in close hand to hand combat, which is very deadly, and usually means
    that one unit is routed.

    The module finds every unit whose mode indicates that it is meleeing, and then resolves the
    melee between those two units. If two unit melee against a third the attacked unit is meleeing
    twice, once with each attacker. 

    This module is executed every 5:th step.
    """

    def __init__(self):
        """
        Initializes the module. Sets a suitable name.
        """

        # call superclass
        Module.__init__(self, 'resolve melee', 30)

    def execute(self, actiondata):
        """
        Executes the module. Loops over all units and checks which units are meleeing, and if
        it is then melee is executed for both parties. A unit that has meleed will be put in a list
        of units already done, so that they won't melee again. However, a unit that is meleeing with
        two other units will melee twice.
        """
        # no units have meleed yet
        self.has_meleed = []

        # loop over all units we have
        for unit in scenario.info.units.values():
            # is the unit currently meleeing or it has already meleed this step? 
            if not unit.getMode().isMeleeing() or unit in self.has_meleed:
                # not meleeing or already meleed next please
                continue

            # ok, this unit has not already meleed, get it's target. the target may already have
            # meleed with some other unit, but we don't mind that, if it is meleeing with two units
            # it should be here twice. we also don't mind who is the attacker and who is the
            # defender here
            target = unit.getTarget()

            # verify that both units are destroyed. the target may also be None if normal combat the
            # same turn destroyed the unit. then the target is set to None, although the mode still
            # says that the unit should melee. so check for None here too
            if target is None or unit.isDestroyed() or target.isDestroyed():
                # either unit is destroyed, so no melee
                print("ResolveMelee.execute: one melee party is destroyed, no melee")

                # clear the target and set the proper mode for the unit
                self.clearTarget(unit, actiondata)

                continue

            # note that melee has no fatigue or morale check. both units melee regardless of their
            # state. one unit may break and rout *after* the melee if morale drops too low, but here
            # we do no such checks

            # resolve the melee between the two units
            self.resolveMelee((unit, target), actiondata)

            # these both units have now meleed
            self.has_meleed.append(unit)
            self.has_meleed.append(target)

    def resolveMelee(self, units, actiondata):
        """
        Resolves one single melee fight between the two units in 'units'. The resulting action is
        put into  'actiondata' and the units are updated accordingly.

        The calculation is performed by taking the base damage value for both units, and using a ratio
        of the damage values as base for the losses. The damage that the units suffer is sent out
        and alos applied to the units directly.

        If one of the units is destroyed then the other one is set as disorganized. This is because
        the unit is not immediately ready for new action.
        """

        print("ResolveMelee.resolveMelee:", units[0], units[1])

        # no damage to anybody yet
        damages = [0.0, 0.0]
        gunsdestroyed = [0, 0]

        # no men yet
        men = 0

        # we need to calculate the damage value for both units
        for index in (0, 1):
            # get the unit
            unit = units[index]

            # add the number of men participating to the total
            men += unit.getMen()

            # get the base weapon damage of the unit
            damage = unit.getDamage()

            # is the unit an artillery unit? they are not useful while at this close range
            if unit.getWeapon().isArtillery():
                # yep, reduce damage by 50%
                damage *= 0.50

            # modify by skill
            damage = unit.getExperience().evaluateMelee(damage)

            # modify by fatigue
            damage = unit.getFatigue().evaluateMelee(damage)

            # entrenchment?
            # entrenchment = 1.0

            # modify damage by terrain and entrenchment level
            # damage = damage * defensemod * entrenchment

            # modify by random damage. range: 0.8 to 1.2
            damage = damage * random.randrange(80, 120) / 100

            # precautin to avoid a damage value of 0 (division by zero later). if the unit does no
            # normal damage it can at least kick the enemy or use foul language to scare it
            damage = max(1.0, damage)

            # store the damage
            damages[index] = damage

        # calculate the damage ratio, i.e how much more damage either unit caused. we
        ratios = (damages[0] / damages[1], damages[1] / damages[0])

        # print "ResolveMelee.resolveMelee: damages: %f %f" % ( damages[0], damages[1] )
        # print "ResolveMelee.resolveMelee: ratios:  %f %f" % ( ratios[0], ratios[1] )

        # use the ratio to see how many men were killed. we directly multiply this ratio with 10% of
        # all the men in both units combined
        killed = (int(men * 0.10 * ratios[0]), int(men * 0.10 * ratios[1]))

        print("ResolveMelee.resolveMelee: killed %d %d" % (killed[0], killed[1]))

        # TODO: did we lose any artillery guns? hmm, do we lose them at all?

        # modify fatigue
        self.__modifyFatigue(units, actiondata)

        # modify morale and check for routs

        # create action for all the damages and modifier changes
        for index in (0, 1):
            # get the unit
            unit = units[index]
            other_unit = units[1 - index]

            # create action for the total damage
            act = DamageAct(unit_id=unit.id, damagetype=constants.KILLED, damagecount=killed[index],
                            attacker_id=other_unit.getId())
            actiondata.append(act)

            # apply the damage. if the unit is destroyed it will mark itself as destroyed and remove
            # itself from the global unit structures
            unit.applyDamage(type=constants.KILLED, count=killed[index])

        # print "ResolveMelee.resolveMelee: destroyed: %d %d" % (units[0].isDestroyed (), units[1].isDestroyed ())

        # did either unit get destroyed and the other is ok? if one unit is destroyed the other one
        # should stop meleeing too and assume a disorganized mode. This is because the unit is not
        # immediately ready for new action. 
        if units[0].isDestroyed() and not units[1].isDestroyed():
            # the first unit was destroyed, make the other one disorganized. the melee is now over
            self.clearTarget(units[1], actiondata)

        if units[1].isDestroyed() and not units[0].isDestroyed():
            # the second unit was destroyed
            self.clearTarget(units[0], actiondata)

    def __modifyFatigue(self, units, actiondata):
        """
        Modifies (increases) the fatigue for both involved units based on their modes. Different
        units have different melee modes, and they add to fatigue differently. Modifies the units
        and creates suitable action data.
        """

        # loop over both units
        for unit in units:
            # get the possible base fatigue change
            fatigue = unit.getMode().getBaseFatigue()

            # multiply it with the number of steps that we have been meleeing. as this is run every
            # 5th step, we should have fatigue five times as great as the base
            # TODO: wrong numbers!
            fatigue *= 5.0

            #  add the fatigue for the unit
            unit.getFatigue().addValue(int(fatigue))

            # create the action stuff too
            self.changeModifiers(unit, actiondata)

    def __modifyMorale(self, units, actiondata, ):
        """
        Modifies the morale for the units. Morale will drop fast if the unit takes heavy
        casualities. Green units also drop morale easier than veteran units. Units that have taken
        casualities earlier also drop morale faster.
        """

        # check for experience

        # check for percentage of men lost earlier and now

        #
        pass
