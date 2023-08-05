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

import os

import pygame
from pygame.locals import *

from civil import properties
from civil.model import scenario


class Layer:
    """
    This class defines a drawable layer in the class Playfield. It knows how to paint itself, but
    the painting will be controlled by the Playfield. Each layer can be as big as the playfield, but
    anything bigger will never be visible.

    Visibility of layers is set in the Playfield class using the method setVisible().

    Each layer also has a name associated with it.

    This layer also provides a dictionary of icons that can be used to paint a border around certain
    parts of the layer.
    """

    # all icons used for frame. shared among instances
    top = None
    bot = None
    left = None
    right = None
    topleft = None
    topright = None
    botleft = None
    botright = None

    # sequence of id:s
    nextid = 0

    # a shared checkbox that can be used by any layer that needs it
    checkbox = None

    def __init__(self, name):
        """
        Initializes the layer.
        """
        # store the passed name and visibility
        self.name = name

        # Default values, all layers are assumed to be
        # of maximum size unless they say otherwise.
        self.x = 0
        self.y = 0

        # TODO: this won't work if we change the size of the playfield, eg. by changing the top-level
        # surface resolution. we need some method for changing the size of a layer too
        self.width = scenario.sdl.getWidth()
        self.height = scenario.sdl.getHeight()

        # get the deltas. It is probably faster to cache them here?
        self.delta_x = properties.hex_delta_x
        self.delta_y = properties.hex_delta_y

        # visibility is unknown
        self.visible = 0

        # load the frame icons
        self.loadFrameIcons()

        # store an id too
        self.id = Layer.nextid
        Layer.nextid += 1

        # Can be set/cleared by playfield.py
        # Used to update the internal graphics of a layer
        self.need_internal_repaint = 0

        # do we need to load external graphics into our static fields?
        if Layer.checkbox is None:
            # no checkbox, so we assume all gfx needs to be loaded
            Layer.checkbox = [pygame.image.load(os.path.join(properties.path_dialogs, "butt-radio-unset.png")).convert(),
                              pygame.image.load(os.path.join(properties.path_dialogs, "butt-radio-set.png")).convert()]

            # make sure they have the transparent color set (always white)
            Layer.checkbox[0].set_colorkey((255, 255, 255), RLEACCEL)
            Layer.checkbox[1].set_colorkey((255, 255, 255), RLEACCEL)

    def updateForResolutionChange(self, oldwidth, oldheight, width, height):
        """
        This method allows the layer to react to the fact that the resolution of the screen may
        have changed. Layers may need to cover a smaller (size decrease) area or larger (size
        increase) area. Layers that depend on the resolution can override this method and provide
        the needed code. The default version of this method just sets the width and height of the
        layer.
        """
        # store new width and height
        self.width = width
        self.height = height

    def center(self):
        """
        Centers the layer.
        """
        self.x = (scenario.sdl.getWidth() - self.width) / 2
        self.y = (scenario.sdl.getHeight() - self.height) / 2

    def paint(self, offset_x, offset_y, dirtyrect=None):
        """
        Paints the layer. This method should be overridden by subclasses, and will if called
        directly raise an exception NotImplementedError. The parametes 'dirtyrect' indicates the
        current area that needs to be repainted, and if set it also indicates a current clipping
        rectangle.
        """

        # raise the exception
        raise NotImplementedError("Layer.paint (): this method must be overridden")

    def isVisible(self):
        """
        Convenience method for checking weather a layer is visible or not. Returns 1 if it is, and
        0 if not. The data for this is set by the playfield when the visibility is changed there,
        and there is no setVisible() method in this class. Change visibility through the Playfield
        class.
        """
        return self.visible

    def isClickable(self):
        """
        Returns 1 if the layer is clickable, i.e. has a method handleClick(). By default the
        layers are not clickable and will return 0. Clickable layers are stored separately.
        """
        return 0

    def getName(self):
        """
        Returns the name of the layer.
        """
        return self.name

    def getBorderWidth(self):
        """
        Returns the width and height of the border that paintBorder() will paint. This method can
        be used to make sure a subclass can take the border into account when drawing/placing
        stuff.
        """
        # just return the sizes
        return Layer.left.get_width(), Layer.top.get_height()

    def getRect(self):
        """
        Returns the rectangle that surrounds the layer and its
        border.
        """
        return pygame.Rect(self.x - Layer.left.get_width(), self.y - Layer.top.get_height(),
                           self.width + Layer.left.get_width() + Layer.right.get_width(),
                           self.height + Layer.top.get_height() + Layer.bot.get_height())

    def paintBorderMinimized(self, basex, basey, width):
        """
        Paints a minimized border around the dialog. This is a border around the dialog with
        normal width, but no height at all. The border is squeezed vertically to take up as little
        space as possible.
        """
        # first fill the area inside that will not be covered by the border. this is a little narrow
        # line a few pixels high and as wide as the dialog
        scenario.sdl.fill((0, 0, 0), (basex, basey - Layer.top.get_height(),
                                      width, Layer.top.get_height() + 2))

        # paint the border with no height
        self.paintBorder(basex, basey, width, 0)

    def paintBorder(self, basex, basey, width, height):
        """
        Paints the border around the dialog.
        """

        # now some gory details. We need to blit stuff onto our frame surface to create the actual
        # frame. We first blit out the borders and the the corners. the corners then overpaint the
        # borders at proper positions

        # save a few dots
        top = Layer.top
        bot = Layer.bot
        left = Layer.left
        right = Layer.right
        topleft = Layer.topleft
        topright = Layer.topright
        botleft = Layer.botleft
        botright = Layer.botright

        # offset the starting point with as much as the border is wide. this means that the base
        # position that we got will remain at exactly that position, not offset
        basex -= Layer.left.get_width()
        basey -= Layer.top.get_height()

        # top/bottom borders

        # so far 0 pixels rendered. also get the width of the left/top border
        tmpx = 0
        tmpy = 0
        lbw = left.get_width()
        tby = top.get_height()

        while tmpx <= width:
            # what width should be used?
            if width - tmpx > top.get_width():
                # full width of icon
                scenario.sdl.blit(top, (basex + lbw + tmpx, basey))
                scenario.sdl.blit(bot, (basex + lbw + tmpx, basey + height + bot.get_height()))

            else:
                # use only part of it
                usew = width - tmpx

                # do the blits
                scenario.sdl.blit(top, (basex + lbw + tmpx, basey),
                                  (0, 0, usew, top.get_height()))
                scenario.sdl.blit(bot, (basex + lbw + tmpx, basey + height + bot.get_height()),
                                  (0, 0, usew, bot.get_height()))

            # add thw width of the label
            tmpx += top.get_width()

        # left/right borders
        while tmpy <= height:

            # what height should be used?
            if height - tmpy > left.get_height():
                # full height of icon
                scenario.sdl.blit(left, (basex, basey + tby + tmpy))
                scenario.sdl.blit(right, (basex + width + right.get_width(), basey + tby + tmpy))

            else:
                # use only the missing part
                useh = height - tmpy

                # do the blits
                scenario.sdl.blit(left, (basex, basey + tby + tmpy),
                                  (0, 0, right.get_width(), useh))

                scenario.sdl.blit(right, (basex + width + right.get_width(), basey + tby + tmpy),
                                  (0, 0, right.get_width(), useh))

            tmpy += right.get_height()

        # top left corner
        scenario.sdl.blit(topleft, (basex, basey))

        # top right corner
        scenario.sdl.blit(topright, (basex + width + topright.get_width(), basey))

        # bottom left corner
        scenario.sdl.blit(botleft, (basex, basey + height + botleft.get_height()))

        # bottom right corner
        scenario.sdl.blit(botright, (basex + width + botright.get_width(),
                                     basey + height + botright.get_height()))

        # return the offsets that the border added
        return left.get_width(), top.get_height()

    def loadFrameIcons(self):
        """
        Loads the needed icons for the frame from files. The icons are stored in static members
        so that all instances can share the same icons.
        """

        # do we already have 'em?
        if Layer.top is not None:
            # yes, no need to load them twice
            return

        # load all icons
        Layer.top = pygame.image.load(os.path.join(properties.path_dialogs, "dialog-widgetFrm-top.png")).convert()
        Layer.bot = pygame.image.load(os.path.join(properties.path_dialogs, "dialog-widgetFrm-bot.png")).convert()
        Layer.left = pygame.image.load(os.path.join(properties.path_dialogs, "dialog-widgetFrm-left.png")).convert()
        Layer.right = pygame.image.load(os.path.join(properties.path_dialogs, "dialog-widgetFrm-right.png")).convert()
        Layer.topleft = pygame.image.load(os.path.join(properties.path_dialogs, "dialog-widgetFrm-topleft.png")).convert()
        Layer.topright = pygame.image.load(os.path.join(properties.path_dialogs, "dialog-widgetFrm-topright.png")).convert()
        Layer.botleft = pygame.image.load(os.path.join(properties.path_dialogs, "dialog-widgetFrm-botleft.png")).convert()
        Layer.botright = pygame.image.load(os.path.join(properties.path_dialogs, "dialog-widgetFrm-botright.png")).convert()

        # set colorkey too
        Layer.top.set_colorkey((255, 255, 255), RLEACCEL)
        Layer.bot.set_colorkey((255, 255, 255), RLEACCEL)
        Layer.left.set_colorkey((255, 255, 255), RLEACCEL)
        Layer.right.set_colorkey((255, 255, 255), RLEACCEL)
        Layer.topleft.set_colorkey((255, 255, 255), RLEACCEL)
        Layer.topright.set_colorkey((255, 255, 255), RLEACCEL)
        Layer.botleft.set_colorkey((255, 255, 255), RLEACCEL)
        Layer.botright.set_colorkey((255, 255, 255), RLEACCEL)

    def __str__(self):
        """
        Returns a string description of the layer. This method is used for debugging.
        """
        return "%2d: %s" % (self.id, self.getName())
