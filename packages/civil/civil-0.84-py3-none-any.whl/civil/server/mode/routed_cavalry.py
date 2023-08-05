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

from civil.server.mode.mode import Mode


class RoutedCavalry(Mode):
    """
    This implements the mode 'routed'. It is used by cavalry units when they are routed,
    either by having taken a punishment or when the player has chosen to retreat the unit
    manually. As long as the unit is moving it will keep this state, and when it stops it will get
    the state 'disorganized'.
    """

    def __init__(self):
        """
        Initializes the mode.
        """
        # call superclass
        Mode.__init__(self, "routedcavalry", "routed")

        # set the modes we change to
        self.onchangemode = ""
        self.onmove = ""
        self.onmovefast = ""
        self.onrotate = ""
        self.onhalt = ""
        self.onretreat = ""
        self.onskirmish = ""
        self.ondone = "disorganizedmounted"
        self.onmelee = "meleeingmounted"
        self.onassault = ""
        self.onchangepolicy = ""
        self.onwait = ""
        self.onrally = ""
        self.ondisorganize = "disorganizedmounted"

        # set a base fatigue
        self.base_fatigue = 0.8
