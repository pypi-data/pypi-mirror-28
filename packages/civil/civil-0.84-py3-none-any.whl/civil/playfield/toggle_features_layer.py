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


class ToggleFeaturesLayer(DialogLayer):
    """
    This class defines a layer that plugs into the PlayField. It provides code a simple dialog that
    lists a number of other playfields and lets the player toggle their visibility. The visualizing
    is done by presenting the player with a checkbox for the layer, along with a name for it. The
    player can then select the layers that should be visible and click 'Ok'.
    
    
    """

    def __init__(self, name):
        """
        Initializes the layer. The checkboxes and labels are not created here.
        """
        # call superclass constructor. note that that size is totally vapour, we'll fill it in layer
        # in the constructor
        DialogLayer.__init__(self, name, 100, 100, properties.layer_togglefeatures_button)

        # set the margins we use from the origin. this gives some padding to the border
        self.margin_x = 15
        self.margin_y = 10

        # set the title
        self.title = self.createLabel("Select visible features")

        # no coordinates yet
        self.coordinates = []

        # checked status for all layers
        self.checkedstatus = {}

        # get the checkbox width and height
        self.checkwidth = Layer.checkbox[0].get_width()
        self.checkheight = Layer.checkbox[0].get_height()

    def setLayers(self, names):
        """
        Sets the names of the layers that this dialog should allow the player to toggle. Creates
        the checkboxes and labels for the layers.
        """

        # store the names
        self.names = names

        # start from a given y coordinate
        y = self.margin_y * 2 + self.title.get_height()

        # loop over all allowed resolutions we can find
        index = 0
        for title, name in names:
            # now create a label for this resolution
            label = self.createLabel(title)

            # create coordinates for exactly where it will be put. we can later use these coordinates to
            # easily check weather a checkbox got clicked
            check_x1 = self.margin_x
            check_y1 = y
            check_x2 = self.margin_x + self.checkwidth
            check_y2 = y + self.checkheight - 15

            # add them along with the label
            self.coordinates.append((check_x1, check_y1, check_x2, check_y2, label, name))

            # add to the y coordinate
            y += self.checkheight - 15

            # find the layer with the given name and see if it's visible at the moment
            visible = self.getLayerVisibility(name)

            # store the visibility status
            self.checkedstatus[name] = visible

            # next index
            index += 1

        # now we know the height
        self.setSize(200, y)

    def handleLeftMousePressed(self, click_x, click_y):
        """
        Method that handles a press with the left mouse button. Checks if any of the checkboxes
        have been pressed, and if so then toggles the status of that checkbox.
        """

        # translate the coordinates so that they are within the coordinates that the checkboxes are given
        # using
        click_x -= self.x
        click_y -= self.y

        # loop over all labels along with the checkbox coordinates
        index = 0
        for check_x1, check_y1, check_x2, check_y2, label, name in self.coordinates:
            # is the click inside this button?
            if check_x1 <= click_x <= check_x2 and check_y1 <= click_y <= check_y2:
                # we have it here, get the old status
                checked = self.checkedstatus[name]

                # store new status by using this extremely clever thing.
                self.checkedstatus[name] = (1, 0)[checked]
                break

            # not yet, next index
            index += 1

        # repaint the playfield
        scenario.playfield.needInternalRepaint(self)

    def customPaint(self):
        """
        Paints the layer by painting the title and the checkboxes along with the labels.
        """

        # paint the title. the coordinates are inherited, and refer to the topleft corner of the
        # content area we're given
        scenario.sdl.blit(self.title, (self.x + self.margin_x, self.y + self.margin_y))

        # loop over all labels along with the checkbox coordinates
        index = 0
        for check_x1, check_y1, check_x2, check_y2, label, name in self.coordinates:
            # add the needed x and y coordinates so that we paint within the dialog 
            check_x1 += self.x
            check_x2 += self.x
            check_y1 += self.y
            check_y2 += self.y

            # should it be checked?
            use = self.checkedstatus[name]

            # we need some extra offset to the y for the label to align it nicely with the
            # checkbox. 
            extray = self.checkheight / 2 - label.get_height() / 2

            # do the blit of the checkbox and the label. also 
            scenario.sdl.blit(Layer.checkbox[use], (check_x1, check_y1))
            scenario.sdl.blit(label, (check_x2 + self.margin_x, check_y1 + extray))

            # next please
            index += 1

    def getLayerVisibility(self, name):
        """
        Checks weather the layer with 'name' is visible or not. Returns 1 if it is and 0 if
        not. The reason for this method is that we have one layer that handles two types of things,
        and it has to be checked separately.
        """
        # are we checking the own symbolic icons?
        if name == 'own_units_symbols':
            return scenario.playfield.getLayer('own_units').unitSymbolsShown()

        # are we checking the own nice guys?
        elif name == 'own_units_icons':
            return scenario.playfield.getLayer('own_units').unitIconsShown()

        # are we checking the enemy symbols?
        elif name == 'enemy_units_symbols':
            return scenario.playfield.getLayer('enemy_units').unitSymbolsShown()

        # are we checking the enemy nice guys?
        elif name == 'enemy_units_icons':
            return scenario.playfield.getLayer('enemy_units').unitIconsShown()

        # no, a normal layer
        return scenario.playfield.getLayer(name).isVisible()

    def updateLayerVisibility(self):
        """
        Updates the visibility for all layers. Sets all layers as either hidden or shown.
        """

        # loop over all layer names that we got
        for name, visible in list(self.checkedstatus.items()):
            # are we setting the own symbolic icons?
            if name == 'own_units_symbols':
                scenario.playfield.getLayer('own_units').showUnitSymbols(visible)

            # are we setting the own nice guys?
            elif name == 'own_units_icons':
                scenario.playfield.getLayer('own_units').showUnitIcons(visible)

            # are we setting the enemy symbols?
            elif name == 'enemy_units_symbols':
                scenario.playfield.getLayer('enemy_units').showUnitSymbols(visible)

            # are we setting the enemy nice guys?
            elif name == 'enemy_units_icons':
                scenario.playfield.getLayer('enemy_units').showUnitIcons(visible)

            else:
                # a normal layer, get the layer
                layer = scenario.playfield.getLayer(name)

                # make it visible or hidden as desired
                scenario.playfield.setVisible(layer, visible)
