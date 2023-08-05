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


class Limbering(Mode):
    """
    This implements the mode 'limbering'. It is used by artillery as an intermediate mode when the
    guns are being limbered and ready for transport. Artillery can not move unless limbered.
    """

    def __init__(self):
        """
        Initializes the mode.
        """
        # call superclass
        Mode.__init__(self, "limbering", "limbering")

        # set the modes we change to
        self.onchangemode = ""
        self.onmove = ""
        self.onmovefast = ""
        self.onrotate = ""
        self.onhalt = ""
        self.onretreat = "retreatinglimbered"
        self.onskirmish = ""
        self.ondone = "limbered"
        self.onmelee = "meleeinglimbered"
        self.onassault = ""
        self.onchangepolicy = "limbering"
        self.onwait = ""

        # set a base fatigue
        self.base_fatigue = 4
