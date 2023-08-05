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

from civil import properties
from civil.model import scenario
from civil.playfield.dialog_layer import DialogLayer
from civil.playfield.layer import Layer


class ChooseUnitsLayer(DialogLayer):
    """
    This class defines a layer that shows a list of units
    that can be activated/deactivated.
    It is used when clicking close to several units.
    """

    def __init__(self, name):
        """
        Initialize the layer.
        """
        # Note that the size is bogus and will be set properly later
        DialogLayer.__init__(self, name, 100, 100, properties.layer_chooseunits_button)

        # Placeholder for what title to display
        self.title = None

        # Placeholder for what units to display
        self.units = None

        # Placeholder for which of them are chosen
        self.selected = None

        # Which are displayed in the gfx
        self.gui_selected = None

        # Hash of unit information
        # self.unitinfo[unit] => ( x, y, width, height, icon, commander name, strength )
        self.unitinfo = {}

        # get the checkbox width and height
        self.checkwidth = Layer.checkbox[0].get_width()
        self.checkheight = Layer.checkbox[0].get_height()

        # set the margins we use. this gives some padding.
        self.margin_x = 15
        self.margin_y = 10

    def __recalc__(self):
        """
        Recalculates the height and width of the layer,
        depending on current information.
        """
        # None is selected
        self.gui_selected = []

        # Calculate maximum width as we go along
        width = self.title.get_width()
        # Calculate total height during traversal
        height = self.margin_y + self.title.get_height() + self.margin_y

        self.unitinfo = {}
        for u in self.units:
            commandername = self.createLabel(u.getCommander().getName())
            w = self.checkwidth + self.margin_x + commandername.get_width()
            self.unitinfo[u] = (self.margin_x, height, w, self.checkheight, None, commandername, None)
            width = max(width, w, 0)
            height += self.checkheight

        # Set the new size
        width += self.margin_x * 2
        self.setSize(width, height)

        # We need repaint of this layer
        scenario.playfield.needInternalRepaint(self)

    def setInformation(self, title, units, selected=None):
        """
        Gives the layer the information what units it is supposed to
        display, and if any of them are already selected.  The
        title is the title of the dialog.
        """
        if not selected:
            selected = []
        assert units

        # Create nice title
        self.title = self.createLabel(title)

        # Set the units and selected units
        self.units = units
        self.selected = []

        # Just in case, match selected with all the units
        for unit in selected:
            if unit in self.units and not unit in self.selected:
                self.selected.append(unit)

        # Recalculate dimensions of dialog
        self.__recalc__()

    def overUnit(self, click_x, click_y):
        """
        Returns over what unit the click was, or
        None if no unit.
        """
        click_x -= self.x
        click_y -= self.y
        for u in list(self.unitinfo.keys()):
            (x1, y1, w, h, dummy1, dummy2, dummy3) = self.unitinfo[u]
            if x1 <= click_x <= x1 + w and y1 <= click_y <= y1 + h:
                return u
        return None

    def handleLeftMousePressed(self, click_x, click_y):
        """
        Handles mouse clicks by selecting and unselecting
        units.
        """
        unit = self.overUnit(click_x, click_y)
        if not unit:
            return
        if unit in self.selected:
            self.selected.remove(unit)
        else:
            self.selected.append(unit)

        # We need repaint of this layer
        scenario.playfield.needInternalRepaint(self)

    def getSelected(self):
        """
        Returns the selected units.
        """
        return self.selected

    def getAllUnits(self):
        """
        Returns the selected units.
        """
        return self.units

    def customPaint(self):
        """
        Paints the layer by painting the title and the checkboxes
        along with the units and their information.
        """
        if not self.need_internal_repaint:
            scenario.sdl.blit(self.title, (self.x + self.margin_x, self.y + self.margin_y))

        for u in self.units:
            (x, y, w, h, dummy1, commander_name, dummy3) = self.unitinfo[u]
            x += self.x
            y += self.y
            if u in self.selected:
                use = 1
            else:
                use = 0
            # we need some extra offset to the y for the label to
            # align it nicely with the checkbox.
            extray = self.checkheight / 2 - commander_name.get_height() / 2

            # Clear first
            scenario.sdl.fill((0, 0, 0), (x, y, w, h))
            # Now blit
            scenario.sdl.blit(Layer.checkbox[use], (x, y))
            scenario.sdl.blit(commander_name, (x + self.margin_x + self.checkwidth, y + extray))

        # Update gui information, last!
        self.gui_selected = self.selected
