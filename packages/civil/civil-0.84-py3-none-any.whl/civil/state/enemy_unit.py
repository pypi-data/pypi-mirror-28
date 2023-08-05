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

from civil.state import state


class EnemyUnit(state.State):
    """
    This class is a state that provides basic handling of enemy units. This state should be
    activated when the player clicks on an enemy unit or some other way makes an enemy unit
    active. Very little can be done with an enemy unit, apart from showing some limited information
    about it in the panel.

    This state will activate the following other states:

    * idle if the player clicks in the terrain somewhere.
    * own_unit if an own unit is clicked.

    * enemy_unit is kept if another enemy unit is clicked on.
    """

    def __init__(self):
        """
        Initializes the instance. Sets default values for all needed members.
        """

        # call superclass constructor
        state.State.__init__(self)

        # set default cursor
        self.setDefaultCursor()

        # set defaults
        self.name = "enemy_unit"

        # define the help text too
        self.helptext = ["An enemy unit is selected",
                         " ",
                         "arrow keys - scroll map",
                         "F1 - show this help text",
                         "F10 - toggle fullscreen mode",
                         "F12 - save a screenshot",
                         "Alt s - save the game"]
