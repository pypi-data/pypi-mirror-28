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


class UnlimberedSkirmish(Mode):
    """
    This implements the mode 'unlimbered skirmish'. It is used by artillery when skirmishing. This
    means that the guns are unlimbered and the guns are actively firing at an enemy.
    """

    def __init__(self):
        """
        Initializes the mode.
        """
        # call superclass
        Mode.__init__(self, "unlimberedskirmish", "unlimbered skirmish")

        # set the modes we change to
        self.onchangemode = "limbered"
        self.onmove = ""
        self.onmovefast = ""
        self.onrotate = "unlimbered"
        self.onhalt = "unlimbered"
        self.onretreat = "retreatingunlimbered"
        self.onskirmish = "unlimberedskirmish"
        self.ondone = "unlimbered"
        self.onmelee = "meleeingunlimberedy"
        self.onassault = ""
        self.onchangepolicy = "unlimberedskirmish"
        self.onwait = ""

        # set a base fatigue
        self.base_fatigue = 6
