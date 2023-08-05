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

from civil import properties
from civil.model import scenario
from civil.playfield.layer import Layer


class DialogLayer(Layer):
    """
    This class defines a base class for layers that need to show a dialog. This class can loads in
    and manages the icons needed for the frame and also painting it. An optional 'Ok' button can be
    shown down in the dialog.

    Override the dialog and make sure the __init__() method is called, as well as the paintFrame()
    method when the frame should be painted.
    """

    # used font
    font = None

    def __init__(self, name, width, height, buttonpath=None):
        """
        Initializes the layer.
        """
        # call superclass constructor
        Layer.__init__(self, name)

        # default borders
        self.borderx = 15
        self.bordery = 15

        # do we have a button?
        if buttonpath is not None:
            self.hasbutton = 1
        else:
            self.hasbutton = 0

        # do we want a button?
        if self.hasbutton:
            # load a button
            try:
                self.button = pygame.image.load(buttonpath).convert()
            except:
                # could not load the file
                raise RuntimeError("Could not load: " + buttonpath + ", reason: " + repr(sys.exc_info()[1]))

        # load the font and set its properties
        DialogLayer.font = pygame.font.Font(properties.layer_dialog_font,
                                            properties.layer_dialog_font_size)

        # finally set the size
        self.setSize(width, height)

    def updateForResolutionChange(self, oldwidth, oldheight, width, height):
        """
        This method is overridden from Layer. It makes sure the dimensions of the layer remain
        unchanged, but does center the layer.
        """

        # do the centering
        self.center()

        # update the button position
        self.fixButtonPosition()

    def fixButtonPosition(self):
        """
        Update button position for layers that actually have it.
        """
        if self.hasbutton:
            margin = 10
            # Not sure if this is a good idea
            if "margin_y" in self.__dict__:
                margin = self.margin_y

            # set button position
            self.buttonx = (scenario.sdl.getWidth() - self.button.get_width()) / 2
            self.buttony = self.y + self.contentheight + margin

    def setSize(self, width, height):
        """
        Sets a new size for the dialog. This can be useful if the size is very dynamic and
        subclasses can not calculate it before initializing this class.
        """

        # store the width and height of the contents
        self.contentwidth = width
        self.contentheight = height
        self.width = width + self.borderx * 2
        self.height = height + self.bordery * 2
        if self.hasbutton:
            self.width = max(self.width, self.button.get_width())

        self.x = (scenario.sdl.getWidth() - self.width) / 2
        self.y = (scenario.sdl.getHeight() - self.height) / 2

        self.fixButtonPosition()

        if self.hasbutton:
            # add the button height to the total height
            self.height += self.button.get_height()

    def getContentGeometry(self):
        """
        Returns a tuple (x,y,width,height) that define the position and dimensions of the content
        part of the dialog. Meant for use by subclasses.
        """
        # return the data
        return self.x, self.y, self.contentwidth, self.contentheight

    def createLabel(self, text, font=None, color=None):
        """
        Creates a label from the passed 'text' and returns it. Uses the standard font, color and
        size, unless another font is given. If 'font' and 'color' are passed they are used isntead.
        """
        # did we not get a supplied font?
        if not font:
            font = DialogLayer.font

        # Check if we have no color defined
        if not color:
            # Default color
            color = properties.layer_dialog_color

        # Create the label
        return font.render(text, 1, color)

    def createParagraphLabels(self, paragraph, maxwidth):
        """
        Creates a number of labels from the passed 'paragraph' and returns them. Uses the standard
        font, color and size. Each line is allowed to have a max width of 'maxwidth' pixels. A new
        line will be started after the max width has been reached. Returns a list of labels.
        """

        tmp = ''
        all = ''

        # a list of labels
        labels = []

        # loop over all words
        for text in paragraph.split(' '):
            # clean up any possible white space
            text = text.strip()

            # make sure we don't render empty stuff
            if text == '':
                continue

            # store the current full line
            tmp = all

            # merge a text we use to test the width with. Don't add a ' ' if we only have one word
            # so far
            if all == '':
                test = text
            else:
                test = all + ' ' + text

            # get the size of the label as it would be when rendered
            x, y = DialogLayer.font.size(test)

            # too wide?
            if x > maxwidth:
                # yep, os use the last 'good' text that fits and render a label
                labels.append(self.createLabel(all))

                # start with a new full line that is the part that was 'too much'
                all = text

            else:
                # it's ok, append new text to full line
                all = all + ' ' + text

                # still something in 'all' that has not made it into a full line? we add a last (short) line
        # with the extra text
        if all != '':
            labels.append(self.createLabel(all))

        # return the labels that we have
        return labels

    def paint(self, offset_x, offset_y, dirtyrect=None):
        """
        Paints the layer by painting all the common stuff, such as the border, background and
        button. Then calls an optional overloadable method for the custom painting.
        """

        # The common stuff should only be updated when we _don't_ have an internal update
        # I think.
        if not self.need_internal_repaint:
            # fill a part of the background with black so that we have something to paint on. note that
            # we do fill a little bit larger than needed to cover up a transparent pixel
            scenario.sdl.fill((0, 0, 0), (self.x - 1, self.y - 1, self.width + 2, self.height + 2))

            # paint the frame
            self.paintBorder(self.x, self.y, self.width, self.height)

            # and the button
            self.paintButton()

        # now call overloaded method
        self.customPaint()

    def customPaint(self):
        """
        Default method for custom repainting of the contents that does nothing
        """
        pass

    def paintButton(self):
        """
        Paints the button if the layer has one.
        """
        # paint the button if we have one
        if self.hasbutton:
            # paint it
            scenario.sdl.blit(self.button, (self.buttonx, self.buttony))

    def isOkPressed(self, x, y):
        """
        Checks weather the mouse click at (x,y) was inside the ok button, i.e. weather ok was
        pressed or not. Returns 1 if it was clicked and 0 if not.
        """

        # do we have a button at all? we can't be inside a button unless we have one
        if not self.hasbutton:
            # no button
            return 0

        # is it inside?
        if self.buttonx <= x <= self.buttonx + self.button.get_width() and \
                self.buttony <= y <= self.buttony + self.button.get_height():
            # yep, inside
            return 1

        # no inside
        return 0

    def handleLeftMousePressed(self, x, y):
        """
        Method that can be overridden by subclasses that want to have custom handling of mouse
        presses. This default version does nothing.
        """
        pass
