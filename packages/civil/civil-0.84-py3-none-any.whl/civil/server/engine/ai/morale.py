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

from civil import constants
from civil import properties
from civil.model import scenario
from civil.server.action.end_game_act import EndGameAct
from civil.server.engine.ai.module import Module


class Morale(Module):
    """
    This class defines a module that when executed checks weather one of the armies is seriously
    demoralized and will auto-surrender. This calculation is performed by just adding all total
    morale in the army and dividing with the count of units. A demoralized army is considered
    unwilling to fight anymore and will surrender.

    If either player has no units left then the game is also ended, in the same way as
    'UnitsDestroyed' would do.

    The setting module_morale_minimum determines the minimum morale.
   
    This module is executed once every turn.

    TODO: handle victories and draws somehow
    """

    def __init__(self):
        """
        Initializes the module. Sets a suitable name.
        """

        # call superclass with the delays and name
        Module.__init__(self, 'morale', 60)

    def execute(self, actiondata):
        """
        Executes the module. Counts the number of units that are left for both armies, and if
        either (or both) players have less units left than a certain % then the game is ended.
        """

        # no morale and no units at all yet
        morale = {constants.REBEL: 0, constants.UNION: 0}
        counts = {constants.REBEL: 0, constants.UNION: 0}

        # loop over all ok units
        for unit in scenario.info.units.values():
            # add to the counts
            morale[unit.getOwner()] += unit.getMorale().getValue()
            counts[unit.getOwner()] += 1

        # we need to check the counts to make sure that neither player has no companies left. If
        # that would happened we'd do a nice ZeroDivisionError when calculating the average morale

        # is the rebel player destroyed?
        if counts[constants.REBEL] == 0:
            # rebels are destroyed
            print("Morale.execute: rebel army destroyed")
            actiondata.append(EndGameAct(constants.REBEL_DESTROYED))
            return

        # is the union player destroyed?
        if counts[constants.UNION] == 0:
            # unions are destroyed
            print("Morale.execute: union army destroyed")
            actiondata.append(EndGameAct(constants.UNION_DESTROYED))
            return

        # get the minimum morale
        minmorale = properties.module_morale_minimum

        # loop over the armies
        for player in (constants.REBEL, constants.UNION):
            # is the total average morale less than the current allowed?
            if float(morale[player]) / counts[player] < minmorale:
                # yep, the army is demoralized
                print("Morale.execute: army for player %d is demoralized" % player)

                # get the flag we should send
                flag = [constants.REBEL_DEMORALIZED, constants.UNION_DEMORALIZED][player]

                # and enqueue the plan ending the game
                actiondata.append(EndGameAct(flag))
