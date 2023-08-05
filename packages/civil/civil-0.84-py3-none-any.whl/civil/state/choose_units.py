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


class ChooseUnits(state.State):
    """
    This class is a state that is used to choose some units from a
    list of given units. It takes care of events and forwards mouse
    presses to the layer for handling.
    """

    def __init__(self, oldstate, units, chosen=None, clear=0):
        """
        Initialize the instance. Note that we have extra parameters
        units and chosen that tells what units we want to display,
        and chosen tells which of them are already chosen.
        """
        # call superclass constructor
        state.State.__init__(self)

        # store the old state
        self.oldstate = oldstate

        # set default cursor
        self.setDefaultCursor()

        # set defaults
        self.name = "choose_units"

        # set the keymap too
        self.keymap[(K_ESCAPE, KMOD_NONE)] = self.close

        # find the question layer
        self.layer = scenario.playfield.getLayer("choose_units")

        self.layer.setInformation("Choose Units", units, chosen)

        # Center it
        self.layer.center()

        # and make it visible
        scenario.playfield.setVisible(self.layer)

        # See state.py
        # Clear list of already selected units?
        self.clear = clear

    def handleLeftMousePressed(self, event):
        """
        Handles a click with the left mouse button. This method
        checks whether the 'Ok' button was clicked, and if it was then
        returns the selected units

        Returns the old state that was active before this state was
        activated.
        """

        # get event position
        xev, yev = event.pos

        # was ok pressed? Let the layer handle the keypress
        if self.layer.isOkPressed(xev, yev):

            units = self.layer.getSelected()

            # Clear previously selected if user didn't press shift/ctrl
            if self.clear:
                self.clearSelectedUnits()
                for unit in units:
                    self.setSelectedUnit(unit, 0)
            else:
                # We must operate ONLY on the units in the
                # "choice box", because other already selected
                # units should stay selected
                all_units = self.layer.getAllUnits()
                for unit in all_units:
                    if unit in units:
                        self.setSelectedUnit(unit, 0)
                    else:
                        self.removeSelectedUnit(unit)

            # Find out what's the next state
            # This depends on whether we have units selected
            # at all
            newstate = self.fixSelected()

            # hide layer
            scenario.playfield.setVisible(self.layer, 0)

            return newstate

        # no 'Ok' clicked, see if there's something else that needs to
        # be take care of
        self.layer.handleLeftMousePressed(xev, yev)

    def close(self):
        """
        Closes the state without doing anything. Hides the dialog and repaints the playfield.
        """

        # find the layer and hide it
        scenario.playfield.setVisible(self.layer, 0)

        # return the previous state
        return self.oldstate
