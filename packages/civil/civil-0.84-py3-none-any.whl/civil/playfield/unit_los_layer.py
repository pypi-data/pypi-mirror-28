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

import math
import time

from civil.model import scenario
from civil.playfield.layer import Layer

# TODO here was import of ccivil


class UnitLosLayer(Layer):
    """
    This class defines a layer that can visualize the LOS of a friendly unit. The los is traced all
    around the unit and an outline is drawn.
    """

    def __init__(self, name):
        """
        Initializes the layer.
        """
        # call superclass constructor
        Layer.__init__(self, name)

        # Cache line of sight calculations
        # A map "unit id => (xpos, ypos, lines)"
        # Automatically being kept up-to-date
        self.los_cache = {}

        # register ourselves to receive 'unitselected' signals
        scenario.dispatcher.registerCallback('units_changed', self.unitsChanged)

    def unitsChanged(self, parameters):
        """
        Signal callback triggered when a unit has been selected or deselected. Forces a repaint
        of the playfield.
        """
        scenario.playfield.needRepaint()

    def paint(self, offset_x, offset_y, dirtyrect=None):
        """
        Paints the layer. Loops over all available friendly units and paints their orders. The
        offsets are used so that we know how  much the map has been scrolled.
        """

        # get the tuple with the visible sizes (in hexes)
        visible_x, visible_y = scenario.playfield.getVisibleSize()

        # precalculate the min and max possible x and y values
        self.min_x = offset_x * self.delta_x
        self.min_y = offset_y * self.delta_y
        self.max_x = (offset_x + visible_x) * self.delta_x
        self.max_y = (offset_y + visible_y) * self.delta_y

        # skip our primary selection for now
        if scenario.selected:
            primary = scenario.selected[0]
        else:
            # no selected unit, we're done
            return

        # is the selected primary unit a friendly unit?
        if primary.getOwner() == scenario.local_player_id:
            # yep, visualize its los
            # self.__visualizeLOS (primary)
            self.__visualizeLOSarea(primary)

    def __visualizeLOS(self, unit):
        """
        Visualizes the unit's Line-Of-Sight, using 360 rays cast into all directions.
        """
        iter = 0
        max_iter = 360
        one_angle_unit = 2.0 * math.pi / float(max_iter)

        lines = []

        u_x, u_y = unit.getPosition()
        if unit.id in self.los_cache:
            c_x, c_y, c_lines = self.los_cache[unit.id]
            if c_x == u_x and c_y == u_y:
                self.__drawLOS(c_lines)
                return

            del self.los_cache[unit.id]

        while iter < max_iter:
            angle = one_angle_unit * iter
            iter += 1
            high = unit.sightRange + 1
            low = 1
            while high - low > 1:
                sight = (high + low) / 2
                dx = math.cos(angle) * sight
                dy = math.sin(angle) * sight
                try:
                    # use newer los method
                    visibility = scenario.map.checkLos((u_x, u_y), (u_x + dx, u_y + dy))

                except:
                    # An error occurred => we are outside the map or
                    # some other error => assume we can't see
                    visibility = 0

                # Binary search

                if visibility == 0:
                    high = sight
                    # or rather, losValue should support this

                else:
                    low = sight

            lines.append((int(u_x + dx), int(u_y + dy)))

        lines.append(lines[0])
        self.los_cache[unit.id] = (u_x, u_y, lines)
        self.__drawLOS(lines)

    def __drawLOS(self, lines):
        """
        Draws the actual los lines.
        """
        for i in range(len(lines) - 1):
            scenario.sdl.drawLine((0, 255, 255),
                                  (lines[i][0] - self.min_x, lines[i][1] - self.min_y),
                                  (lines[i + 1][0] - self.min_x, lines[i + 1][1] - self.min_y))

    def __visualizeLOSarea(self, unit):
        """
         """
        t = time.time()
        # TODO this will fail because we do not compile the c code
        l = map.los.ccivil.getlosarea(unit.getPosition())
        t1 = time.time()
        # print "getLOSarea: ", t1-t
        t = t1
        for (x1, y1, x2, y2) in l:
            scenario.sdl.drawLine((0, 255, 255), (x1 - self.min_x, y1 - self.min_y),
                                  (x2 - self.min_x, y2 - self.min_y))
        t1 = time.time()
        # print "draw lines: ", t1-t
