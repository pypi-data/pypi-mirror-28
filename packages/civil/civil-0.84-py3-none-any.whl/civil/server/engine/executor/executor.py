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
from civil.server.action.change_modifiers_act import ChangeModifiersAct
from civil.server.action.set_mode_act import SetModeAct
from civil.server.mode.mode_factory import createMode


class Executor:
    """
    This class is a base class for all available types of plan executors. It is supposed to be
    subclassed for each plan that is to be executed. So if there is a plan 'Move' then there should
    be a 'MoveExec' that knows how to execute that plan. Each executor knows the unit that owns the
    executed plan and the plan itself.

    When the executor is created the plan is assumed to be ready to be executed, no extra delays
    needed. 

    The method 'execute()' is the method that executes the plan, and it is called once for each turn
    that the plan is being executed. This methis should return one or more subclasses of Action that
    contains the action for a single turn, or None if no action is wanted.

    Each executor knows all units, and should alter the affected units before returning the action
    instance from 'execute()'. The reasoning behind this is that each executor when it executes does
    not need to worry where a unit is supposed to be at that step. Instead one can think that it has
    already applied all earlier computed action.
    """

    def __init__(self, unit, plan, delay=-1):
        """
        Initializes the instance. Stores the unit and the plan this executor handles.
        """
        # store the passed data
        self.unit = unit
        self.plan = plan

        # store the given delay
        self.delay = delay

        # not finished nor executing yet
        self.finished = 0
        self.executing = 0

        # execution not yet started (for those who need this)
        self.firsttime = 1

    def setDelay(self, delay):
        """
        Sets a new delay for the plan executor.
        """
        self.delay = delay

        # print "Executor.setDelay: plan %s, delay %d" % ( self.plan.getName(), delay )

    def decrementDelay(self, delay=1):
        """
        Decrements the delay of the plan with the given value. If the delay becomes 0 then the
        plan can be executed and 1 is returned. If the plan is not yet ready 0 is returned.
        """
        self.delay -= delay

        # print "Executor.decrementDelay: %d" % self.delay

        # did we get to 0?
        if self.delay <= 0:
            # yep, we're ready to start executing
            self.executing = 1
            return 1

        # not yet ready
        return 0

    def isExecuting(self):
        """
        Returns 1 if the executur is being currently executed.
        """
        return self.executing

    def isFinished(self):
        """
        Returns 1 if the execuor has determined that the plan has been finished. Returns 0 if it
        should still be executed.
        """
        return self.finished

    def getUnit(self):
        """
        Returns the unit that the executed plan belongs to.
        """
        return self.unit

    def getPlan(self):
        """
        Returns the plan that is being executed.
        """
        return self.plan

    def execute(self):
        """
        Executes the plan for the current turn. This method must be overridden by subclasses. The
        method may return either a single Action subclass, or a list/tuple of the same.
        """

        # must override!
        raise NotImplementedError("Executor.execute: this method must be overridden")

    def setUnitMode(self, unit, modename):
        """
        This is a convenience method for setting a new mode for a unit based on a mode name. The
        mode is set immediately for the unit that the executed plan refers to and the correct action
        is returned.
        """

        # create the proper mode instance
        newmode = createMode(modename)

        # assign it to the unit
        unit.setMode(newmode)

        # create the action that sets the new mode for clients too and return it
        return SetModeAct(unit.getId(), modename)

    def changeModifiers(self, unit):
        """
        This method is a convenience method for subclasses that need to generate action for
        changed modifiers. The call to make the action is a bit long and unwieldy, so it has been
        put here instead. Returns a new ChangeModifiersAct.
        """

        # create the action
        return ChangeModifiersAct(unit_id=unit.getId(),
                                  fatigue=unit.getFatigue().getValue(),
                                  morale=unit.getMorale().getValue(),
                                  experience=unit.getExperience().getValue())

    def validateUnit(self, id):
        """
        Validates that a given unit is valid. Tries to get the unit with the given id from the
        unit collection. Returns the unit if found and None if not found.
        """
        # do we have such a unit?
        if id not in scenario.info.units:
            # no such unit
            return None

        # get it!
        return scenario.info.units[id]
