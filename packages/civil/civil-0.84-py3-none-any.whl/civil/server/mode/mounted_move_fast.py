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


class MountedMoveFast(Mode):
    """
    This implements the mode 'mounted move fast'. It is used by cavalry when the troops are mounted on their
    horses and the unit is moving at a fast pace. 

 """

    def __init__(self):
        """
        Initializes the mode.
        """
        # call superclass
        Mode.__init__(self, "mountedmovefast", "moving fast as mounted")

        # set the modes we change to
        self.onchangemode = ""
        self.onmove = "mountedmove"
        self.onmovefast = "mountedmovefast"
        self.onrotate = "mountedmovefast"
        self.onhalt = "mounted"
        self.onretreat = "retreatingmounted"
        self.ondone = "mounted"

        self.onskirmish = "mountedskirmish"
        self.onmelee = "meleeingmounted"
        self.onassault = "mountedassault"
        self.onchangepolicy = "mountedmovefast"
        self.onwait = ""

        # set a base fatigue
        self.base_fatigue = 1.5
