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

import pickle
import string

from pygame.locals import *

from civil.ui.button import Button
from civil.serialization.scenario_manager import ScenarioManager
from civil.serialization.scenario_parser import ScenarioParser
from civil.ui.dialog import *
from civil.ui.info_scenario import InfoScenario
from civil.ui.messagebox import Messagebox
from civil.ui.normal_label import NormalLabel
from civil.ui.title_label import TitleLabel


class LoadGame(Dialog):
    """
    This class is used as a dialog for selecting a game among saved games. The user is presented
    a list of all saved games found in properties.path_saved_games, and can select one of these.
    """

    def __init__(self):
        """
        Creates the dialog.
        """
        # define a map with the scenario names to the file names
        self.namemap = {}

        # no scenario data yet
        self.lines = None

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
        self.wm.register(TitleLabel("Select a saved game", (20, 10)))

        # start index for the labels
        x = 100
        y = 100

        # create a scenario manager even if we already have one, just to make sure it's reset
        self.scenario_manager = ScenarioManager()

        # now load info about the scenarios
        infos = self.scenario_manager.loadAllScenarioInfos(properties.path_saved_games)

        # do we even have any saved games?
        if len(infos) == 0:
            # no saved games, create a label
            text = "No saved games available"

            # create a label and register it
            self.wm.register(NormalLabel(text, (x, y)))

        else:
            # start from index 0
            index = 0

            # loop over all infos we got
            for info in infos:
                # get the name and location
                name = info.getName()
                location = info.getLocation()

                # get the date and create a string
                (year, month, day, hour, minute) = info.getStartDate()
                date = repr(year) + "." + repr(month) + "." + repr(day) + " " + repr(hour) + ":" + repr(minute)

                # create a label
                text = name + ", " + location + ", " + date

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
        Callback triggered when the user clicks the 'Ok' button. Reads in a selected scenario.
        """

        # TODO: this method is wrong, it does not handle the los_map at all!
        print ("LoadGame.ok: this method is wrong, it does not handle the los_map at all!")

        # load the scenario
        lines, los_map = self.scenario_manager.loadScenario(scenario.info.getPath())

        # did we get anything?
        if lines is None:
            # oops, bad data
            Messagebox("Could not load scenario '%s'!" % scenario.info.getName())

            # repaint and go away
            self.wm.paint(force=1, clear=1)

            # we're cancelling the dialog
            self.state = REJECTED
            return widget.DONE

        # parse the read data after flattening it to a string
        ScenarioParser().parseString("".join(lines))

        # did we get a los map? if not then the scenario was saved without a LOS map
        # TODO los_data unknown
        if los_data is None:
            # no los map, create it
            print("LoadGame.loadScenario: creating the LOS map...")
            scenario.map.createLosMap()

        else:
            # we have data, unpickle the LOS map from the given data
            print("LoadGame.loadScenario: loading the LOS map...")
            # TODO los_data unknown
            los_map = pickle.loads(los_data)

            # and assign it to the map
            scenario.map.setLosMap(los_map)

        # perform general scenario setup
        self.__setupScenario()

        # the lines are not needed anymore
        self.lines = None

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

        NOTE: this same method is copied in select_scenario.py, keep both up-todate!
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
