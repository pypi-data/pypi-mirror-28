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

from civil import constants
from civil.model import scenario
from civil.server.action.action import Action
from civil.ui.messages import COMBAT, DESTROYED


class DamageAct(Action):
    """
    This class implements the action 'damage'. This command is sent when a unit has
    been shot at. This update contains the id of the affected unit, the type of damage and the
    amount of that particular damage. The type can be lost guns and men, and the amount thus the
    number of guns/men.

    If the unit is destroyed it will be
    """

    def __init__(self, unit_id=-1, damagetype=-1, damagecount=-1, attacker_id=-1):
        """
        Initializes the instance.
        """
        # call superclass constructor
        Action.__init__(self, "damage_act")

        # set illegal values for all data
        self.unit_id = unit_id
        self.damagetype = damagetype
        self.damagecount = damagecount
        self.attacker_id = attacker_id

    def extract(self, parameters):
        """
        Extracts the data for the move.
        """

        # parse out the data
        self.unit_id = int(parameters[0])
        self.damagetype = int(parameters[1])
        self.damagecount = int(parameters[2])
        self.attacker_id = int(parameters[3])

    def execute(self):
        """
        Executed the command. Finds the affected unit and updates the damage. If the unit is
        destroyed it will be removed and all units targetting it will lose their targets.
        """

        # get the units with the given ids
        unit = scenario.info.units[self.unit_id]

        # precautions when getting the attacker
        if self.attacker_id != -1:
            attacker = scenario.info.units[self.attacker_id]
        else:
            # oops, warn about this
            print("DamageAct.execute: attacker not set properly")

        # apply the damage. if the unit is destroyed it will mark itself as destroyed and remove
        # itself from the global unit structures
        unit.applyDamage(self.damagetype, self.damagecount)

        # nothing beyond this point for AI players!
        if scenario.local_player_ai:
            return

        # is this an artillery unit? if so we use a special firing sample
        if attacker is not None and attacker.getType() == constants.ARTILLERY:
            # yes, arty unit
            scenario.audio.playSample('firing_artillery')
        else:
            # other infantry based unit
            scenario.audio.playSample('firing_infantry')

            # is the unit destroyed? we'll let the world know of this, but not for the ai
        if unit.isDestroyed():
            # let the world know of the destroyed unit
            scenario.dispatcher.emit('unit_destroyed', (unit,))
        else:
            # not destroyed, just changed 
            scenario.dispatcher.emit('units_changed', (unit,))

        # do we need to show a message in the messages? only for local players
        if self.damagecount > 0 and unit.getOwner() == scenario.local_player_id:
            # what type of damage?
            if self.damagetype == constants.KILLED:
                # lost men
                scenario.messages.add('%s lost %d men' % (unit.getName(), self.damagecount), COMBAT)
            else:
                # lost guns
                scenario.messages.add('%s lost %d guns' % (unit.getName(), self.damagecount), COMBAT)

                # play a "gun destroyed" sample
                scenario.audio.playSample('explosion')

        # did it get destroyed too?
        if unit.destroyed == 1:
            # no men left, it's a goner
            message = '%s is destroyed!' % unit.getName()

            # add the message
            scenario.messages.add(message, DESTROYED)

            # clear units that targeted the destroyed one
            self.clearTargetters(unit)

            # was the unit selected?
            if unit in scenario.selected:
                # delete it
                scenario.selected.remove(unit)

            # let the world know that this unit should no longer be selected
            scenario.dispatcher.emit('unit_selected', None)

    def clearTargetters(self, destroyed):
        """
        Makes sure no unit it targetting this unit anymore. This is used when the unit has been
        destroyed. Loops through all units and clears their target if they were targetting this
        unit.
        """

        # find all units (enemies) who have targeted this unit
        for unit in scenario.info.units.values():
            # did it target this unit?
            if unit.getTarget() == destroyed:
                # yes, clear the target
                unit.setTarget(None)

                # print "DamageAct.clearTargetters: cleared: %d, %s" % ( unit.getId(), unit.getName())

    def toString(self):
        """
        Returns a string representation of the command, suitable for sending over a socket.
        """
        # create a string and return
        return "%s %d %d %d %d\n" % (self.getName(), self.unit_id, self.damagetype,
                                     self.damagecount, self.attacker_id)

    def __str__(self):
        """
        Convenience wrapper for toString() suitable for using when debugging and printing the
        command to the screen. Will just call toString().
        """
        return self.toString()
