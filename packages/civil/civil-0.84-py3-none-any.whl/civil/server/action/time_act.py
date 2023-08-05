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

import datetime

from civil.model import scenario
from civil.server.action.action import Action


class TimeAct(Action):
    """
    This class implements the action 'time'. This is sent by the server when the time has
    changed. It is sent out regularly so that players can keep up with what's going on. The time is
    given in elapsed seconds since the last update.
    """

    def __init__(self, seconds=-1):
        """
        Initializes the instance.
        """
        # call superclass constructor
        Action.__init__(self, "time_act")

        # store all data
        self.seconds = seconds

    def extract(self, parameters):
        """
        Extracts the data for the command.
        """
        # parse out the data
        self.seconds = int(parameters[0])

    def execute(self):
        """
        Executed the action. Adds the given number of seconds to the current game time.
        """

        # create a delta time
        delta = datetime.timedelta(seconds=self.seconds)

        # set the new time
        scenario.info.setCurrentDate(scenario.info.getCurrentDate() + delta)

        # make sure the world knows of this change
        if not scenario.local_player_ai:
            scenario.dispatcher.emit('time_changed', None)

    def toString(self):
        """
        Returns a string representation of the command, suitable for sending over a socket.
        """
        # create a string and return
        return "%s %d\n" % (self.getName(), self.seconds)

    def __str__(self):
        """
        Convenience wrapper for toString() suitable for using when debugging and printing the
        command to the screen. Will just call toString().
        """
        return self.toString()
