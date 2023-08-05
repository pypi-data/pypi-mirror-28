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


class Formation(Mode):
    """
    This implements the mode 'formation'. It is used by infantry only and means that the troops are
    laid out in a battle formation, i.e. on a line. This mode is used in combat and gives the unit
    good possibilities to advance, defend etc.
    """

    def __init__(self):
        """
        Initializes the mode.
        """
        # call superclass
        Mode.__init__(self, "formation", "formation")

        # set the modes we change to
        self.onchangemode = "changingtocolumn"
        self.onmove = "formationmove"
        self.onmovefast = ""
        self.onrotate = "formation"
        self.onhalt = ""
        self.onretreat = "retreatingformation"

        self.onskirmish = "formationskirmish"
        self.onmelee = "meleeingformation"
        self.onassault = "formationassault"

        self.ondone = "formation"
        self.onchangepolicy = "formation"
        self.onwait = "formation"

        # set a base fatigue
        self.base_fatigue = -1
