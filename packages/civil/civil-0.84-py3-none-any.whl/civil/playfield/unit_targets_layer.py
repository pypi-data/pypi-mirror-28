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


class UnitTargetsLayer(Layer):
    """
    This class defines a layer that can visualize the attack targets all friendly units have. The
    serious forms of attack are shown with different colored lines from the attacker to the target.

    The attack modes are:

    o skirmish
    o attack
    o assault
    
    Only the atack orders of friendly units are show.
    """

    def __init__(self, name):
        """
        Initializes the layer.
        """
        # call superclass constructor
        Layer.__init__(self, name)

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

        # get the id of the own units
        local_player = scenario.local_player_id

        # loop over all units in the map
        for unit in scenario.info.units.values():
            # is the unit our and has it got a target?
            if unit.getOwner() == local_player and unit.getTarget() is not None:
                # yep, handle the target for the unit
                self.visualizeUnitTargets(unit)

    def visualizeUnitTargets(self, unit, ):
        """
        Visualizes the target for 'unit'. The unit is assumed to be a local unit owned by the


 """

        # get the position, attack mode of the unit
        ourpos = unit.getPosition()
        # mode = unit.getAttackMode ()
        mode = 0
        # print "UnitTargetsLayer.visualizeUnitTargets: using hardcoded attack mode"

        # get target position. we just assume the unit is found in the map
        targetpos = unit.getTarget().getPosition()

        # translate both our and the target's position so that they are within the playfield
        ourpos = (ourpos[0] - self.min_x, ourpos[1] - self.min_y)
        targetpos = (targetpos[0] - self.min_x, targetpos[1] - self.min_y)

        # draw a line from the source to the destination
        scenario.sdl.drawLine(properties.layer_targets_mode_color[mode], ourpos, targetpos)
