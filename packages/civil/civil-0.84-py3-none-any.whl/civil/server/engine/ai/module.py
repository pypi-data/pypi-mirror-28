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

import copy
import datetime

from civil.model import scenario
from civil.server.action.change_modifiers_act import ChangeModifiersAct
from civil.server.action.clear_target_act import ClearTargetAct
from civil.server.action.set_mode_act import SetModeAct
from civil.server.mode.mode_factory import createMode


class Module:
    """
    This class defines the interface for module classes. A module is simply some code that plugs
    into the engine and provides simple AI-like functionality. Modules are executed by the engine
    every turn by running the method execute(). If a module should not be executed each turn it must
    keep track of that internally.

    Subclasses must override the method execute() and do something meaningful in it. They are also
    required to pass a name to the constructor of this class. The name can be used for debugging
    later.

    The method execute() should return a list of action data that the module created, and also to
    make sure that the same action is applied to the units.

    Modules are checked weather they are ready to exeute using the method isReady(). By default all
    modules execute at all turns, but by setting a custom timedelta it can be made to execute less
    often.

    """

    def __init__(self, name, delay=0):
        """
        Initializes the module. Stores the passed name. The delay is the delay in simulation
        seconds before the module is executed again. The default value 0 makes the module execute
        every time.
        """
        self.name = name

        # store the delay seconds
        self.delay = delay

        # store the last executed time, this is the current time of the scenario
        start = scenario.info.getCurrentDate()
        self.last_executed = datetime.datetime(start.year, start.month, start.day, start.hour,
                                               start.minute, start.second)

    def getName(self):
        """
        Returns the name of the module.
        """
        return self.name

    def isReady(self):
        """
        Checks weather the module is ready to be executed. Returns 1 if it is and 0 if not.
        """
        # create a delta time
        delta = datetime.timedelta(seconds=self.delay)

        # print  self.name, scenario.info.getCurrentDate (),  self.last_executed, delta

        # is the current date past the date when the module should be executed?
        if self.last_executed + delta > scenario.info.getCurrentDate():
            # not yet ready
            # print "Module.isReady: %s not ready" % self.name
            return 0

        # print "Module.isReady: %s *is* ready" % self.name

        # ready for execute, store new last executed time
        self.last_executed = copy.deepcopy(scenario.info.getCurrentDate())
        return 1

    def execute(self, actiondata):
        """
        Executes the module. The module can perform whatever automatic tasks it wants to. This
        method must be overridden by subclasses.

        The created action should be appended to the 'actiondata' list passed as a parameter.  The
        same action should also be applied to the units.
        """

        raise NotImplementedError("Module.execute: this method must be overridden")

    def setMode(self, unit, mode, actiondata):
        """
        Convenience method creating a new mode for a unit and also create the needed action
        data.
        """
        # make action for the new mode and add to the result
        actiondata.append(SetModeAct(unit.getId(), mode))

        # create the proper mode and assign it to the unit
        unit.setMode(createMode(mode))

    def clearTarget(self, unit, actiondata):
        """
        Clears the target for the unit. Modifies the unit and also create action for the
        clearing and puts it onto 'actiondata'. The unit is set to have whatever mode is proper for


 """

        # clear the target for the unit 
        unit.setTarget(None)

        # create action too
        actiondata.append(ClearTargetAct(unit.getId()))

        # set a mode too that should be when the unit is done with combat
        self.setMode(unit, unit.getMode().onDone(), actiondata)

    def changeModifiers(self, unit, actiondata):
        """
        This method is a convenience method for subclasses that need to generate action for
        changed modifiers. The call to make the action is a bit long and unwieldy, so it has been
        put here instead. Puts a new ChangeModifiersAct to the actiondata.
        """

        # create the action
        actiondata.append(ChangeModifiersAct(unit_id=unit.getId(),
                                             fatigue=unit.getFatigue().getValue(),
                                             morale=unit.getMorale().getValue(),
                                             experience=unit.getExperience().getValue()))
