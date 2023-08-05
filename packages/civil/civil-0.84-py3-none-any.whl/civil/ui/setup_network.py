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
import socket

from pygame.locals import *

from civil.ui.button import Button
from civil.ui.dialog import *
from civil.ui.editfield import EditField
from civil.ui.messagebox import Messagebox
from civil.ui.normal_label import NormalLabel
from civil.ui.tiny_label import TinyLabel
from civil.ui.title_label import TitleLabel
from civil.net.connection import Connection


class SetupNetwork(Dialog):
    """
    This class is used as a dialog for setting up the connection to the game server. It lets the
    player choose what kind of opponent he/she is playing against. There are three choices:

    * human opponent where we are the server
    * human opponent where we connect to a server
    * ai opponent

    For the second choice this dialog will attempt to connect to the server. That may fail if the
    remote has not yet launched the server, and in that case an error is shown and the player can
    try again. For the first and third choices nothing special will be done, some settings are
    simply stored so that the server and/or ai client can later be started.
    """

    def __init__(self):
        """
        Creates the dialog.
        """
        # init superclass
        Dialog.__init__(self, scenario.sdl)

        # set our background to a tiled image
        self.setBackground(properties.window_background)

    def createWidgets(self):
        """
        Creates all widgets for the dialog. Depending on weather we're a server or a client
        different widgets will be shown.
        """

        # create the version label
        version = "Version %s" % properties.version
        self.wm.register(TinyLabel(version, (15, 745)))

        # are we a server?
        if not scenario.start_server:
            # we're running as client. need an additional label and edit field for the hostname
            self.wm.register(NormalLabel("Server runs on host: ", (250, 250)))

            self.host = EditField("localhost", 200, (500, 240))

            self.wm.register(self.host)

        # common widgets
        self.wm.register(TitleLabel("Setup network information", (20, 10)))

        self.wm.register(NormalLabel("Server uses port: ", (250, 310)))
        self.port = EditField(str(properties.network_port), 200, (500, 300))

        self.wm.register(self.port)

        # buttons
        self.wm.register(Button(os.path.join(properties.path_dialogs, "butt-ok-moff.png"),
                                os.path.join(properties.path_dialogs, "butt-ok-mover.png"),
                                (284, 650), {widget.MOUSEBUTTONUP: self.ok}), K_RETURN)
        self.wm.register(Button(os.path.join(properties.path_dialogs, "butt-back-moff.png"),
                                os.path.join(properties.path_dialogs, "butt-back-mover.png"),
                                (528, 650), {widget.MOUSEBUTTONUP: self.back}))

        # if we're supposed to start immediately then enable the timer
        if scenario.commandline_quickstart != 0:
            self.enableTimer(500)
            self.quickstart_state = 0

    def timer(self):
        """
        Callback triggered when the timer has fired. This is used if Civil is supposed to be
        started immediately without any user intervention. This will simulate a mouse click in the
        XXX button when YYY.
        """
        if 0:
            pass

        elif self.quickstart_state == 0:
            pygame.event.post(pygame.event.Event(widget.MOUSEBUTTONDOWN, {"pos": (290, 670)}))

        elif self.quickstart_state == 1:
            pygame.event.post(pygame.event.Event(widget.MOUSEBUTTONUP, {"pos": (290, 670)}))

        else:
            self.disableTimer()

        # increment state machine
        self.quickstart_state += 1

    def ok(self, trigger, event):
        """
        Callback triggered when the user clicks the 'Ok' button. Applies the changes after
        verifying the given data, and closes the dialog. Tries to connect to the remote server if
        the player is not supposed to start the server. If something fails the player may choose
        again. If some data is missing the player must choose again
        """

        # get the port. this is common for both client and server
        try:
            properties.network_port = int(self.port.getText())

            # is it valid?
            if not 1 <= properties.network_port <= 65535:
                # not a valid number, show a messagebox
                Messagebox("Invalid port number, must be in the range 1 to 65535!")

                # repaint and go away
                self.wm.paint(force=1, clear=1)
                return widget.HANDLED

        except TypeError:
            # not a valid number, show a messagebox
            Messagebox("Invalid port number!")

            # repaint and go away
            self.wm.paint(force=1, clear=1)
            return widget.HANDLED

        # are we not supposed to start a server?
        if not scenario.start_server:
            # nope, so try to connect to the server
            return self.__connectToServer()

        # all is ok, we're accepting the dialog
        self.state = ACCEPTED
        return widget.DONE

    def back(self, trigger, event):
        """
        Callback triggered when the user clicks the 'Back' button. Simply closes the dialog and
        returns to the main dialog, ignoring any changes. This is used when the player wants to
        change something.
        """
        # we're cancelling the dialog
        self.state = REJECTED

        return widget.DONE

    def __connectToServer(self):
        """
        Connects to the server. If all is ok a connection is stored in the scenario. On error a
        dialog is shown to the user and the user may try again. An error is thus not fatal in any
        way. A messagebox is shown with some info to the player that he/she should try again when the
        server is ready.
        """

        # get the name of the host
        host = self.host.getText()

        print("SetupNetwork: trying to connect to %s:%d" % (host, properties.network_port))

        # did we get a hostname?
        if host == "":
            # oops, no host given, show a messagebox
            Messagebox("No server hostname given!")

            # repaint and go away
            self.wm.paint(force=1, clear=1)
            return widget.HANDLED

        try:
            # create the socket
            new_socket = socket.socket()

            # connect to the remote system
            new_socket.connect((host, properties.network_port))

            # all ok, store the new and connected socket and the extra info
            scenario.connection = Connection(new_socket)

            # send our name
            scenario.connection.send(scenario.local_player_name + '\n')

        except:
            Messagebox("Could not connect to server, maybe the server is not ready?")

            # repaint and go away
            self.wm.paint(force=1, clear=1)

            return widget.HANDLED

        # all is ok, we're accepting the dialog
        self.state = ACCEPTED

        return widget.DONE
