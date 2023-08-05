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

import string

from pygame.locals import *

from civil.ui.button import Button
from civil.ui.dialog import *
from civil.ui.editfield import EditField
from civil.ui.listbox import Listbox
from civil.ui.lounge_select_scenario import LoungeSelectScenario
from civil.ui.normal_label import NormalLabel
from civil.ui.title_label import TitleLabel
from civil.serialization.scenario_manager import ScenarioManager


class Lounge(Dialog):
    """
    This class is used as a dialog for connecting to the lounge. The lounge is a server where the
    players can chat with other players and download scenarios. This lounge dialog is the main
    dialog that connects to the server and displays chat data.

    TODO: fill in the blanks...
    """

    def __init__(self, connection, username):
        """
        Creates the dialog.
        """
        # load the fonts too
        self.chatfont = pygame.font.Font(properties.textfont, 12)

        # store the connection
        self.connection = connection

        # join the lounge
        self.connection.send('join %s\n' % username)

        # store the username too
        self.username = username

        # we want timer events
        self.enableTimer(200)

        # now finally init the superclass. we can't do this until now, as the connection must be
        # defined before calling the superclass
        Dialog.__init__(self, scenario.sdl)

        # set our background to a tiled image
        self.setBackground(properties.window_background)

    def createWidgets(self):
        """
        Creates all widgets for the dialog. The actual widgets created depend on weather we managed
        to connect to the server or not.
        """

        # register a title
        self.wm.register(TitleLabel("Civil Lounge", (20, 10)))

        # did we manage a connection?
        if self.connection is None:
            # no connection, so we failed
            self.wm.register(NormalLabel(self.errormessage, (150, 200)))

            # create the ok button in the middle of the dialog
            self.wm.register(Button(os.path.join(properties.path_dialogs, "butt-ok-moff.png"),
                                    os.path.join(properties.path_dialogs, "butt-ok-mover.png"),
                                    (406, 650), {widget.MOUSEBUTTONUP: self.back}), K_RETURN)
            return

        # we got this far, so create all normal widgets

        # the status label
        self.wm.register(NormalLabel("Lounge guests", (55, 100)))
        self.wm.register(NormalLabel("Messages", (305, 100)))
        self.wm.register(NormalLabel("Your message", (55, 550)))

        # create listboxes for the guests and messages
        self.guests = Listbox(size=(175, 400), position=(50, 125), font=self.chatfont,
                              color=properties.normal_font_color2)
        self.messages = Listbox(size=(674, 400), position=(300, 125), font=self.chatfont,
                                color=properties.normal_font_color2)

        # register them too
        self.wm.register(self.guests)
        self.wm.register(self.messages)

        # create the editfield where the player inputs stuff
        self.ownmessage = EditField(text=' ', width=904, position=(50, 575),
                                    callbacks={widget.KEYDOWN: self.sendText})

        self.wm.register(self.ownmessage)

        # create the buttons
        self.wm.register(Button(os.path.join(properties.path_dialogs, "butt-scenario-moff.png"),
                                os.path.join(properties.path_dialogs, "butt-scenario-mover.png"),
                                (284, 650), {widget.MOUSEBUTTONUP: self.selectScenario}))

        self.wm.register(Button(os.path.join(properties.path_dialogs, "butt-back-moff.png"),
                                os.path.join(properties.path_dialogs, "butt-back-mover.png"),
                                (528, 650), {widget.MOUSEBUTTONUP: self.back}))

    def timer(self):
        """
        Callback triggered when the dialog has enabled timers and a timer fires. Checks weather
        there is any data to be read from the lounge connection. If there is something to be read
        it's read and handled. The possible actions so far are:

        * messages from lounge guests
        * leaves
        * joins
        * 'in':s which are sent when connecting.
        """

        line = ''

        # loop while there are more lines to be read from the lounge
        while 1:
            # read what there is to read
            try:
                line = self.connection.readLine()
            except IOError:
                # failed to read from the guest
                print("failed to read from lounge server, closing connection")
                self.connection.close()

                # we're actually done here

            # ok, what did we get?
            if line == '' or line is None:
                break

            # split the line so that we get the command and the 'payload'
            data = line.split()
            cmd = data[0]
            payload = "".join(data[1:])

            # what did we actually get?
            if cmd == 'msg':
                # a message
                print("message: '%s'" % payload)
                self.messages.addLabel(payload.strip())

                # repaint the stuff if needed
                self.wm.paint()

            elif cmd == 'join':
                # a new client joins
                print("join: '%s'" % payload)
                self.guests.addLabel(payload.strip())

            elif cmd == 'leave':
                # guest leaving
                print("leave: '%s'" % payload)

            elif cmd == 'in':
                # we're getting the initial list of connected guests
                print("in: '%s'" % payload)
                self.guests.addLabel(payload.strip())

            else:
                # something unknown?
                print("Lounge.timer: got unknown data: ", line)

    def sendText(self, trigger, event):
        """
        Callback triggered when the player presses a key in the editfield. If 'enter' is pressed
        the line should be sent to the lounge and then cleared.
        """
        # did we get an enter?
        if event.key != K_RETURN:
            # nope, go away
            return

        # get the text of the editfield
        text = self.ownmessage.getText().strip()

        # anything left?
        if text == '':
            # nope, so don't send it then
            return

        # send off the message
        self.connection.send('msg %s: %s\n' % (self.username, text))

        # and clear the text
        self.ownmessage.setText(' ')

    def back(self, trigger, event):
        """
        Callback triggered when the user clicks the 'Back' button. Simply closes the dialog and
        returns to the main dialog. If we're connected to the lounge a 'leave' is sent to the lounge
        first.
        """

        # do we have a connection?
        if self.connection is not None:
            # leave the lounge
            self.connection.send('leave')
            self.connection.close()

        # we're cancelling the dialog
        self.state = ACCEPTED

        return widget.DONE

    def selectScenario(self, trigger, event):
        """
        Callback triggered when the user clicks the 'Scenario' button. Brings up a dialog where
        the scenarios the server provides are shown. First talks to the server and retrieves the
        index of scenarios. This index contains information all the scenarios, and will be
        instantiated by the ScenarioManager to ScenarioIndex instances. This data is then passed to
        the dialog.
        """

        # create a scenario manager if we don't already have one. This will read the scenarios from
        # the server
        manager = ScenarioManager()

        try:
            # retrieve the index file about all scenarios from the lounge
            manager.retrieveScenarios(self.connection)

            print("Lounge.selectScenario: got info about %d scenarios" % len(manager.getScenarios()))

            # now we can create and
            LoungeSelectScenario(manager, self.connection).run()

            # ok, dialog executed, nothing to do then but a repaint
            self.wm.paint(force=1, clear=1)

        except:
            raise
