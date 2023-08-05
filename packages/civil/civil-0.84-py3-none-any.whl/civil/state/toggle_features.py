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

from pygame.locals import *

from civil.state import state
from civil.model import scenario


class ToggleFeatures(state.State):
    """
    This class is a state that is used to drive the dialog layer ToggleFeatures. It shows the layer
    and handles the mousepress events for the dialog.
    """

    def __init__(self, oldstate):
        """
        Initializes the instance. Sets default values for all needed member.
        """

        # call superclass constructor
        state.State.__init__(self)

        # store the old state
        self.oldstate = oldstate

        # set default cursor
        self.setDefaultCursor()

        # set defaults
        self.name = "toggle_features"

        # set the keymap too
        self.keymap[(K_ESCAPE, KMOD_NONE)] = self.close

        # find the question layer
        self.layer = scenario.playfield.getLayer("toggle_features")

        # update it so that it knows what layers it should control
        self.layer.setLayers((("Map labels", "locations"),
                              ("Objectives", "objectives"),
                              ("Own unit symbols", "own_units_symbols"),
                              ("Own unit icons", "own_units_icons"),
                              ("Enemy unit symbols", "enemy_units_symbols"),
                              ("Enemy unit icons", "enemy_units_icons"),
                              ("Unit orders", "unit_orders"),
                              ("Unit line of sight", "unit_los"),
                              ("Superior commanders", "unit_commanders"),
                              ("Weapon ranges", "weapon_ranges")))

        # and make it visible
        scenario.playfield.setVisible(self.layer)

    def handleLeftMousePressed(self, event):
        """
        Handles a click with the left mouse button. This method checks weather the 'Ok' button was
        clicked, and if it was then sets the new policy for all selected units. If no button was not
        clicked then nothing will be done. Activates the state OwnUnit when closed.
        """

        # get event position
        xev, yev = event.pos

        # was ok pressed? Let the layer handle the keypress
        if self.layer.isOkPressed(xev, yev):
            # ok was pressed, have the layer update the layer status
            self.layer.updateLayerVisibility()

            # return the old state by closing the dialog
            return self.close()

        # no 'Ok' clicked, see if there' something else that needs to be take care of
        self.layer.handleLeftMousePressed(xev, yev)

    def close(self):
        """
        Closes the state without doing anything. Hides the dialog.
        """

        # find the layer and hide it
        scenario.playfield.setVisible(self.layer, 0)

        # we need an update now of the playfield
        scenario.playfield.needRepaint()

        # return the previous state
        return self.oldstate
