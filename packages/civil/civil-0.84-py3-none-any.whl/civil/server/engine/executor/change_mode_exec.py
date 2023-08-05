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
from civil.server import properties as server_properties
from civil.server.engine.executor.executor import Executor


class ChangeModeExec(Executor):
    """
    This class executes the plan 'changemode'. This plan is sent by clients when a unit has been
    ordered to change it mode. Modes can by the player be changed like this:

    * limbered -> unlimbering -> unlimbered
    * mounted -> dismounting -> dismounted
    * formation -> changing to formation -> column

    And of course the reverse too. This plan will alter the mode of the unit, i.e. basically toggle it.
    """

    def __init__(self, unit, plan):
        """
        Initializes the instance.
        """
        # call superclass constructor
        Executor.__init__(self, unit, plan)

    def execute(self):
        """
        Executes the plan. Sets the intermediate mode for the unit, i.e. the unit to use while
        the mode is being changed. After the mode change is complete then the target mode is
        set. The intermediate mode is active for a certain period of time. If the unit already is in
        the wanted state then nothing will be done.

        The unit will gain fatigue while it is changing the mode, and that fatigue action is
        returned as long as the plan is executed.

        The unit will be in an intermediate state while performing the mode change. The length of
        this depends on the mode change delay for the unit.
        """

        # is this the first time we're executing the plan?
        if self.firsttime:
            # not first time anymore
            self.firsttime = 0

            # now we're setting the intermediate mode that the unit is using while it performs the
            # mode change operation this will be calculated from the unit's delay (in seconds) and
            # the normal speedup factor. if the engine runs 10 times as fast as real time and the
            # unit delay is 60s then the waiting time is 60/10=6s
            self.wait = self.unit.getModeChangeDelay() / server_properties.speedup_factor

            # create the action that sets the intermediate mode
            return self.setUnitMode(self.unit, self.unit.getMode().onChangeMode())

        # not the first time we're executing, so are we done yet?
        if self.wait <= 0:
            # yep, the unit has changed mode now, set the final changed mode. this is the mode that
            # the unit gets after its intermediate mode, i.e. the one it was changing to in the
            # first place

            # execution is finished
            self.finished = 1

            # return the new mode changing action
            return self.setUnitMode(self.unit, self.unit.getMode().onDone())

        # no, decrement the counter that indicates how long the unit is doing the 'reorganization' 
        self.wait -= 1

        # get the base fatigue change for the mode
        fatigue = self.unit.getMode().getBaseFatigue()

        # modify the value by the terrain too. it is more exhausting to change the mode when in
        # woods than when on an open field
        fatigue *= scenario.map.getTerrain(self.unit.getPosition()).movementFatigueModifier(self.unit)

        # did we get any fatigue?
        if fatigue > 0:
            # yes, add the fatigue for the unit
            self.unit.getFatigue().addValue(int(fatigue))

            # create action for that too and return it
            return self.changeModifiers(self.unit)
