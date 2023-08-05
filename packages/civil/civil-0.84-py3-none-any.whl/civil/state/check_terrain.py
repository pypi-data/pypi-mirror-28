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

from civil.state import state
from civil import properties
from civil.model import scenario


class CheckTerrain(state.State):
    """
    This class is a state that takes care of letting the user check the type of terrain on a clicked
    position on the map. When this state is activated the user should click the map and then the
    state will figure out the terrain at the given position, after which the previous state is
    activated. 

    Uses a crosshair cursor.

    Pressing 'Escape' terminates the terrain checking.
    """

    # define a shared base cursor
    cursor = None

    def __init__(self, caller):
        """
        Initializes the instance. Sets default values for all needed members.
        """

        # call superclass constructor
        state.State.__init__(self)

        # store the calling state
        self.caller = caller

        # do we have a cursor already loaded? 
        if not CheckTerrain.cursor:
            # nope, so load it. First get the file names
            datafile = properties.state_check_terrain_cursor_data
            maskfile = properties.state_check_terrain_cursor_mask

            # now load it
            CheckTerrain.cursor = pygame.cursors.load_xbm(datafile, maskfile)

        # set our own cursor cursor
        pygame.mouse.set_cursor(*CheckTerrain.cursor)

        # set defaults
        self.name = "check_terrain"

        # set the keymap too
        self.keymap[(K_ESCAPE, KMOD_NONE)] = self.close

        # define the help text too
        self.helptext = ["Terrain check",
                         " ",
                         "arrow keys - scroll map",
                         "F1 - show this help text",
                         "F10 - toggle fullscreen mode",
                         "F12 - save a screenshot",
                         "esc - cancel the terrain check"]

        # let the player know what we're doing
        scenario.messages.add("Click the map to determine terrain type")

    def close(self):
        """
        Callback triggered when the user presses the 'escape' key. Terminates the state and
        activates the previous state. Sets a default cursor.
        """
        # set the default cursor
        self.setDefaultCursor()

        # return the previous state
        return self.caller

    def handleLeftMousePressed(self, event):
        """
        Method for handling a mouse pressed. Checks weather the mouse was clicked in the map or in
        the panel. Only clicks in the map will do anything useful, all other clicks are
        ignored.

        If the click is in the map then LOS to that position is checked for the given unit.
        """
        # get global event position
        x, y = self.toGlobal(event.pos)

        # get the terrain type
        terrain_type = scenario.map.getTerrain((x, y)).getType()

        # let the player know what we're doing
        scenario.messages.add("Terrain at %d,%d is: %s" % (x, y, terrain_type))

        # we're done here
        return self.close()
