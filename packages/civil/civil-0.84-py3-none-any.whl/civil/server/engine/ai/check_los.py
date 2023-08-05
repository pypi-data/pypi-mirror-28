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
from civil.model import scenario
from civil.server.action.set_visibility_act import SetVisibilityAct
from civil.server.engine.ai.module import Module


class CheckLOS(Module):
    """
    This class defines a module that checks line of sight for all units. It iterates over all
    units and checks weather they see any other enemy unit. Changed LOS data is sent out to clients
    so that they can keep consistent LOS information.
    """

    def __init__(self):
        """
        Initializes the module. Sets a suitable name.
        """
        # call superclass
        Module.__init__(self, 'checklos', 10)

    def execute(self, actiondata):
        """


 """

        # a hash for all the units
        visible = {}

        # loop over all units we have
        for unit1 in scenario.info.units.values():
            # and again, we need a cross product
            for unit2 in scenario.info.units.values():
                # now check weather unit1 sees unit2
                # TODO: add asymmetric LOS
                if unit1.seesEnemy(unit2):
                    # they see each other
                    visible[unit1.getId()] = 1
                    visible[unit2.getId()] = 1
                else:
                    # does not see it, so no LOS between the units
                    visible[unit1.getId()] = 0
                    visible[unit2.getId()] = 0

        # now all the units have flags set that match their visibility for the opponent
        for unit in scenario.info.units.values():
            # has the unit changed visibility for the enemy player?
            if unit.isVisible() == visible[unit.getId()]:
                # same value, so no change
                continue

            # unit has changed visibility, get the enemy to send to
            send_to_id = (constants.UNION, constants.REBEL)[unit.getOwner()]
            new_visibility = (1, 0)[unit.isVisible()]

            # create action for it
            actiondata.append(SetVisibilityAct(unit.getId(), new_visibility, send_to_id))

            # finally assign the new visibility to the units so that the server at least has
            # up-to-date data :) 
            unit.setVisible(new_visibility)
