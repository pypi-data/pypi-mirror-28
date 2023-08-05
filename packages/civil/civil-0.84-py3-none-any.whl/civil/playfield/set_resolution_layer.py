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

from civil import properties
from civil.model import scenario
from civil.playfield.dialog_layer import DialogLayer
from civil.playfield.layer import Layer


class SetResolutionLayer(DialogLayer):
    """
    This class defines a layer that plugs into the PlayField. It provides code...
    """

    def __init__(self, name):
        """
        Initializes the layer.
        """
        # call superclass constructor. note that that size is totally vapour, we'll fill it in layer
        # in the constructor
        DialogLayer.__init__(self, name, 100, 100, properties.layer_setresolution_button)

        # set the margins we use from the origin. this gives some padding to the border
        self.margin_x = 15
        self.margin_y = 10

        # set the title
        self.title = self.createLabel("Select resolution")

        # no coordinates yet
        self.coordinates = []

        # get the checkbox width and height
        self.checkwidth = Layer.checkbox[0].get_width()
        self.checkheight = Layer.checkbox[0].get_height()

        # start from a given y coordinate
        y = self.margin_y * 2 + self.title.get_height()

        # loop over all allowed resolutions we can find
        index = 0
        for res_x, res_y in pygame.display.list_modes():
            # now create a label for this resolution
            label = self.createLabel('%d x %d' % (res_x, res_y))

            # create coordinates for exactly where it will be put. we can later use these coordinates to
            # easily check weather a checkbox got clicked
            check_x1 = self.margin_x
            check_y1 = y
            check_x2 = self.margin_x + self.checkwidth
            check_y2 = y + self.checkheight

            # add them along with the label
            self.coordinates.append((check_x1, check_y1, check_x2, check_y2, label))

            # add to the y coordinate
            y += self.checkheight - 5

            # should this one be checked?
            if (res_x, res_y) == scenario.sdl.getSize():
                # yep, mark it
                self.checked = index

            # next index
            index += 1

        self.gui_checked = None

        # now we know the height
        self.setSize(200, y)

    def getResolution(self):
        """
        Returns the selected resolution as a (width, height) tuple.
        """
        # just index the modes with our checked label
        return pygame.display.list_modes()[self.checked]

    def handleLeftMousePressed(self, click_x, click_y):
        """
        Method that handles a press with the left mouse button. Checks if any of the checkboxes
        have been pressed, and if so then sets the internal flag that indicates that something
        changed.
        """

        # translate the coordinates so that they are within the coordinates that the checkboxes are given
        # using
        click_x -= self.x
        click_y -= self.y

        # loop over all labels along with the checkbox coordinates
        index = 0
        for check_x1, check_y1, check_x2, check_y2, label in self.coordinates:
            # is the click inside this button?
            if check_x1 <= click_x <= check_x2 and check_y1 <= click_y <= check_y2:
                # we have it here
                self.checked = index

            # not yet, next index
            index += 1

        # repaint the playfield
        scenario.playfield.needInternalRepaint(self)

        # print "SetResolutionLayer.handleLeftMousePressed: ", self.checked

    def customPaint(self):
        """
        Paints the layer by painting the title and the checkboxes along with the labels.
        """

        # paint the title. the coordinates are inherited, and refer to the topleft corner of the
        # content area we're given
        if not self.need_internal_repaint:
            scenario.sdl.blit(self.title, (self.x + self.margin_x, self.y + self.margin_y))

        # loop over all labels along with the checkbox coordinates
        index = 0
        for check_x1, check_y1, check_x2, check_y2, label in self.coordinates:
            # add the needed x and y coordinates so that we paint within the dialog 
            check_x1 += self.x
            check_x2 += self.x
            check_y1 += self.y
            check_y2 += self.y

            # should it be checked?
            if index == self.checked:
                # this one is checked
                use = 1
            else:
                # nope, draw an unchecked
                use = 0

            # we need some extra offset to the y for the label to align it nicely with the
            # checkbox. 
            extray = self.checkheight / 2 - label.get_height() / 2

            if self.need_internal_repaint:
                if index == self.checked or index == self.gui_checked:
                    # Fill empty
                    scenario.sdl.fill((0, 0, 0), (check_x1, check_y1,
                                                  max(Layer.checkbox[0].get_width(),
                                                      Layer.checkbox[1].get_width()),
                                                  max(Layer.checkbox[0].get_height(),
                                                      Layer.checkbox[1].get_height())))
                    # do the blit of the checkbox
                    scenario.sdl.blit(Layer.checkbox[use], (check_x1, check_y1))
            else:
                # do the blit of the checkbox and the label. also 
                scenario.sdl.blit(Layer.checkbox[use], (check_x1, check_y1))
                scenario.sdl.blit(label, (check_x2 + self.margin_x, check_y1 + extray))

            # next please
            index += 1

        # Update gui information, last!
        # TODO AttributeError: 'SetResolutionLayer' object has no attribute 'checked'
        self.gui_checked = self.checked
