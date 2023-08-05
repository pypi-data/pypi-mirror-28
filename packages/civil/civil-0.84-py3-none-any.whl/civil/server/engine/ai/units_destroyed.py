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


class UnitsDestroyed(Module):
    """
    This class defines a module that when executed checks weather one or both of the armies have
    lost more units than a specified percentage, say 75%. If this happens then the army is
    considered to be collapsed and not useful anymore and the server will automatically surrender
    that player. If both armies have been reduced sufficiently then a draw will be declared, as
    neither army is anymore fit for combat.

    The setting module_unitsdestroyed_percentage determines the minimum morale.
    
    This module is executed once every minute.

    TODO: handle victories and draws somehow
    """

    def __init__(self):
        """
        Initializes the module. Sets a suitable name.
        """

        # call superclass with the delays
        Module.__init__(self, 'unitsdestroyed', 60)

    def execute(self, actiondata):
        """
        Executes the module. Counts the number of units that are left for both armies, and if
        either (or both) players have less units left than a certain % then the game is ended.
        """

        # nothing alive at all yet
        ok = {constants.REBEL: 0, constants.UNION: 0}
        destroyed = {constants.REBEL: 0, constants.UNION: 0}

        # loop over all ok units
        for unit in scenario.info.units.values():
            # add to the counts
            ok[unit.getOwner()] += 1

        # loop over all destroyed units
        for unit in list(scenario.info.destroyed_units.values()):
            # add to the counts
            destroyed[unit.getOwner()] += 1

        # get the ratio
        ratio = properties.module_unitsdestroyed_percentage

        # do we have more rebel units destroyed than the ratio?
        if destroyed[constants.REBEL] > 0 and \
                float(ok[constants.REBEL]) / (destroyed[constants.REBEL] + ok[constants.REBEL]) < ratio:
            # rebel army destroyed
            rebeldestroyed = 1
        else:
            # not yet destroyed
            rebeldestroyed = 0

        # do we have more union units destroyed than the ratio?
        if destroyed[constants.UNION] > 0 and \
                float(ok[constants.UNION]) / (destroyed[constants.UNION] + ok[constants.UNION]) < ratio:
            # union army destroyed
            uniondestroyed = 1
        else:
            # not yet destroyed
            uniondestroyed = 0

        # are both destroyed?
        if rebeldestroyed and uniondestroyed:
            # both armies destroyed, a draw
            print("UnitsDestroyed.execute: rebel and union armies destroyed, draw")
            actiondata.append(EndGameAct())

        elif rebeldestroyed:
            # rebel army destroyed
            print("UnitsDestroyed.execute: rebel army destroyed")
            actiondata.append(EndGameAct(constants.REBEL_DESTROYED))

        elif uniondestroyed:
            # union army destroyed
            print("UnitsDestroyed.execute: union army destroyed")
            actiondata.append(EndGameAct(constants.UNION_DESTROYED))
