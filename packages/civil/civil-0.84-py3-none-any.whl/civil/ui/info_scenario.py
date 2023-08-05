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

from civil.ui import normal_label
from civil.ui.button import Button
from civil.ui.dialog import *
from civil.ui.normal_label import NormalLabel
from civil.ui.title_label import TitleLabel


class InfoScenario(Dialog):
    """
    This class is used as a dialog for showing information about the scenario. It shows the
    background information about the selected scenario. 

 """

    def __init__(self, info):
        """
        Creates the dialog. The passed 'info' is a ScenarioInfo about which the data should
        be displayed.
        """

        # store the info
        self.info = info

        # init superclass
        Dialog.__init__(self, scenario.sdl)

        # self.description =
        self.createDescription()

        # set our background to a tiled image
        self.setBackground(properties.window_background)

    def createDescription(self):
        """
        Creates the description labels. The description may be one or more lines of free text,
        and it needs to be created into a series of labels that can be blitted out. This method
        tries to separate the text into as large lines as possible and create a list of labels.
        """

        # max width and starting x and y
        width = 740
        x = 230
        y = 220

        # number of lines so far
        count = 0

        # loop over all paragraphs in the description
        for para in self.info.getDescription():
            # format the para to get rid of unwanted whitespace
            para = ' '.join(para.split())

            # temporaries
            testline = ''

            # loop over all words in the paragraph
            for word in para.split(' '):
                # store the current full line
                okline = testline

                # merge a text we use to test the width with. Don't add a ' ' if we only have one word
                # so far
                if testline == '':
                    testline = word
                else:
                    testline = testline + ' ' + word

                # get the size of the label as it would be when rendered using a normal font
                sizex, sizey = normal_label.size(testline)

                # too wide?
                if sizex > width:
                    # yep, so use the last 'good' text that fits and render a label
                    label = NormalLabel(okline, (x, y + count * 20),
                                        color=properties.normal_font_color2)

                    # register it
                    self.wm.register(label)

                    # start with a new full line that is the part that was 'too much'
                    testline = word

                    # one more label rendered
                    count += 1

            # still something in 'all' that has not made it into a full line? we add a last (short) line
            # with the extra text
            if testline != '':
                label = NormalLabel(testline, (x, y + count * 20),
                                    color=properties.normal_font_color2)

                # register it
                self.wm.register(label)

                # one more label rendered, add some empty space too
                count += 2

    def createWidgets(self):
        """
        Creates all widgets for the dialog.
        """
        # buttons
        self.wm.register(Button(os.path.join(properties.path_dialogs, "butt-ok-moff.png"),
                                os.path.join(properties.path_dialogs, "butt-ok-mover.png"),
                                (284, 650), {widget.MOUSEBUTTONUP: self.ok}), K_RETURN)
        self.wm.register(Button(os.path.join(properties.path_dialogs, "butt-forward-moff.png"),
                                os.path.join(properties.path_dialogs, "butt-forward-mover.png"),
                                (528, 650), {widget.MOUSEBUTTONUP: self.nextScreen}))

        # get the date as a string
        datestr = scenario.info.getStartDateString()

        # labels
        self.wm.register(TitleLabel("Scenario information", (20, 10)))
        self.wm.register(NormalLabel("Name: ", (50, 100)))
        self.wm.register(NormalLabel("Start date: ", (50, 130)))
        self.wm.register(NormalLabel("Location: ", (50, 160)))
        self.wm.register(NormalLabel("Turns: ", (50, 190)))
        self.wm.register(NormalLabel("Description:", (50, 220)))

        self.wm.register(NormalLabel(self.info.getName(), (230, 100),
                                     color=properties.normal_font_color2))
        self.wm.register(NormalLabel(datestr, (230, 130),
                                     color=properties.normal_font_color2))
        self.wm.register(NormalLabel(self.info.getLocation(), (230, 160),
                                     color=properties.normal_font_color2))
        self.wm.register(NormalLabel(str(self.info.getMaxTurns()), (230, 190),
                                     color=properties.normal_font_color2))

    def ok(self, trigger, event):
        """
        Callback triggered when the user clicks the 'Ok' button. Simply closes the dialog.
        """
        # we're cancelling the dialog
        self.state = ACCEPTED

        return widget.DONE

    def nextScreen(self, triggered, event):
        """
        Callback triggered when the user clicks the 'Next' button. Shows the map info
        dialog. After the dialog has been shown this dialog is repainted.
        """

        print("nextScreen")
        # run the dialog
        #        InfoMap ().run ()

        # repaint the stuff if needed
        self.wm.paint(force=1, clear=1)
