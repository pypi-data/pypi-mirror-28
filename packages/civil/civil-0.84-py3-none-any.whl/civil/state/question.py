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
import pygame.event
from pygame.locals import *

from civil.state import state
from civil.model import scenario


class Question(state.State):
    """
    This class is a state that is used to show a simple question text on the screen. It will add a new
    layer to the playfield and use it to display a dialog with some question text. The user can click a
    button 'Ok' or 'Cancel' to return to the previous state pr press 'Escape' or 'Enter' to achieve
    the same result. The kay F12 can be used to save a screenshot.

    The proper way to use this class is:

        # ask the question
        if question.Question ( ['Some question'] ).run () == 1:
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

    def __init__(self, labels):
        """
        Initializes the instance. Sets default values for all needed members and shows the
        question layer that contains the graphics for the dialog..
        """

        # call superclass constructor
        state.State.__init__(self)

        # set default cursor
        self.setDefaultCursor()

        # set defaults
        self.name = "question_state"

        # find the question layer
        self.questionlayer = scenario.playfield.getLayer("question")

        # set the labels it should show
        self.questionlayer.setQuestion(labels)

        # and make it visible
        scenario.playfield.setVisible(self.questionlayer)

    def run(self):
        """
        Runs the main loop of the question state. This loop will totally hog the event handling
        and let no other part of the application run. Is it bad? Possibly. The handled events are
        only the left mouse button clicks and the keys Escape, Enter and F12. The method returns 1
        if the question was accepted and 0 if it was rejected.
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
                if self.questionlayer.isOkPressed(xev, yev):
                    # yep, accept the dialog
                    return self.accept()

                # was cancel pressed?
                if self.questionlayer.isCancelPressed(xev, yev):
                    # yep, reject the dialog
                    return self.reject()


            # do we have a key pressed pressed?
            elif event.type == KEYDOWN:
                # get the table of pressed keys
                pressed = pygame.key.get_pressed()

                if pressed[K_RETURN] != 0:
                    # enter pressed, accept the dialog
                    return self.accept()

                elif pressed[K_ESCAPE] != 0:
                    # escape pressed, reject the dialog
                    return self.reject()

                elif pressed[K_F12] != 0:
                    # F12, save screenshot
                    self.saveScreenshot()

    def accept(self):
        """
        Accepts the dialog. Hides the dialog layer and returns 1 to indicate that the user
        accepted the dialog.
        """

        # find the layer and hide it
        scenario.playfield.setVisible(self.questionlayer, 0)

        # we're being accepted
        return 1

    def reject(self):
        """
        Rejects the dialog.  Hides the dialog layer and returns 0 to indicate that the user
        rejected the dialog.
        """

        # find the layer and hide it
        scenario.playfield.setVisible(self.questionlayer, 0)

        # we're being rejected
        return 0
