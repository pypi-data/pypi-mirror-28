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

import pygame
import pygame.cursors
from pygame.locals import *

from civil.state import own_unit
from civil.state import state
from civil import properties
from civil.ui import messages
from civil.model import scenario
from civil.server.ai.basic_path import PathFinder
from civil.plan.move import Move


class MoveUnit(state.State):
    """
    This class is a state that takes care of letting the user click on a position in the map where a
    unit should be moved. This state should only be activated when an own unit is selected. When the
    user has clicked in the map and the unit has started to move a state OwnUnit is activated.

    A packet 'move' will also be sent to the server if we're the client or just added to the queue
    of data if we're the server.
    """

    # define a shared base cursor
    cursor = None

    def __init__(self):
        """
        Initializes the instance. Sets default values for all needed members.
        """

        # call superclass constructor
        state.State.__init__(self)

        # do we have a cursor already loaded? 
        if not MoveUnit.cursor:
            # nope, so load it. First get the file names
            datafile = properties.state_move_cursor_data
            maskfile = properties.state_move_cursor_mask

            # now load it
            MoveUnit.cursor = pygame.cursors.load_xbm(datafile, maskfile)

        # set our own cursor cursor
        pygame.mouse.set_cursor(*MoveUnit.cursor)

        # set defaults
        self.name = "move_unit"

        # set the keymap too
        self.keymap[(K_ESCAPE, KMOD_NONE)] = self.cancel

        # define the help text too
        self.helptext = ["Move a unit",
                         " ",
                         "arrow keys - scroll map",
                         "F1 - show this help text",
                         "F10 - toggle fullscreen mode",
                         "F12 - save a screenshot",
                         "esc - cancel the order"]

    def cancel(self):
        """
        Callback triggered when the user presses the 'escape' key. Cancels the moving and makes a
        OwnUnit state active again.
        """
        # return a new state
        return own_unit.OwnUnit()

    def handleLeftMousePressed(self, event):
        """
        Method for handling a mouse pressed. Checks weather the mouse was clicked in the map or in
        the panel. Only clicks in the map will do anything useful, all other clicks are
        ignore. Accepts the movement target if a click is made in the map and return a new 'OwnUnit'
        if the unit will be moved.

        If all is ok a new plan for moving to the clicked position is created and added to the plans
        for the unit.
        """

        # get event position
        x, y = event.pos

        # the click is on the main playfield, so get the clicked coordinate
        globalx, globaly = self.toGlobal((x, y))

        (hexx, hexy) = scenario.map.pointToHex2((globalx, globaly))
        if not scenario.map.isInside(hexx, hexy):
            return None

        # get all currently pressed modifiers
        mods = pygame.key.get_mods()

        pathfind = 0
        simple = 0
        # are we pressing down the shift button?
        if mods & KMOD_RSHIFT:
            # shift is pressed, so we need to do a pathfinding instead of doing a straight move to
            # the destination
            simple = 0
            pathfind = 1
        elif mods & KMOD_LSHIFT:
            simple = 1
            pathfind = 1

        to_same_spot = 0
        if mods & KMOD_LCTRL or mods & KMOD_RCTRL:
            to_same_spot = 1

        # normal straight move. get the relative coordinates. this is done wrt to the mains elected
        # unit so that all others get the same relative coordinates, i.e. the movement is in a formation
        basex, basey = self.getSelectedUnit().getLatestPosition()
        delta_x = globalx - basex
        delta_y = globaly - basey

        # loop over all selected unit
        for unit in self.getSelectedUnits():
            # can the unit move?
            if not self.__canMove__(unit):
                # nope, the unit mode or fatigue prohibits it, next unit
                scenario.messages.add('%s can not move' % unit.getName(), messages.ERROR)
                continue

            # get the unit position
            x, y = unit.getLatestPosition()

            #
            # If we are moving to the same spot, we must adjust the delta_x and delta_y
            # variables. This is true for both pathfinding and regular move.
            #
            if to_same_spot:
                delta_x = globalx - x
                delta_y = globaly - y

            if pathfind:
                self.doPathfindingMove(unit, x + delta_x, y + delta_y, simple)
            else:
                #  create a new 'move' plan and add the deltas, send it off too
                self.__sendMovementPlan(unit=unit, x=x + delta_x, y=y + delta_y)

        # we have changed some units
        scenario.dispatcher.emit('units_changed', self.getSelectedUnits())

        # unit is now moved as far as we are concerned, let the engine sort it all out and resume to
        # having the unit activated
        return own_unit.OwnUnit()

    def doPathfindingMove(self, unit, globalx, globaly, simple=0):
        """
        This method moves a unit using pathfinding to the given destination. It
        will move in several small steps, trying to find the fastest path. The found path is added
        to the unit as several Move plans (or whetever that __makeMovementPlan__() returns).
        """

        x, y = unit.getLatestPosition()
        delta_x = globalx - x
        delta_y = globaly - y

        # create a new pathfinder that we use for all paths
        pathfinder = PathFinder()

        # add the deltas to the position so that we get the relative position for the unit (wrt
        # to the "main" selected unit) and then create the hex positions by transforming the
        # pixel positions into hex positions
        sourcehex = scenario.map.pointToHex2((x, y))
        desthex = scenario.map.pointToHex2((globalx, globaly))

        # print "MoveUnit.doPathfindingMove: %d,%d -> %d,%d" % (x,y,x + delta_x,y + delta_y)
        # print "MoveUnit.doPathfindingMove: ", sourcehex, " -> ", desthex

        # now we know where the unit should head from its current position. create a path to it
        # and at the same time fix it so that it works better in a pixel environment
        path = pathfinder.calculatePath(sourcehex, desthex)
        if not simple:
            path = self.__fixPath(path)

        print("MoveUnit.doPathfindingMove: using hex path:", path)

        # loop over all parts of the calculated path. if we got no path at all we just don't do anything
        for hex in path:
            # convert the hex to pixel coordinates
            # pathx, pathy = scenario.map.hexToPoint ( hex )
            pathx, pathy = hex

            # create plans for each path part
            self.__sendMovementPlan(unit=unit, x=pathx, y=pathy)

            # send off the plan
            # scenario.connection.send ( plan.toString () )

        # and add the final position so that the unit moves exactly to the clicked position, not
        # just close to it
        self.__sendMovementPlan(unit=unit, x=x + delta_x, y=y + delta_y)

    def __fixPath(self, path):
        """
        This method will fix a path so that it works better in a pixel world. All paths are hex
        based, not pixel based, so the first and last part of a path may need to be tweaked. The
        method will also remove any unnecessary middle steps, where several steps form straight
        lines. These will be combined into one single long step. The new path is returned.
        """
        # do we have a long path where we can get rid of the first step?
        if len(path) > 2:
            # yep, get rid of them
            path = path[1:-1]

        # is it long enough for some simplifications?
        if len(path) <= 2:
            # no, too short, so just get lost
            return path

        # loop over all possible starting positions
        deltas = []
        for index in range(len(path) - 1):
            # get the positions
            x1, y1 = path[index]
            x2, y2 = path[index + 1]

            # do we already have such a delta there?
            deltas.append((x2 - x1, y2 - y1, x1, y1, index))

        # the initially empty fixed path
        fixedpath = []

        # start with delta values that are clearly way out
        lastx = -100000
        lasty = -100000

        # loop over all the data we calculated above
        for dx, dy, x, y, index in deltas:
            # is the delta different from the last step? if it is not then we can safely ignore it 
            if lastx != dx or lasty != dy:
                # different, so we have a "milestone"
                fixedpath.append((x, y))

            lastx = dx
            lasty = dy

        # always add the last step of the path
        fixedpath.append(path[-1])

        # return the fixed and simplified path
        return fixedpath

    def __sendMovementPlan(self, unit, x, y):
        """
        Creates a movement plan and sends it on the socket. This is a separate method so that the
        method doPathfindingMove() can be overridden by MoveFast. The subclass can then provide an
        own version of this method.
        """
        # create a new plan
        plan = Move(unit.getId(), x, y)

        # and send it
        scenario.connection.send(plan.toString())

        # add the plan last among the unit's plans
        unit.getPlans().append(plan)

    def __canMove__(self, unit):
        """
        Tells us if the unit can move. A separate method so it can be overriden in MoveFast.
        """
        if not unit.getMode().canMove() or not unit.getFatigue().checkMove():
            # nope, the unit mode or fatigue prohibits it, next unit
            return 0
        return 1
