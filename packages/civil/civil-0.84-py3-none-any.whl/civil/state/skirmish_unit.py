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

import civil.ui.messages as messages
from civil.state import combat
from civil.state import own_unit
from civil import properties
from civil.model import scenario
from civil.plan.skirmish import Skirmish


class SkirmishUnit(combat.Combat):
    """
    This class is a state that takes care of letting the user click on an enemy unit to be a
    skirmish target. This state should only be activated when an own unit is selected. When the user
    has clicked in the map and the plan has been sent to the server the state OwnUnit is activated.

    Some basic verifications wrt the unit state is performed to speed up execution. Checks is made
    to see weather:

    * enemy is in range
    * enemy is seen
    * morale allows combat

    If the unit does not see the enemy it will turn to face it.
    """

    # define a shared base cursor
    cursor = None

    def __init__(self):
        """
        Initializes the instance. Sets default values for all needed members.
        """

        # call superclass constructor
        combat.Combat.__init__(self)

        # do we have a cursor already loaded? 
        if not SkirmishUnit.cursor:
            # nope, so load it. First get the file names
            datafile = properties.state_attack_cursor_data
            maskfile = properties.state_attack_cursor_mask

            # now load it
            SkirmishUnit.cursor = pygame.cursors.load_xbm(datafile, maskfile)

        # set our own cursor cursor
        pygame.mouse.set_cursor(*SkirmishUnit.cursor)

        # set defaults
        self.name = "skirmish_unit"

        # set the keymap too
        self.keymap[(K_ESCAPE, KMOD_NONE)] = self.cancel

        # define the help text too
        self.helptext = ["Skirmish",
                         " ",
                         "arrow keys - scroll map",
                         "F1 - show this help text",
                         "F10 - toggle fullscreen mode",
                         "F12 - save a screenshot",
                         "esc - cancel the order"]

    def cancel(self):
        """
        Callback triggered when the user presses the 'escape' key. Cancels the skirmishing and makes a
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
         """

        # no changed units yet
        changed = 0

        # get event position
        x, y = event.pos

        # the click is on the main playfield, so get the clicked coordinate
        globalx, globaly = self.toGlobal((x, y))

        # find the id of the targeted unit (if any)
        targetid = self.findTarget(globalx, globaly)

        # did we find any unit?
        if targetid == -1:
            # no target unit in clicked position, let player try again
            return self

        # loop over all selected units
        for unit in self.getSelectedUnits():
            # check morale, fatigue
            if unit.getMorale().checkSkirmish() == 0 or unit.getFatigue().checkSkirmish() == 0:
                # either the morale is too low or the fatigue is too high, we won't do combat
                scenario.messages.add('%s can not skirmish' % unit.getName(), messages.ERROR)
                continue

            # can the unit skirmish?
            if not unit.getMode().canSkirmish():
                # nope, the unit mode prohibits it, next unit
                scenario.messages.add('%s can not skirmish' % unit.getName(), messages.ERROR)
                continue

            # morale and fatigue ok, create a new 'skirmish' plan
            plan = Skirmish(unit_id=unit.getId(), targetid=targetid)

            # send off the plan to the server
            scenario.connection.send(plan.toString())

            # add the plan last among the unit's plans
            unit.getPlans().append(plan)

            # at least one changed unit
            changed = 1

        # any changed units?
        if changed:
            # we have changed some units
            scenario.dispatcher.emit('units_changed', self.getSelectedUnits())

        # the units have now got a target
        return own_unit.OwnUnit()

