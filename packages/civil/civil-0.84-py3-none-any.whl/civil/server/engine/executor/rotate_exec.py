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

from civil.server.action.rotate_act import RotateAct
from civil.server.engine.executor.executor import Executor
from civil.server.engine.executor.rotate_util import calculateTurnSpeed, calculateAngle, rotate


class RotateExec(Executor):
    """
    This class implements an executor for the plan 'Rotate'. It contains the actual code for
    executing a rotation for a unit. The engine will based on the data calculate when and how the
    rotation takes place. The unit rotates without altering state anyhow. A unit in column mode
    rotates in column mode etc.
    """

    def __init__(self, unit, plan):
        """
        Initializes the instance.
        """
        # call superclass constructor
        Executor.__init__(self, unit, plan)

        # calculate turning speed
        self.turnspeed = calculateTurnSpeed(self.unit)

        xunit, yunit = self.unit.getPosition()
        xtarget, ytarget = self.plan.getTarget()

        # calculate the angle the unit should rotate to
        self.targetfacing = calculateAngle(xunit, yunit, xtarget, ytarget)

        # get the current facing for the unit
        self.currentfacing = self.unit.getFacing()

    def execute(self):
        """
        Executes the plan. Performs all calculation checks and weather the unit can rotate at
        all. The reasons for that might be:

        * no command control
        * bad state (routed)

        If all is ok separate 'rotate' action events will be created, one for every step the unit
        will spend rotating. For a small rotation this may be only one action, but for larger the
        rotation will take several steps.
        """

        # is the rotation done?
        if self.currentfacing == self.targetfacing:
            # we're done, no rotation needed anymore
            self.finished = 1
            return None

        # TODO: can the unit perform the rotation anymore?

        # get the new facing for the unit
        self.currentfacing = rotate(self.currentfacing, self.targetfacing, self.turnspeed)

        # assign the new facing to the unit too
        self.unit.setFacing(int(self.currentfacing))

        # create action for the changed facing
        return RotateAct(self.unit.getId(), int(self.currentfacing))
