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

import random

from civil.model import scenario
from civil.editor import globals
from civil.editor import undostack
from civil.editor.plugins.plugin import Plugin
from civil.map.hex import Hex

# up-right, right, down-right, down-left, left, up-left
# "bitwise or" them together to describe the directions of a piece
UR = 1
R = 2
DR = 4
DL = 8
L = 16
UL = 32


def tuple2bits(val):
    """

    Args:
        val: 

    Returns:

    """
    bit = 1
    index = 0
    ans = 0
    while index < 6:
        if val[index]:
            ans += bit
        bit += bit
        index += 1
    return ans


class Creator(Plugin):
    """
    Generic class for creating "fast terrain", e.g. finding icons
    of rivers etc that match with each other.
    """

    # Keys are three-tuples, values from the domain
    # (terrain, deltaheight, road, river), leave
    # one key away

    init = 0
    set_terrains = {}  # leave terrain away
    set_deltaheights = {}  # leave deltaheight
    set_roads = {}  # leave road
    set_rivers = {}  # leave river

    def __init__(self, iconview, addkind, name, longname):
        Plugin.__init__(self, name, longname)
        self.iconview = iconview
        self.sets = {}
        self.fromset = {}
        self.randgen = random.Random()
        self.addkind = addkind
        if Creator.init == 0:
            Creator.init = 1
            print("Creator.__init__: This line should only appear once")
            self.createAllRegisterSets()

    addkind__forest = 1  # N/A
    addkind__hill = 2  # N/A
    addkind__river = 3
    addkind__path = 4
    addkind__sea = 5  # N/A
    addkind__sand = 6  # N/A
    addkind__rubble = 7  # N/A

    mustfix = [0, 1, 0, 0, 0, 1, 1, 1]

    def createAllRegisterSets(self):
        """

        """
        print("createAllRegisterSets...")
        imax = max(globals.icons.keys()) + 1

        # Creates Hex.templates
        Hex(1)

        for id in range(1, imax):
            if globals.icons.isInvalid(id):
                continue

            hextemplate = Hex.templates[id]

            terrains = hextemplate.getTerrains()
            deltaheights = hextemplate.getDeltaHeights()
            roads = hextemplate.getRoads()
            rivers = hextemplate.getRivers()

            # Change this to 7 when needed
            assert (len(terrains) == 6)
            terrains = (terrains[0], terrains[1], terrains[2], terrains[3], terrains[4], terrains[5])
            deltaheights = (
                deltaheights[0], deltaheights[1], deltaheights[2], deltaheights[3], deltaheights[4], deltaheights[5])
            roads = (roads[0], roads[1], roads[2], roads[3], roads[4], roads[5])
            rivers = (rivers[0], rivers[1], rivers[2], rivers[3], rivers[4], rivers[5])

            ter_key = (deltaheights, roads, rivers)
            dh_key = (terrains, roads, rivers)
            road_key = (terrains, deltaheights, rivers)
            river_key = (terrains, deltaheights, roads)

            if ter_key not in Creator.set_terrains:
                Creator.set_terrains[ter_key] = {}

            if dh_key not in Creator.set_deltaheights:
                Creator.set_deltaheights[dh_key] = {}

            if road_key not in Creator.set_roads:
                Creator.set_roads[road_key] = {}

            if river_key not in Creator.set_rivers:
                Creator.set_rivers[river_key] = {}

            assert (id not in Creator.set_terrains[ter_key])
            assert (id not in Creator.set_deltaheights[dh_key])
            assert (id not in Creator.set_roads[road_key])
            assert (id not in Creator.set_rivers[river_key])

            Creator.set_terrains[ter_key][id] = terrains
            Creator.set_deltaheights[dh_key][id] = deltaheights
            Creator.set_roads[road_key][id] = tuple2bits(roads)
            Creator.set_rivers[river_key][id] = tuple2bits(rivers)

        print("...done")

    def __getSetAndTuple__(self, id):
        # copy-pasted...

        hextemplate = Hex.templates[id]

        terrains = hextemplate.getTerrains()
        deltaheights = hextemplate.getDeltaHeights()
        roads = hextemplate.getRoads()
        rivers = hextemplate.getRivers()

        terrains = (terrains[0], terrains[1], terrains[2], terrains[3], terrains[4], terrains[5])
        deltaheights = (
            deltaheights[0], deltaheights[1], deltaheights[2], deltaheights[3], deltaheights[4], deltaheights[5])
        roads = (roads[0], roads[1], roads[2], roads[3], roads[4], roads[5])
        rivers = (rivers[0], rivers[1], rivers[2], rivers[3], rivers[4], rivers[5])

        tup = None
        set = None

        if self.addkind == Creator.addkind__path:
            tup = (terrains, deltaheights, rivers)
            set = Creator.set_roads[tup]
        elif self.addkind == Creator.addkind__river:
            tup = (terrains, deltaheights, roads)
            set = Creator.set_rivers[tup]
        elif self.addkind == Creator.addkind__forest:
            tup = (deltaheights, roads, rivers)
            set = Creator.set_terrains[tup]
        elif self.addkind == Creator.addkind__hill:
            # doesn't work
            tup = (terrains, roads, rivers)
            set = Creator.set_deltaheights[tup]

        assert set
        assert tup

        return set, tup

    def getNeighborsInSet(self, neighbors):
        """

        Args:
            neighbors: 

        Returns:

        """
        ret = []
        for (x, y, b) in neighbors:
            terrain = scenario.map.getHexes()[y][x]
            terrain_id = terrain.getIconId()

            (set, tup) = self.__getSetAndTuple__(terrain_id)

            if terrain_id in list(set.keys()):
                if not Creator.mustfix[self.addkind] and self.isEmpty(set, terrain_id):
                    # "empty" square, nothing to see here...
                    continue
                found = (set, terrain_id)
                ret.append((x, y, b, found))

        return ret

    def isEmpty(self, id):
        """
        Returns true if the given id is "empty" of specific
        features (forest, road etc.), depending on which subclass we have
        """
        assert 0

    def getSetOf(self, id):
        """
        Get which set this id belongs to.
        """
        (set, tup) = self.__getSetAndTuple__(id)

        if id in list(set.keys()):
            return set

        # Check the fromsets.
        # for s in self.fromset.keys():
        #    if id in self.fromset[s]:
        #        return self.sets[s]

        print("AAARGH Couldn't find proper set for %d" % id)
        return None

    def chooseCandidate(self, need, candidates_list):
        """
        Chooses from the list of (bits, id) a proper candidate, depending
        on need. It favors exact matches => prettier results.
        """

        # This part is only needed for exact matching
        exact = []
        for (candidate_need, candidate_id) in candidates_list:
            if candidate_need == need:
                exact.append((candidate_need, candidate_id))
        if len(exact) > 0:
            candidates_list = exact

        # The non-favoring solution is easy:
        candidates = [x[1] for x in candidates_list]
        return candidates[self.randgen.randrange(0, len(candidates))]

    def mapClickedLeft(self, pixelx, pixely, hexx, hexy):
        """
        Creates the terrain, according to neighbors.
        """
        """
        Inner working:
        1. Create list of neighbors
        2. Discard those that don't belong to the magic sets...
        3. For each neighbor,
        3.1 Check if we can add a connection from us to the neighbor
        3.1.1 Meaning create all the valid connections of the neighbor,
              and check if we can add this connection and still find
              a new icon matching at least those requirements from the
              same set.
        3.2 If not, discard the neighbor
        4. Find the icons that satisfy at least the requirements,
           from the same set as it was in.
        6. Change neighbors to satisfy the new link
        7. Always return something(?)
        """

        n1 = scenario.map.getNeighbors(hexx, hexy)

        n2 = self.getNeighborsInSet(n1)

        new_icon_need = self.get_empty_need()
        new_neighbors = []
        for (x, y, b, terrain) in n2:
            # The neighbors of the neighbors of the original hex...
            neigh1 = scenario.map.getNeighbors(x, y)
            neigh2 = self.getNeighborsInSet(neigh1)

            need = self.calcNeed(x, y, neigh2, b)

            print("Need %d,%d,%d,%s" % (x, y, b, str(need)))

            # Do we have a new neighbor
            fixes = []
            for id in list(terrain[0].keys()):
                if self.match(terrain[0][id], need):
                    # Yes, so we can add this connection
                    new_icon_need |= b
                    # print "New Need %d" % new_icon_need
                    fixes.append((terrain[0][id], id))
            if fixes:
                new_neighbors.append((x, y, b, terrain[1], need, fixes))

            print("New Icon Need", new_icon_need)

        # Good, so now let's find a suitable icon
        # BUG should take background into consideration
        terrain = scenario.map.getHexes()[hexy][hexx]
        terrain_id = terrain.getIconId()
        myset = self.getSetOf(terrain_id)
        while 1:
            candidates = []
            for id in list(myset.keys()):
                if myset[id] and self.match(myset[id], new_icon_need):
                    candidates.append((myset[id], id))

            if candidates:
                break
            # Zero out a bit, so we have a lesser requirement
            # BUG: Theoretically this could spin on forever...
            bit = self.randgen.randrange(0, 6)
            bit = 1 << bit
            new_icon_need &= ~bit
            # Remove the appropriate neighbor
            nn = []
            for (x, y, b, id, neigh_need, neigh_candidates) in new_neighbors:
                if b == bit:
                    continue
                nn.append((x, y, b, id, neigh_need, neigh_candidates))
            new_neighbors = nn

            # No suitable icon? => Completely away, don't change anything
            if new_icon_need == 0:
                return

        # Create undo list
        undo = [(hexx, hexy)]
        for (x, y, b, id, neigh_need, neigh_candidates) in new_neighbors:
            if id in neigh_candidates:
                # Skip this, no need to change to another icon that
                # has the exact same connections
                continue
            undo.append((x, y))
        undostack.addUndoList(undo)

        # Paste new icon
        candidate = self.chooseCandidate(new_icon_need, candidates)
        self.iconview.pasteNoUndo(candidate, hexx, hexy)

        # Fix the neighbors
        for (x, y, b, id, neigh_need, neigh_candidates) in new_neighbors:
            if id in neigh_candidates:
                # Skip this, no need to change to another icon that
                # has the exact same connections
                continue
            candidate = self.chooseCandidate(neigh_need, neigh_candidates)
            self.iconview.pasteNoUndo(candidate, x, y)

    def get_empty_need(self):
        """

        Returns:

        """
        return 0

    def calcNeed(self, n_x, n_y, neighbors, bit_from_our_hex):
        """
        Calculate the need of a neighbor square, depending on its
        neighbors.
        """
        need = 0
        for (xn, yn, bn, tn_id) in neighbors:
            # Reverse of our current direction
            rev = bn << 3
            if rev > UL: rev = bn >> 3
            if tn_id[0][tn_id[1]] & rev:
                need |= bn

        # Add connection to our primary hex
        rev = bit_from_our_hex << 3
        if rev > UL: rev = bit_from_our_hex >> 3
        return need | rev

    def match(self, from_set, our_need):
        """

        Args:
            from_set: 
            our_need: 

        Returns:

        """
        return from_set & our_need == our_need
