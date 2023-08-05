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
from civil.server.action.add_plan_act import AddPlanAct
from civil.server.action.clear_plans_act import ClearPlansAct
from civil.server.action.move_act import MoveAct
from civil.server.action.rotate_act import RotateAct
from civil.server.action.set_target_act import SetTargetAct
from civil.plan.retreat import Retreat
from civil.plan.rout import Rout
from civil.server.engine.executor.move_util import calculatePosAlongFacing
from civil.server.engine.executor.executor import Executor
from civil.server.engine.executor.move_util import calculateDistance, calculateMovementSpeed, calculateMovementDeltas
from civil.server.engine.executor.rotate_util import rotate, calculateTurnSpeed, calculateAngle, calculateReverseFacing


class AssaultExec(Executor):
    """
    This class implements an executor for the plan 'Assalt'. It contains the actual code for
    executing an assault for a unit. The assaulting is performed in a few steps:

    o set an assault mode

    o make the unit face its target

    o if the unit is too far from the target to fire it will move against it until it comes withing
    firing range

    o when the unit has reached firing range it will start firing regularly, while still moving
    forward against the unit

    o when the unit has reached assault range it will start the final assault and engage in hand to
    hand combat with the target.

    Usually either the atatcker or target breaks down before the assault is completed.
    """

    def __init__(self, unit, plan):
        """
        Initializes the instance.
        """
        # call superclass constructor
        Executor.__init__(self, unit, plan)

        # calculate turning speed
        self.turnspeed = calculateTurnSpeed(self.unit)

        # calculate the slow movement speed for the unit
        self.movespeed = calculateMovementSpeed(self.unit, self.unit.getAssaultMovementSpeed())

        # store the current x and y values, these get incremented by the deltas
        self.currentx, self.currenty = self.unit.getPosition()

        # get the target we're attacking
        self.target = self.validateUnit(plan.getTargetId())

        # did we get a target?
        if not self.target:
            # no target, we're done here, we need the target for the rest of our stuff
            self.finished = 1
            return

        # get the target position, i.e. where we're heading. if we're not close enough to the target
        # we must move towards it. the unit will never move all the way to the target, instead it
        # will just move closer, and when close enough, do the final assault.
        #
        # TODO: what if the target moves? or are we just assaulting a map location, and not a
        # specific unit?
        self.target_x, self.target_y = self.target.getPosition()

        # calculate the angle the unit should rotate to
        self.targetfacing = calculateAngle(self.currentx, self.currenty,
                                           self.target_x, self.target_y)

        # create a list with data that says what the plan should do during its loop. This data
        # should be constructed to reflect the unit experience and morale
        self.loop = ['m', 'f', 'r', 'r', 'p', 'm', 'm', 'm', 'm', 'm', 'm']

        # current index in the loop
        self.looppos = 0

        # final rush has not started yet
        self.rushstarted = 0

    def execute(self):
        """
        Executes the plan for this step. There are a few things that need to be done, in this
        order:

        o set an assault mode
        o sets the target for the unit
        o make the unit face its target
        o if the unit is too far from the target it will move against it
        o when the unit has reached firing range it will start firing regularly
        o when the unit has reached assault range it will start the final assault

        If the target moves, which is not too unlikely, the target data must be recalculated.
        """

        # has the unit or target died?
        if self.unit is None or self.target is None:
            # ah, during refreshUnit() we couldn't get the unit or the target, so this plan is done
            self.finished = 1
            return

        # is this the first time we call this method?
        if self.firsttime:
            # this is the first time called, setup for execution
            self.firsttime = 0

            # set unit in assault mode 
            return self.setUnitMode(self.unit, self.unit.getMode().onAssault())

        # does the unit have the correct target set?
        if self.unit.getTarget() != self.target:
            # the unit does not have the same target as us, set it
            self.unit.setTarget(self.target)

            # and return the same action too
            return SetTargetAct(self.unit.getId(), self.target.getId())

        # is the rotation done?
        if self.unit.getFacing() != self.targetfacing:
            # no, first get the new facing for the unit
            self.unit.setFacing(rotate(self.unit.getFacing(), self.targetfacing, self.turnspeed))

            #  create action for the changed facing and return it. we're done for this step
            return RotateAct(self.unit.getId(), self.unit.getFacing())

        # we keep track of the target's last known position by checking weather we still see the
        # target. if the position has changed and the unit is visible we need to get the updated
        # position and recalculate all parameters
        if self.unit.seesEnemy(self.target) and (self.target_x, self.target_y) != self.target.getPosition():
            # get updated position
            self.target_x, self.target_y = self.target.getPosition()

        # are we not in range of the target?
        if not self.unit.inRange(self.target):
            # not yet in firing range. so our unit must move closer before it can start the main
            # assault loop or the final assault
            return self.move()

        # get the distance we still have to travel
        distance = calculateDistance(self.currentx, self.currenty, self.target_x, self.target_y)

        # are we done? check weather the unit has come within range for the final assault
        if distance < 100:
            # we're close enough for the final assault
            return self.runAssault()

        else:
            # advance or fire against the enemy by running the loop to see what we want to do 
            return self.runLoop()

    def runLoop(self):
        """
        This method is used when the unit is facing the enemy and is in range and should just
        fire at the enemy. The method runs an eternal loop that contains 'actions' for the
        unit. Each turn an action is calculated and then it is executed. The actions that can be
        performed are:

        * move
        * pause
        * fire
        * reload

        Of these only 'fire' and 'move' actually does anything, i.e. enqueue a fire request to the
        server and move closer. Each step the unit must pass a morale check in order to proceed with
        the assault. If the check fails the unit will retreat instead.
        """

        # check morale first. if this fails then we're done here
        moraleaction = self.moraleCheck()
        if moraleaction is not None:
            # morale has failed for the unit
            return moraleaction

        # we're now facing the enemy, get the current loop action
        stepaction = self.loop[self.looppos]

        # what should we do?
        if stepaction == 'p' or stepaction == 'r':
            # pause or reload, do nothing
            pass

        if stepaction == 'm':
            # do a move
            return self.move()

        else:
            # resolve the skirmishing
            return combat_util.skirmish(self.unit, self.target)

        # advance loop position
        self.looppos += 1

        if self.looppos == len(self.loop):
            # reset to first position so that we start over
            self.looppos = 0

    def move(self):
        """
        Performs one step of the movement of the unit. Calculates the new movement deltas based
        on the unit's current speed. The speed changes during the assault, so it must be
        recalculated. Creates and returns a 'MoveAct'.
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

        # set the new position
        self.unit.setPosition((newx, newy))

        # create the action and return it
        return MoveAct(self.unit.getId(), newx, newy)

    def runAssault(self):
        """
        This method is called when the unit is close enough for the final assault. It means that
        the unit has advanced as close as needed for it to perform the final rush and engage in
        close combat. The morale is also checked, and if it fails then we're done here.
        """

        print("AssaultExec.runAssault: close enough for final assault.")

        # have our final rush already started?
        if not self.rushstarted:
            # nope, so get assault speed of the unit. this speed is then used in each movement step
            # calculation, so the unit will move faster now
            self.movespeed = calculateMovementSpeed(self.unit, self.unit.getAssaultMovementSpeed())

            # the rush has started now, make sure this code is not run again
            self.rushstarted = 1

            print("AssaultExec.runAssault: final rush has started. speed:", self.movespeed)

            # check morale first. if this fails then we're done here
        moraleaction = self.moraleCheck()
        if moraleaction is not None:
            # morale has failed for the unit
            return moraleaction

        # check the distance to the unit
        if self.unit.distance(self.target) < 20:
            # close enough for hand to hand combat, the assault is now done, let the ai module
            # figure out the rest 
            self.finished = 1

            # clear all plans for the unit. they're meleeing now and that cancels all their
            # plans
            self.unit.setPlans([])
            self.target.setPlans([])

            print("AssaultExec.runAssault: mode:", self.unit.getMode())
            print("AssaultExec.runAssault: on melee:", self.unit.getMode().onMelee())
            print("AssaultExec.runAssault: on melee:", self.target.getMode().onMelee())

            # create the final action that sets both units to a melee state and clears all plans for
            # both involved units 
            return (ClearPlansAct(self.target.getId()),
                    ClearPlansAct(self.unit.getId()),
                    self.setUnitMode(self.unit, self.unit.getMode().onMelee()),
                    self.setUnitMode(self.target, self.target.getMode().onMelee()))

        else:
            # rush closer, not yet reached the enemy
            print("AssaultExec.runAssault: rush closer")

            # do a move
            return self.move()

    def moraleCheck(self, finalassault=0):
        """
        Checks the morale for the unit. A unit must have sufficient morale in order to double
        time towards the enemy, and then even more morale to do the final assault against it. If the
        morale check fails then this plan will be marked as done, and a new plan created. If the
        final assault has started, ie. 'finalassault' is 1, then the new plan will be a routed plan,
        and if the morale fails while not yet doing the final assault, the new plan will just be a
        retreat.

        Returns a list of action if morale fails, and None if all is ok.
        """

        # are we doing the final assault?
        if finalassault:
            # yep, check the current morale
            if self.unit.getMorale().checkFinalsAssault():
                # morale holds
                return None

            # morale fails, so find out where the unit would go. it'll retreat a few hundred meters
            x, y = self.findRetreatTo(self.unit.getPosition(), 300)

            # morale fails, create a new rout plan
            rout = Rout(unit_id=self.unit.getId(), x=x, y=y)

            # add it to the plans for the unit. all the units plans must be cleared, so we just set the
            # rout plan as the only plan.
            self.unit.setPlans(list(rout))

            # this plan is done
            self.finished = 1

            # return the new plan and new mode
            return (ClearPlansAct(self.unit.getId()),
                    AddPlanAct(self.unit.getId(), rout))

        # still advancing
        if self.unit.getMorale().checkAssault():
            # morale holds
            return None

        # morale fails, so find out where the unit would go. it'll retreat a few hundred meters
        x, y = self.findRetreatTo(self.unit.getPosition(), 200)

        # create the plan
        retreat = Retreat(unit_id=self.unit.getId(), x=x, y=y)

        # add it to the plans for the unit. all the units plans must be cleared, so we just set the
        # retreat plan as the only plan.
        self.unit.setPlans(list(retreat))

        # this plan is done
        self.finished = 1

        # return the new plans and new mode
        return (ClearPlansAct(self.unit.getId()),
                AddPlanAct(self.unit.getId(), retreat))

    def findRetreatTo(self, position, distance):
        """
        Finds out a place the unit could retreat to. It will retreat for 'distance' meters, while 
        keeping the same facing. The position is calculated by using the reverse facing, and going
        in that direction some distance.
        """

        # first calculate the reverse facing for the unit, ie. the direction of the retreat
        reversefacing = calculateReverseFacing(self.unit.getFacing())

        # now calculate a path along that facing
        delta_x, delta_y = calculatePosAlongFacing(reversefacing, distance)

        # return this new position. TODO: could this overflow and get outside the map?
        x, y = position
        return x + delta_x, y + delta_y
