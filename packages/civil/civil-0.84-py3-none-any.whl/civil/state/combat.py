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

from civil.state import state
from civil.model import scenario


class Combat(state.State):
    """
    This class is a base class for a state that manages combat. It contains a few methods that are
    shared among combat classes. It should never be instantiated directly. It defines no keymap,
    help texts or cursors.
    """

    def __init__(self):
        """
        Initializes the instance. Does nothing useful.
        """
        # call superclass constructor
        state.State.__init__(self)

    def findTarget(self, x, y):
        """
        Checks for an enemy unit at the given position or within a short distance from the position and
       returns its id. If no enemy unit was found at the position then -1 is returned.
       """

        # get the units
        units = scenario.info.units

        # loop over all units
        for unit in list(units.values()):
            # get the unit's position
            (unitx, unity) = unit.getPosition()

            # calculate the square of distance from the given point to the unit
            distance = (x - unitx) ** 2 + (y - unity) ** 2

            # is the distance within picking range?
            if distance < 100:
                # is this unit an own unit or enemy unit?
                if unit.getOwner() != scenario.local_player_id:
                    # they're the target
                    return unit.getId()

        # no unit found
        return -1

    def inRange(self, unit, target):
        """


 """

        x1, y1 = unit.getPosition()
        x2, y2 = target.getPosition()

        # do a simple squared range calculation (no square roots)
        if ((x2 - x1) ** 2 + (y2 - y1) ** 2) > unit.getWeapon().getRange() ** 2:
            # out of range
            return 0

        # we're in range
        return 1
