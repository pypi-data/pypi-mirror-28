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
from civil.server.action.reinforcements_act import ReinforcementsAct
from civil.server.engine.ai.module import Module


class CheckReinforcements(Module):
    """
    This class defines a module that when executed checks weather any reinforcement units have
    become available. The units that are marked as reinforcements are checked one by one and if they
    are scheduled to arrive at this time they are made visible to the owning player.
   
    This module is executed once every minute.
    """

    def __init__(self):
        """
        Initializes the module. Sets a suitable name.
        """

        # call superclass with the delays and name
        Module.__init__(self, 'check_reinforcements', 60)

    def execute(self, actiondata):
        """
        Executes the module. Checks weather any reinforcements have arrived this turn. This is
        done by iterating the global data structure that contains the arrival turns. If any new unit
        have arrived they will be made available and shown. Sends an ReinforcementsAct action to the
        players.

        It should maybe not be sent to both players, only to the one that gets the reinforcements?
        What about the new units being seen by the other player then, would that work?
        """

        # no reinforcements yet
        reinforcements = []

        # get the current date
        current_date = scenario.info.getCurrentDate()

        # loop over all reinforcements that are available
        for company, arrive_date in list(scenario.info.reinforcements.values()):
            # has this unit arrived at the battlefield?
            # TODO current_turn unknown
            if current_turn < arrive_date:
                # not yet, next unit please
                continue

            # so the unit has arrived, add it to the global structure of available units
            scenario.info.units[company.getid()] = company

            # remove the unit from the map of reinforcements
            del scenario.info.reinforcements[company.getid()]

            # we have something now
            reinforcements.append(company.getid())

        # ok, all units iterated, did we get anything this turn?
        if len(reinforcements) > 0:
            # yes, create the needed action
            actiondata.append(ReinforcementsAct(reinforcements))
