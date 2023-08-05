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


class MeleeingUnlimbered(Mode):
    """
    This implements the mode 'meleeing' for unlimbered units. It is used by unlimbered artillery units
    when they are meleeing, ie in close combat with some attacking unit. Meleeing unlimbered means that
    the men may  probably use normal rifles instead of the guns, as the enemy is upon them.

    After melee the unlimbered will be disorganized, or it may also rout.
    """

    def __init__(self):
        """
        Initializes the mode.
        """
        # call superclass
        Mode.__init__(self, "meleeingunlimbered", "meleeing")

        # set the modes we change to
        # self.onchangemode  = ""
        # self.onmove        = ""
        # self.onmovefast    = ""
        # self.onrotate      = ""
        # self.onhalt        = ""
        self.onretreat = "retreatingunlimbered"
        # self.onskirmish    = ""
        self.ondone = "disorganizedunlimbered"
        self.onmelee = "meleeingunlimbered"
        # self.onassault      = ""
        # self.onchangepolicy = ""
        # self.onwait         = ""

        # this is a meleeing mode
        self.ismeleeing = 1

        # set a base fatigue
        self.base_fatigue = 5.0
