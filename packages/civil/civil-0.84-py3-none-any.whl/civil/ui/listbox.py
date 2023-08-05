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
from pygame.locals import *

from civil import properties
from civil.ui.widget import Widget


class Listbox(Widget):
    """
    This class defines a listbox containing labels.
    """

    # static images for the frame around the listbox
    frameicons = {}

    # names for the icons
    frameiconnames = ['topleft', 'top', 'topright', 'right', 'botright', 'bot', 'botleft', 'left']

    def __init__(self, size, font, position=(0, 0), callbacks=None, color=(255, 255, 255), alpha=255,
                 background=(0, 0, 0)):
        """
        Initializes the widget. Renders the font using the passed data.
        """

        # first call superclass constructor
        Widget.__init__(self, position, callbacks)

        # create a base surface of the given size
        self.surface = pygame.Surface(size)

        # set the alpha too
        self.surface.set_alpha(alpha, RLEACCEL)

        # store the needed data so that we can set the text later
        self.font = font
        self.color = color
        self.background = background

        # fill the listbox with the background color
        self.surface.fill(background)

        self.width, self.height = size

        # create the frame
        self.createFrame(self.width, self.height)

        # how many labels can we fit into our listbox?
        self.maxlabels = self.height / font.get_height() - 1

        # no labels yet
        self.labels = []

    def addLabel(self, text, index=-1):
        """
        Adds a new label to the listbox. The 'text' is an ascii string, not a fullblown label
        instance. If 'index' is given, i.e. != -1, then the label is added at that position in the
        listbox. If it's -1 the label is appended.
        """
        # did we get any text?
        if text == '':
            # use an empty string
            # TODO: fix this bug!
            text = ' '

        # create the surface
        label = self.font.render(text, 1, self.color)

        # where to add it?
        if index != -1:
            # somewhere else than the end
            print("Listbox.AddLabel: index!=-1 not supported yet")

        # add the label
        self.labels.append(label)

        # do we have too many labels?
        # TODO: make this an option
        if len(self.labels) > self.maxlabels:
            # yes, discard from the beginning
            self.labels = self.labels[len(self.labels) - self.maxlabels:]

        # we're dirty now
        self.dirty = 1

    def deleteLabel(self, index):
        """
        Deletes the label at 'index' in the list.
        """
        pass

    def getLabel(self, index):
        """
        Returns the text of the label at 'index'. If the index is invalid then None is
        returned. An empty label is always returned as an empty string.
        """
        pass

    def paint(self, destination, force=0):
        """
        Method that paints the listbox. This method will simply blit out the surface of the widget
        onto the destination surface. The reason for this behaviour is
        """
        # are we dirty or not?
        if not self.dirty and not force:
            # not dirty, nothing to do here
            return 0

        # we're dirty, blit out the frame with the background first
        destination.blit(self.surface, self.position)

        # start blitting labels from somewhere under the frame
        x, y = self.position
        y += Listbox.frameicons['top'].get_height() + 5
        x += Listbox.frameicons['left'].get_width() + 5

        # loop over all labels we have
        for label in self.labels:
            # blit the label
            destination.blit(label, (x, y))

            # add the label height and then some
            y += label.get_height()

        self.dirty = 0

        # we did something, make sure the widget manager knows that
        return 1

    def createFrame(self, width, height):
        """
        Creates the frame around the base surface of the listbox.
        """
        # load the frame icons
        self.loadFrameIcons()

        # now some gory details. We need to blit stuff onto our frame surface to create the actual
        # frame. We first blit out the borders and the the corners. the corners then overpaint the
        # borders at proper positions
        top = Listbox.frameicons['top']
        bot = Listbox.frameicons['bot']
        left = Listbox.frameicons['left']
        right = Listbox.frameicons['right']
        topleft = Listbox.frameicons['topleft']
        topright = Listbox.frameicons['topright']
        botleft = Listbox.frameicons['botleft']
        botright = Listbox.frameicons['botright']

        # top/bottom borders
        x = 0
        while x < width:
            # what width should be used?
            if x + top.get_width() < width:
                # full width of icon
                self.surface.blit(top, (x, 0))
                self.surface.blit(bot, (x, height - bot.get_height()))

            else:
                # use only part of it
                usew = width - x
                self.surface.blit(top, (x, 0), (0, 0, usew, bot.get_height()))

                self.surface.blit(bot, (x, height - bot.get_height()), (0, 0, usew, bot.get_height()))

            # add thw width of the label
            x += top.get_width()

        # left/right borders
        y = 0
        while y < height:
            # what height should be used?
            if y + left.get_height() < height:
                # full height of icon
                self.surface.blit(left, (0, y))
                self.surface.blit(right, (width - right.get_width(), y))

            else:
                # use only the missing part
                useh = height - y
                self.surface.blit(left, (0, y), (0, 0, right.get_width(), useh))

                self.surface.blit(right, (width - right.get_width(), y), (0, 0, right.get_width(), useh))

            y += right.get_height()

        # top left corner
        self.surface.blit(topleft, (0, 0))

        # top right corner
        self.surface.blit(topright, (width - topright.get_width(), 0))

        # bottom left corner
        self.surface.blit(botleft, (0, height - botleft.get_height()))

        # bottom right corner
        self.surface.blit(botright, (width - botright.get_width(), height - botright.get_height()))

    def loadFrameIcons(self):
        """
        Loads the needed icons for the frame from files. The icons are stored in static members
        so that all instances can share the same icons.
        """

        # do we already have icons loaded?
        if Listbox.frameicons != {}:
            return

        # base file name
        base = os.path.join(properties.path_dialogs, "dialog-widgetFrm-")

        # loop and read all the icons
        for name in Listbox.frameiconnames:
            # create the file name
            file_name = os.path.join(base, name + '.png')

            # load it 
            icon = pygame.image.load(file_name).convert()

            # set transparency and store in the map
            icon.set_colorkey((255, 255, 255), RLEACCEL)
            Listbox.frameicons[name] = icon
