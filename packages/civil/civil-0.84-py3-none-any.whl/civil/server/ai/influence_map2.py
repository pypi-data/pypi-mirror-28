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
# John Eikenberry <jae@zhar.net>
"""

# TODO this does not work anymore, is it needed (would probably use NumPy now)
SIX = array(6.).astype(Float32)
EDGE_MOD = array(0.66).astype(Float32)
ONE = array(1.).astype(Float32)
ZERO = array(0.).astype(Float32)
FACTOR = (ONE / SIX)


class InfluenceMap:
    """
    There are 2 primary ways to setup the influence map, either might be useful
    depending on your needs. The first is to recreate the map each 'turn' the
    second is to keep the map around and just update it each turn. The first
    way is simple and easy to understand, both in terms of tweaking and later
    analysis. The second gives the map a sense of time and allows for fewer
    iterations of the spreading algorithm per 'turn'. 

    Setting up the map to for one or the other of these is a matter of tweaking
    the code. There are 3 main bits of code which are described below and
    indicated via comments in the code.
    
    First some terminology:

    - weight_map stores the current influence map
    - neighbors is used as the memory buffer to calculate a the influence
      spreading
    - const_map contains a map with only the unit's scores present
    - when I refer to a 'multi-turn map' I mean using one instance of the
      influence map throughout the game without resetting it.

    [1] neighbors *= ZERO

        At the end of each iteraction, the neighbors take on the values of the
        weight_map from the previous step. This will reset those values to
        zero.

        This has a 1% performance hit.

    [2] putmask(neighbors,const_map,const_map)

        This keeps the values of the units hexes constant through all
        iterations.

        This results in about a 40% performance hit. This needs improvement.

    [3] setDecayRate([float])
        
        This is meant to be used with a multi-turn map. It sets the floating
        point value (N>0.0<1.0)which is used on the map each turn to modify
        the current map before the influence spreading. 

        No performance hit.

    If just [1] used then it will cause all influence values to decend
    toward zero. Not sure what this would be useful for, just documenting the
    effect.

    If [1] is not used (commented out) then the map values will never balance
    out, rising with each iteration. This is fine if you plan on resetting the
    influence map each turn. Allowing you to tweak the number of iterations to
    get the level of values you want. But it would cause problem with a
    multi-turn map unless [3] is used to keep this in check. 
        
    Using [2] without [1] will accellerate the rising of the values described
    above. It will also lead to more variation amoung the influence values
    when using fewer iterations. High peaks and steep sides. Using neither [1]
    nor [2] the peaks are much lower.

    If [1] and [2] are both used the map will always attain a point of balance
    no matter how many iterations are run. This is desirable for maps used
    throughout the entire game (multi-turn maps) for obvious reasons. Given the
    effect of [1] this also limits the need for [3] as the influence values in
    areas of the map where units are no longer present will naturally decrease.
    Though the decay rate may still be useful for tweaking this.
    

    """

    _decay_rate = None

    def __init__(self, hex_map):
        """
         hex_map is the in game (civl) map object
         """
        self.map_size = map_size = hex_map.size
        ave_size = (map_size[0] + map_size[1]) / 2
        self._iterations = ave_size / 2
        # is the hex_map useful for anything other than size?
        self.hex_map = hex_map

        # const_map == initial unit locations
        self.const_map = zeros((map_size[1], map_size[0]), Float32)
        # weight_map == influence map
        # start it off blank
        self.reset()

    def setUnitMap(self, units):
        """
         Put unit scores on map
            -units is a list of (x,y,score) tuples
             where x,y are map coordinates and score is the units influence
             modifier
        """
        weight_map = self.weight_map
        const_map = self.const_map
        const_map *= ZERO
        # maybe use the hex_map here to get terrain effects?
        for (x, y, score) in units:
            weight_map[y, x] = score
            const_map[y, x] = score

    def setInterations(self, iterations):
        """
         Set number of times through the influence spreading loop
         """
        assert type(iterations) == IntType, "Bad arg type: setIterations([int])"
        self._iterations = iterations

    # [3] above
    def setDecayRate(self, rate):
        """
         Set decay rate for a multi-turn map.
         """
        assert type(rate) == FloatType, "Bad arg type: setDecayRate([float])"
        self._decay_rate = array(rate).astype(Float32)

    def reset(self):
        """
         Reset an existing map back to zeros
         """
        map_size = self.map_size
        self.weight_map = zeros((map_size[1], map_size[0]), Float32)

    def step(self, iterations=None):
        """
         One set of loops through influence spreading algorithm
         """
        # save lookup time
        const_map = self.const_map
        weight_map = self.weight_map
        if not iterations:
            iterations = self._iterations

        # decay rate can be used when the map is kept over duration of game,
        # instead of a new one each turn. the old values are retained,
        # degrading slowly over time. this allows for fewer iterations per turn
        # and gives sense of time to the map. its experimental at this point.
        if self._decay_rate:
            weight_map = weight_map * self._decay_rate

        # working memory for map shifting sums
        neighbors = weight_map.copy()
        # tried pre-allocating this memory, but it didn't seem to help any.

        # spread the influence
        while iterations:
            # [1] in notes above
            #            neighbors *= ZERO
            # diamond_hex layout
            neighbors[:-1, :] += weight_map[1:, :]  # shift up
            neighbors[1:, :] += weight_map[:-1, :]  # shift down
            neighbors[:, :-1] += weight_map[:, 1:]  # shift left
            neighbors[:, 1:] += weight_map[:, :-1]  # shift right
            neighbors[1::2][:-1, :-1] += weight_map[::2][1:, 1:]  # hex up (even)
            neighbors[1::2][:, :-1] += weight_map[::2][:, 1:]  # hex down (even)
            neighbors[::2][:, 1:] += weight_map[1::2][:, :-1]  # hex up (odd)
            neighbors[::2][1:, 1:] += weight_map[1::2][:-1, :-1]  # hex down (odd)
            # keep influence values balanced
            neighbors *= FACTOR

            # [2] above - maintain scores in unit hexes
            # putmask(neighbors,const_map,const_map)
            # using 'where' instead of 'putmask' cuts the number of function
            # calls in half and shaves about 10% off the processing time
            #            neighbors = where(const_map,const_map,neighbors)

            # prepare for next iteration
            weight_map, neighbors = neighbors, weight_map
            iterations -= 1

        # save for next turn
        self.weight_map = weight_map
