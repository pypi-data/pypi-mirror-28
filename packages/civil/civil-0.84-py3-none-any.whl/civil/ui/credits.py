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

from civil.ui.button import Button
from civil.ui.dialog import *


class Credits(Dialog):
    """
    This class is used as a dialog for showing credits information. The only thing this dialog
    should do is to provide a credits image and a button to close the dialog. It would server no
    specific purpose other than showing the image.
    """

    def __init__(self):
        """
        Creates the dialog.
        """
        # init superclass
        Dialog.__init__(self, scenario.sdl)

        # set our background to a tiled image
        self.setBackground(properties.credits_background)

    def createWidgets(self):
        """
        Creates all widgets for the dialog.
        """

        # create the cancel button
        self.wm.register(Button(os.path.join(properties.path_dialogs, "butt-ok-moff.png"),
                                os.path.join(properties.path_dialogs, "butt-ok-mover.png"),
                                (750, 650), {widget.MOUSEBUTTONUP: self.ok}))

    def ok(self, trigger, event):
        """
        Callback triggered when the user clicks the 'Ok' button. Simply closes the dialog and
        returns to the main dialog.
        """

        # we're cancelling the dialog
        self.state = ACCEPTED

        return widget.DONE
