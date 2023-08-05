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

from civil import properties
from civil.model import scenario
from civil.playfield.layer import Layer


class WeaponRangeLayer(Layer):
    """
    This class defines a layer that can visualize the maximum attack range for the primary weapon
    for the unit. The range is visualized as a circle centered around the unit.
    
    Only the attack range of friendly units are show.
    """

    def __init__(self, name):
        """
        Initializes the layer.
        """
        # call superclass constructor
        Layer.__init__(self, name)

        # get the color and width of the circle
        self.color = properties.layer_weapon_range_color
        self.weaponwidth = properties.layer_weapon_range_width

    def paint(self, offset_x, offset_y, dirtyrect=None):
        """
        Paints the layer. Loops over all selected friendly units and paints the range circles.
        """

        # get the tuple with the visible sizes (in hexes)
        visible_x, visible_y = scenario.playfield.getVisibleSize()

        # precalculate the min and max possible x and y values
        self.min_x = offset_x * self.delta_x
        self.min_y = offset_y * self.delta_y
        self.max_x = (offset_x + visible_x) * self.delta_x
        self.max_y = (offset_y + visible_y) * self.delta_y

        # get the id of the own units
        local_player = scenario.local_player_id

        # loop over all selected units 
        for unit in scenario.selected:
            # is the unit our and has it got a target?
            if unit.getOwner() == local_player:
                # yep, handle the target for the unit
                self.visualizeUnitRange(unit)

    def visualizeUnitRange(self, unit):
        """
        Visualizes the range of the weapon for 'unit'. The visualization is done using a circle
        """

        # get the position, attack mode of the unit
        pos = unit.getPosition()

        # the range of the primary weapon
        rng = unit.getWeapon().getRange()

        # translate our position so that it is within the playfield
        pos = (pos[0] - self.min_x, pos[1] - self.min_y)

        # draw a circle centered at the unit
        scenario.sdl.drawCircle(self.color, pos, rng, self.weaponwidth)
