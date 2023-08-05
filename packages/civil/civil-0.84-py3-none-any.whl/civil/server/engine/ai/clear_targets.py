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
from civil.server.engine.ai.module import Module


class ClearTargets(Module):
    """
    This class defines a module that when executed checks all units that have a target. If the
    units that have a target can not for some reason longer shoot at the target, then the target
    will be cleared. Reasons for a target to be cleared can be:

    o target has been destroyed
    o target hs moved out of sight
    o target hs moved out of range
    o unit has a mode that does not allow skirmishing

    This module is executed every step.
    """

    def __init__(self):
        """
        Initializes the module. Sets a suitable name.
        """

        # call superclass
        Module.__init__(self, 'clear targets')

    def execute(self, actiondata):
        """
        Executes the module. Loops over all units and checks weather they have targets that still
        exist and are visible.
        """

        # loop over all units we have
        for unit in scenario.info.units.values():
            # does the unit already have a target?
            target = unit.getTarget()
            if target is None:
                # no target, next unit
                continue

            # TODO: this relies on that the units always have damage applied to them, as the next
            # check needs to know if a unit is already destroyed.

            # does the target still exist?
            if target.isDestroyed():
                # the target has been destroyed somehow, clear the target
                print("ClearTargets.execute: %s can not skirmish: target destroyed" % unit.getName())
                self.clearTarget(unit, actiondata)
                continue

            # does the unit's mode still allow it to skirmish?
            if not unit.getMode().canSkirmish() and not unit.getMode().isMeleeing():
                # unit can't skirmish in it's current mode
                print("ClearTargets.execute: %s can not skirmish/melee: bad mode" % unit.getName())
                self.clearTarget(unit, actiondata)
                continue

            # is the unit too fatigued or has too low morale for skirmish?
            if unit.getMorale().checkSkirmish() == 0 or unit.getFatigue().checkSkirmish() == 0:
                # unit can't skirmish, too tired or low on morale
                print("ClearTargets.execute: %s can not skirmish/melee: tired or low morale" % unit.getName())
                self.clearTarget(unit, actiondata)
                continue

            # is the enemy visible?
            if not unit.seesEnemy(target):
                # not visible anymore
                print("ClearTargets.execute: %s can not skirmish: enemy not seen" % unit.getName())
                self.clearTarget(unit, actiondata)
                continue

            # is the unit still in range?
            if not unit.inRange(target):
                # unit has moved out of range
                print("ClearTargets.execute: %s can not skirmish: out of range" % unit.getName())
                self.clearTarget(unit, actiondata)
                continue
