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


class LimberedMove(Mode):
    """
    This implements the mode 'limbered move'. It is used by artillery when moving. This means that
    the guns are limbered and horses are pulling the guns. Note that there is now mode 'unlimbered
    move', as the guns must be limbered in order to move.
    """

    def __init__(self):
        """
        Initializes the mode.
        """
        # call superclass
        Mode.__init__(self, "limberedmove", "moving")

        # set the modes we change to
        self.onchangemode = ""
        self.onmove = "limberedmove"
        self.onmovefast = ""
        self.onrotate = "limberedmove"
        self.onhalt = "limbered"
        self.onretreat = "retreatinglimbered"
        self.onskirmish = ""
        self.ondone = "limbered"
        self.onmelee = "meleeinglimbered"
        self.onassault = ""
        self.onchangepolicy = "limberedmove"
        self.onwait = ""

        # set a base fatigue
        self.base_fatigue = 2
