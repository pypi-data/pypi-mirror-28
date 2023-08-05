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
from math import log

from civil.server.engine.executor import rotate_util
from civil import constants
from civil.model import scenario
from civil.server.action.change_modifiers_act import ChangeModifiersAct
from civil.server.action.damage_act import DamageAct


def skirmish(attacker, defender):
    """
    Executes a single skirmish where an attacker fires at a defender. Returns the generated
    action in a list. The action can be damage, changed modifiers, routs etc
    """

    # does the attacker defender still exist?
    if attacker.isDestroyed():
        # attacker has died, nothing to do
        return []

    # defender still ok?
    if defender.isDestroyed():
        # the defender has been destroyed somehow, clear the defender for the unit 
        attacker.setDefender(None)

        # TODO unknown, create action for that too
        return [ClearDefenderAct(attacker.getId())]

    # both are still ok, resolve this attack

    actiondata = []

    # no damage to anybody yet
    killed = 0
    gunsdestroyed = 0

    # is the attacker within range for melee combat? if so we don't resolve it here, that has a
    # separate module
    if attacker.getMode().isMeleeing():
        # yep, the attacker is already meleeing, so we don't resolve that here
        print("combat_util.resolveAttack: attacker already meleeing, not handled here")
        return []

    print("combat_util.resolveAttack: %s -> %s" % (attacker.getName(), defender.getName()))

    # is the attacker an artillery unit with guns left?
    if attacker.getWeapon().isArtillery() and attacker.getWeaponCounts()[0] > 0:
        # yes, check for exploded gun. possibility: 2%
        if random.randrange(0, 100) < 2:
            # oops, boom, there goes a gun , create action for that
            actiondata.append(DamageAct(unit_id=attacker.id, damagetype=constants.GUNSDESTROYED,
                                        damagecount=1, attacker_id=attacker.getId()))

            # also apply the damage to the unit. one less intact gun, one more destroyed gun
            ok, destroyed = attacker.getWeaponCounts()
            attacker.setWeaponCounts(ok - 1, destroyed + 1)

    # calculate the full attack value

    # get weapon base damage of the unit
    value = attacker.getDamage()

    # modify by attacker terrain
    value = value * scenario.map.getTerrain(attacker.getPosition()).attackModifier()

    # modify by attacked mode
    value *= 1.0

    # modify by attacker skill
    value = attacker.getExperience().evaluateAttack(value)

    # modify by attacker fatigue
    value = attacker.getFatigue().evaluateAttack(value)

    # now modify by defender data

    # modify by defender terrain. first get the terrain modifier and entrenchment level
    defensemod = scenario.map.getTerrain(defender.getPosition()).defenseModifier()
    entrenchment = 1.0

    # modify value by defender terrain and entrenchment level
    value = value * defensemod * entrenchment

    # modify by attack direction. we use a deviation of 5 from the defender facing to be the max value
    # before the attack is a flank attack. so the interval is +-5 from the defender facing
    if rotate_util.isFlankAttack(attacker, defender, 5):
        # we have a flank attack, modify damage
        value *= 1.5

    # modify by distance. At max distance the effectiveness is  greatly reduced.
    value *= 1.0

    # modify by defender mode
    value *= 1.0

    # modify by random value. range: 0.8 to 1.2
    value = value * random.randrange(80, 120) / 100

    # convert the value to a number of men killed and wounded. why log()?  um.... it seems to
    # normalize the ranges a bit???
    try:
        killed = log(value)
    except OverflowError:
        # hmm...
        killed = 0
    except ValueError:
        # hmm again?
        raise RuntimeError("ValueError raised for: %f" % value)

    # if the defender has guns there may be a gun knocked out. possibility: 5%
    if defender.getWeapon().isArtillery() and random.randrange(0, 100) < 5:
        # a gun was destroyed
        gunsdestroyed = 1
    else:
        # no guns were destroyed
        gunsdestroyed = 0

    # modify morale and check for retreats, routs or gets disorganizations

    # check if attacker gets a morale boost

    # modify fatigue. the defender gets some minor added fatigue due to combat stress
    defender.getFatigue().setValue(defender.getFatigue().getValue() + 1)

    # modify experience

    # send out a damage command. damage command needs work...  also, we're currently ignoring
    # destroyed guns.
    print("combat_util.resolveAttack: unit: %d, killed: %d of %d" % (defender.id, killed, defender.men))

    # do we have destroyed guns?
    if gunsdestroyed > 0:
        # yep, add action for that too
        actiondata.append(DamageAct(unit_id=defender.id, damagetype=constants.GUNSDESTROYED,
                                    damagecount=gunsdestroyed, attacker_id=attacker.getId()))

        # apply the damage. if the unit is destroyed it will mark itself as destroyed and remove
        # itself from the global unit structures
        defender.applyDamage(type=constants.GUNSDESTROYED, count=gunsdestroyed)

    # create action for the total damage
    actiondata.append(DamageAct(unit_id=defender.id, damagetype=constants.KILLED,
                                damagecount=killed, attacker_id=attacker.getId()))

    # apply the damage. if the unit is destroyed it will mark itself as destroyed and remove itself
    # from the global unit structures
    defender.applyDamage(type=constants.KILLED, count=killed)

    # now add action for the optionally changed modifiers for both the attacker and defender. these
    # all have already been applied locally, so we just copy the values from the units and send 'em
    actiondata.extend(createModifierActions(attacker, defender))

    # return all good stuff we got
    return actiondata


def createModifierActions(attacker, defender):
    """
    Creates the needed action for sending out changed modifiers for the attacker and
    defender. The defender data is sent only if the defender still is alive. The data is returned as
    one or two ChangeModifiersAct instances in a list.
    """

    # attacker is assumed to be alive
    act1 = ChangeModifiersAct(unit_id=attacker.id,
                              fatigue=attacker.getFatigue().getValue(),
                              morale=attacker.getMorale().getValue(),
                              experience=attacker.getExperience().getValue())

    # is the defender still alive? if it isn't we don't bother sending out action for that
    if defender.isDestroyed():
        # destroyed, we're done here
        return act1,

    # seems to be alive, so create action for it too
    act2 = ChangeModifiersAct(unit_id=defender.id,
                              fatigue=defender.getFatigue().getValue(),
                              morale=defender.getMorale().getValue(),
                              experience=defender.getExperience().getValue())

    # and add them for sending out too
    return act1, act2
