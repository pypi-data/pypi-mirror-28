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
from civil.server.action.action import Action


class ChangeModifiersAct(Action):
    """
    This class implements the action 'change_modifier'. This is sent by the server when an unit
    has got one or more of its modifiers changed. All of them need not have changed, but they are
    all transmitted in this action anyway. The sent ones are:

    * fatigue
    * morale
    * experience

    The data is simply just applied to the concerned unit.
    """

    def __init__(self, unit_id=-1, fatigue=-1, morale=-1, experience=-1):
        """
        Initializes the instance.
        """
        # call superclass constructor
        Action.__init__(self, "change_modifiers_act")

        # store all data
        self.unit_id = unit_id
        self.fatigue = fatigue
        self.morale = morale
        self.experience = experience

    def extract(self, parameters):
        """
        Extracts the data for the command.
        """
        # parse out the data
        self.unit_id = int(parameters[0])
        self.fatigue = int(parameters[1])
        self.morale = int(parameters[2])
        self.experience = int(parameters[3])

    def execute(self):
        """
        Executed the action. Finds the affected unit and updates its modifiers.
        """

        # precautions
        if self.unit_id not in scenario.info.units:
            # no such unit? bad stuff...
            raise RuntimeError("could not find unit: %d" % self.unit_id)

        # get the unit with the given id 
        unit = scenario.info.units[self.unit_id]

        # set the new modifiers
        unit.getFatigue().setValue(self.fatigue)
        unit.getMorale().setValue(self.morale)
        unit.getExperience().setValue(self.experience)

        # make sure the world knows of this change
        if not scenario.local_player_ai:
            scenario.dispatcher.emit('units_changed', (unit,))

    def toString(self):
        """
        Returns a string representation of the command, suitable for sending over a socket.
        """
        # create a string and return
        return "%s %d %d %d %d\n" % (self.getName(), self.unit_id, self.fatigue, self.morale, self.experience)

    def __str__(self):
        """
        Convenience wrapper for toString() suitable for using when debugging and printing the
        command to the screen. Will just call toString().
        """
        return self.toString()
