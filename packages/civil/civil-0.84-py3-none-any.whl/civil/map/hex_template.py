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

from civil.map import terrain


class HexTemplate:
    """
    This class defines a template for a given hex. It contains only static data that actual Hex
    class instances can refer to. This means that a lot of memory is saved by only storing the
    static non-changing data for a hex in one place.

    The data that this class contains is:

    * a set of Terrain instances, one for each triangle
    * a height for each triangle
    * a color that that be used to represent the hex

    The height is not absolute, it is instead a relative height among the triangles in the
    hex, which 0 being baseline height, negative values sunk down and positive values hills etc.
    """

    def __init__(self, id, terrains, heights, color):
        """
        Initializes the hex template and parses passed data.
        """
        # store the id
        self.id = id

        # no terrains, heights now rivers/roads yet
        self.terrains = []
        self.heights = []

        # set color 
        self.color = (int(color[0]), int(color[1]), int(color[2]))

        # parse and store all the data
        self.__setTerrains(terrains)
        self.__setHeights(heights)

    def getId(self):
        """
        Returns the id of the icon.
        """
        return self.id

    def getTerrains(self):
        """
        Returns a list of the terrain data for all the triangles. There is one instance of
        Terrain for each triangle.
        """
        return self.terrains

    def getTerrain(self, triangle):
        """
        Returns the terrain data for a given triangle. Valid values are 0..5.
        """
        return self.terrains[triangle]

    def getColor(self):
        """
        Returns a tuple (red,green,blue) that represents the general color of the icon. This color
        can be used in for instance the minimap.
        """
        return self.color

    def getDeltaHeights(self):
        """
        Returns a list of all the relative heights of the triangles in the hex compared to a
        baseline of 0.
        """
        return self.heights

    def getDeltaHeight(self, triangle):
        """
        Returns the height of a given triangle, 1-6, relative
        to the middle of the hex.
        """
        return self.heights[triangle - 1]

    def __setTerrains(self, terrains):
        """
        Creates a list of Terrain instances based on the 'terrains' list. The parameter list is
        just characters that are used to describe a hex.
        """

        # loop over all the parts
        for code in terrains:
            # get the terrain instance and add it
            self.terrains.append(terrain.terrainDict[code])

    def __setHeights(self, heights):
        """
        Stores the relative heights of each triangle. Each height in the list os given as a
        character in the range 0..9. The height are all offset by 5 so that we have positive values,
        meaning that 5 has to be subtracted before the value is used.
        """
        # loop over all the 
        for height in heights:
            # convert the character to an int and subtract the offset we used
            self.heights.append(int(height) - 5)
