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
from civil.ui.checkbox import CheckBox
from civil import constants
from civil.ui.dialog import *
from civil.ui.normal_label import NormalLabel
from civil.ui.select_scenario import SelectScenario
from civil.ui.title_label import TitleLabel


class NewGame(Dialog):
    """
    This class is used as a dialog for setting up parameters for a new game.
    """

    def __init__(self):
        """
        Creates the dialog.
        """

        # init superclass
        Dialog.__init__(self, scenario.sdl)

        # set our background to a tiled image
        self.setBackground(properties.window_background)

        # store a default theater
        self.theater = 'us-civil'

    def createWidgets(self):
        """
        Creates all widgets for the dialog.
        """

        # labels
        self.wm.register(TitleLabel("Start a new game", (10, 10)))

        self.wm.register(NormalLabel("Select the theater:", (300, 220)))

        # checkboxes, one for each theater of war
        self.wm.register(CheckBox("US Civil War, 1861-1865",
                                  os.path.join(properties.path_dialogs, "butt-radio-set.png"),
                                  os.path.join(properties.path_dialogs, "butt-radio-unset.png"),
                                  checked=1, position=(400, 270),
                                  callbacks={}))
        # extra theaters go here...

        self.wm.register(NormalLabel("Play as: ", (300, 350)))

        # checkboxes
        self.union = CheckBox("The union side",
                              os.path.join(properties.path_dialogs, "butt-radio-set.png"),
                              os.path.join(properties.path_dialogs, "butt-radio-unset.png"),
                              checked=1, position=(400, 380),
                              callbacks={widget.MOUSEBUTTONUP: self.togglePlayer})
        self.rebel = CheckBox("The rebel side", os.path.join(properties.path_dialogs, "butt-radio-set.png"),
                              os.path.join(properties.path_dialogs, "butt-radio-unset.png"), position=(400, 420),
                              callbacks={widget.MOUSEBUTTONUP: self.togglePlayer})

        # buttons
        self.wm.register(Button(os.path.join(properties.path_dialogs, "butt-scenario-moff.png"),
                                os.path.join(properties.path_dialogs, "butt-scenario-mover.png"),
                                (284, 650), {widget.MOUSEBUTTONUP: self.selectScenario}))
        self.wm.register(Button(os.path.join(properties.path_dialogs, "butt-cancel-moff.png"),
                                os.path.join(properties.path_dialogs, "butt-cancel-mover.png"),
                                (528, 650), {widget.MOUSEBUTTONUP: self.cancel}))

        # register the labels and checkboxes for management
        self.wm.register(self.rebel)
        self.wm.register(self.union)

    def selectScenario(self, widget, event):
        """
        Callback triggered when the user clicks the 'Select scenario' button.
        """

        # store the side we have
        if self.rebel.isChecked():
            # we're playing as rebel 
            scenario.local_player_id = constants.REBEL
        else:
            # we're playing as union 
            scenario.local_player_id = constants.UNION

        # create the dialog for selecting the scenario
        state = SelectScenario(self.theater).run()

        # was the dialog rejected?
        if state != REJECTED:
            # we're accepting the dialog
            self.state = ACCEPTED
            return DONE

        # repaint the stuff if needed
        self.wm.paint(force=1, clear=1)

    def togglePlayer(self, trigger, event):
        """
        Callback triggered when one of the checkboxes are clicked. This method makes sure the
        other checkboxes are unchecked.
        """
        # who triggered the event?
        if trigger == self.union:
            # disable the other button
            self.rebel.setChecked(0)

        else:
            # disable the other button
            self.union.setChecked(0)

        # force a repaint as checkboxes leave stuff behind
        self.wm.paint(1)

    def cancel(self, trigger, event):
        """
        Callback triggered when the user clicks the 'Cancel' button. Simply closes the dialog and
        returns to the main dialog, ignoring any changes.
        """
        # we're cancelling the dialog
        self.state = REJECTED

        return widget.DONE

    def updateTheater(self, theater):
        """
        Updates all data that depends on the theater. This is mainly some properties paths. This
        method creates full paths to some resources that has to be loaded depending on the theater.
        """
        # update the paths
        properties.path_units = properties.path_gfx + '/units/' + theater + '/'
        properties.path_periphery = properties.path_gfx + '/periphery/' + theater + '/'
        properties.path_cursors = properties.path_gfx + '/pointers/' + theater + '/'
