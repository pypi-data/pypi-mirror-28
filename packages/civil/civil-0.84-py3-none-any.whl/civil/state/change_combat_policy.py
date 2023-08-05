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

from civil.model import scenario
from civil.plan import change_combat_policy
from civil.state import state, own_unit


class ChangeCombatPolicy(state.State):
    """
    This class is a state that is used to...
    """

    def __init__(self):
        """
        Initializes the instance. Sets default values for all needed member.
        """

        # call superclass constructor
        state.State.__init__(self)

        # set default cursor
        self.setDefaultCursor()

        # set defaults
        self.name = "change_combat_policy"

        # set the keymap too
        self.keymap[(K_ESCAPE, KMOD_NONE)] = self.close

        # find the question layer
        self.policylayer = scenario.playfield.getLayer("combat_policy")

        # update it so that it knows selected units
        self.policylayer.updateUnits()

        # and make it visible
        scenario.playfield.setVisible(self.policylayer)

    def handleLeftMousePressed(self, event):
        """
        Handles a click with the left mouse button. This method checks weather the 'Ok' button was
        clicked, and if it was then sets the new policy for all selected units. If no button was not
        clicked then nothing will be done. Activates the state OwnUnit when closed.
        """

        # get event position
        xev, yev = event.pos

        # was ok pressed? Let the layer handle the keypress
        if self.policylayer.isOkPressed(xev, yev):
            # get the new selected policy
            policy = self.policylayer.getPolicy()

            # do we have a changed policy? If it's not changed (-1) then we have nothing to do here
            if policy != -1:
                # loop over all selected units
                for unit in scenario.selected:
                    # create new plans for each unit that changes the policy
                    newplan = change_combat_policy.ChangeCombatPolicy(unit_id=unit.getId(),
                                                                      policy=policy)

                    # send off the plan to the server
                    scenario.connection.send(newplan.toString())

                    # add the plan last among the unit's plans
                    unit.getPlans().append(newplan)

            # we're done, hide the layer
            scenario.playfield.setVisible(self.policylayer, 0)

            # we have changed some units
            scenario.dispatcher.emit('units_changed', self.getSelectedUnits())

            # default to own unit state
            return own_unit.OwnUnit()

        # no 'Ok' clicked, see if there' something else that needs to be take care of
        self.policylayer.handleLeftMousePressed(xev, yev)

    def close(self):
        """
        Closes the state without doing anything. Hides the dialog and repaints the playfield.
        """

        # find the layer and hide it
        scenario.playfield.setVisible(self.policylayer, 0)

        # return the previous state
        return own_unit.OwnUnit()
