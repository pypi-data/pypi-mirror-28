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


class Input(state.State):
    """
    This class is a state that is used to ask the user to write a simple input text. It will add
    a new layer to the playfield and use it to display a dialog with a question and a field where
    the input text will be shown. The user can input text, click a button 'Ok' or 'Cancel' to return
    to the previous state pr press 'Escape' or 'Enter' to achieve the same result. The kay F12 can be
    used to save a screenshot.

    The proper way to use this class is:

        # ask the question
        text = input.Input ( ['Some question'], 'default text' ).run ()
        if text != None:
            # dialog was accepted
            ...
        else:
            # question was rejected
            ...

    The method 'run()' must be called, otherwise this state works just like any other state and will
    do nothing useful.

    WARNING: This state will fully grab all event handling, letting no other parts of the
    application run!
    
    
    """

    def __init__(self, labels, default=""):
        """
        Initializes the instance. Sets default values for all needed members and shows the
        question layer that contains the graphics for the dialog..
        """

        # call superclass constructor
        state.State.__init__(self)

        # set default cursor
        self.setDefaultCursor()

        # set defaults
        self.name = "input_state"

        # no text apart from the default yet
        self.text = default

        # store the cursor position
        self.cursor = len(self.text)

        # find the input layer
        self.inputlayer = scenario.playfield.getLayer("input")

        # set the labels it should show
        self.inputlayer.setQuestion(labels)
        self.inputlayer.setText(self.text)

        # and make it visible
        scenario.playfield.setVisible(self.inputlayer)

    def run(self):
        """
        Runs the main loop of the question state. This loop will totally hog the event handling
        and let no other part of the application run. Is it bad? Possibly.

        If the user presses a key that can be visualized it will be added to the internal string and
        the new text repainted. Apart from printable keys Escape, Enter and F12 are handled. The
        method returns the input text if accepted and None if rejected.
        """

        # do an initial repaint of the playfield as we've now shown the dialog. This is a little bit
        # of a hack basically ugly as sin, but it makes things so much easier.
        scenario.playfield.paint()
        scenario.sdl.update()

        # loop while we have SDL events to handle
        while 1:
            # get next event
            event = pygame.event.wait()

            # do we have a left mouse button pressed?
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                # left mouse button pressed, get event position
                xev, yev = event.pos

                # was ok pressed?
                if self.inputlayer.isOkPressed(xev, yev):
                    # yep, accept the dialog
                    return self.accept()

                # was cancel pressed?
                if self.inputlayer.isCancelPressed(xev, yev):
                    # yep, reject the dialog
                    return self.reject()


            # do we have a key pressed pressed?
            elif event.type == KEYDOWN:
                # get the key and the unicode string
                key = event.key

                # Weird fix. This is required on RedHat pygame 1.5.3??
                ev_unicode = event.str
                if type(ev_unicode) == str or type(ev_unicode) == str:
                    if ev_unicode == '':
                        ev_unicode = 0
                    else:
                        ev_unicode = ord(ev_unicode)

                value = chr(ev_unicode).encode('latin1')

                if key == K_RETURN:
                    # enter pressed, accept the dialog
                    return self.accept()

                if key == K_ESCAPE:
                    # escape pressed, reject the dialog
                    return self.reject()

                if key == K_F12:
                    # F12, save screenshot
                    self.saveScreenshot()
                    continue

                if key == K_BACKSPACE:
                    # remove one character
                    self.text = self.text[0:self.cursor - 1] + self.text[self.cursor:]

                    # update cursor position
                    if self.cursor > 0:
                        self.cursor -= 1

                elif key == K_DELETE:
                    # remove one character from the right
                    self.text = self.text[0:self.cursor] + self.text[self.cursor + 1:]

                    if self.cursor < 0:
                        self.cursor = 0

                elif key == K_TAB:
                    # ignore this
                    continue

                elif key == K_LEFT:
                    # one pos left
                    if self.cursor > 0:
                        self.cursor -= 1

                elif key == K_RIGHT:
                    # one pos right
                    if self.cursor < len(self.text):
                        self.cursor += 1

                elif key == K_HOME:
                    # move to the first position
                    self.cursor = 0

                elif key == K_END:
                    # move the the last position
                    self.cursor = len(self.text)

                elif ev_unicode != 0:
                    # a normal key pressed, merge in the text
                    self.text = self.text[0:self.cursor] + value + self.text[self.cursor:]

                    # update cursor position
                    self.cursor += 1

                # make the new text visualized in the layer
                self.inputlayer.setText(self.text)

                # update all
                scenario.playfield.needInternalRepaint(self.inputlayer)
                scenario.playfield.paint()
                scenario.sdl.update()

    def accept(self):
        """
        Accepts the dialog. Hides the dialog layer and returns the input text to indicate that
        the user accepted the dialog.
        """

        # find the layer and hide it
        scenario.playfield.setVisible(self.inputlayer, 0)

        # we're being accepted
        return self.text

    def reject(self):
        """
        Rejects the dialog.  Hides the dialog layer and returns None to indicate that the user 
        rejected the dialog.
 """

        # find the layer and hide it
        scenario.playfield.setVisible(self.inputlayer, 0)

        # we're being rejected
        return None
