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

from pygame.locals import *
from civil.ui.button import Button
from civil.ui.dialog import *
from civil.ui.image import Image
from civil.ui.normal_label import NormalLabel


class Messagebox(Dialog):
    """
    This class is used as a messagebox to display messages to the user while he/she is setting up
    the game. A messagebox is shown centered in the screen and will fade all other contents close to
    black so that the message will be clearly visible. The message is then shown in a smaller box in
    the middle of the screen. No other dialogs or widgets will be receiving events while a
    messagebox is shown. The messagebox can be closed (and the original contents of the window
    restored) by clicking on a button.

    The messagebox attempts to format the passed string as a NormalLabel string and present it in a
    nice manner.

    The messagebox works like a dialog, but the run() method does not need to be called. Instead it
    will be shown immediately when created.
    
    Use this class when you need to show some message temporarily to the user.
    """

    def __init__(self, text=""):
        """
        Creates the messagebox and shows it. The user needs to click the button to get close it.
        """

        # init superclass
        Dialog.__init__(self, scenario.sdl)

        # load the fade and the box
        self.fade = Image(properties.messagebox_background, (0, 0), alpha=220)
        self.box = Image(properties.messagebox_dialog, (112, 200))

        # the actual message we're showing
        self.message = NormalLabel(text, (250, 215), color=(255, 255, 0))

        # buttons. We create only the Cancel button so far, the other are created later
        self.button = Button(os.path.join(properties.path_dialogs, "butt-ok-moff.png"),
                             os.path.join(properties.path_dialogs, "butt-ok-mover.png"),
                             (406, 500), {widget.MOUSEBUTTONUP: self.ok})

        # register the widgets
        self.wm.register(self.fade)
        self.wm.register(self.box)
        self.wm.register(self.message)
        self.wm.register(self.button, K_RETURN)

        # run ourselves!
        self.run()

    def ok(self, trigger, event):
        """
        Callback triggered when the user clicks the 'Ok' button. Simply closes the messagebox.
        """
        # we're cancelling the dialog
        self.state = ACCEPTED
        return widget.DONE
