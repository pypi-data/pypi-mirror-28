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

import string

from civil.model import scenario
from civil.server.action.action import Action


class ReinforcementsAct(Action):
    """
    This class implements the action 'reinforcements'. This is sent by the server when a number of
    units have arrived at the battle scene as reinforcements. Both Union and Rebel units are in this
    same action. The player owned units are just set to be visible, and the enemy units are visible
    only if a friendly unit sees them.
    """

    def __init__(self, unit_ids=None):
        """
        Initializes the instance.
        """
        # call superclass constructor
        Action.__init__(self, "reinforcements_act")

        # store all data
        if unit_ids is None:
            unit_ids = []
        self.unit_ids = unit_ids

    def extract(self, parameters):
        """
        Extracts the data for the command.
        """
        # the parameters is a list of the ids, but as strings. so convert each string to an integer
        # and create a list from that
        self.unit_ids = [int(id) for id in parameters]

    def execute(self):
        """
        Executed the command. Finds the affected unit and updates its facing to the new
        facing.
        """

        arrived = 0

        # loop over all unit ids that should be shown
        for unit_id in self.unit_ids:
            # get the real unit
            unit = scenario.info.units[unit_id]

            # is it ours?
            if unit.getOwner() == scenario.local_player_id:
                # yes, so just set it as visible
                unit.setVisible(visible=1)

                # remove from the internal reinforcements map
                if unit_id in scenario.info.reinforcements:
                    del scenario.info.reinforcements[unit_id]

                # so the unit has arrived, add it to the global structure of available units
                scenario.info.units[unit_id] = unit

                # one more arrived
                arrived += 1

            else:
                # TODO: an enemy unit has arrived check if any of our units see it?
                pass

            # did we get any own units?
            if arrived > 0:
                scenario.messages.add('%d reinforcements units have arrived' % arrived)

                # make sure the world knows of this change
                # if not scenario.local_player_ai:
                #    scenario.dispatcher.emit ( 'units_changed', (unit,) )

    def toString(self):
        """
        Returns a string representation of the command, suitable for sending over a socket.
        """
        # create a space separated string from all the id:s
        id_string = "".join([str(id) for id in self.unit_ids])

        # create a string and return
        return "%s %s\n" % (self.getName(), id_string)

    def __str__(self):
        """
        Convenience wrapper for toString() suitable for using when debugging and printing the
        command to the screen. Will just call toString().
        """
        return self.toString()
