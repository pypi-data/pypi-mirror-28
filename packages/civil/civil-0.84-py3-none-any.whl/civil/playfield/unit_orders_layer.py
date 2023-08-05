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

import sys

import pygame
import pygame.image
from pygame.locals import *

from civil import properties
from civil.model import scenario
from civil.playfield.layer import Layer


class UnitOrdersLayer(Layer):
    """
    This class defines a layer that can visualize the orders of the friendly units on the map. The
    player can then easily see what a unit will do the next turns. The following orders are
    visualized:

    o movement orders (normal, fast)
    o retreat orders
    o rotations
    o attack orders

    Only the orders of friendly units are show.
    """

    def __init__(self, name):
        """
        Initializes the layer.
        """
        # call superclass constructor
        Layer.__init__(self, name)

        try:
            # load the icons for the waypoint
            self.waypoint = pygame.image.load(properties.layer_unit_orders_waypoint).convert()
            self.waypoint_mainsel = pygame.image.load(properties.layer_unit_orders_waypoint_main).convert()

            # set the transparent color for the icons
            self.waypoint.set_colorkey((255, 255, 255), RLEACCEL)
            self.waypoint_mainsel.set_colorkey((255, 255, 255), RLEACCEL)

            # get the width and height of the waypoint
            width, height = self.waypoint.get_size()

            # get deltas that are used to make sure the waypoint is centered when blitted
            self.waypoint_delta_x = width / 2
            self.waypoint_delta_y = height / 2

        except:
            # failed to load icons
            print("UnitOrdersLayer: failed to load icon for waypoints, exiting.")
            sys.exit(1)

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

        # get the id of the own units
        local_player = scenario.local_player_id

        primary = None
        # skip our primary selection for now
        if scenario.selected:
            primary = scenario.selected[0]

        # loop over all units in the map
        for unit in scenario.info.units.values():
            # is the unit visible
            if unit.getOwner() != local_player:
                # not our unit, get next
                continue

            # Skip primary selection for now
            if unit == primary:
                continue

            # handle the plans for the unit
            self.visualizeUnitOrders(unit)

        # put primary selection's orders on top
        if primary and primary.getOwner() == local_player:
            self.visualizeUnitOrders(primary)

    def visualizeUnitOrders(self, unit):
        """
        Visualizes all plans for 'unit'. The unit is assumed to be a local unit owned by the
        local player. All plans for the unit that can be visualized are visualized. The plans are
        painted sequentially with the 'nearest' plan (the one that will be executed first)
        visualized first. Every other visualized plan will start from the position the last
        visualization returned.
        """

        # Kludge: store this here since paintWaypoint needs it
        self.cur_unit = unit

        # get the commands of the unit
        plans = unit.getPlans()
        startpos = unit.getPosition()

        # Collect all waypoints to be blitted here
        self.waypoints = []

        # loop over all plans
        for plan in plans:
            # can the plan be visualized on the playfield?
            if not plan.showOnPlayfield():
                # no, get next
                continue

            # get the name of the plan
            name = plan.getName()

            #
            # Do it once here, almost everybody needs this anyway
            #
            # translate both source and dest so that they are within the playfield
            s = (startpos[0] - self.min_x, startpos[1] - self.min_y)
            t = None
            tpos = None
            if "target_x" in plan.__dict__:
                t = (plan.target_x - self.min_x, plan.target_y - self.min_y)
                tpos = (plan.target_x, plan.target_y)

            # what do we have here?
            if name == 'move':
                # paint a 'move' plan
                startpos = self.__paintMove(startpos, s, tpos, t)

            elif name == 'movefast':
                # paint a 'move fast' plan
                startpos = self.__paintMoveFast(startpos, s, tpos, t)

            elif name == 'rotate':
                # paint a 'rotate' plan
                startpos = self.__paintRotate(startpos, s, tpos, t)

            elif name == 'retreat':
                # paint a 'retreat' plan
                startpos = self.__paintRetreat(startpos, s, tpos, t)

            elif name == 'changemode':
                # paint a 'changemode' plan
                startpos = self.__paintChangeMode(startpos)

            elif name == 'wait':
                # paint a 'changemode' plan
                startpos = self.__paintWait(startpos)

            elif name == 'skirmish':
                # paint a 'skirmish' plan
                startpos = self.__paintSkirmish(startpos, s, plan.getTargetId())

            elif name == 'assault':
                # paint a 'assault' plan
                startpos = self.__paintAssault(startpos, s, plan.getTargetId())

            else:
                # unknown plan
                print("UnitOrdersLayer.visualizeUnitOrders: unknown plan:", name)

        self.__paintAllUnitWayPoints()

    def __paintMove(self, source, source_on_map, dest, dest_on_map):
        """
        """

        # draw a line from the source to the destination
        scenario.sdl.drawLine(properties.layer_unit_orders_move, source_on_map, dest_on_map)

        # paint a waypoint at the position
        self.__paintWaypoint(dest)

        # return the new starting position for the next plan
        return dest

    def __paintMoveFast(self, source, source_on_map, dest, dest_on_map):
        """
        """

        # draw a line from the source to the destination
        scenario.sdl.drawLine(properties.layer_unit_orders_movefast, source_on_map, dest_on_map)

        # paint a waypoint at the position
        self.__paintWaypoint(dest)

        # return the new starting position for the next plan
        return dest

    def __paintRetreat(self, source, source_on_map, dest, dest_on_map):
        """
        """

        # draw a line from the source to the destination
        scenario.sdl.drawLine(properties.layer_unit_orders_retreat, source_on_map, dest_on_map)

        # paint a waypoint at the position
        self.__paintWaypoint(dest)

        # return the new starting position for the next plan
        return dest

    def __paintRotate(self, source, source_on_map, look_at, look_at_on_map):
        """
        Visualizes a rotate plan. Draws a line from the unit to the location that was
        clicked. The line indicates the new facing the unit will have after the rotation.
        """

        # draw a line from the source to the destination
        scenario.sdl.drawLine(properties.layer_unit_orders_rotate, source_on_map, look_at_on_map)

        # compensate for the size of the waypoint
        look_at_on_map = (look_at_on_map[0] - self.waypoint_delta_x, look_at_on_map[1] - self.waypoint_delta_y)

        # paint a waypoint at the position
        scenario.sdl.blit(self.waypoint, look_at_on_map)

        # return the new starting position for the next plan. Note that we don't use that 'look_at'
        # as the returned destination, as the unit does not move there. This should be the identical
        # source as we were passed in the first place
        return source

    def __paintChangeMode(self, source):
        """
        Visualizes a plan that changes the unit mode. TODO: how should this be shown? I have no
        idea.
        """

        print("UnitOrdersLayer.__paintChangeMode: TODO")

        # return the untouched source position
        return source

    def __paintWait(self, source):
        """
        Visualizes a plan that has the unit waiting for a certain time. TODO: how should this be
        shown? I have no idea.
        """

        print("UnitOrdersLayer.__paintWait: TODO")

        # return the untouched source position
        return source

    def __paintSkirmish(self, source, source_on_map, targetid):
        """
        Visualizes an skirmish plan. The unit fires at the target. This method will not change
        the destination of the unit, so the original position is returned
        """

        # has the target been destroyed?
        if targetid not in scenario.info.units:
            # no such unit there anymore, return the untouched source position
            return source

            # get the target and its position
        target = scenario.info.units[targetid]
        target_x, target_y = target.getPosition()

        # translate target pos so that it is within the playfield
        targetpos = (target_x - self.min_x, target_y - self.min_y)

        # draw a line from the source to the target
        scenario.sdl.drawLine(properties.layer_unit_orders_skirmish, source_on_map, targetpos)

        # return the untouched source position
        return source

    def __paintAssault(self, source, source_on_map, targetid):
        """
        Visualizes an assault plan. The unit moves towards the unit and will assault it when
        close. This method will change the destination of the unit to the position of the target.
        """

        # has the target been destroyed?
        if targetid not in scenario.info.units:
            # no such unit there anymore, return the untouched source position
            return source

            # get the target and its position
        target = scenario.info.units[targetid]
        target_x, target_y = target.getPosition()

        # translate target pos so that it is within the playfield
        targetpos = (target_x - self.min_x, target_y - self.min_y)

        # draw a line from the source to the target
        scenario.sdl.drawLine(properties.layer_unit_orders_assault, source_on_map, targetpos)

        # return the position of the target
        return target_x, target_y

    def __paintWaypoint(self, position):
        """
        Paints a small waypoint marker at the given position, which should be a tuple of x, y
        coordinates. The waypoint is centered on the position.
        """

        # fix the coordinates so that the waypoint is centered
        x = position[0] - self.waypoint_delta_x - self.min_x
        y = position[1] - self.waypoint_delta_y - self.min_y

        icon = self.waypoint
        if scenario.selected and scenario.selected[0] == self.cur_unit:
            icon = self.waypoint_mainsel

        # Collect everything and paint it later => waypoints appear on top of lines
        self.waypoints.append((icon, (x, y)))

    def __paintAllUnitWayPoints(self):
        """
        Does the raw blitting of all the waypoint icons.
        """
        # do the blit
        for icon, pos in self.waypoints:
            x, y = pos
            scenario.sdl.blit(icon, (x, y))
