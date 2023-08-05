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


class Rest(Module):
    """
    This class defines a module that rests a unit. Every unit which is in a mode that reduces
    fatigue will rest. If the unit rests the a ChangeModifiersAct is sent out with the new data.

    This module is executed every step.
    """

    def __init__(self):
        """
        Initializes the module. Sets a suitable name.
        """
        # call superclass
        Module.__init__(self, 'rest')

    def execute(self, actiondata):
        """
        Executes the module. Loops over all units and checks weather they are in a  mode that
        reduces fatigue (the fatigue change is negative). If the fatigue changes downwards then
        action is returned. For increased fatigue nothing will be done.
        """

        # loop over all units we have
        for unit in scenario.info.units.values():
            # get the possible base fatigue change and multiply by 5, as we run this only every 5th step
            # TODO: wrong numbers!
            fatigue = unit.getMode().getBaseFatigue() * 5

            # does it decrease?
            if fatigue < 0:
                # yes, the unit will rest for this step, first get the old fatigue value so that we
                # can see weather we got a difference at all
                oldfatigue = unit.getFatigue().getValue()

                # add the new fatigue
                unit.getFatigue().addValue(int(fatigue))

                # did they change?
                if oldfatigue != unit.getFatigue().getValue():
                    # yes, it changed, create action for that
                    self.changeModifiers(unit, actiondata)

                    # we're done with the clearing of targets
