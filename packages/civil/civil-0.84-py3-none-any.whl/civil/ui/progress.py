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

from civil.ui.dialog import *
from civil.ui.image import Image
from civil.ui.label import Label


class Progress(Dialog):
    """
    This class is used as a messagebox to display messages to the user while he/she is setting up
    the game. A messagebox is shown centered in the screen and will fade all other contents close to
    black so that the message will be clearly visible. The message is then shown in a smaller box in
    the middle of the screen. No other dialogs or widgets will be receiving events while a
    messagebox is shown. The messagebox can be closed (and the original contents of the window
    restored) by clicking on a button.

    The messagebox attempts to format the passed string using the font 'properties.textfont' and
    present it in a nice manner.

    The messagebox works like a dialog, but the run() method does not need to be called. Instead it
    will be shown immediately when created.
    
    Use this class when you need to show some message temporarily to the user.
    """

    def __init__(self, text=""):
        """
        Creates the messagebox and shows it. The user needs to click the button to get close it.
        """

        # load the fonts
        self.font = pygame.font.Font(properties.textfont, 14)

        # init superclass
        Dialog.__init__(self, scenario.sdl)

        # load the fade and the box
        self.fade = Image(properties.progress_background, (0, 0), alpha=160)
        self.box = Image(properties.progress_dialog, (262, 200))
        self.message = Label(self.font, text, (406, 215), color=(255, 255, 0))

        # buttons. We create only the Cancel button so far, the other are created later
        #        self.button = Button ( properties.path_gfx + "butt-ok-moff.png",
        #                               properties.path_gfx + "butt-ok-mover.png",
        #                               (406, 500 ), {widget.MOUSEBUTTONUP : self.ok } )

        # register the widgets
        self.wm.register(self.fade)
        self.wm.register(self.box)
        self.wm.register(self.message)
        # self.wm.register ( self.button )

        # the last percent we updated
        self.percent = 0

    def update(self, percent):
        """
        .
        """

        # is this percent larger?
        if percent <= self.percent + 5:
            # nope, just go away
            return

        # self.message.setText ( "Loading: " + str (percent) )

        # repaint the stuff if needed
        # self.wm.paint ()

        # store new percent
        self.percent = percent

        print("Progress.update: now at %d%%" % self.percent)
