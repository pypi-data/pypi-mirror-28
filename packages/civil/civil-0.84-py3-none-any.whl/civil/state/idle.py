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
from civil.model import scenario


class Idle(state.State):
    """
    This class is the default state in the game. It will only activate other states depending on
    input events. It does handle some basic common functionality such as:

    * scrolling with the keyboard
    
    This state will activate the following other states:

    * enemy_unit if an enemy unit is clicked.
    * own_unit if an own unit is clicked.

    * idle is kept if no other state is activated.
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
        self.name = "idle"

        # no selected unit
        if self.clearSelectedUnits():
            scenario.dispatcher.emit('unit_selected', None)
