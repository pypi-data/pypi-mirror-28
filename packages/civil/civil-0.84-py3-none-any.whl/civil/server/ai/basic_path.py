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

from array import array
from operator import add
from functools import reduce

# make sure you have this add-on library (not in standard lib)
try:
    from pqueue import PQueue
except ImportError:
    from civil.server.ai.pypqueue import PQueue

# from heap import Heap
# PQueue = Heap

# MAP_SHAPE = 'diamond_v' # diamond shaped - stacked vertically
# MAP_SHAPE = 'diamond_h' # diamond shaped - stacked horizontally
MAP_SHAPE = 'rectangle'  # array like layout

# A* distance cost algorithms. Either C or python.
# TODO 
#from civil.server.ai import dc_algorithm

# Civil specific. Get the scenario info (map, units, etc).
from civil.model import scenario


class PathFinder:
    """
    Some documentation here.
    """

    def __init__(self, map=None):
        """
        Initializes the pathfinder. If no 'map' is given then the default
         scenario.map is used instead.
         """
        # did we get a map?
        if map:
            self.map = map
        else:
            # no, so use the default one, assume it's properly set up
            self.map = scenario.map

        self._init_terrain_cost()

    # The static terrain cost makes 2 assumptions; first that the terrain
    # doesn't change, second that units have the same movement costs
    # the cost calculation is oversimplified. but works well for now.
    # 
    # Note: This no longer works as the terrain costs are different for each
    # type of unit. Should there be a terrain map created for each unit type or
    # should these be calculated on the fly. Classic memory/speed trade-off.
    # Though terrain maps don't use much memory, so I'm leading toward multiple
    # maps.

    tc_map = []

    def _init_terrain_cost(self):
        if self.tc_map: return
        size_x, size_y = self.map.size
        getHex = self.map.getHex
        tc_map = self.tc_map

        # temporary hack until units can be handled
        class Unit:  # fake infantry unit
            """

            """
            def __init__(self):
                pass

            def getType(self):
                """

                Returns:

                """
                return 0

        unit = Unit()
        tc_map[:] = [array('f', [0] * size_x) for i in range(size_y)]
        for y in range(size_y):
            for x in range(size_x):
                tc_map[y][x] = reduce(add,
                                      [t.movementSpeedModifier(unit)
                                       for t in getHex(x, y).getTerrains()]) / 6.

    # node = (g_cost,depth,point,parent_node)
    # point is both the x,y coord and the state
    # g_cost is cost so far
    def _new_node(self, p, parent, g_cost):
        if not parent:
            return 0, 0, p, parent
        else:
            return g_cost, parent[1] + 1, p, parent

    # getHexAdjacent() includes hexes off the edge of the map. 
    def _in_bounds(self, xxx_todo_changeme):
        (x, y) = xxx_todo_changeme
        xedge, yedge = self.map.size
        return x > -1 and y > -1 and x < xedge and y < yedge

    def calculatePath(self, start, end, transform=1, _test=0):
        """
        transform - if not 0 then the hex coordinates are transformed into pixel
        coordinates before returned.
        """

        tc_map = self.tc_map
        p = start
        p1 = end
        # uses priority queue 
        node_queue = PQueue()
        # stores all nodes already checked - this assumes the hex will 
        # have the same movement cost no matter how its traversed
        skip_nodes = {}
        # some micro optimizations
        distance_cost = dc_algorithm[MAP_SHAPE]
        getNeighbors = self.map.getNeighbors
        new_node = self._new_node

        # Classic A* does while loop over queue (len test) and uses a break on
        # the location matching test. I found it easier to reverse these 2
        # because of python's handy while: else: syntax
        node = new_node(p, None, 0)
        while node[2] != p1:
            x, y = node[2]
            new_points = [(x, y) for (x, y, b) in getNeighbors(x, y)]
            parent_cost = node[0]
            for pN in new_points:
                if pN in skip_nodes:
                    f, g = skip_nodes[pN]
                else:
                    terrain = tc_map[pN[0]][pN[1]]
                    if terrain == 0.0:
                        terrain = 0.01
                    # h is the heuristic of future cost
                    # assumes an average movement cost of 1
                    h = distance_cost(pN, p1)
                    actual_cost = 1 / terrain
                    # g is the cost so far
                    g = parent_cost + actual_cost
                    f = h + g
                    node_queue.insert(f, new_node(pN, node, g))
                    skip_nodes[pN] = f, g
            if not node_queue:
                path = []
                break
            node_cost, node = node_queue.pop()
        else:
            # what we're here for
            path = []
            hexToPoint = self.map.hexToPoint
            if scenario.playfield:
                debug_layer = scenario.playfield.getLayer("ai_debug")
                debug_layer.labels = {}
            while node:  # get path
                # BUG: debug_layer.values doesn't exist at the moment? --msa
                try:
                    if scenario.playfield: debug_layer.values[node[2]] = 'X'
                except:
                    pass
                if transform:  # should we transform to pixel coordinates?
                    path.append(hexToPoint(node[2]))
                else:  # no transforms
                    path.append(node[2])
                node = node[3]
            path.reverse()

        if _test:
            return path, skip_nodes
        else:
            return path


## pseudo-code for path smoothing. ignore for now.
def simpleSmooth(self, path):
    """

    Args:
        self: 
        path: 
    """
    assert type(path) is list and path, 'Bad arg type: simpleSmooth([list])'
    checkPoint = path[0]
    currentPoint = path[1]
    for i in len(path):
        # TODO traversable unknown
        if traversable(checkPoint, currentPoint):
            del path[1]
            currentPoint = path[1]
        else:
            checkPoint, currentPoint = currentPoint
