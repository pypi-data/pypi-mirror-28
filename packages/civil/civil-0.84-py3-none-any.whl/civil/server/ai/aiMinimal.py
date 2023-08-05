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
from civil.plan.assault import Assault
from civil.plan.move import Move


class aiMinimal:
    """
    This class creates a minimal AI.

    It is intended mostly a a proof-of-concept and for subclassing.
    """

    def __init__(self):
        """
        Doesn't need to do anything yet.
        """

    def nextTurn(self):
        """
        A new turn has started; issue order accordingly.
        """

        target = -1

        # pick the last enemy unit.  Yes, this is a really
        # stupid way to do this.  It's 12:30 AM, what do you want?
        for unit in scenario.info.units.values():
            if unit.owner != scenario.local_player_id:
                target = unit

        # if anybody on our side isn't busy, they should attack that unit.
        for unit in scenario.info.units.values():
            if unit.owner != scenario.local_player_id:
                continue  # not ours

            if unit.getActivePlan() is not None:
                continue  # nope, this unit is busy                    

            if not target.isVisible():
                # we can't see him.  move toward the target.

                # can the unit move?
                if unit.getMode().canMove() and unit.getFatigue().checkMove():
                    x1, y1 = unit.getLatestPosition()
                    x2, y2 = target.getPosition()

                    #  create a new 'move' plan to go halfway to the target/
                    plan = Move(unit_id=unit.getId(), x=(x1 + x2) / 2, y=((y1 + y2) / 2))

                    # add it to the plans for the unit
                    unit.getPlans().append(plan)
                continue

                # This next block is cut-and-pasted from assault state code.
            # Should probably only be in one place somehow.

            # check morale, fatigue
            if unit.getMorale().checkAssault() == 0 or unit.getFatigue().checkAssault() == 0:
                # either the morale is too low or the fatigue is too high, we won't do combat
                # scenario.messages.add ( '%s can not assault' % unit.getName (), messages.ERROR )
                continue

            # can the unit assault?
            if not unit.getMode().canAssault():
                # nope, the unit mode prohibits it, next unit
                # scenario.messages.add ( '%s can not assault' % unit.getName (), messages.ERROR )
                continue

            # morale and fatigue ok, create a new 'assault' plan 
            plan = Assault(unit_id=unit.getId(), targetid=target.getId())

            # add it to the plans for the unit
            unit.getPlans().append(plan)

        return
