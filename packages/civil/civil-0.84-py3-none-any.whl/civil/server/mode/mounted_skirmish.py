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


class MountedSkirmish(Mode):
    """
    This implements the mode 'mountedskirmish'. It is used by cavalry only and means that the troops are
    horsemounted, i.e. battle ready and are skirmishing with an enemy unit. 

 """

    def __init__(self):
        """
        Initializes the mode.
        """
        # call superclass
        Mode.__init__(self, "mountedskirmish", "mounted skirmish")

        # set the modes we change to
        self.onchangemode = ""
        self.onmove = "mountedmove"
        self.onmovefast = "mountedmovefast"
        self.onrotate = "mounted"
        self.onhalt = "mounted"
        self.onretreat = "retreatingmounted"
        self.ondone = "mounted"

        self.onskirmish = "mountedskirmish"
        self.onmelee = "meleeingmounted"
        self.onassault = "mountedassault"
        self.onchangepolicy = "mountedskirmish"
        self.onwait = ""

        # set a base fatigue
        self.base_fatigue = 3.0
