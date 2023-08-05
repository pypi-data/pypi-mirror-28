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

from civil.ui.button import Button
from civil.ui.dialog import *
from civil.ui.messagebox import Messagebox
from civil.ui.normal_label import NormalLabel


class WaitClient(Dialog):
    """
    This class is used as a dialog for showing 

 """

    def __init__(self):
        """
        Creates the dialog.
        """

        # init superclass
        Dialog.__init__(self, scenario.sdl)

        # set our background to a tiled image
        self.setBackground(properties.window_background)

        # we want timer events
        self.enableTimer(200)

    def createWidgets(self):
        """
        Creates all widgets for the dialog.
        """

        # create a message
        message = "Waiting for other player to connect..."

        # the status label
        self.wm.register(NormalLabel(message, (340, 213)))

        # create the cancel button
        self.wm.register(Button(os.path.join(properties.path_dialogs, "butt-cancel-moff.png"),
                                os.path.join(properties.path_dialogs, "butt-cancel-mover.png"),
                                (406, 650), {widget.MOUSEBUTTONUP: self.cancel}))

    def timer(self):
        """
        Callback triggered when the dialog has enabled timers and a timer fires. First tries to
        read the configuration from the connection, and if that succeeds further calls will read the
        raw scenario data. If all succeeds the dialog is accepted.
        """

        try:
            # get data about the scenario from the server, block until we get it
            scenario_line = scenario.connection.readLine(-1)

            # get data about the opponent from the server, block until we get it
            player_line = scenario.connection.readLine(-1)

        except Exception as e :
            print(e)
            # failed to get data?
            Messagebox("Error getting data from server!")

            # we're cancelling the dialog
            return self.reject()

        print("WaitClient.timer: got '%s'" % scenario_line)
        print("WaitClient.timer: got '%s'" % player_line)

        # we're done with the dialog
        return self.accept()

    def cancel(self, trigger, event):
        """
        Callback triggered when the user clicks the 'Cancel' button. Simply closes the dialog and
        returns to the main dialog, ignoring any changes.
        """

        # we're cancelling the dialog
        return self.reject()
