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

from civil.state import move_unit
from civil import properties
from civil.model import scenario
from civil.plan.move_fast import MoveFast


class MoveUnitFast(move_unit.MoveUnit):
    """
    This class is a state that takes care of letting the user click on a position in the map where a
    unit should be moved in a fast pace. This state should only be activated when an own unit is
    selected. When the user has clicked in the map and the unit has started to move a state OwnUnit
    is activated.

    A packet 'movefast' will also be sent to the server if we're the client or just added to the
    queue of data if we're the server.
    """

    # define a shared base cursor
    cursor = None

    def __init__(self):
        """
        Initializes the instance. Sets default values for all needed members.
        """

        # call superclass constructor
        move_unit.MoveUnit.__init__(self)

        # do we have a cursor already loaded? 
        if not MoveUnitFast.cursor:
            # nope, so load it. First get the file names
            datafile = properties.state_movefast_cursor_data
            maskfile = properties.state_movefast_cursor_mask

            # now load it
            MoveUnitFast.cursor = pygame.cursors.load_xbm(datafile, maskfile)

        # set our own cursor cursor
        pygame.mouse.set_cursor(*MoveUnitFast.cursor)

        # set defaults
        self.name = "move_unit_fast"

        # set the keymap too
        self.keymap[(K_ESCAPE, KMOD_NONE)] = self.cancel

        # define the help text too
        self.helptext = ["Move a unit fast",
                         " ",
                         "arrow keys - scroll map",
                         "F1 - show this help text",
                         "F10 - toggle fullscreen mode",
                         "F12 - save a screenshot",
                         "esc - cancel the order"]

    def __sendMovementPlan(self, unit, x, y):
        """
        Creates a movement plan and sends it on the socket. This is overridden from Move to
        create MoveFast plans.
        """
        # create a new plan
        plan = MoveFast(unit.getId(), x, y)

        # and send it
        scenario.connection.send(plan.toString())

        # add the plan last among the unit's plans
        unit.getPlans().append(plan)

    def __canMove__(self, unit):
        """
        Overridden since we need canMoveFast().
        """
        if not unit.getMode().canMoveFast() or not unit.getFatigue().checkMove():
            return 0
        return 1
