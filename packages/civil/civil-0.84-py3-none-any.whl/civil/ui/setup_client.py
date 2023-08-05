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

import getpass

import os

import pygame.display
import pygame.surface
from pygame.locals import *

from civil.ui.button import Button
from civil.ui.checkbox import CheckBox
from civil.ui.credits import Credits
from civil.ui.dialog import *
from civil.ui.editfield import EditField
from civil.ui.lounge import Lounge
from civil.ui.lounge_setup import LoungeSetup
from civil.ui.normal_label import NormalLabel
from civil.ui.tiny_label import TinyLabel
from civil.ui.title_label import TitleLabel


class SetupClient(Dialog):
    """
    This class is used as a dialog for letting the player select a name that is shown to the other
    player. The player can also choose to run the game as fullscreen or windowed
    """

    def __init__(self):
        """
        Creates the dialog.
        """
        # init superclass
        Dialog.__init__(self, scenario.sdl)

        # set our background to a tiled image
        self.setBackground(properties.window_background)

        # not fullscreen by default
        self.use_fullscreen = 0

    def createWidgets(self):
        """
        Creates all widgets for the dialog.
        """
        # labels
        self.wm.register(TitleLabel("Welcome to Civil", (20, 10)))
        self.wm.register(NormalLabel("My name: ", (300, 220)))

        # create the version label
        version = "Version %s" % properties.version
        self.wm.register(TinyLabel(version, (15, 745)))

        # get the user name from the environment if it works
        try:
            name = getpass.getuser()
            try:
                import pwd
                # Try to get the user's first name, as given
                # in the password database
                name = pwd.getpwnam(name)[4].split()[0]
            except:
                # Ignore, and use username
                pass
        except:
            name = "My name"

        self.use_this_name = name

        # the editfields
        self.user = EditField(name, 300, (450, 215))

        # checkbox
        import os
        self.fullscreen = CheckBox("Toggle fullscreen mode", os.path.join(properties.path_dialogs, "butt-radio-set.png"),
                                   os.path.join(properties.path_dialogs, "butt-radio-unset.png"), position=(290, 295),
                                   callbacks={widget.MOUSEBUTTONUP: self.toggleFullscreen})

        self.wm.register(self.user)
        self.wm.register(self.fullscreen)

        # buttons
        self.wm.register(Button(os.path.join(properties.path_dialogs, "butt-ok-moff.png"),
                                os.path.join(properties.path_dialogs, "butt-ok-mover.png"),
                                (40, 650), {widget.MOUSEBUTTONUP: self.ok}), K_RETURN)
        self.wm.register(Button(os.path.join(properties.path_dialogs, "butt-quit-moff.png"),
                                os.path.join(properties.path_dialogs, "butt-quit-mover.png"),
                                (282, 650), {widget.MOUSEBUTTONUP: self.quitCivil}))
        self.wm.register(Button(os.path.join(properties.path_dialogs, "butt-credits-moff.png"),
                                os.path.join(properties.path_dialogs, "butt-credits-mover.png"),
                                (528, 650), {widget.MOUSEBUTTONUP: self.credits}))
        self.wm.register(Button(os.path.join(properties.path_dialogs, "butt-lounge-moff.png"),
                                os.path.join(properties.path_dialogs, "butt-lounge-mover.png"),
                                (772, 650), {widget.MOUSEBUTTONUP: self.lounge}))

        if scenario.commandline_quickstart != 0:
            self.enableTimer(500)
            self.quickstart_state = 0

    def timer(self):
        """

        """
        if 0:
            pass

        elif self.quickstart_state == 0:
            pygame.event.post(pygame.event.Event(widget.MOUSEBUTTONDOWN, {"pos": (320, 370)}))

        elif self.quickstart_state == 1:
            pygame.event.post(pygame.event.Event(widget.MOUSEBUTTONUP, {"pos": (320, 370)}))

        elif self.quickstart_state == 2:
            pygame.event.post(pygame.event.Event(widget.MOUSEBUTTONDOWN, {"pos": (50, 660)}))

        elif self.quickstart_state == 3:
            pygame.event.post(pygame.event.Event(widget.MOUSEBUTTONUP, {"pos": (50, 660)}))

        else:
            self.disableTimer()

        # increment statemachine
        self.quickstart_state += 1

    def ok(self, trigger, event):
        """
        Callback triggered when the user clicks the 'Ok' button. Applies the changes after
        verifying the given data, and closes the dialog.
        """

        # store our name, if we got anything
        if self.user.getText() == "":
            # nothing there, use the login name
            scenario.local_player_name = self.use_this_name
        else:
            scenario.local_player_name = self.user.getText()

        # we're accepting the dialog
        self.state = ACCEPTED

        return widget.DONE

    def quitCivil(self, trigger, event):
        """
        Callback triggered when the user clicks the 'Quit' button. Simply closes the dialog and
        returns to the main dialog, ignoring any changes.
        """
        # we're cancelling the dialog
        self.state = REJECTED

        return widget.DONE

    def toggleFullscreen(self, trigger, event):
        """
        Toggles the fullscreen mode.
        """
        # toggle fullscreen mode on/off
        pygame.display.toggle_fullscreen()

        # force a repaint as checkboxes leave stuff behind
        self.wm.paint(1)

    def credits(self, trigger, event):
        """
        Callback triggered when the user clicks the 'Credits' button. Executes the dialog that
        shows credits information. Then returns to this dialog.
        """

        # just create a dialog and run it
        Credits().run()

        # repaint the stuff if needed
        self.wm.paint(force=1, clear=1)

    def lounge(self, trigger, event):
        """
        Callback triggered when the user clicks the 'Lounge' button. Executes the dialog that
        contains the lounge date. Then returns to this dialog.
        """

        # just create a dialog and run it
        dialog = LoungeSetup()

        if dialog.run() != ACCEPTED:
            # the dialog was cancelled or failed, do nothing
            self.wm.paint(force=1, clear=1)
            return

        # get the connection to the lounge
        connection = dialog.getConnection()

        # accepted, so run the lounge
        Lounge(connection, self.user.getText()).run()

        # repaint the stuff if needed
        self.wm.paint(force=1, clear=1)
