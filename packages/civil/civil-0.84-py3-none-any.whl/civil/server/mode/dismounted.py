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


class Dismounted(Mode):
    """
    This implements the mode 'dismounted'. It is used by cavalry when the troops are dismounted. 

 """

    def __init__(self):
        """
        Initializes the mode.
        """
        # call superclass
        Mode.__init__(self, "dismounted", "dismounted")

        # set the modes we change to
        self.onchangemode = "mounting"
        self.onmove = "dismountedmove"
        self.onmovefast = ""
        self.onrotate = "dismounted"
        self.onhalt = ""
        self.onretreat = "retreatingdismounted"
        self.onskirmish = "dismountedskirmish"
        self.ondone = "dismounted"
        self.onmelee = "meleeingdismounted"
        self.onassault = ""
        self.onchangepolicy = "dismounted"
        self.onwait = "dismounted"

        # set a base fatigue
        self.base_fatigue = -1.0
