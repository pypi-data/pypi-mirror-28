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


class FormationMove(Mode):
    """
    This implements the mode 'formation move'. It is used by infantry that is moving in a formation
    mode. Infantry having the mode 'formation' which then moves normally will have this mode. Moving
    in formation is slower than moving in column.
    """

    def __init__(self):
        """
        Initializes the mode.
        """
        # call superclass
        Mode.__init__(self, "formationmove", "moving in formation")

        # set the modes we change to
        self.onchangemode = ""
        self.onmove = "formationmove"
        self.onmovefast = ""
        self.onrotate = "formationmove"
        self.onhalt = "formation"
        self.onretreat = "retreatingformation"
        self.onskirmish = ""
        self.ondone = "formation"
        self.onmelee = "meleeingformation"
        self.onassault = ""
        self.onchangepolicy = "formationmove"
        self.onwait = ""

        # set a base fatigue
        self.base_fatigue = 2
