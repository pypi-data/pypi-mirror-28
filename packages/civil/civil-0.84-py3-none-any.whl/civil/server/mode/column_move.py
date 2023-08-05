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


class ColumnMove(Mode):
    """
    This implements the mode 'column move'. It is used by infantry in 'column' mode that are
    moving. It is faster for an infantry company to move in column than in formation, as the men are
    physically laid out so that they can march faster on narrow paths or roads.
    """

    def __init__(self):
        """
        Initializes the mode.
        """
        # call superclass
        Mode.__init__(self, "columnmove", "moving in column")

        # set the modes we change to
        self.onchangemode = ""
        self.onmove = "columnmove"
        self.onmovefast = "columnmovefast"
        self.onrotate = "columnmove"
        self.onhalt = "column"
        self.onretreat = "retreatingcolumn"
        self.onskirmish = ""
        self.ondone = "column"
        self.onmelee = "meleeingicolumn"
        self.onassault = ""
        self.onchangepolicy = "columnmove"
        self.onwait = ""

        # set a base fatigue
        self.base_fatigue = 1
