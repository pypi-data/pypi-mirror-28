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
import pygame.image
from pygame.locals import *

from civil import properties
from civil.model import scenario
from civil.playfield.layer import Layer


class MenuLayer(Layer):
    """
    This class defines a layer that plugs into the PlayField. It provides code for showing a simple
    popup menu at a certain playfield position. The popup contains a number of textual items that
    are rendered as labels. When the user moves the mouse the item under the pointer is highlighted.

    The method 'getSelectedItem()' can be used to get the selected key from the menu. The method
    'updateMousePosition()' should be called when the mouse has moved.

    To use this layer set the show keymap using setKeymap() to populate the menu and setPosition()
    to update the position when the menu moves.
    """

    def __init__(self, name):
        """
        Initializes the layer.
        """
        # call superclass constructor
        Layer.__init__(self, name)

        # set default pos and size
        self.x = 100
        self.y = 100
        self.width = 200
        self.height = 100

        # create a new surface for the menu
        self.menu = None

        # no selected item yet
        self.selected = (None, None)

        # What the gui thinks is currently selected
        self.gui_selected = (None, None)

        # all labels
        self.labels = []

    def setPosition(self, position):
        """
        Sets the position where the popup should appear. The passed 'position' is the position
        where the mouse was pressed. Depending on that position the popup is shown on the
        screen. Normally the coordinate is directly taken as the location of the upper left corner
        of the popup, but it the position would make the popup fall (partially or all) outside the
        playfield then the position is adjusted to be one of the other corners.

        When this method is called we should already know the contents, and thus the dimensions of
        the menu.
        """

        # explode the positions
        x, y = position

        # check coordinates
        if x + self.width > scenario.sdl.getWidth():
            # x coordinate would be too large, flip menu to the left side
            x -= self.width

        if y + self.height > scenario.sdl.getHeight():
            # y coordinate would be too large, flip menu to the upper side
            y -= self.height

        # store locally
        self.x, self.y = x, y

    def setKeymap(self, keymap):
        """
        Sets the keymap the menu should show. The passed 'keymap' is a map that contains key
        values (such as K_s) as the keys the strings as the values. The values should be shown in
        the menu, and once an alternative is selected the key should be posted as an event.
        """

        # clear old labels and mappings
        self.labels = []

        # how many items do we have in the menu? 
        self.width = 0
        self.height = 0

        # load the font for the labels
        font = pygame.font.Font(properties.layer_menu_font, properties.layer_menu_font_size)

        # loop over all items
        for text, key, modifier in keymap:
            # create the surface and the shadow
            highlight = font.render(text, 1, properties.layer_menu_color_hi, properties.layer_menu_color_bg)
            normal = font.render(text, 1, properties.layer_menu_color_fg, properties.layer_menu_color_bg)

            # is this wider than the maximum width so far? We want to cache this here to avoid
            # having to loop all labels before painting
            if highlight.get_width() > self.width:
                # yes, we have a new maximum width
                self.width = highlight.get_width()

            # add to the total height of the labels 
            self.height += highlight.get_height() + 2

            # store the labels along with the key
            self.labels.append((key, normal, highlight, modifier))

        # allocate a surface that fits all items
        self.width += 20
        self.height += 10
        self.menu = pygame.Surface((self.width, self.height), HWSURFACE)
        self.menu.fill(properties.layer_menu_color_bg)

        # convert to a more efficient format
        self.menu = self.menu.convert()

        # no selected item yet
        self.selected = (None, None)

    def updateMousePosition(self, pos):
        """
        This method is called when the position of the mouse has been changed. Updates the
        currently highlighted menu item if needed. Returns 1 if a repaint is needed and 0 if not.
        """

        # is the position even inside the menu?
        if not self.isInside(pos[0], pos[1]):
            # not even inside
            self.selected = (None, None)

            # But there can still be a graphical change
            if self.gui_selected != self.selected:
                return 1
            return 0

        # get the mouse x and y
        mousex, mousey = pos

        # start looping from where the first item is supposed to be
        y = self.y + 5

        # loop over all labels
        for key, normal, highlight, modifier in self.labels:
            # is the y coordinate inside it?
            if y <= mousey <= y + normal.get_height():
                # do, we have a new selected item?
                if key == self.selected[0]:
                    # no, it's the same label as last time, we can go out now, as no other layer can
                    # be the selected one
                    return 0

                # store new selected label and a repaint is needed
                self.selected = (key, modifier)
                return 1

            # advance to the next label
            y += normal.get_height() + 2

        # did not change, no new item
        return 0

    def getSelectedItem(self):
        """
        Returns a tuple with thee key and modifier for the selected menu item. The key is one of
        the K_x constants, and is the key that corresponds to the menu item. If no key is selected
        then (None,None) is returned.
        """

        return self.selected

    def isInside(self, x, y):
        """
        Checks weather the mouse click at (x,y) was inside the menu or not. If it's inside returns
        1, otherwise 0.
        """

        # is it inside?
        if self.x <= x <= self.x + self.width and self.y <= y <= self.y + self.height:
            # yep, inside
            return 1

        # not inside
        return 0

    def paint(self, offset_x, offset_y, dirtyrect=None):
        """
        Paints the layer. Loops and blits out all labels. The offsets are used so that we know how
        much the map has been scrolled, but are not used. The highlighted label (the one under the
        mouse) is highlighted.
        """

        # fill a part of the background with black so that we have something to paint on
        if not self.need_internal_repaint:
            scenario.sdl.blit(self.menu, (self.x, self.y))

        # loop over all labels and paint them
        y = self.y + 5
        x = self.x + 10

        for key, normal, highlighted, modifier in self.labels:
            # is this label selected, i.e. under the mouse?
            if key == self.selected[0]:
                # yes, use the highlighted label
                scenario.sdl.blit(highlighted, (self.x + 10, y))

            elif key == self.gui_selected[0] or not self.need_internal_repaint:
                # nope, use the plain label
                scenario.sdl.blit(normal, (self.x + 10, y))

            # add the label height to the coordinate
            y += normal.get_height() + 2

        self.gui_selected = self.selected
