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

import sys

import pygame
import pygame.image

from civil import properties
from civil.model import scenario
from civil.playfield.layer import Layer


class HelpLayer(Layer):
    """
    This class defines a layer that plugs into the PlayField. It provides code for showing a number
    of labels in a dialog in the middle of the screen. It works as a dialog box that can be used for
    help texts etc. This layer should be added last to the playfield, so that it is drawn on top ove
    everything else.

    To use this layer set the labels using setLabels() and make sure it is shown.
    """

    def __init__(self, name):
        """
        Initializes the layer.
        """
        # call superclass constructor
        Layer.__init__(self, name)

        # no labels yet
        self.labels = []

        # max width and default borders
        self.maxwidth = 100
        self.borderx = 15
        self.bordery = 15

        # set total height of the labels 
        self.totalheight = 50

        # load a button
        try:
            self.button = pygame.image.load(properties.layer_help_button).convert()
        except:
            # could not load the file
            print("Could not load: " + properties.layer_help_button + ", reason: " + repr(sys.exc_info()[1]))
            sys.exit(1)

    def setLabels(self, labels):
        """
        Sets the labels that should be shown. The passed 'labels' should be a list containing
        strings, one string for each line. This method will create pygame labels for the texts and
        resize the dialog to fit the width and height of all the labels. They will be drawn
        justified to the left.
        """

        # clear old labels
        self.labels = []

        # set default total height of the labels 
        self.totalheight = self.button.get_height() + self.bordery
        self.maxwidth = 100

        # load the font for the labels
        labelfont = pygame.font.Font(properties.layer_help_font,
                                     properties.layer_help_font_size)

        # loop over the global location labels we have
        for label in labels:
            # create the surface and the shadow
            surface = labelfont.render(label, 1, properties.layer_help_color)

            # is this wider than the maximum width so far? We want to cache this here to avoid
            # having to loop all labels before painting
            if surface.get_width() > self.maxwidth:
                # yes, we have a new maximum width
                self.maxwidth = surface.get_width()

            # add to the total height of the labels 
            self.totalheight += surface.get_height() + 3

            # store the label
            self.labels.append(surface)

    def isOkPressed(self, x, y):
        """
        Checks weather the mouse click at (x,y) was inside the ok button, i.e. weather ok was
        pressed or not. Returns 1 if it was clicked and 0 if not.
        """

        # is it inside?
        if self.buttonx <= x <= self.buttonx + self.button.get_width() and \
                self.buttony <= y <= self.buttony + self.button.get_height():
            # yep, inside
            return 1

        # no inside
        return 0

    def paint(self, offset_x, offset_y, dirtyrect=None):
        """
        Paints the layer. Loops and blits out all labels. The offsets are used so that we know how
        much the map has been scrolled.
        """

        # get width and height of the area
        width = self.maxwidth + 2 * self.borderx
        height = self.totalheight + 2 * self.bordery

        # get starting position
        x = scenario.sdl.getWidth() / 2 - width / 2
        y = (scenario.sdl.getHeight() - self.totalheight) / 2

        # fill a part of the background with black so that we have something to paint on
        scenario.sdl.fill((0, 0, 0), (x - 1, y - 1, width + 2, height + 2))

        # paint the border first
        self.paintBorder(x, y, width, height)

        # add our internal margins too before we start painting labels
        x += self.borderx
        y += self.bordery

        # loop over all labels we have
        for label in self.labels:
            # now blit out the label
            scenario.sdl.blit(label, (x, y))

            # increment height
            y += label.get_height() + 3

        # get the button position
        self.buttonx = scenario.sdl.getWidth() / 2 - self.button.get_width() / 2
        self.buttony = y + 15

        # blit it out
        scenario.sdl.blit(self.button, (self.buttonx, self.buttony))
