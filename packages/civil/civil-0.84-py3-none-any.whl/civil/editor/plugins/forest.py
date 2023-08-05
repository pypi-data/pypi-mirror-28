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

from civil.editor.plugins.creator import *


class ForestCreator(Creator):
    """
    ForestCreator creates the proper icons for a continuous block
    of forest.
    """

    def __init__(self, iconview):
        Creator.__init__(self, iconview, Creator.addkind__forest, "ForestCreator", "Create continuous blocks of forest")

    def isEmpty(self, set, id):
        """

        Args:
            set: 
            id: 

        Returns:

        """
        for i in set[id]:
            if i == terrain.terrainDict['w']:
                return 0
        return 1

    def get_empty_need(self):
        """

        Returns:

        """
        return [None, None, None, None, None, None]

    def calcNeed(self, x, y, neighbors, bit_from_our_hex):
        """

        Args:
            x: 
            y: 
            neighbors: 
            bit_from_our_hex: 

        Returns:

        """
        t = scenario.map.getHex(x, y).template.getTerrains()

        # Add connection to our primary hex
        rev = bit_from_our_hex << 3
        if rev > UL: rev = bit_from_our_hex >> 3

        w = terrain.terrainDict['w']
        if rev == 1:
            t[0] = w
        if rev == 2:
            t[1] = w
        if rev == 4:
            t[2] = w
        if rev == 8:
            t[3] = w
        if rev == 16:
            t[4] = w
        if rev == 32:
            t[5] = w
        return t

    def match(self, from_set, our_need):
        """

        Args:
            from_set: 
            our_need: 

        Returns:

        """
        assert (len(from_set) == len(our_need))
        for i in range(len(from_set)):
            if from_set[i] != our_need[i]:
                return 0
        return 1


def new(iconview):
    """

    Args:
        iconview: 

    Returns:

    """
    return ForestCreator(iconview)
