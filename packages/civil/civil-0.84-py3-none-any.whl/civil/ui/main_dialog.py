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

import os.path
import time
import socket

import pygame.font
from pygame.locals import *

from civil.ui.button import Button
from civil import constants
from civil.net.connection import Connection
from civil.model.organization import toString
from civil.ui.dialog import *
from civil.ui.load_game import LoadGame
from civil.ui.messagebox import Messagebox
from civil.ui.new_game import NewGame
from civil.ui.normal_label import NormalLabel
from civil.ui.title_label import TitleLabel
from civil.ui.wait_client import WaitClient


class MainDialog(Dialog):
    """
    This class is used as the main dialog for the application. It is launched as the first graphical
    part of civil as soon as it starts. It presents the user with a basic dialog where some actions
    can be performed through clicking buttons:

    o start a new game with a new scenario
    o load a saved game (not yet implemented)
    o set options for the game
    o start the game
    o quit
    """

    def __init__(self):
        """
        Creates the dialog.
        """

        # init superclass
        Dialog.__init__(self, scenario.sdl)

        # set our background to a tiled image
        self.setBackground(properties.window_background)

        # by default we assume we'll start a standard game
        self.game_type = constants.STANDARD

    def createWidgets(self):
        """
        Creates all widgets for the dialog.
        """
        # labels
        self.wm.register(TitleLabel("Civil scenario setup", (20, 10)))
        self.wm.register(NormalLabel("Scenario name:", (250, 180)))
        self.wm.register(NormalLabel("Scenario location:", (250, 230)))
        self.wm.register(NormalLabel("Scenario date:", (250, 280)))
        self.wm.register(NormalLabel("Play as: ", (250, 330)))
        self.wm.register(NormalLabel("My name: ", (250, 380)))

        # create the changeable labels
        self.scenarioname = NormalLabel("no scenario ", (500, 180), color=properties.normal_font_color2)
        self.scenariolocation = NormalLabel("no scenario ", (500, 230), color=properties.normal_font_color2)
        self.scenariodate = NormalLabel("no scenario ", (500, 280), color=properties.normal_font_color2)
        self.sidelabel = NormalLabel("not yet set", (500, 330), color=properties.normal_font_color2)

        # the changeable label
        self.usernamelabel = NormalLabel(scenario.local_player_name, (500, 380), color=properties.normal_font_color2)

        # register the labels for management
        self.wm.register(self.scenarioname)
        self.wm.register(self.scenariolocation)
        self.wm.register(self.scenariodate)
        self.wm.register(self.sidelabel)
        self.wm.register(self.usernamelabel)

        # buttons
        self.wm.register(Button(os.path.join(properties.path_dialogs, "butt-new-game-moff.png"),
                                os.path.join(properties.path_dialogs, "butt-new-game-mover.png"),
                                (40, 650), {widget.MOUSEBUTTONUP: self.newGame}))
        self.wm.register(Button(os.path.join(properties.path_dialogs, "butt-loadgame-moff.png"),
                                os.path.join(properties.path_dialogs, "butt-loadgame-mover.png"),
                                (282, 650), {widget.MOUSEBUTTONUP: self.loadGame}))
        self.wm.register(Button(os.path.join(properties.path_dialogs, "butt-quit-moff.png"),
                                os.path.join(properties.path_dialogs, "butt-quit-mover.png"),
                                (772, 650), {widget.MOUSEBUTTONUP: self.quitAndExit}))

    def newGame(self, trigger, event):
        """
        Callback triggered when the user clicks the 'New game' button.
        """
        # create a dialog and run it
        state = NewGame().run()

        # was it accepted or rejected?
        if state == ACCEPTED:
            # dialog was ok:ed, we should now activate the button that allows us to start the game
            self.wm.register(Button(os.path.join(properties.path_dialogs, "butt-startgame-moff.png"),
                                    os.path.join(properties.path_dialogs, "butt-startgame-mover.png"),
                                    (528, 650), {widget.MOUSEBUTTONUP: self.startGame}), K_RETURN)

            # do we noe have some info about the scenario?
            if scenario.info:
                # yep, update the label, create the text for the label

                # get the name and location
                name = scenario.info.getName()
                location = scenario.info.getLocation()
                date = scenario.info.getStartDateString()

                # set the texts
                self.scenarioname.setText(name)
                self.scenariolocation.setText(location)
                self.scenariodate.setText(date)

                # yep, so we need to update our display too, first set the labels
                self.sidelabel.setText(toString(scenario.local_player_id).capitalize())

                # we have a standard game now
                self.game_type = constants.STANDARD

        # repaint the stuff if needed
        self.wm.paint(force=1, clear=1)

    def loadGame(self, trigger, event):
        """
        Callback triggered when the user clicks the 'Load game' button. Activates the LoadGame
        dialog and lets the player choose a game to load.
        """
        # create a dialog and run it
        state = LoadGame().run()

        # was it accepted or rejected?
        if state == ACCEPTED:
            # dialog was ok:ed, we should now activate the button that allows us to start the game
            self.wm.register(Button(os.path.join(properties.path_dialogs, "butt-startgame-moff.png"),
                                    os.path.join(properties.path_dialogs, "butt-startgame-mover.png"),
                                    (528, 650), {widget.MOUSEBUTTONUP: self.startGame}))

            # do we noe have some info about the scenario?
            if scenario.info:
                # yep, update the label, create the text for the label

                # get the name and location
                name = scenario.info.getName()
                location = scenario.info.getLocation()

                # get the date and create a string
                (year, month, day, hour, minute) = scenario.info.getStartDate()

                # get the nice textual month and day extension
                month = ('x', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec')[month]
                ext = self.__dayExtension(day)

                # and create the date
                date = "%s %d%s, %d, at %02d:%02d" % (month, day, ext, year, hour, minute)

                # set the texts
                self.scenarioname.setText(name)
                self.scenariolocation.setText(location)
                self.scenariodate.setText(date)

                # yep, so we need to update our display too, first set the labels
                self.sidelabel.setText(toString(scenario.local_player_id).capitalize())

                # we have a saved game now
                self.game_type = constants.SAVED

        # repaint the stuff if needed
        self.wm.paint(force=1, clear=1)

    def quitAndExit(self, trigger, event):
        """
        Callback triggered when the user clicks the 'Quit' button. Will send the command 'quit'
        to the server and the quit.
        """
        # send our resignation
        if scenario.connection:
            scenario.connection.send('quit\n')

        # just go away
        pygame.quit()
        sys.exit(0)

    def startGame(self, trigger, event):
        """
        Callback triggered when the user clicks the 'Start game' button. Starts the server and
        the AI client and then waits until the other player (or the Ai client) has joined before
        accepting the dialog.
        """

        # set waiting cursor. we leave this cursor on until the main game has started, as those
        # parts will always set a custom cursor. by doing this we can make sure the wait cursor is
        # active until all data has been loaded and initialized
        self.setWaitCursor()

        # start the server
        self.__startServer()

        # let the server start up
        time.sleep(2)

        # now connect ourselves to the server too
        self.__connectToServer()

        # do we want an AI client?
        if scenario.start_ai:
            # yes, do it
            self.__startAI()

        # run a dialog that shows some nice info while we wait for the other player to connect and
        # the server to send us some nice info
        if WaitClient().run() == REJECTED:
            # oh damn, something went wrong...
            print("MainDialog.startGame: *** other player failed to connect... ***")
            print("MainDialog.startGame: TODO: what to do now? ***")
            return self.reject()

        # we're accepting the dialog 
        return self.accept()

    def __connectToServer(self):
        """
        Connects to the server. If all is ok a connection is stored in the scenario. TODO: this
        method is doing basically the same as the one in SetupNetwork. Redesign a bit?
        """
        try:
            # create our socket for the connection
            new_socket = socket.socket()

            # connect to the server. the server is always on our own system
            new_socket.connect(('localhost', properties.network_port))

        except socket.error as error:
            # failed to connect or send data?
            print(error)
            Messagebox("Error connecting to server!")
            return

        # all ok, store the new and connected socket and the extra info
        scenario.connection = Connection(new_socket)

        try:
            # create the initial data we should send
            data = 'setup %d %s\n' % (scenario.local_player_id, scenario.local_player_name)

            # send it
            scenario.connection.send(data)

        except:
            # failed to connect or send data?
            Messagebox("Error sending data to server!")

    def __startAI(self):
        """
        Launches the AI client, which will connect to this instance.
        """

        # BUG
        ### Duh, let the operating system go through $PATH and execute civil-ai
        ### Perhaps developers should add /home/to/the/civil/project first into their $PATH?

        # get the full path to the ai app
        command = properties.path_ai_client

        # linux, unix etc. assume that & works here.
        # if it won't work for some platform add new
        supported = {"linux": self.__startAIUnix,  # tested
                     "bsd": self.__startAIUnix,  # not tested
                     "darwin": self.__startAIOSX,  # osx
                     "windows": self.__startAIWindows  # tested
                     }

        # get the method to run
        method = supported[properties.platform_name]

        # and run it
        #method(command)
        self.__startAIWindows(command)

    def __startAIUnix(self, command):
        """
        Performs the AI starting on Linux/Unix.
        """
        # add a & to make it go in the background

        # do we have an installed version?
        # TODO paths not existing anymore
        if os.path.exists(paths.prefix + "/civil-ai"):
            # yeah, use this, add the port
            print("launching AI client: " + paths.prefix + "/civil-ai")
            os.system(paths.prefix + "/civil-ai" + " --port=%d &" % properties.network_port)
            return

        # do we have a local version in pwd
        if os.path.exists("./civil-ai"):
            # yeah, use this, add the port
            print("launching AI client: " + "./civil-ai")
            os.system("./civil-ai --port=%d &" % properties.network_port)
            return

        # are we debugging?
        if properties.debug:
            # yeah, use the direct .py file
            print("trying server: " + "./civil-ai.py")
            os.system("./civil-ai.py --port=%d &" % properties.network_port)

        else:
            # last resort, try one that is in path
            print("trying server: " + "civil-ai")
            os.system("civil-ai --port=%d &" % properties.network_port)

    def __startAIOSX(self, command):
        """
        Performs the AI starting on OSX
        """

        # Add the extension to the passed command...
        # command += '.py'

        # create the port parameter
        port = " --port=%d &" % properties.network_port

        # and launch
        os.system('/usr/local/bin/python ' + command + port)

    def __startAIWindows(self, command):
        """
        Performs the AI starting on Windows.
        """

        # add the port data
        # command += " --port=%d" % properties.network_port

        command = command.replace('\\', '/')

        # execute using the windows specific function
        # os.startfile(command)

        # start a process instead
        ai_process = AIProcess()
        ai_process.start()



    def __startServer(self):
        """
        Launches the server client, which will connect to this instance.
        """

        # BUG
        ### Duh, let the operating system go through $PATH and execute civil-server
        ### Perhaps developers should add /home/to/the/civil/project first into their $PATH?

        # get the full path to the server
        command = properties.path_server

        # we only want the basename of the path to the scenario, the type below is used by the other
        # party to figure out where the scenario is
        file_name = os.path.basename(scenario.info.getPath())

        # get the type
        type = ('standard', 'saved', 'custom')[self.game_type]

        # linux, unix etc. assume that & works here.
        # if it won't work for some platform add new
        supported = {"linux": self.__startServerUnix,  # tested
                     "bsd": self.__startServerUnix,  # not tested
                     "darwin": self.__startServerOSX,  # osx
                     "windows": self.__startServerWindows  # tested
                     }

        print("MainDialog: starting server for platform %s" % properties.platform_name)

        # get the method to run
        method = supported[properties.platform_name]

        # and run it
        #method(command, file_name, type)
        self.__startServerWindows(command, file_name, type)

    def __startServerUnix(self, command, file_name, type):
        """
        Performs the server starting on Linux/Unix.
        """
        # create the parameter list
        params = " %s %s %d &" % (file_name, type, properties.network_port)

        # add a & to make it go in the background

        # do we have an installed version?
        if os.path.exists(paths.prefix + "/civil-server"):
            # yeah, use this, add the port
            print("launching server: " + paths.prefix + "/civil-server")
            os.system(paths.prefix + "/civil-server" + params)
            return

        # do we have a local version in pwd
        if os.path.exists("./civil-server"):
            # yeah, use this, add the port
            print("launching server: " + "./civil-server")
            os.system("./civil-server " + params)
            return

        # are we debugging?
        if properties.debug:
            # yeah, use the direct .py file
            print("trying server: " + "./civil-server.py %s" % params)
            os.system("./civil-server.py %s" % params)

        else:
            # last resort, try one that is in path
            print("trying server: " + "civil-server")
            os.system("civil-server %s &" % params)

    def __startServerOSX(self, command, file_name, type):
        """
        Performs the server starting on OSX
        """

        # create the parameter list
        params = " %s %s %d &" % (file_name, type, properties.network_port)

        # and launch
        os.system('/usr/local/bin/python ' + command + params)

    def __startServerWindows(self, command, file_name, type):
        """
        Performs the server starting on Windows.
        """
        # create the parameter list
        params = " %s %s %d" % (file_name, type, properties.network_port)

        command = command.replace('\\', '/')

        # execute using the windows specific function
        # os.startfile(command + params)

        # we just start civil_start in a new process
        argv = ('civil-server', file_name, type, properties.network_port)
        print('civil-server {}'.format(argv))
        server_process = ServerProcess(argv)
        server_process.start()

import multiprocessing

class ServerProcess(multiprocessing.Process):

    def __init__(self, argv):
        super().__init__()
        self.argv = argv

    def run(self):
        sys.argv = self.argv
        from civil import civil_server
        civil_server.main()

class AIProcess(multiprocessing.Process):

    def __init__(self):
        super().__init__()

    def run(self):
        from civil import civil_ai
        civil_ai.main()


