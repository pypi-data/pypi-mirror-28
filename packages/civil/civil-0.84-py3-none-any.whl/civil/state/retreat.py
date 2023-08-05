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

from civil.ui import messages
from civil.state import own_unit
from civil.state import state
from civil import properties
from civil.model import scenario
from civil.plan import retreat


class Retreat(state.State):
    """
    This class is a state that takes care of letting the user click on a position in the map where a
    unit should be retreated. This state should only be activated when an own unit is selected. When the
    user has clicked in the map and the unit has started to retreat a state OwnUnit is activated.

    A plan 'retreat' will also be sent to the server if we're the client or just added to the queue
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
        if not Retreat.cursor:
            # nope, so load it. First get the file names
            datafile = properties.state_retreat_cursor_data
            maskfile = properties.state_retreat_cursor_mask

            # now load it
            Retreat.cursor = pygame.cursors.load_xbm(datafile, maskfile)

        # set our own cursor cursor
        pygame.mouse.set_cursor(*Retreat.cursor)

        # set defaults
        self.name = "retreat"

        # set the keymap too
        self.keymap[(K_ESCAPE, KMOD_NONE)] = self.cancel

        # define the help text too
        self.helptext = ["Retreat a unit",
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
        ignore. Accepts the retreat target if a click is made in the map and return a new 'OwnUnit'
        if the unit will be retreatd.
        
        Sends off the command to the server if we're the client and enqueues the same command to the
        server command queue if we're the server.
        """

        # TODO: handle relative coordinates (copy from MoveUnit)

        # get event position
        x, y = event.pos

        # the click is on the main playfield, so get the clicked coordinate
        globalx, globaly = self.toGlobal((x, y))

        # If outside map, skip
        (hexx, hexy) = scenario.map.pointToHex2((globalx, globaly))
        if not scenario.map.isInside(hexx, hexy):
            return None

        # get the relative coordinates. this is done wrt to the mains elected unit so that all
        # others get the same relative coordinates, i.e. the movement is in a formation
        basex, basey = self.getSelectedUnit().getPosition()
        delta_x = globalx - basex
        delta_y = globaly - basey

        # loop over all selected unit
        for unit in self.getSelectedUnits():
            # can the unit retreat?
            if not unit.getMode().canRetreat() or not unit.getFatigue().checkRetreat():
                # nope, the unit mode or fatigue prohibits it, next unit
                scenario.messages.add('%s can not retreat' % unit.getName(), messages.ERROR)
                continue

            # get the unit position
            x, y = unit.getPosition()

            #  create a new 'retreat' plan and add the deltas
            newplan = retreat.Retreat(unit_id=unit.getId(), x=x + delta_x, y=y + delta_y)

            # send off the plan to the server
            scenario.connection.send(newplan.toString())

            # add the plan last among the unit's plans
            unit.getPlans().append(newplan)

        # we have changed some units
        scenario.dispatcher.emit('units_changed', self.getSelectedUnits())

        # unit is now retreated as far as we are concerned, let the engine sort it all out and resume to
        # having the unit activated
        return own_unit.OwnUnit()
