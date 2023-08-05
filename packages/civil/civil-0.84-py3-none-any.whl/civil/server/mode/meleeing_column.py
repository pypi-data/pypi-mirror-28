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


class MeleeingColumn(Mode):
    """
    This implements the mode 'meleeing' for infantry units in column. It is used by column
    units when they are meleeing, ie in close combat with some attacking unit.

    After melee the column will be disorganized, or it may also rout.
    """

    def __init__(self):
        """
        Initializes the mode.
        """
        # call superclass
        Mode.__init__(self, "meleeingcolumn", "meleeing")

        # set the modes we change to
        # self.onchangemode  = ""
        # self.onmove        = ""
        # self.onmovefast    = ""
        # self.onrotate      = ""
        # self.onhalt        = ""
        self.onretreat = "retreatingcolumn"
        # self.onskirmish    = ""
        self.ondone = "disorganizedcolumn"
        self.onmelee = "meleeingcolumn"
        # self.onassault      = ""
        # self.onchangepolicy = ""
        # self.onwait         = ""

        # this is a meleeing mode
        self.ismeleeing = 1

        # set a base fatigue
        self.base_fatigue = 5.0
