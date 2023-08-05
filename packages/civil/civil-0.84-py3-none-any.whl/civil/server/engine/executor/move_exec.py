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
from civil.server.action.clear_plans_act import ClearPlansAct
from civil.server.action.move_act import MoveAct
from civil.server.action.rotate_act import RotateAct
from civil.server.engine.executor.executor import Executor
from civil.server.engine.executor.move_util import calculateDistance, calculateMovementSpeed, calculateMovementDeltas
from civil.server.engine.executor.rotate_util import calculateAngle, rotate, calculateTurnSpeed


class MoveExec(Executor):
    """
    This class implements an executor for the plan 'Move'. It contains the actual code for
    executing a move for a unit. The engine will based on the data calculate when and how the
    movement takes place. The unit will change to a 'moving mode' if one is applicable for the unit.

    If the unit moves into impassable terrain all its plans will be cleared.
    """

    def __init__(self, unit, plan):
        """
        Initializes the instance.
        """
        # call superclass constructor
        Executor.__init__(self, unit, plan)

        # calculate turning speed
        self.turnspeed = calculateTurnSpeed(self.unit)

        # store the current x and y values, these get incremented by the deltas
        self.currentx, self.currenty = self.unit.getPosition()

        # get the target position, i.e. where we're heading
        self.target_x, self.target_y = self.plan.getTarget()

        # calculate the angle the unit should rotate to
        self.targetfacing = calculateAngle(self.currentx, self.currenty, self.target_x, self.target_y)

        # get the current facing for the unit
        self.currentfacing = self.unit.getFacing()

    def getMovementSpeed(self):
        """
        Returns the movemnt speed of the unit. This is a separate method so that subclasses can


 """
        # return the slow speed
        return self.unit.getNormalMovementSpeed()

    def execute(self):
        """
        Executes the plan. This method will take care of all movement related code. Puts the unit
        in a moving mode and then proceeds to rotate the unit to face the destination. When the unit
        has fully rotated it will move towards the destination in small steps. The movement speed
        depends on the unit and terrain, and is updated for every step. When the movement is done
        the unit is again placed in whatever mode is should get after movement.
        """
        # is this the first time we call this method?
        if self.firsttime:
            # this is the first time called, setup for execution
            self.firsttime = 0

            # set unit in movement mode 
            return self.setMovingMode()

        # is the rotation done?
        if self.currentfacing != self.targetfacing:
            # no, first get the new facing for the unit
            self.currentfacing = rotate(self.currentfacing, self.targetfacing, self.turnspeed)

            # assign the new facing to the unit too
            self.unit.setFacing(int(self.currentfacing))

            # create action for the changed facing and return it, we're done for now
            return RotateAct(self.unit.getId(), int(self.currentfacing))

        # get the distance we still have to travel
        distance = calculateDistance(self.currentx, self.currenty, self.target_x, self.target_y)

        # are we done?
        if (self.currentx, self.currenty) == (self.target_x, self.target_y):
            # yes, all movement is now done
            self.finished = 1

            # set unit in whatever mode it'll have after the move is done
            return self.setUnitMode(self.unit, self.unit.getMode().onDone())

        # calculate the movement speed for the unit. this must be recalculated for each step, as the
        # unit may have suffered losses ort something else that affects the speed. this speed is
        # used below
        self.movespeed = calculateMovementSpeed(self.unit, self.getMovementSpeed())

        # is the movement as good as done, i.e. the distance is less than what we can move in one
        # move? if it is we just move there
        if distance < self.movespeed and self.movespeed > 0:
            # very close, do this last step. next time we enter this method the final check above
            # will notice this and terminate the moving
            self.currentx, self.currenty = self.target_x, self.target_y

            # set the new position
            self.unit.setPosition((self.target_x, self.target_y))

            # now create the action and return it
            return MoveAct(self.unit.getId(), self.target_x, self.target_y)

        # not yet there, perform one step of the movement
        return self.move()

    def move(self):
        """
        Performs one step of the movement of the unit. Calculates and adds one 'MoveAct' for the
        unit. The movement deltas are recalculated for each step, as the unit may have entered
        terrain that is slower/faster, or it may have gained fatigue which slow it down.
        """

        # calculate deltas for the movement, i.e. how much the unit moves in x and y each step. this
        # must be repeated in each step, as the unit movement speed may have changed due to terrain
        # or similar
        self.delta_x, self.delta_y = calculateMovementDeltas(self.currentx, self.currenty,
                                                           self.target_x, self.target_y,
                                                           self.movespeed)
        # not yet there, update internal position
        self.currentx += self.delta_x
        self.currenty += self.delta_y

        # get new position of the unit after this step
        newx = int(self.currentx)
        newy = int(self.currenty)

        # get terrain
        terrain = scenario.map.getTerrain((newx, newy))

        # validate that the terrain can be entered by the unit. this must be done before the new
        # position is set for the unit
        if not terrain.canUnitEnter(self.unit):
            # the unit can't enter the terrain! all movement is now done
            self.finished = 1

            # clear all the plans for the unit and set it in whatever mode it'll have after the
            # movement is done
            return (ClearPlansAct(self.unit.getId()),
                    self.setUnitMode(self.unit, self.unit.getMode().onDone()))

        # set the new position
        self.unit.setPosition((newx, newy))

        # create the action for the movement
        moveaction = MoveAct(self.unit.getId(), newx, newy)

        # get the possible base fatigue change
        fatigue = self.unit.getMode().getBaseFatigue()

        # modify the value by the terrain too
        fatigue *= scenario.map.getTerrain(self.unit.getPosition()).movementFatigueModifier(self.unit)

        # did we get any fatigue?
        if fatigue > 0:
            # yes, add the fatigue for the unit
            self.unit.getFatigue().addValue(int(fatigue))

            # create action for that too and return it along with the movement action
            return moveaction, self.changeModifiers(self.unit)

        # no fatigue change, so just send out the move action
        return moveaction

    def setMovingMode(self):
        """
        This method is called when the unit starts to move, and sets the mode of the unit to a
        suitable 'moving' mode, based on what mode the unit may currently have. An action SetMode
        with the new mode is created and returned.
        """

        # get new mode
        mode = self.unit.getMode().onMove()

        # create the action and return it
        return self.setUnitMode(self.unit, mode)
