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


class QuestionLayer(Layer):
    """
    This class defines a layer that plugs into the PlayField. It provides code for asking a question
    from the user and provides buttons for Ok and Cancel. A label is rendered and shown in the
    window.

    Note that this layer contains no own eventhandling, so the state of the game that has shown a
    question must track mouse/key presses and ask the layer weather a button was pressed or not.

    To use this layer set the question using setQuestion() and make sure it is shown. Check weather a
    button was pressed by calling 'isOkPressed()' and 'isCancelPressed()'.
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
        self.minwidth = 300
        self.maxwidth = 400
        self.borderx = 15
        self.bordery = 15

        # set total height of the labels 
        self.totalheight = 50

        # load a button
        try:
            self.ok = pygame.image.load(properties.layer_question_ok).convert()
        except:
            # could not load the file
            print("Could not load: " + properties.layer_question_ok + ", reason: " + repr(sys.exc_info()[1]))
            sys.exit(1)

        # load a button
        try:
            self.cancel = pygame.image.load(properties.layer_question_cancel).convert()
        except:
            # could not load the file
            print("Could not load: " + properties.layer_question_cancel + ", reason: " + repr(sys.exc_info()[1]))
            sys.exit(1)

    def setQuestion(self, question):
        """
        Sets the question that should be shown. The passed 'question' should be a list containing
        strings, one string for each line. This method will create pygame labels for the texts and
        resize the dialog to fit the width and height of all the labels. They will be drawn
        justified to the left.
        """

        # clear old labels
        self.labels = []

        # we do all calculations with the ok-button. They are identical anyway

        # set default total height of the labels 
        self.totalheight = self.ok.get_height() + self.bordery
        self.totalwidth = self.minwidth

        # load the font for the labels
        labelfont = pygame.font.Font(properties.layer_question_font,
                                     properties.layer_question_font_size)

        # loop over the global location labels we have
        for line in question:
            # create the surface and the shadow
            surface = labelfont.render(line, 1, properties.layer_question_color)

            # is this wider than the maximum width so far? We want to cache this here to avoid
            # having to loop all labels before painting
            if surface.get_width() > self.totalwidth:
                # yes, we have a new maximum width
                self.totalwidth = surface.get_width()

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
        if self.okx <= x <= self.okx + self.ok.get_width() and \
                self.oky <= y <= self.oky + self.ok.get_height():
            # yep, inside
            return 1

        # not inside
        return 0

    def isCancelPressed(self, x, y):
        """
        Checks weather the mouse click at (x,y) was inside the cancel button, i.e. weather cancel was
        pressed or not. Returns 1 if it was clicked and 0 if not.
        """
        # is it inside?
        if self.cancelx <= x <= self.cancelx + self.cancel.get_width() and \
                self.cancely <= y <= self.cancely + self.cancel.get_height():
            # yep, inside
            return 1

        # not inside
        return 0

    def paint(self, offset_x, offset_y, dirtyrect=None):
        """
        Paints the layer. Loops and blits out all labels. The offsets are used so that we know how
        much the map has been scrolled. Blits out the labels too.
        """

        # get width and height of the area
        width = self.totalwidth + 2 * self.borderx
        height = self.totalheight + 2 * self.bordery

        # get starting position
        x = scenario.sdl.getWidth() / 2 - width / 2
        y = (scenario.sdl.getHeight() - self.totalheight) / 2

        # fill a part of the background with black so that we have something to paint on
        scenario.sdl.fill((0, 0, 0), (x - 1, y - 1, width + 2, height + 2))

        # paint the border first
        self.paintBorder(x, y, width, height)

        # add the borders before we start painting labels
        x += self.borderx
        y += self.bordery

        # loop over all labels we have
        for label in self.labels:
            # now blit out the label
            scenario.sdl.blit(label, (x, y))

            # increment height
            y += label.get_height() + 3

        # get the button positions
        self.okx = scenario.sdl.getWidth() / 2 - (width / 2) + 15
        self.oky = y + 15
        self.cancelx = scenario.sdl.getWidth() / 2 + (width / 2) - self.ok.get_width() - 15
        self.cancely = y + 15

        # blit them out
        scenario.sdl.blit(self.ok, (self.okx, self.oky))
        scenario.sdl.blit(self.cancel, (self.cancelx, self.cancely))
