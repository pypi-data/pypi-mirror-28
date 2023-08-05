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


class ColumnSkirmish(Mode):
    """
    This implements the mode 'columnskirmish'. It is used by infantry only and means that the troops
    are ready for marching but are firing at some target. Compared to the mode 'formationskirmish'
    units in this mode fire at a greatly reduced effectivity, as the troops are not lined up for
    effective firing.
    """

    def __init__(self):
        """
        Initializes the mode.
        """
        # call superclass
        Mode.__init__(self, "columnskirmish", "column skirmish")

        # set the modes we change to
        self.onchangemode = ""
        self.onmove = "columnmove"
        self.onmovefast = "columnmovefast"
        self.onrotate = "column"
        self.onhalt = ""
        self.onretreat = "retreatingcolumn"
        self.onskirmish = "columnskirmish"
        self.ondone = "column"
        self.onmelee = "meleeingcolumn"
        self.onassault = ""
        self.onchangepolicy = "columnskirmish"
        self.onwait = ""

        # set a base fatigue
        self.base_fatigue = 2.0
