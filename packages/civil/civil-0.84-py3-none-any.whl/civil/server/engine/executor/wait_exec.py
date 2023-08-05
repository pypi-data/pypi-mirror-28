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

from civil.server.engine.executor.executor import Executor


class WaitExec(Executor):
    """
    This class executes the plan 'wait'. This plan is sent by clients when a unit has been
    ordered to wait for a certain amount of time. This executor will simply be delayed that amount
    of time and then it will be finished. No other action. The unit wil lnot gain fatigue.
    """

    def __init__(self, unit, plan):
        """
        Initializes the instance.
        """
        # call superclass constructor
        Executor.__init__(self, unit, plan)

    def execute(self):
        """
        Executes the plan. Does nothing, when we get this far the plan is already executed, as


 """

        # execution is finished, nothing to do at all
        self.finished = 1
