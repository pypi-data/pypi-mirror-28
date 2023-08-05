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


class Column(Mode):
    """
    This implements the mode 'column'. It is used by infantry only and means that the troops are
    ready for marching. This means that the troops will march a few men wide and as a long
    column. This mode is used for moving the troops longer distances when not engaged.
    """

    def __init__(self):
        """
        Initializes the mode.
        """
        # call superclass
        Mode.__init__(self, "column", "column")

        # set the modes we change to
        self.onchangemode = "changingtoformation"
        self.onmove = "columnmove"
        self.onmovefast = "columnmovefast"
        self.onrotate = "column"
        self.onhalt = ""
        self.onretreat = "retreatingcolumn"
        self.onskirmish = "columnskirmish"
        self.ondone = "column"
        self.onmelee = "meleeingcolumn"
        self.onassault = ""
        self.onchangepolicy = "column"
        self.onwait = "column"

        # set a base fatigue
        self.base_fatigue = -2.0
