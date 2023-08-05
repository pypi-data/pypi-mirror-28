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
from civil.model.organization import Battalion, Regiment
from civil.model.unit import Headquarter
from civil.playfield.layer import Layer


class CommandersLayer(Layer):
    """
    This class defines a layer that can visualize the superior commanders of selected units. This
    works by painting a line from the company to its suerior and then lines from that superior to
    its superior and so on.
    
    Only the orders of friendly units are show.
    """

    def __init__(self, name):
        """
        Initializes the layer.
        """
        # call superclass constructor
        Layer.__init__(self, name)

    def paint(self, offset_x, offset_y, dirtyrect=None):
        """
        Paints the layer. Loops over all available friendly units and paints their commanders. The
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

        # loop over all selected units
        for unit in scenario.selected:
            # is the unit visible
            if unit.getOwner() != local_player:
                # not our unit, get next
                continue

            # visualize the commanders for the unit
            self.visualizeCommanders(unit)

            # visualize the subordinates for the unit
            self.visualizeUnits(unit)

    def visualizeCommanders(self, unit):
        """
        Visualizes all commanders for 'unit' by painting lines from the unit to it superior and
        from that superior to its superior etc.
        """

        # get the superiors and position for the unit
        superiors = unit.getSuperiors()
        currentpos = unit.getPosition()

        # loop over all superiors
        for hq in superiors:
            # is the hq destroyed?
            if hq.isDestroyed():
                # hq is dead, next
                continue

            # get the unit's position
            pos = hq.getPosition()

            # precaution to avoid unnecessary painting
            if currentpos != pos:
                # translate both source and dest so that they are within the playfield
                source = (currentpos[0] - self.min_x, currentpos[1] - self.min_y)
                dest = (pos[0] - self.min_x, pos[1] - self.min_y)

                # draw a line from the source to the destination
                scenario.sdl.drawLine((128, 255, 128), source, dest)

                # store new source position
                currentpos = pos

    def visualizeUnits(self, unit):
        """
        Visualizes all companies that belong to a certain unit. This is only done for regiments
        and battalions that may have companies directly under their command. For brigades and
        higher organizations this is never done. So if a unit has the commander for a regiment or
        battalion, and there are companies directly under that commander (regiments may have only
        battalions under them) then lines are painted from 'unit' to the companies.

        Companies that are reinforcements are not visualized, as they are not on the battlefield
        yet. 
        """

        # are we a headquarter?
        if not isinstance(unit, Headquarter):
            # not a headquarter, so we have nu subordinate units
            return

        # get the units this unit is headquarter for
        organization = unit.getHeadquarterFor()

        # yes, it's a headquarter, but is it a hq for a regiment or battalion?
        if not isinstance(organization, Battalion) and not isinstance(organization, Regiment):
            # no hq for anything we know
            return

        # does it have any companies?
        companies = organization.getCompanies()
        if len(companies) == 0:
            # no companies, so it's a regiment with battalions or all units are eliminated
            # print "CommandersLayer.visualizeUnits:  unit %d has no subunits" % unit.getId ()
            return

        # get the unit'sposition
        hqx, hqy = unit.getPosition()

        # loop over all companies
        for company in companies:
            # is the company still alive and has it arrived on the battle field?
            if company.isDestroyed() or company.getId() in scenario.info.reinforcements:
                # yes, it's a goner or reinforcement, then we shouldn't visualize it
                continue

            # get unit position
            unitx, unity = company.getPosition()

            # translate both source and dest so that they are within the playfield
            source = (unitx - self.min_x, unity - self.min_y)
            dest = (hqx - self.min_x, hqy - self.min_y)

            # draw a line from the source to the destination
            scenario.sdl.drawLine((0, 128, 255), source, dest)
