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

from civil.server.engine.executor.move_exec import MoveExec


class MoveFastExec(MoveExec):
    """
    This class implements an executor for the plan 'MoveFast'. It contains the actual code for
    executing a fast move for a unit. The engine will based on the data calculate when and how the
    movement takes place. The unit will change to a 'moving fast mode' if one is applicable for the
    unit.

    This class inherits 'MoveExec', and only overrides some key functionality.
    """

    def __init__(self, unit, plan):
        """
        Initializes the instance.
        """
        # call superclass constructor
        MoveExec.__init__(self, unit, plan)

    def getMovementSpeed(self):
        """
        Returns the movemnt speed of the unit. This is a separate method so that subclasses can
        override it. This method is overridden from the one in MoveExec to return the speed for fast
        movement.
        """
        # return the fast speed
        return self.unit.getFastMovementSpeed()

    def setMovingMode(self):
        """
        This method is called when the unit starts to move, and sets the mode of the unit to a
        suitable 'moving' mode, based on what mode the unit may currently have. An action SetMode
        with the new mode is created and returned. 

        This method is overridden from the one in MoveExec, as it sets the unit the the proper mode
        for fast movement.
        """

        # get new mode
        mode = self.unit.getMode().onMoveFast()

        # create the action and return it
        return self.setUnitMode(self.unit, mode)
