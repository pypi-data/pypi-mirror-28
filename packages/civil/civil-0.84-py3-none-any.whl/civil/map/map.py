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

from math import floor, ceil, pi, atan2

from civil import properties
from civil.model import scenario
from civil.util import geometry


class Map:
    """
    This class defines the basic map of the game. It contains a 2D matrix of the hexes in the game. 

    It also a list of 6 instances of Terrain for each hex. The terrains contains information about
    the terrain type (forest, hill etc), altitude and other modifiers.
    """

    def __init__(self, size_x, size_y):
        """
        Initializes the map and allocates necessary data.
        """
        # store the size
        self.size = (size_x, size_y)

        # initialize the array of hexes
        self.hexes = [None] * size_y
        for index in range(size_y):
            self.hexes[index] = [None] * size_x

        # initialize the array of altitude formulas
        self.tris = [None] * size_y
        for index in range(size_y):
            self.tris[index] = [None] * size_x

        # now loop over the entire matrix and init the alts
        for y in range(size_y):
            for x in range(size_x):
                # create the tuple
                self.tris[y][x] = [(0, 0, 0), (0, 0, 0), (0, 0, 0),
                                   (0, 0, 0), (0, 0, 0), (0, 0, 0)]

        # a dict with all features of the map. we have nothing by default
        self.features = {}

    def getSize(self):
        """
        Returns the size of the map. The result is a tuple (x,y).
        """
        return self.size

    def getsize_x(self):
        """
        Returns the x-size of the map.
        """
        return self.size[0]

    def getsize_y(self):
        """
        Returns the y-size of the map.
        """
        return self.size[1]

    def getHexes(self):
        """
        Returns the 2D matrix of the hexes of the map.
        """
        return self.hexes

    def getHex(self, x, y):
        """
        Convenience method that returns a hex with given coordinates.
        """
        x = int(x)
        y = int(y)
        return self.hexes[y][x]

    def isInside(self, x, y):
        """
        Returns true if x,y coord is inside map.
        """
        return 0 <= x < self.size[0] and 0 <= y < self.size[1]

    def __getNeighbors__(self, hexx, hexy):
        if hexy % 2 == 0:
            return [(hexx, hexy - 1, 1), (hexx + 1, hexy, 2), (hexx, hexy + 1, 4),
                    (hexx - 1, hexy + 1, 8), (hexx - 1, hexy, 16), (hexx - 1, hexy - 1, 32)]
        else:
            return [(hexx + 1, hexy - 1, 1), (hexx + 1, hexy, 2), (hexx + 1, hexy + 1, 4),
                    (hexx, hexy + 1, 8), (hexx - 1, hexy, 16), (hexx, hexy - 1, 32)]

    def getNeighbors(self, hexx, hexy):
        """
        Returns valid neighbors as a list of (x, y, bit) tuples.
        The bit value starts at up-right, going clockwise.
        """
        # I need this implementation in ./src/editor/plugins/creator.py
        neighbors = self.__getNeighbors__(hexx, hexy)
        size = scenario.map.getSize()
        return [(hx, hy, bit) for (hx, hy, bit) in neighbors
                if not (hx >= size[0] or hy >= size[1] or hx < 0 or hy < 0)]

    def hexHeight(self, x, y):
        """
        center altitude of hex x,y - estimate if there is no such hex.
        """
        # really, we should average the real altitudes of adjacent hexes, if any have some,
        # for default, then fall back on using 0.

        altitude = self.getHex(x, y).getHeight()
        return altitude

    def getHexCorners(self, x, y):
        """
        lists the map coordinates of the corners of the hex with hex
        coordinates (x,y), starting at the top and working clockwise.
        """
        px, py = self.hexToPoint([x, y])
        return [[px, py - 27], [px + 24, py - 9], [px + 24, py + 9], [px, py + 27], [px - 24, py + 9],
                [px - 24, py - 9]]

    def getHexAdjacent(self, hexx, hexy):
        """
        lists the hex coordinates adjacent to hex with hex coord x,y, starting
        at upper right and working clockwise.
        """
        if hexy % 2 == 0:
            return [(hexx, hexy - 1), (hexx + 1, hexy), (hexx, hexy + 1),
                    (hexx - 1, hexy + 1), (hexx - 1, hexy), (hexx - 1, hexy - 1)]
        else:
            return [(hexx + 1, hexy - 1), (hexx + 1, hexy), (hexx + 1, hexy + 1),
                    (hexx, hexy + 1), (hexx - 1, hexy), (hexx, hexy - 1)]

    def calculateHexTris(self, x, y):
        """
         given hex coordinates (x,y) , calculate & return a list of the planes which compose
        its triangles (usual order, upper right then clockwise).
        Right now, return coefficients of plane (a,b,c) to save object overhead, not planes.
        """

        adjHex = self.getHexAdjacent(x, y)
        # first, calculate corners list [[x,y,z],[x,y,z]...
        corners = self.getHexCorners(x, y)  # flat.
        for index in range(6):
            # average the 3 adjacent hex heights for each corner height
            height = (self.hexHeight(x, y) + self.hexHeight(adjHex[index][0], adjHex[index][1]) +
                      self.hexHeight(adjHex[(index - 1) % 6][0], adjHex[(index - 1) % 6][1])) / 3.0
            corners[index].append(height)
        center = self.hexToPoint((x, y)) + [self.hexHeight(x, y)]
        tris = []

        # for the center and each pair of adjacent corners, calculate plane that contains them.
        for index in range(6):
            print(center, corners[index], corners[(index + 1) % 6])
            slope = geometry.plane3d(center, corners[index], corners[(index + 1) % 6])
            tris.append(slope.coeffs())
        return tris

    def getHeight(self, pos):
        """
        Returns the height of the map position pos, which is a (x,y) tuple. The position should
        refer to map coordinates, not hex coordinates. Looks up the height in the internal matrix of
        terrains.
        """

        # Find out the triangle the point is in.
        px, py = pos

        # Map the map coordinate to hexes
        hx, hy = self.pointToHex2(pos)

        baseHeight = self.hexHeight(hx, hy)

        # Map hex to map coordinates. Note! we get the _center_ of the hex
        cx, cy = self.hexToPoint((hx, hy))

        coefficient = 3 * pi
        triangle = int(floor(atan2(cx - px, py - cy) * coefficient) % 6)
        # should work.  Or maybe it's exactly backwards... needs testing.
        (a, b, c) = self.tris[hy][hx][triangle]
        return a * px + b * py + c + baseHeight

    def getTerrain(self, pos):
        """
        Returns the terrain for position (x,y) tuple 'pos'. The passed parameter is given in map
        coordinates, *not* hexes.
        """

        # ick.  need a pointToHexTriangle function.  Wasted calculation.

        # map the map coordinate to hexes
        hx, hy = self.pointToHex2(pos)

        # find out the triangle the point is in.
        px, py = pos
        cx, cy = self.hexToPoint((hx, hy))
        coefficient = 3 * pi
        triangle = int(floor(atan2(cx - px, py - cy) * coefficient) % 6)
        # should work.  Or maybe it's exactly backwards... needs testing.

        return self.hexes[int(hy)][int(hx)].getTerrain(triangle)

    def pointToHex2(self, P):
        """
        New method to calculate in what hex point P is.
        """
        xp, yp = P
        # The calculations below are designed for icon at
        # hex coordinates (0,0) to be at gfx coordinates (-24, -12),
        # top-left corner of the icon.
        # Do a trivial translation here otherwise

        # xp -= 0
        # yp -= 0

        # Assume hexagon with two vertical lines and the rest diagonal
        width = properties.hex_delta_x
        height = properties.hex_delta_y

        magic = 12  # For horizontal region calculations

        # Base calculation of what x and y hex this is
        #
        # Yes, the int() is necessary because somebody
        # sends us floats...
        y = int(yp) / height
        x = int(xp) / width
        if y % 2 == 0 and xp % width >= width / 2:
            x += 1

        # Divide icon into three horizontal regions, of which the two first
        # are trivial, we're in a rectangle. Only one region requires
        # special attention, those with diagonal lines.
        if (yp / magic) % 3 != 2:
            # Easy case, we're in the "inside rectangle" of a hex
            # Do nothing, base calculation is correct
            pass
        else:
            # xh value:  0  24  0  
            # \    /\    /\    /   0
            #  \  /  \  /  \  /         yh value
            #   \/    \/    \/     12
            xh = xp % width
            yh = yp % magic
            if xh > width / 2:
                xh = width - xh
            if y % 2 == 0:
                # We're in a /\ group
                # Invert xh
                xh = width / 2 - xh
                # On which side of the hex lines are we?
                if width / 2 * yh > xh * magic:
                    y += 1
                    # We could have done a +1 higher up in base
                    # calculations, which is wrong. So recalculate
                    x = xp / width
            else:
                # We're in a \/ group
                # xh is already correct.
                # On which side of the hex lines are we?
                if width / 2 * yh > xh * magic:
                    y += 1
                    if xp % width > width / 2:
                        x += 1

        # NOTE: We don't require it to be within
        # bounds of the map size, since various
        # routines (like MOUSEMOVE events) need to check
        # for out-of-bounds hexes. Hmm.. perhaps we
        # could throw some kind of an Exception
        return x, y

    def hexToPoint(self, hex):
        """
        Returns a (x,y) tuple that contains the center of the given hex in global coordinates.
        """
        # optimization. avoids dots
        size_hex = properties.hex_size
        delta_x = properties.hex_delta_x
        delta_y = properties.hex_delta_y
        delta_x_half = delta_x / 2

        # explode the hex
        x, y = hex

        # This catches most guys who pass in map coordinates instead of hex coordinates
        assert (self.isInside(x, y))

        # now determine weather we have a odd or even offset and the current row. This is a
        # little bit ugly, but it works. Some artifacts remain on the edges though
        if y % 2 == 0:
            # the icon is painted as far left as possible
            return x * delta_x - delta_x_half, y * delta_y - (size_hex - delta_y)

            # the icon is indented half a hex to the right.
        return x * delta_x, y * delta_y - (size_hex - delta_y)

    def __triangleCrossings(self, p1, p2):
        """
        Returns the list of points where the line from p1 to p2 crosses triangle boundries
         and the points themselves.
         """
        x1, y1 = p1
        x2, y2 = p2
        path = geometry.line2dFromPoints(p1, p2)
        Crossings = [p1, p2]

        # probably not fastest way to do this.
        first = ceil(min((x1 / 24.0), (x2 / 24.0)))
        last = ceil(max((x1 / 24.0), (x2 / 24.0)))
        for index in range(first, last):
            L = geometry.line2d(1, 0, (index * 24))
            Crossings.append(L.intersect(path))
        first = ceil(min(((x1 + 2 * y1) / 48.0), ((x2 + 2 * y2) / 48.0)))
        last = ceil(max(((x1 + 2 * y1) / 48.0), ((x2 + 2 * y2) / 48.0)))
        for index in range(first, last):
            L = geometry.line2d(1, 2, (index * 48))
            Crossings.append(L.intersect(path))
        first = ceil(min(((x1 - 2 * y1) / 48.0), ((x2 - 2 * y2) / 48.0)))
        last = ceil(max(((x1 - 2 * y1) / 48.0), ((x2 - 2 * y2) / 48.0)))
        for index in range(first, last):
            L = geometry.line2d(1, -2, (index * 48))
            Crossings.append(L.intersect(path))

        # NOTE! we can get the triangles in a completely wrong order!
        Crossings.sort()
        if Crossings[0] == p2:
            Crossings.reverse()

        result = [Crossings[0]]
        for i in range(1, len(Crossings)):
            if Crossings[i] != Crossings[i - 1] and Crossings[i] != []:
                result.append(Crossings[i])

        return result

    def getAllFeatures(self):
        """
        Returns all features that have been loaded. If no features exist in the map then an empty
        dictionary is returned. The dict is indexed by the type of feature, such as 'house',
        'trench' etc, and the value for each key is a list of feature tuples. Each tuple contains
        tha data (x, y, id, icon).
        """
        return self.features

    def addFeature(self, type, id, x, y):
        """
        Adds a new feature to the internal dictionary. A feature is something that is blitted on
        top of the normal terrain, and just adds to it. The 'type' is used to organize the data in
        the internal dict. The position defines where the feature is (upper left corner). The id is
        the unique id of the feature's icon.
        """

        # do we already have such features?
        if type not in self.features:
            # nope, add an empty list
            self.features[type] = []

        # now we want to load an icon too if we're a graphical client, ie non-ai
        if scenario.local_player_ai:
            # local player is ai, no icon needed
            icon = None
        else:
            # load the icon
            icon = self.loadFeatureIcon(id)

        # add the data about this feature 
        self.features[type].append((x, y, id, icon))
