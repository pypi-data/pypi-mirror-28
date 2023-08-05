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


class CombatPolicyLayer(DialogLayer):
    """
    This class defines a layer that plugs into the PlayField. It provides code...
    """

    def __init__(self, name):
        """
        Initializes the layer.
        """
        # call superclass constructor
        DialogLayer.__init__(self, name, 250, 130, properties.layer_combatpolicy_button)

        # create the labels for the three check boxes
        self.labels = [self.createLabel('Hold your fire'),
                       self.createLabel('Defensive fire only'),
                       self.createLabel('Fire at will')]

        # set the margins we use from the origin. this gives some padding to the border
        self.margin_x = 15
        self.margin_y = 10

    def updateUnits(self):
        """
        Creates labels based on currently selected units. This must be run each time the dialog
        is shown, as the selected units change all the time.
        """

        # create the fonts we need. do we have one or more selected units?
        if len(scenario.selected) == 1:
            # only one unit, so we use its name
            name = scenario.selected[0].getName()
            self.title = self.createLabel("Setting combat policy for '%s'" % name)

            # checked should be the one matching the unit combat policy
            self.checked = scenario.selected[0].getCombatPolicy()

        else:
            # apparently more units
            length = len(scenario.selected)
            self.title = self.createLabel("Setting combat policy for %d units" % length)

            # no box checked
            self.checked = -1

    def getPolicy(self):
        """
        Returns the selected combat policy. If the player did not select a combat policy at all
        then this method returns -1. A valid policy is 0 to 2.
        """
        return self.checked

    def handleLeftMousePressed(self, click_x, click_y):
        """
        Method that handles a press with the left mouse button. Checks if any of the checkboxes
        have been pressed, and if so then sets the internal flag that indicates that something
        changed.
        """

        # get the buttons width and height. Note that we reduce from the height of the checkboxes,
        # as they contain a lot of extra empty space below the checkbox
        width = Layer.checkbox[0].get_width()
        height = Layer.checkbox[0].get_height() - 15

        # loop over all three buttons
        for index in range(3):
            # get y coordinate for this checkbox. note the added 10 to make sure that the click is
            # inside the check. the image is a little bit too big, meaning that you can actually
            # click all around it and still get a hit
            y = properties.layer_combatpolicy_checks_y[index] + self.y + 10

            # add offsets
            x = self.x

            # is the click inside that checkbox?
            if x <= click_x <= x + width and y <= click_y <= y + height:
                # yep, this checkbox was clicked, set it as the new one
                self.checked = index

                # repaint the playfield
                scenario.playfield.needInternalRepaint(self)

    def customPaint(self):
        """
        Paints the layer by painting the contents and the callin the superclass method for doing
        the frame painting.
        """

        # get the width and height of a checkbox and some extra offset
        extrax = Layer.checkbox[0].get_width() + 10
        extray = Layer.checkbox[0].get_height() / 2 - self.labels[0].get_height() / 2

        # paint the title. the coordinates are inherited, and refer to the topleft corner of the
        # content area we're given
        if not self.need_internal_repaint:
            scenario.sdl.blit(self.title, (self.x + self.margin_x, self.y + self.margin_y))

        # loop and blit the three check boxes
        for index in range(3):
            # get y coordinate for this checkbox
            y = properties.layer_combatpolicy_checks_y[index] + self.margin_y

            # should it be checked?
            if index == self.checked:
                # this one is checked
                use = 1
            else:
                # nope, draw an unchecked
                use = 0

            scenario.sdl.fill((0, 0, 0), (self.x, self.y + y, Layer.checkbox[1].get_width(),
                                          Layer.checkbox[1].get_height()))

            # do the blit of the checkbox and the label
            scenario.sdl.blit(Layer.checkbox[use], (self.x, self.y + y))
            if self.need_internal_repaint:
                continue
            scenario.sdl.blit(self.labels[index], (self.x + extrax, self.y + y + extray))
