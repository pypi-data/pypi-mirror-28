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


class ColumnMoveFast(Mode):
    """
    This implements the mode 'column move fast'. It is used by infantry in 'column' mode that is
    moving double march. Only infantry in column mode can move fast.
    """

    def __init__(self):
        """
        Initializes the mode.
        """
        # call superclass
        Mode.__init__(self, "columnmovefast", "moving fast in column")

        # set the modes we change to
        self.onchangemode = ""
        self.onmove = "columnmove"
        self.onmovefast = "columnmovefast"
        self.onrotate = "columnmovefast"
        self.onhalt = "column"
        self.onretreat = "retreatingcolumn"
        self.onskirmish = ""
        self.ondone = "column"
        self.onmelee = "meleeingcolumn"
        self.onassault = ""
        self.onchangepolicy = "columnmovefast"
        self.onwait = ""

        # set a base fatigue
        self.base_fatigue = 4
