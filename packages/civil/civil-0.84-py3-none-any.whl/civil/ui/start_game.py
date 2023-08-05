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
from civil.serialization.scenario_manager import ScenarioManager
from civil.ui.dialog import *
from civil.ui.image import Image
from civil.ui.normal_label import NormalLabel


class StartGame(Dialog):
    """
    This class is used as a dialog for showing some information to the player while the game sets up
    the network connection and receives the scenario information. Shows a centered splash screen
    with a label of information on it. The scenario is loaded and parsed.
    """

    def __init__(self):
        """
        Creates the dialog.
        """
        # init superclass
        Dialog.__init__(self, scenario.sdl)

        # set our background to a tiled image
        self.setBackground(properties.window_background)

        # no error yet
        self.error = ()

        # no lines to read yet
        self.linecount = -1
        self.lastratio = -1

        # no progress images yet
        self.progress_images = []

        # no scenario file name yet
        self.file_name = ''

        # we want timer events
        self.enableTimer(300)

    def createWidgets(self):
        """
        Creates all widgets for the dialog.
        """

        # create a message
        message = "Waiting for other player to perform setup..."

        # create the splash
        self.splash = Image(properties.dialog_splash, (272, 204))
        self.wm.register(self.splash)

        # the status label
        self.statuslabel = NormalLabel(message, (340, 213))
        self.wm.register(self.statuslabel)

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

        # read scenario config
        if not self.readConfig():
            # failed to read config data
            self.state = REJECTED
            return widget.DONE

        # now read in the scenario
        if not self.loadScenario():
            # failed to load the scenario
            self.state = REJECTED
            return widget.DONE

        # we're done here, closing the dialog
        self.state = ACCEPTED
        return widget.DONE

    def readConfig(self):
        """
        Reads the configuration data from the network connection. If all is ok sets the flag that
        indicates that the configuration is now read.
        """

        # get data about the scenario from the server, block until we get it
        scenario_line = scenario.connection.readLine(-1)

        # get data about the opponent from the server, block until we get it
        player_line = scenario.connection.readLine(-1)

        # did we get a status
        if scenario_line is None or player_line is None:
            # nothing was read, go on
            return 1

        # split up the received message into components 
        scenario_parts = scenario_line.split()
        player_parts = player_line.split()

        # the scenario consists of the scenario type and scenario file name
        # the player data consists of the id and name of the remote player

        # get all data from the read parts
        self.type = scenario_parts[0]
        self.file_name = os.path.join(properties.path_scenarios, scenario_parts[1])
        scenario.local_player_id = 1 - int(player_parts[0])
        scenario.remote_player_name = "".join(player_parts[1:])

        print("StartGame.readConfig: we got id %d, other player has name %s" % (scenario.local_player_id,
                                                                                scenario.remote_player_name))
        # all is ok
        return 1

    def loadScenario(self):
        """
        Callback triggered when the user clicks the 'Ok' button. Reads in a selected scenario and
        the LOS map, parses the scenario and the map. The LOS map assigned to the main map.
        """

        # set waiting cursor
        self.setWaitCursor()

        print("StartGame.loadScenario: loading scenario: '%s'" % self.file_name)

        # load the scenario
        if ScenarioManager().loadScenario(self.file_name) == 0:
            # oops, bad data
            self.messagebox("Could not load scenario '%s'!" % self.file_name)

            # repaint and go away
            self.wm.paint(force=1, clear=1)

            # set normal cursor
            self.setNormalCursor()

            # we're cancelling the dialog
            self.state = REJECTED
            return widget.DONE

        # set normal cursor
        self.setNormalCursor()

        # we're ok the dialog
        self.state = ACCEPTED
        return widget.DONE

    def progressCallback(self, current, total):
        """
         """
        # loop over all old progress images and deregister them. they may be left from some old
        # progress counter
        for image in self.progress_images:
            self.wm.deRegister(image)

        # clear the images now, we'll get new ones
        self.progress_images = []

        # get a ratio of the progress
        ratio = int(float(current) / total * 32.0)

        # have we advanced another 10%?
        if ratio > self.lastratio:
            # yep, let the user feel the update
            self.lastratio = ratio

            # create the position
            xpos = 352 + self.lastratio * 10
            ypos = 461

            # create a new part of the progress bar
            progress = Image(file_name=properties.progress_bar_mid, position=(xpos, ypos))
            self.wm.register(progress)

            # add to our progress images
            self.progress_images.append(progress)

            # we must repaint the entire dialog
            self.wm.paint(clear=0, force=0)

    def cancel(self, trigger, event):
        """
        Callback triggered when the user clicks the 'Cancel' button. Simply closes the dialog and
        returns to the main dialog, ignoring any changes.
        """

        # we're cancelling the dialog
        self.state = REJECTED

        return widget.DONE
