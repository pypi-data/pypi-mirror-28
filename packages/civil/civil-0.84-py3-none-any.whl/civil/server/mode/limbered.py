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


class Limbered(Mode):
    """
    This implements the mode 'limbered'. It is used by artillery when the guns are limbered and
    ready for transport. Artillery can not move unless limbered.
    """

    def __init__(self):
        """
        Initializes the mode.
        """
        # call superclass
        Mode.__init__(self, "limbered", "limbered")

        # set the modes we change to
        self.onchangemode = "unlimbering"
        self.onmove = "limberedmove"
        self.onmovefast = ""
        self.onrotate = "limbered"
        self.onhalt = ""
        self.onretreat = "retreatinglimbered"
        self.onskirmish = ""
        self.ondone = "limbered"
        self.onmelee = "meleeinglimbered"
        self.onassault = ""
        self.onchangepolicy = "limbered"
        self.onwait = "limbered"

        # set a base fatigue
        self.base_fatigue = -2
