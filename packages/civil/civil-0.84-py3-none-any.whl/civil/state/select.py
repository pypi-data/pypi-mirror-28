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

from civil.state import state
from civil.state import idle
from civil.state import own_unit
from civil.model import scenario


class Select(state.State):
    """
    This class is a state that is used when the player has pressed down the left mouse button on some
    part of the map where there was no unit. As long as the left mouse button is pressed the player
    is assumed to preform a selection. When it is released this state will check what unit were
    inside the selection and make them the current units.

    Only own units will be selected, all enemies are silently ignored. Even if there are only
    enemies inside the rectangle they'll be ignored. There is no real reason to have several enemies
    selected, and if one needs to be selected, it can be clicked.
    """

    def __init__(self, position):
        """
        Initializes the instance. Sets default values for all needed member.
        """

        # call superclass constructor
        state.State.__init__(self)

        # set default cursor
        self.setDefaultCursor()

        # set defaults
        self.name = "select_state"

        # set the keymap to something empty. we don't want to handle anything
        self.keymap = {}

        # find the selection layer
        self.selectionlayer = scenario.playfield.getLayer("selection")

        # we want mouse motion events
        self.wantmousemotion = 1

        # store the position of the mouse now when the drag starts and also let the layer know about it
        self.start = position
        self.selectionlayer.setStartPosition(position)
        scenario.playfield.setVisible(self.selectionlayer, 1)

    def handleLeftMouseReleased(self, event):
        """
        Handles a the event when the left mouse button is released. This method will check what
        units are within the rectangle formed by the starting position and the current position and
        activate them.

        If no units are selected this method returns the calling class. If units were selected then
        OwnUnit is returned.
        """

        # get the position
        pos = event.pos

        # finish the selection
        self.selectionlayer.finishSelection()

        # get the units inside the the selection
        inside = self.findSelected(self.start[0], self.start[1], pos[0], pos[1])

        # always clear selection
        changed = self.clearSelectedUnits()

        # did we have any own units in the selection rectangle?
        if inside:
            # loop over the units
            for unit in inside:
                # set it as selected
                self.setSelectedUnit(unit=unit, clearfirst=0)

            # we have a new selected unit
            scenario.dispatcher.emit('unit_selected', self.getSelectedUnit())

            # we have a new state
            return own_unit.OwnUnit()

        if changed:
            # no units, make the sure all parts of Civil know that
            scenario.dispatcher.emit('unit_selected', None)

        # return the idle state
        return idle.Idle()

    def handleMouseMotion(self, event):
        """
        This method handles the mouse moving around. It is used to be able to track where the
        mouse is right now and highlight the current alternative.
        """

        # Grab all mouse movements, but use only the last one. avoids flicker
        event = self.latestMousemove(event)

        # update the current ending position in the selection layer
        self.selectionlayer.setEndPosition(event.pos)

        # the selection layer needs a repaint
        scenario.playfield.needInternalRepaint(self.selectionlayer)

        return None

    def findSelected(self, x1, y1, x2, y2):
        """
        Checks all units to see which are inside the rectangle formed by the points (x1,y1) and
        (x2,y2). Returns a list of those units or an empty list if none is found. Will only select
        own units, never enemies.
        """
        # so far no found
        found = []

        # get the smaller coordinates as start and larger as end
        xstart, ystart = self.toGlobal((min(x1, x2), min(y1, y2)))
        xend, yend = self.toGlobal((max(x1, x2), max(y1, y2)))

        # loop over all units
        for unit in scenario.info.units.values():
            # an own unit?
            if not unit.getOwner() == scenario.local_player_id:
                # nope, we don't select enemies
                continue

            # get the unit position
            ux, uy = unit.getPosition()

            # is the unit inside?
            if xstart <= ux <= xend and ystart <= uy <= yend and unit.isVisible():
                # yep, so add the unit
                found.append(unit)

        # return whatever we have
        return found
