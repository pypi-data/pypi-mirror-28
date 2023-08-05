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


class WeaponInfo(state.State):
    """
    
    This class is a state that is used to show a small dialog with information about the weapon of
    the current unit. It will add a new layer to the playfield and use it to display a dialog with
    the information. The user can click a button 'Ok' to return to the previous state pr press
    'Escape'.
    """

    def __init__(self, weapon, caller):
        """
        Initializes the instance. Sets default values for all needed member.
        """

        # call superclass constructor
        state.State.__init__(self)

        # set default cursor
        self.setDefaultCursor()

        # set defaults
        self.name = "weapon_info"

        # store the calling state
        self.caller = caller

        # set the keymap too
        self.keymap[(K_ESCAPE, KMOD_NONE)] = self.close

        # find the weapon info layer
        self.weaponinfo = scenario.playfield.getLayer("weapon_info")

        # set the labels it should show
        self.weaponinfo.setWeapon(weapon)

        # and make it visible
        scenario.playfield.setVisible(self.weaponinfo)

    def handleLeftMousePressed(self, event):
        """
        Handles a click with the left mouse button. This method checks weather the 'Ok' button was
        clicked, and if it was then terminates this state. If the button was not clicked then
        nothing will be done.
        """

        # get event position
        xev, yev = event.pos

        # get button x, y, w and h
        # x =
        # y =
        # w = self. .get_width ()
        # h = self. .get_height ()

        # is the click within the button?
        # if xev < x or xev > x + w  or  yev < y or yev > y + h:
        #    # no, it's outside, can't close yet
        #    return None

        # find the layer and hide it
        scenario.playfield.setVisible(self.weaponinfo, 0)

        # return the previous state
        return self.caller

    def close(self):
        """


 """

        # find the layer and hide it
        scenario.playfield.setVisible(self.weaponinfo, 0)

        # return the previous state
        return self.caller
