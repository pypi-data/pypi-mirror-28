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

import socket

from pygame.locals import *

from civil.ui.button import Button
from civil.ui.dialog import *
from civil.ui.editfield import EditField
from civil.ui.messagebox import Messagebox
from civil.ui.normal_label import NormalLabel
from civil.ui.title_label import TitleLabel
from civil.net.connection import Connection


class LoungeSetup(Dialog):
    """
    This class is used as a dialog for setting up the parameters for the connection to the game
    lounge. It asks for the host where the lounge is running and the port. The port can usually be
    left at the default value, but the host will need to be changed to a host where the server
    actually runs.

    When the player clicks 'Ok' a connection to the lounge is initialized. The dialog then
    closes. The connection can then be retrieved using 'getConnection()'.
    """

    def __init__(self):
        """
        Creates the dialog.
        """
        # init superclass
        Dialog.__init__(self, scenario.sdl)

        # set our background to a tiled image
        self.setBackground(properties.window_background)

        # by default we have no valid connection to the server
        self.connection = None

    def createWidgets(self):
        """
        Creates all widgets for the dialog.
        """

        # labels
        self.wm.register(TitleLabel("Setup lounge information", (20, 10)))
        self.wm.register(NormalLabel("Lounge port: ", (250, 300)))
        self.wm.register(NormalLabel("Lounge host: ", (250, 240)))

        # editfields
        self.host = EditField(properties.lounge_host, 200, (450, 240))
        self.port = EditField(str(properties.lounge_port), 200, (450, 300))

        self.wm.register(self.host)
        self.wm.register(self.port)

        # buttons
        self.wm.register(Button(os.path.join(properties.path_dialogs, "butt-ok-moff.png"),
                                os.path.join(properties.path_dialogs, "butt-ok-mover.png"),
                                (284, 650), {widget.MOUSEBUTTONUP: self.ok}), K_RETURN)
        self.wm.register(Button(os.path.join(properties.path_dialogs, "butt-back-moff.png"),
                                os.path.join(properties.path_dialogs, "butt-back-mover.png"),
                                (528, 650), {widget.MOUSEBUTTONUP: self.back}))

    def ok(self, trigger, event):
        """
        Callback triggered when the user clicks the 'Ok' button. Applies the changes after
        verifying the given data, and closes the dialog. Tries to connect to the lounge and if all
        is ok the dialog is accepted. If something fails the player may choose again. If some data
        is missing the player must choose again
        """

        try:
            # get the port
            port = int(self.port.getText())

            # is it valid?
            if not 1 <= port <= 65535:
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

        # init client-side socket
        return self.initSocket(port)

    def initSocket(self, port):
        """
        Connects to the server. If all is ok a connection is stored in the scenario. On error a
        dialog is shown to the user and the user may try again.
        """

        # get the name of the host
        host = self.host.getText()

        # did we get a hostname?
        if host == "":
            # oops, no host given, show a messagebox
            Messagebox("No server hostname given!")

            # repaint and go away
            self.wm.paint(force=1, clear=1)
            return widget.HANDLED

        try:
            # create the socket
            newSocket = socket.socket()

            # connect to the remote system
            newSocket.connect((host, port))

            # all ok, store the new and connected socket and the extra info
            self.connection = Connection(newSocket)

        except socket.error as error:
            Messagebox("Could not connect to lounge!")

            # repaint and go away
            self.wm.paint(force=1, clear=1)

            return widget.HANDLED

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

    def getConnection(self):
        """
        Returns the connection to the server. If it has not been successfully created this method
        will return None.
        """
        return self.connection
