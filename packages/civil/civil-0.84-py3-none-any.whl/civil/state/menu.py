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

from civil.state import state
from civil.model import scenario


class Menu(state.State):
    """
    This class is a state that is used to show a menu on the screen. The menu is placed where the
    mouse is as given in the x, y tuple 'pos'. The entries in the menu are made up from the passed
    keymap, which contains keys and associated texts.

    The method 'run()' must be called, otherwise this state works just like any other state and will
    do nothing useful.

    WARNING: This state will fully grab all event handling, letting no other parts of the
    application run!
    """

    def __init__(self, keymap, position):
        """
        Initializes the instance. Sets default values for all needed member.
        """

        # call superclass constructor
        state.State.__init__(self)

        # set default cursor
        self.setDefaultCursor()

        # set defaults
        self.name = "menu_state"

        # find the menu layer
        self.menulayer = scenario.playfield.getLayer("menu")

        # set the keymap the menu should show
        self.menulayer.setKeymap(keymap)

        # set the position where the menu should pop up
        self.menulayer.setPosition(position)

        # and make it visible
        scenario.playfield.setVisible(self.menulayer)

    def run(self):
        """
        Runs the main loop of the question state. This loop will totally hog the event handling
        and let no other part of the application run. Is it bad? Possibly. The handled events are
        only the left mouse button clicks and the keys Escape, Enter and F12. The method returns a
        tuple with the pressed key and the posisble modifier (such as shift, alt etc). If no key was
        selected (None,None) is returned.
        """

        # do an initial repaint of the playfield as we've now shown the dialog. This is a little bit
        # of a hack basically ugly as sin, but it makes things so much easier.
        scenario.playfield.paint()
        scenario.sdl.update()

        repaintneeded = 0

        # loop while we have SDL events to handle
        while 1:
            # get next event
            event = pygame.event.wait()

            # Grab all mouse movements (if it's such an event), but use only the last one. avoids
            # flicker 
            event = self.latestMousemove(event)

            # do we have a left mouse button pressed?
            if event.type == MOUSEMOTION:
                # update the layer
                if self.menulayer.updateMousePosition(event.pos):
                    # the current item changed, so an internal
                    # repaint is needed
                    scenario.playfield.needInternalRepaint(self.menulayer)
                    # Flag that a repaint is needed
                    repaintneeded = 1

            elif event.type == MOUSEBUTTONDOWN and event.button == 1:
                # left mouse button pressed, get the pressed key, if any
                key, modifier = self.menulayer.getSelectedItem()

                # No selection if pressed outside menu window
                if not self.menulayer.isInside(event.pos[0], event.pos[1]):
                    key = None

                # find the menu layer and hide it
                scenario.playfield.setVisible(self.menulayer, 0)
                scenario.playfield.paint()
                scenario.sdl.update()

                return key, modifier

            # do we have a key pressed pressed?
            elif event.type == KEYDOWN:
                # get the table of pressed keys
                pressed = pygame.key.get_pressed()

                if pressed[K_ESCAPE] != 0:
                    # escape pressed, no menu alternative pressed, find the menu layer and hide it
                    scenario.playfield.setVisible(self.menulayer, 0)
                    scenario.playfield.paint()
                    scenario.sdl.update()
                    return None, None

                elif pressed[K_F12] != 0:
                    # F12, save screenshot
                    self.saveScreenshot()

            # loop handled, do we need a repaint?
            if repaintneeded:
                scenario.playfield.paint()
                scenario.sdl.update()

                # no repaint needed for a while
                repaintneeded = 0
