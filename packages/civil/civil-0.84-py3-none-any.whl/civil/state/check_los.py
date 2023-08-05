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
from pygame.locals import *

from civil import properties
from civil.model import scenario
from civil.state import state, own_unit


class CheckLos(state.State):
    """
    This class is a state that takes care of letting the user check line of sight (los) for the
    current unit to various positions on the map. A line is drawn from the unit position to the
    current mouse position. This state will track the mouse.

    Clicking a mouse button or pressing 'Escape' terminates the LOS-checking.
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
        if not CheckLos.cursor:
            # nope, so load it. First get the file names
            datafile = properties.state_check_los_cursor_data
            maskfile = properties.state_check_los_cursor_mask

            # now load it
            CheckLos.cursor = pygame.cursors.load_xbm(datafile, maskfile)

        # set our own cursor cursor
        pygame.mouse.set_cursor(*CheckLos.cursor)

        # set defaults
        self.name = "check_los"

        # set the keymap too
        self.keymap[(K_ESCAPE, KMOD_NONE)] = self.cancel

        # we want mouse motion events
        self.wantmousemotion = 1

        # define the help text too
        self.helptext = ["Line of sight test",
                         " ",
                         "arrow keys - scroll map",
                         "F1 - show this help text",
                         "F10 - toggle fullscreen mode",
                         "F12 - save a screenshot",
                         "esc - cancel the los test"]

    def handleMouseMotion(self, event):
        """
        This method handles mouse motion events. Checks the current unit and mouse positions and
        traces a LOS to the current mouse position. If the position can be seen by the unit then a
        green line is drawn in the 'los' playfield layer, and if not, then a red line is drawn.

        Returns None to indicate that a new state should not be activated.
        """
        # get the selected unit
        unit = self.getSelectedUnit()

        # get the selected unit's position
        unitx, unity = unit.getPosition()

        # the click is on the main playfield, so get the clicked coordinate
        globalx, globaly = self.toGlobal(event.pos)

        # check visibility
        last_seen = scenario.map.traceLos(start=(unitx, unity), end=(globalx, globaly),
                                          max_distance=unit.sightRange, debug=1)

        # did we see it?
        if last_seen == (globalx, globaly):
            # yep, we see all the way
            sees = 1
        else:
            sees = 0

        print("CheckLos.handleMouseMotion: sees:", sees)

    def handleLeftMousePressed(self, event):
        """
        Handles an event when the left mouse button is pressed. This will immediately cancel the
        state and return to the OwnUnit state.
        """
        return self.cancel()

    def handleMidMousePressed(self, event):
        """
        Handles an event when the middle mouse button is pressed. This will immediately cancel the
        state and return to the OwnUnit state.
        """
        return self.cancel()

    def handleRightMousePressed(self, event):
        """
        Handles an event when the right mouse button is pressed. This will immediately cancel the
        state and return to the OwnUnit state.
        """
        return self.cancel()

    def cancel(self):
        """
        Callback triggered when the user presses the 'escape' key. Cancels the moving and makes a
        OwnUnit state active again.
        """
        # return a new state
        return own_unit.OwnUnit()

