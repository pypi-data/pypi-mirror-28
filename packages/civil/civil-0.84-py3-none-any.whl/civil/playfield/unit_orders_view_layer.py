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

from civil.model import scenario
from civil.playfield.floating_window_layer import FloatingWindowLayer


class UnitOrdersViewLayer(FloatingWindowLayer):
    """
    This class defines a layer that shows the orders for a unit in a little dialog. This differs
    from the normal unit orders visualization in that it shows the orders as textual labels, not
    lines as the UnitOrdersLayer.

    This class has a callback for the following signals:

         o unitselected
         

    This layer is a floating window layer, which means it can be dragged around the map.
    """

    def __init__(self, name):
        """
        Initializes the layer.
        """
        # call superclass constructor
        FloatingWindowLayer.__init__(self, name)

        # register ourselves to receive 'unitselected' signals
        scenario.dispatcher.registerCallback('unit_selected', self.unitSelected)
        scenario.dispatcher.registerCallback('units_changed', self.unitsChanged)

        # no labels yet
        self.labels = []

        # the unit we show labels for
        self.shown_unit = None

        # set the margins we use from the origin. this gives some padding to the border
        self.margin_x = 10
        self.margin_y = 5

        # get the border dimensions
        borderw, borderh = self.getBorderWidth()

        # set default dimensions. we want to take the border into account and then also leave a few
        # pixels space before the edges. makes it a bit more "airy"
        self.x = scenario.sdl.getWidth() - borderw - 120 - 5
        self.y = scenario.sdl.getHeight() - borderh - 100 - 5
        self.width = 120
        self.height = 100

        # no offset yet
        self.offset = 0

    def paint(self, offset_x, offset_y, dirtyrect=None):
        """
        Paints the layer. Blits out the orders for the unit surrounded by a border. If the
        selected unit is an enemy unit then no orders are shown.
        """
        # are we minimized?
        if self.isMinimized():
            # yes, paint just the minimized layer, no content, and then go away
            self.paintBorderMinimized(self.x, self.y, self.width)
            return

        # fill a part of the background with black so that we have something to paint on
        scenario.sdl.fill((0, 0, 0), (self.x - 1, self.y - 1, self.width + 2, self.height + 2))

        # paint the border first
        self.paintBorder(self.x, self.y, self.width, self.height)

        # start from our top-level position
        x = self.x + self.margin_x
        y = self.y + self.margin_y

        # loop over all labels we got
        for label in self.labels:
            # blit out the label
            scenario.sdl.blit(label, (x, y))

            # add the proper offset for the next label
            y += label.get_height()

            # can we fit more labels, or are we out of height?
            if y >= self.y + self.height:
                # no more labels
                return

    def unitSelected(self, parameters):
        """
        Callback triggered when a new unit has been selected. This updates the orders data for
        the unit if it's a friendly unit. For enemy units nothing is shown. The orders are rendered
        as a set of labels, one label for each order.
        """

        # clear the orders
        self.labels = []

        # get the unit, it may be none to indicate that no unit is selected
        unit = parameters

        # is this a unit at all, and if so, is it a friendly unit?
        if unit is None or unit.getOwner() != scenario.local_player_id:
            # nothing we want to bother about
            return

        # we need to get the orders for the unit
        plans = unit.getPlans()

        # loop over all labels
        for index in range(self.offset, len(plans)):
            # get the label and add to our displayable labels
            self.labels.append(plans[index].getLabel())

        # store the shown unit
        self.shown_unit = unit

    def unitsChanged(self, parameters):
        """
        Callback triggered when an unit has been changed. This updates the orders data for
        the currently selected unit if it is among the changed units. If it is not there then
        nothing will be done.
        """

        # is our unit among the changed?
        if not self.shown_unit in parameters:
            # nah, go away
            return

        # yes, it has changed, update all orders labels for it. send the unit we show as a parameter
        self.unitSelected(self.shown_unit)
