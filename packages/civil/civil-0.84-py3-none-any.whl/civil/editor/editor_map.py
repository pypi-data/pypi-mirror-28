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

from civil.model import scenario
from civil.map.map_displayable import MapDisplayable


class MapHeightException(Exception):
    """
    Simple class for keeping x,y pairs of map height errors. This is used only within the editor,
    so it is defined here and not in the regular map classes.
    """

    def __init__(self, pairs):
        self.value = pairs
        Exception.__init__(self)


class EditorMap(MapDisplayable):
    """
    This class defines a map as needed by the scenario editor. It inherits a normal displayable map
    and just provides some extra functionality needed by the editor, such as:

    * height calculation.
    """

    def __init__(self, size_x, size_y):
        """
        Initializes the map and allocates necessary data.
        """
        MapDisplayable.__init__(self, size_x, size_y)

    def calculateAbsoluteHeights(self):
        """
        This method will loop over all hexes and calculate an overall height for all the
        triangles of all hexes. When loaded the heights are all 0. This method starts from one
        corner of the map and propagates the height to neighbours to get an overall and absolute
        height. When the heights are calculated an offset is added so that the lowest point on the
        map has the height 0.

        This should be called after all hexes have been set.
        """
        print("EditorMap.calculateAbsoluteHeights")

        height = 0
        lowest_height = 0

        # list of (x,y) pairs of map height errors
        # this way we can throw all errors at the same time
        map_errors = []

        for y in range(self.size[1]):
            for x in range(self.size[0]):
                curhex = self.getHex(x, y)
                curhex.setHeight(height)

                # update lowest height
                lowest_height = min(lowest_height, height)

                # Calculate height for next hex
                if x == self.size[0] - 1:
                    if y == self.size[1] - 1:
                        # last hex
                        break
                    # right edge
                    # Skip to next row
                    height = self.__calcHeight__(0, y + 1, 1, [])[1]
                else:
                    heights = []

                    h1 = self.__calcHeight__(x + 1, y, 1, map_errors)
                    h2 = self.__calcHeight__(x + 1, y, 6, map_errors)
                    h3 = self.__calcHeight__(x + 1, y, 5, map_errors)
                    if h1 and h1[0]:
                        heights.append(h1[1])
                    if h2 and h2[0]:
                        heights.append(h2[1])
                    if h3 and h3[0]:
                        heights.append(h3[1])

                    if len(heights) == 0:
                        # Everything bad, we can just take one of them
                        if h1:
                            height = h1[1]
                        elif h2:
                            height = h2[1]
                        elif h2:
                            height = h3[1]
                        map_errors.append((x + 1, y))
                    else:
                        best_index = 0
                        best_times = -1
                        for i in range(len(heights)):
                            times = heights.count(heights[i])
                            if times > best_times:
                                best_index = i
                                best_times = times
                        height = heights[best_index]
                        if best_times != len(heights):
                            map_errors.append((x + 1, y))

        if map_errors:
            print("Map height errors found.")
            print(map_errors)
            raise MapHeightException(map_errors)

        else:
            print("No map errors found.")

        # Update heights so lowest height on map is zero.
        for y in range(self.size[1]):
            for x in range(self.size[0]):
                curhex = self.getHex(x, y)
                h = curhex.getHeight()
                h -= lowest_height

                # Each height unit is 20 meters
                curhex.setHeight(h * 20)

    def __calcHeight__(self, hexx, hexy, dir, errorlist):
        """
        Calculate what height we should have at (hexx,hexy),
        depending on the hex in direction dir.
        """

        thehex = self.__getNeighbors__(hexx, hexy)[dir - 1]
        size = scenario.map.getSize()
        if thehex[0] < 0 or thehex[0] >= size[0] or thehex[1] < 0 or thehex[1] >= size[1]:
            return None
        checkhex = self.getHex(thehex[0], thehex[1])
        checkheight = checkhex.getHeight()
        oppositedir = (3 + dir - 1) % 6 + 1
        checkheight += checkhex.template.getDeltaHeight(oppositedir)
        # And add the negative delta height of the next hex
        checkheight -= self.getHex(hexx, hexy).template.getDeltaHeight(dir)

        if (thehex[0], thehex[1]) in errorlist:
            return 0, checkheight

        return 1, checkheight
