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

from civil.ui import widget
from civil import properties
from civil.model import scenario
from civil.ui.widget import *
from civil.ui.widget_manager import WidgetManager

# return codes used to indicate what should happen
ACCEPTED = 0
REJECTED = 1


class Dialog(Widget):
    """
    This class is used as a base class for dialogs. A dialog is a window with widgets that occupies
    the whole or part of the screen. Currently only whole screen dialogs are supported. This class
    contains the main widget manager to which widgets are added. Subclasses could override the
    method createWidgets() to create their own widgets, but that is not mandatory.

    It also contains the main event loop which is started using the method run(). The event loop
    handles events from all registered widgets and calls their callbacks.

    A dialog can have a background. It is set using setBackground() and can be either painted once
    or tiled over the entire screen.
    """

    # define a shared cache
    cache = {}

    # a normal and waiting cursor
    normalcursor = None
    waitcursor = None

    def __init__(self, surface):
        """
        Creates the dialog.
        """
        # call superclass
        Widget.__init__(self)

        # create the widget manager so that it manages our canvas and then paints out its stuff on
        # the root window
        self.wm = WidgetManager(surface, self)

        # register ourselves as a paintable object to the widget manager. This should insure that we
        # get repainted too
        self.wm.register(self)

        # create all widgets
        self.createWidgets()

        # flags used for indicating what we've done
        self.state = REJECTED

        # no background
        self.background = None
        self.tile = 0

        # load the cursors if we don't already have 'em
        if Dialog.normalcursor is None:
            # no such cursor, do it
            normaldata = properties.setup_cursor_normal_data
            normalmask = properties.setup_cursor_normal_mask
            waitdata = properties.setup_cursor_wait_data
            waitmask = properties.setup_cursor_wait_mask

            # now load them
            Dialog.waitcursor = pygame.cursors.load_xbm(waitdata, waitmask)
            Dialog.normalcursor = pygame.cursors.load_xbm(normaldata, normalmask)

        # by default we set the normal cursor
        self.setNormalCursor()

    def createWidgets(self):
        """
        Creates all widgets for the dialog. Override in subclasses.
        """
        pass

    def setBackground(self, file_name, tile=1):
        """
        Sets a background for the entire dialog. The background is loaded from the passed
        'file_name'. It is painted either only once or tiled, depending on the setting for 'tile'. A
        value of 1 will tile the image, any other value will draw the background once centered.
        """

        # do we have the wanted image in our cache?
        if file_name in Dialog.cache:
            # yep, use that instead
            self.background = Dialog.cache[file_name]

        else:
            # not in memory, try to load the surfaces
            self.background = pygame.image.load(file_name).convert()

            # store in the cache for later use
            Dialog.cache[file_name] = self.background

        # store the tiling value
        self.tile = tile

        # we're dirty now
        self.dirty = 1

    def getWidth(self):
        """
        Returns the width of the dialog.
        """
        return 0

    def getHeight(self):
        """
        Returns the height of the widget.
        """
        return 0

    def getGeometry(self):
        """
        Returns the geometry of the widget. This is a tuple containing the x, y, width and height
        of the dialog. Not currently meaningful.
        """
        return self.position[0], self.position[1], 0, 0

    def isInside(self, position):
        """
        Checks weather the passed point is inside the dialog. Returns 1 if inside and 0 if
        outside. A point on the border of the widget is considered to be inside. Currently always
        returns 0.
        """
        # not inside
        return 0

    def paint(self, destination, force=0):
        """
        Method that paints the dialog. This method will simply blit out the background if one has
        been set. Override if custom painting is needed.
        """
        # are we dirty or not?
        if self.background is None or (self.dirty == 0 and force == 0):
            # not dirty, or no background nothing to do here
            return 0

        # get the dimensions of the background
        width, height = self.background.get_size()

        # should we tile or not?
        if self.tile:
            # perform tiling of the background
            for y in range(scenario.sdl.getHeight() // height + 1):
                for x in range(scenario.sdl.getWidth() // width + 1):
                    # what height should be used?
                    if y * height > scenario.sdl.getHeight():
                        # use only the missing part
                        heighty = ((y + 1) * height) - scenario.sdl.getHeight()

                    else:
                        # full height of icon
                        heighty = height

                    # what width should be used?
                    if x * width > scenario.sdl.getWidth():
                        # use only the missing part
                        widthx = ((x + 1) * width) - scenario.sdl.getWidth()

                    else:
                        # full width of icon
                        widthx = width

                        # blit it all out
                        destination.blit(self.background, (x * width, y * height))

        else:
            # no tiling, just blurt it out once
            destination.blit(self.background, self.position)

        self.dirty = 0

        # we did something, make sure the widget manager knows that
        return 1

    def run(self):
        """
        Executes the dialog and runs its internal loop until a callback returns widget.DONE. When
        that dialog is terminated this method also returns.
        """

        # loop forever
        while 1:
            # repaint the stuff if needed
            self.wm.paint()

            # get next event
            event = pygame.event.wait()

            # see weather the widget manager wants to handle it
            if event != -1:
                # handle event and get the return code that tells us weather it was handled or not
                returncode = self.wm.handle(event)

                # is the event loop done?
                if returncode == widget.DONE:
                    # disable the timer
                    self.disableTimer()

                    return self.state

    def quit(self):
        """
        Callback triggered when the player wants to quit. This can be overridden to provide
        custom quitting behaviour. The default just simply exits.
        """
        print("quitting...")

        # terminate pygame
        pygame.quit()

        # and go away
        sys.exit(0)

    def accept(self):
        """
        Accepts the dialog. Will close it and return from it's event loop with the return status
        'dialog.ACCEPTED'.
        """
        # we're accepting the dialog
        self.state = ACCEPTED

        return widget.DONE

    def reject(self, ):
        """
        Accepts the dialog. Will close it and return from it's event loop with the return status
        'dialog.REJECTED'.
        """
        # we're cancelling the dialog
        self.state = REJECTED

        return widget.DONE

    def messagebox(self, message):
        """

        Args:
            message: 
        """
        from civil.ui import messagebox

        # failed to init network connection, show a messagebox
        messagebox.Messagebox(message)

        # repaint the stuff if needed
        self.wm.paint(force=1, clear=1)

    def enableTimer(self, ms):
        """
        Enables timer events. Calling this method will make the method timer() get called every
        'ms' milliseconds. Call disableTimer() to disable the timer.
        """

        # scenario.dispatcher.registerTimerCallback ( ms, self.timer, self )

        # just call the method, make no checks
        pygame.time.set_timer(TIMER, ms)

    def disableTimer(self):
        """
        Disables timer events.
        """
        # just call the method, make no checks
        # scenario.dispatcher.deregisterTimerCallback ( self )

        pygame.time.set_timer(TIMER, 0)

        # remove all old stale events that may have been left in the queue
        pygame.event.get([TIMER])

    def timer(self):
        """
        Callback triggered when the dialog has enabled timers and a timer fires. This should be
        overridden by subclasses to provide the needed code.
        """
        # by default we're handled
        return widget.HANDLED

    def setNormalCursor(self):
        """
        Sets the normal cursor for the setup dialogs. This is a cursor that should be used when
        the player is not waiting for something, ie. when he/she is allowed to do something. This
        cursor is always set by the constructor.
        """
        # just set it
        pygame.mouse.set_cursor(*Dialog.normalcursor)

    def setWaitCursor(self):
        """
        Enables a waiting cursor. This should be used when the game is doing something and can
        not respond to player actions.
        """
        # just set it
        pygame.mouse.set_cursor(*Dialog.waitcursor)
