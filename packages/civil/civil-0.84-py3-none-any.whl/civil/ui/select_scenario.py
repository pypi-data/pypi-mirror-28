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
from civil.serialization.scenario_manager import ScenarioManager
from civil.ui.dialog import *
from civil.ui.info_scenario import InfoScenario
from civil.ui.normal_label import NormalLabel
from civil.ui.title_label import TitleLabel


class SelectScenario(Dialog):
    """
    This class is used as a dialog for selecting a scenario among the available scenarios. It
    displays all scenarios in a nice list. The scenarios are queried from the central scenario
    manager, which takes care of loading the data.
    """

    def __init__(self, theater):
        """
        Creates the dialog.
        """

        # store the theater
        self.theater = theater

        # define a map with the scenario names to the file names
        self.namemap = {}

        # no labels yet
        self.labels_unselected = []
        self.labels_selected = []

        # init superclass
        Dialog.__init__(self, scenario.sdl)

        # set our background to a tiled image
        self.setBackground(properties.window_background)

        # the extra buttons are not yet created
        self.extra_buttons = 0

    def createWidgets(self):
        """
        Creates all widgets for the dialog.
        """
        # labels
        self.wm.register(TitleLabel("Select a scenario", (20, 10)))

        # start index for the labels
        x = 100
        y = 100

        # create a scenario manager. we do this even if we have an old one
        self.scenario_manager = ScenarioManager()

        # read in all scenario info:s
        standard = self.scenario_manager.loadAllScenarioInfos(properties.path_scenarios)

        # and all personal home made scenarios too
        custom = self.scenario_manager.loadAllScenarioInfos(properties.path_custom_scenarios)

        # start from index 0
        index = 0

        # loop over all infos we got, both the standard ones and the optional custom ones
        for info in standard + custom:
            # is the info valid for use within the game?
            if not info.isValid():
                # not valid, so get the next one. increment the index too
                index += 1
                continue

            # the scenario sure seems to be valid, get the name and location
            name = info.getName()
            location = info.getLocation()

            # get the date as a string
            datestr = info.getStartDateString()

            # create a label
            text = name + ",   " + location + ",   " + datestr

            # create a label
            label1 = NormalLabel(text, (x, y), color=properties.menu_color,
                                 callbacks={widget.MOUSEBUTTONUP: self.select})
            label2 = NormalLabel(text, (x, y), color=properties.menu_color_hi,
                                 callbacks={widget.MOUSEBUTTONUP: self.select})

            # add to our containers
            self.labels_unselected.append(label1)
            self.labels_selected.append(label2)

            # register them
            self.wm.register(label1)
            self.wm.register(label2)

            # by default we hide the highlighted version
            label2.setVisible(0)

            # make sure we know the file name from the label later
            self.namemap[text] = (index, info)

            # increment the y-offset and index
            y += label1.getHeight() + 5
            index += 1

        # buttons. We create only the Cancel button so far, the other are created later
        self.wm.register(Button(os.path.join(properties.path_dialogs, "butt-cancel-moff.png"),
                                os.path.join(properties.path_dialogs, "butt-cancel-mover.png"),
                                (650, 650), {widget.MOUSEBUTTONUP: self.cancel}))

    def select(self, trigger, event):
        """
        Callback triggered when the user clicks one of the scenario labels. Shows the yellow box
        that indicates the wanted scenario as well as the 'Ok' button (if not shown).
        """

        try:
            # well, is the triggered label an unselected label?
            found = self.labels_unselected.index(trigger)

        except ValueError:
            # ok, not found, it's an selected label then
            found = self.labels_selected.index(trigger)

        # loop over all labels we have and make sure only one label is highlighted
        for tmp in range(len(self.labels_selected)):
            if tmp != found:
                # not the selected/found one, make the unselected label visible
                self.labels_selected[tmp].setVisible(0)
                self.labels_unselected[tmp].setVisible(1)

            else:
                # selected one, show the "selected" label
                self.labels_selected[tmp].setVisible(1)
                self.labels_unselected[tmp].setVisible(0)

        # get the url and index of the clicked label
        (index, info) = self.namemap[trigger.getText()]

        # store the current scenario info
        scenario.info = info

        # now we have a selected scenario, show 'Ok' button and the 'Info' button if not already
        # created
        if not self.extra_buttons:
            self.wm.register(Button(os.path.join(properties.path_dialogs, "butt-ok-moff.png"),
                                    os.path.join(properties.path_dialogs, "butt-ok-mover.png"),
                                    (406, 650), {widget.MOUSEBUTTONUP: self.ok}), K_RETURN)

            self.wm.register(Button(os.path.join(properties.path_dialogs, "butt-info-moff.png"),
                                    os.path.join(properties.path_dialogs, "butt-info-mover.png"),
                                    (162, 650), {widget.MOUSEBUTTONUP: self.showInfo}))

            # now we have 'em
            self.extra_buttons = 1

        # we must repaint the entire dialog to get the old box cleared out
        self.wm.paint(clear=1, force=1)

        # we've selected a scenario
        self.state = ACCEPTED

        # we're done here
        return widget.HANDLED

    def ok(self, trigger, event):
        """
        Callback triggered when the user clicks the 'Ok' button. Reads in a selected scenario and
        the LOS map, parses the scenario and the map. The LOS map assigned to the main map.
        """

        # set waiting cursor
        self.setWaitCursor()

        print("SelectScenario.ok: selected scenario:", scenario.info.getPath())

        # load the scenario
        if not self.scenario_manager.loadScenario(scenario.info.getPath()):
            # oops, bad data
            self.messagebox("Could not load scenario '%s'!" % scenario.info.getName())

            # repaint and go away
            self.wm.paint(force=1, clear=1)

            # set normal cursor
            self.setNormalCursor()

            # we're cancelling the dialog
            self.state = REJECTED
            return widget.DONE

        # perform general scenario setup
        self.__setupScenario()

        # set normal cursor
        self.setNormalCursor()

        # we're ok the dialog
        self.state = ACCEPTED
        return widget.DONE

    def cancel(self, trigger, event):
        """
        Callback triggered when the user clicks the 'Cancel' button. Simply closes the dialog and
        returns to the main dialog.
        """
        # we're cancelling the dialog
        self.state = REJECTED

        return widget.DONE

    def showInfo(self, trigger, event):
        """
        Callback triggered when the user clicks the 'Info' button.
        """

        # create a new dialog and run it
        InfoScenario(scenario.info).run()

        # repaint the stuff if needed
        self.wm.paint(force=1, clear=1)

        return widget.HANDLED

    def __setupScenario(self):
        """
        Performs various scenario setup. When this method is called the scenario is already
        loaded. Sets unit visibility for the local player.

        NOTE: this same method is copied in load_game.py, keep both up-todate!
        """
        # first loop over all units and make sure they are hidden. this loop can not be combined
        # with the next loop, as we might be hiding units that have already been found to be visible
        for unit in scenario.info.units.values():
            # our unit?
            if unit.getOwner() == scenario.local_player_id:
                # our, so show it
                unit.setVisible(1)
            else:
                # enemy, make sure it's hidden
                unit.setVisible(0)
