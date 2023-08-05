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

from civil.server.engine.executor import move_util
from civil.server.engine.executor import rotate_util
from civil.model import scenario
from civil.server.action.clear_plans_act import ClearPlansAct
from civil.server.action.move_act import MoveAct
from civil.server.action.rotate_act import RotateAct
from civil.server.engine.executor.executor import Executor


class RoutExec(Executor):
    """
    This class implements an executor for the plan 'Rout'. It contains the actual code for
    executing a rout for a unit. The engine will based on the data calculate when and how the
    routing takes place. The unit will change to a 'routing mode' if one is applicable for the unit.
    """

    def __init__(self, unit, plan):
        """
        Initializes the instance.
        """
        # call superclass constructor
        Executor.__init__(self, unit, plan)

        # calculate the slow movement speed for the unit
        self.movespeed = move_util.calculateMovementSpeed(self.unit, self.getMovementSpeed())

        # store the current x and y values, these get incremented by the deltas
        self.currentx, self.currenty = self.unit.getPosition()

        # get the target position, i.e. where we're heading
        self.target_x, self.target_y = self.plan.getTarget()

        # calculate the angle the unit should rotate to
        self.targetfacing = rotate_util.calculateAngle(self.currentx, self.currenty,
                                                       self.target_x, self.target_y)

        # calculate deltas for the movement, i.e. how much the unit moves in x and y each step
        self.delta_x, self.delta_y = move_util.calculateMovementDeltas(self.currentx, self.currenty,
                                                                     self.target_x, self.target_y,
                                                                     self.movespeed)

    def getMovementSpeed(self):
        """
        Returns the routing speed of the unit. This is a separate method so that subclasses can


 """
        # return the slow speed
        return self.unit.getRoutMovementSpeed()

    def execute(self):
        """
        Executes the pland. This will first set the unit in a routing mode, change to face the
        destination and after that start moving it towards the destination. This differs from a
        normal moving mode, which will change facing. 

        When the unit reaches the destination it will be put in a disorganized mode.
        """

        # is this the first time we call this method?
        if self.firsttime:
            # this is the first time called, setup for execution
            self.firsttime = 0

            # set unit in routing mode 
            return self.setRoutingMode()

        # is the rotation done?
        if self.unit.getFacing() != self.targetfacing:
            # no, first get the new facing for the unit, rotate it.
            # TODO: this should be a much higher speed, possibly the unit just does a 180 degree
            # turn and runs, without any formation stuff.
            self.unit.setFacing(rotate_util.rotate(self.unit.getFacing(), self.targetfacing, self.turnspeed))

            #  create action for the changed facing and return it. we're done for this step
            return RotateAct(self.unit.getId(), self.unit.getFacing())

        # get the distance we still have to travel
        distance = move_util.calculateDistance(self.currentx, self.currenty, self.target_x, self.target_y)

        # are we done?
        if (self.currentx, self.currenty) == (self.target_x, self.target_y):
            # yes, all retreating is now done
            self.finished = 1

            # create the final action that sets the mode the unit should have after a retreat
            return self.setUnitMode(self.unit, self.unit.getMode().onDone())

        # is the movement as good as done, i.e. the distance is less than what we can move in one
        # step? if it is we just move there
        if distance < self.movespeed and self.movespeed > 0:
            # very close, do this last step. next time we enter this method the final check above
            # will notice this and terminate the moving
            self.currentx, self.currenty = self.target_x, self.target_y

            # set the new position
            self.unit.setPosition((self.target_x, self.target_y))

            # now create the action and return it
            return MoveAct(self.unit.getId(), self.target_x, self.target_y)

        # not yet there, perform one step of the rout
        return self.rout()

    def rout(self):
        """
        Performs one step of the movement of the unit. Calculates, creates and returns a
        'MoveAct'. The deltas for the movement are simply added to the current position.
        """

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

            # clear all the plans for the unit and just leave it there...
            # TODO unit unknown
            return ClearPlansAct(unit.getId())

        # set the new position
        self.unit.setPosition((newx, newy))

        # create the action and return it
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

    def setRoutingMode(self):
        """
        This method is called when the unit starts to rout, and sets the mode of the unit to a


 """

        # get new mode
        mode = self.unit.getMode().onRout()

        # create the action and return it
        return self.setUnitMode(self.unit, mode)
