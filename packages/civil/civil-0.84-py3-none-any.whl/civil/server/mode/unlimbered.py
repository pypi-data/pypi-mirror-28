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


class Unlimbered(Mode):
    """
    This implements the mode 'unlimbered'. It is used by artillery when the guns are unlimbered and
    ready for battle action. Artillery can not fire the guns unless unlimbered. Unlimbered guns are
    placed in a battle formation.

    Unlimbered artillery forced to retreat may abandon their guns as it can't move unless limbered.
    """

    def __init__(self):
        """
        Initializes the mode.
        """
        # call superclass
        Mode.__init__(self, "unlimbered", "unlimbered")

        # set the modes we change to
        self.onchangemode = "limbering"
        self.onmove = ""
        self.onmovefast = ""
        self.onrotate = "unlimbered"
        self.onhalt = ""
        self.onretreat = "retreatingunlimbered"
        self.onskirmish = "unlimberedskirmish"
        self.ondone = "unlimbered"
        self.onmelee = "meleeingunlimbered"
        self.onassault = ""
        self.onchangepolicy = "unlimbered"
        self.onwait = "unlimbered"

        # set a base fatigue
        self.base_fatigue = -1
