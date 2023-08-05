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

from pygame.locals import *

from civil.ui.button import Button
from civil.ui.checkbox import CheckBox
from civil.ui.dialog import *
from civil.ui.tiny_label import TinyLabel
from civil.ui.title_label import TitleLabel


class SetupOpponent(Dialog):
    """
    This class is used as a dialog for letting the player select weather to run as a client or a
    server. The player can also choose to play against an AI player.

    The dialog mainly contains three checkboxes with where the player selects the opponent.
    """

    def __init__(self):
        """
        Creates the dialog.
        """
        # init superclass
        Dialog.__init__(self, scenario.sdl)

        # set our background to a tiled image
        self.setBackground(properties.window_background)

        # the default is that we are running as server, with ai. these must be changed if the
        # checkboxes below change default values
        scenario.start_server = 1
        scenario.start_ai = 1

    def createWidgets(self):
        """
        Creates all widgets for the dialog.
        """
        # labels
        self.wm.register(TitleLabel("Choose game type", (20, 10)))

        # create the version label
        version = "Version %s" % properties.version
        self.wm.register(TinyLabel(version, (15, 745)))

        # checkboxes. by default we play against the computer. if that changes the value
        # "scenario.start_ai" must also be changed
        self.server = CheckBox("Human player, start a server", os.path.join(properties.path_dialogs, "butt-radio-set.png"),
                               os.path.join(properties.path_dialogs, "butt-radio-unset.png"), position=(300, 220),
                               callbacks={widget.MOUSEBUTTONUP: self.toggleServer})
        self.client = CheckBox("Human player, connect to a server", os.path.join(properties.path_dialogs, "butt-radio-set.png"),
                               os.path.join(properties.path_dialogs, "butt-radio-unset.png"), position=(300, 265),
                               callbacks={widget.MOUSEBUTTONUP: self.toggleServer})
        self.computer = CheckBox("Computer opponent",
                                 os.path.join(properties.path_dialogs, "butt-radio-set.png"),
                                 os.path.join(properties.path_dialogs, "butt-radio-unset.png"),
                                 checked=1, position=(300, 310),
                                 callbacks={widget.MOUSEBUTTONUP: self.toggleServer})

        self.wm.register(self.server)
        self.wm.register(self.client)
        self.wm.register(self.computer)

        # buttons
        self.wm.register(Button(os.path.join(properties.path_dialogs, "butt-ok-moff.png"),
                                os.path.join(properties.path_dialogs, "butt-ok-mover.png"),
                                (284, 650), {widget.MOUSEBUTTONUP: self.ok}), K_RETURN)
        self.wm.register(Button(os.path.join(properties.path_dialogs, "butt-back-moff.png"),
                                os.path.join(properties.path_dialogs, "butt-back-mover.png"),
                                (528, 650), {widget.MOUSEBUTTONUP: self.back}))

    def toggleServer(self, trigger, event):
        """
        Callback triggered when one of the client/server checkboxes are clicked. This method
        makes sure the  other checkboxes are unchecked.
        """
        # who triggered the event?
        if trigger == self.server:
            # disable the client and ai buttons
            self.client.setChecked(0)
            self.computer.setChecked(0)

            # running as server, no ai
            scenario.start_server = 1
            scenario.start_ai = 0

        elif trigger == self.client:
            # disable the server and ai buttons
            self.server.setChecked(0)
            self.computer.setChecked(0)

            # running as client, no ai
            scenario.start_server = 0
            scenario.start_ai = 0

        else:
            # disable the server and ai buttons
            self.server.setChecked(0)
            self.client.setChecked(0)

            # running as server, with ai
            scenario.start_server = 1
            scenario.start_ai = 1

        # force a repaint as checkboxes leave stuff behind
        self.wm.paint(1)

    def ok(self, trigger, event):
        """
        Callback triggered when the user clicks the 'Ok' button. Just closes the dialog.
        """

        # we're accepting the dialog
        self.state = ACCEPTED
        return widget.DONE

    def back(self, trigger, event):
        """
        Callback triggered when the user clicks the 'Back' button. Simply closes the dialog,
        ignoring any changes.
        """
        # we're cancelling the dialog
        self.state = REJECTED

        return widget.DONE
