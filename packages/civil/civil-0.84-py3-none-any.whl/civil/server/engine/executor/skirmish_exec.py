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

from civil.server.engine.executor import combat_util
from civil.server.engine.executor import rotate_util
from civil.model import scenario
from civil.server.action.rotate_act import RotateAct
from civil.server.action.set_target_act import SetTargetAct
from civil.server.engine.executor.executor import Executor


class SkirmishExec(Executor):
    """
    This class implements an executor for the plan 'Skirmish'. It contains the actual code for
    skirmishing with a unit. The assaulting is performed in a few steps:

    1. set an skirmish mode
    2. make the unit face its target
    3. if the unit is too far from the target to fire it will finish the plan and idle
    4. if the unit is within range it will start the skirmish

    When the unit actually fires the damage is calculated and action created for the
    """

    def __init__(self, unit, plan):
        """
        Initializes the instance.
        """
        # call superclass constructor
        Executor.__init__(self, unit, plan)

        # get the target we're skirmishing
        self.target = scenario.info.units[plan.getTargetId()]

        # calculate our turning speed
        self.turnspeed = rotate_util.calculateTurnSpeed(self.unit)

        # store the current x and y values, these get incremented by the deltas
        self.currentx, self.currenty = self.unit.getPosition()

        # get the target position, i.e. where we're heading. if we're not close enough to the target
        # we must move towards it. the unit will never move all the way to the target, instead it
        # will just move closer, and when close enough, do the final assault
        self.target_x, self.target_y = self.target.getPosition()

        # calculate the angle the unit should rotate to
        self.targetfacing = rotate_util.calculateAngle(self.currentx, self.currenty,
                                                       self.target_x, self.target_y)

        # get the current facing for the unit
        self.currentfacing = self.unit.getFacing()

        # set the initial delay to be 0 so the unit can fire immediately
        self.delay = 0
        # self.__setFiringDelay ()

    def execute(self):
        """
        Executes one single step the skirmishing plan. There are a few things that need to be
        done, in this order:

        o set an skirmish mode
        o make the unit face its target
        o if the unit is too far from the target it will cancel the skirmishing
        o if the unit is within range it will start the skirmish by setting a target and then
          ending the plan. 

        Actual firing is done by the combat modules in the engine. This plan merely sets a nice
        skirmish mode and assigns a target to the unit.
        """

        # is this the first time we call this method?
        if self.firsttime:
            # this is the first time called, setup for execution
            self.firsttime = 0

            # set unit in skirmish mode 
            return self.setUnitMode(self.unit, self.unit.getMode().onSkirmish())

        # is the target still alive, within range and visible? we may have lost it during the
        # turning phase, i.e. the unit has moved away, been destroyed or something similar
        if not self.unit.seesEnemy(self.target) or not self.unit.inRange(self.target) or \
                self.target.isDestroyed():
            # oops, can't skirmish with that one anymore
            print("SkirmishExec.execute: **** target %d lost for %d" % (self.target.getId(),
                                                                        self.unit.getId()))
            # this one is done
            self.finished = 1

            # set unit in whatever mode it'll have after the skirmish is done
            return self.setUnitMode(self.unit, self.unit.getMode().onDone())

        # does the unit have the correct target set?
        if self.unit.getTarget() != self.target:
            # the unit does not have the same target as us, set it
            self.unit.setTarget(self.target)

            # and return the same action too
            return SetTargetAct(self.unit.getId(), self.target.getId())

        # is the rotation done?
        if self.currentfacing != self.targetfacing:
            # no, first get the new facing for the unit
            self.currentfacing = rotate_util.rotate(self.currentfacing, self.targetfacing, self.turnspeed)

            # assign the new facing to the unit too
            self.unit.setFacing(int(self.currentfacing))

            #  create action for the changed facing and return it. we're done for this step
            return RotateAct(self.unit.getId(), int(self.currentfacing))

        # we got this far, now the unit can start firing as fast as it can. decrement the delay and
        # see if we reach 0
        self.delay -= 1

        print("SkirmishExec.execute: delay: %d" % self.delay)

        # did we reach 0 now?
        if self.delay <= 0:
            # we're ready to fire, set new delay
            self.__setFiringDelay()

            # resolve the skirmishing
            return combat_util.skirmish(self.unit, self.target)

        return None

    def __setFiringDelay(self):
        """
        Assigns the firing delay for the unit. The delay is used when checking how often the unit
        can fire during one turn. The delay has a base delay of 5 iterations and then up to 0-10
        steps added depending on the unit experience.
        """

        # do the funky math
        self.delay = 5 + int((100.0 - self.unit.getExperience().getValue()) * 0.01)

        print("SkirmishExec.__setFiringDelay: delay: %d" % self.delay)
