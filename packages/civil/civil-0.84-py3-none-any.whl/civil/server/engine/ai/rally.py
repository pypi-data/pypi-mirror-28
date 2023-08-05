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


class Rally(Module):
    """
    This class defines a module that 

    This module is executed every step.
    """

    def __init__(self):
        """
        Initializes the module. Sets a suitable name.
        """

        # call superclass, run once per minute
        Module.__init__(self, 'rally', 60)

    def execute(self, actiondata):
        """
        Executes the module. Loops over all units and checks weather they are disorganized or
        routed. Checks weather the unit can rally and if it can then it's mode is set to the mode it
        should have after after being disorganized/routed.

        A unit can rally or become disorganized if its morale is high enough. The limits for
        rallying are:

        * routed -> disorganized: 30
        * disorganized -> normal: 45
        """

        # TODO: using hardcoded morale values here

        # loop over all units we have
        for unit in scenario.info.units.values():
            # is the unit currently able to rally?
            if unit.getMode().canRally():
                # yes, it could optionally rally, it its morale high enough?
                if unit.getMorale().getValue() > 45:
                    # yep, it can rally
                    self.setMode(unit, unit.getMode().onRally(), actiondata)

            # no, it can't rally, can it become disorganized, ie is it routed?
            elif unit.getMode().canDisorganize():
                # yes, it could optionally become disorganized, it its morale high enough?
                if unit.getMorale().getValue() > 30:
                    # yep, it can rally
                    self.setMode(unit, unit.getMode().onDisorganize(), actiondata)
