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


class DismountedMove(Mode):
    """
    This implements the mode 'dismounted'. It is used by cavalry when the troops are dismounted and
    the unit is moving. This mode is slower for movement that 'mounted move'.
    """

    def __init__(self):
        """
        Initializes the mode.
        """
        # call superclass
        Mode.__init__(self, "dismountedmove", "moving dismounted")

        # set the modes we change to
        self.onchangemode = ""
        self.onmove = "dismountedmove"
        self.onmovefast = ""
        self.onrotate = "dismountedmove"
        self.onhalt = "dismounted"
        self.onretreat = "retreatingdismounted"
        self.onskirmish = ""
        self.ondone = "dismounted"
        self.onmelee = "meleeingdismounted"
        self.onassault = ""
        self.onchangepolicy = "dismountedmove"
        self.onwait = ""

        # set a base fatigue
        self.base_fatigue = 2
