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

from civil.ui import widget, sdl
from civil import constants
from civil import properties
from civil.model import scenario
from civil.ui.button import Button
from civil.ui.normal_label import NormalLabel
from civil.ui.tiny_label import TinyLabel
from civil.ui.title_label import TitleLabel
from civil.ui.widget_manager import WidgetManager


class InfoUnits:
    """
    This class is used as a dialog for showing the 'order of battle', i.e. which units participate
    in the battle from the rebel and union sides. The full organizations are shown along with all
    available stats for all units.
    """

    def __init__(self):
        """
        Creates the dialog.
        """

        # create a new surface matching the display
        self.surface = sdl.surface_new(0, scenario.sdl.getWidth(), scenario.sdl.getHeight(),
                                       properties.window_depth, (0, 0, 0, 0)).convert_display()

        # create the labels for the rebel and union units
        #        rebellabels = self.createLabels ( constants.REBEL )
        #        unionlabels = self.createLabels ( constants.UNION )

        # loop over all labels we got
        #        for index in range ( len (rebellabels) ):
        #            # get the current label
        #            indent, labels = rebellabels[index]
        #
        #            # do we have one or more labels?
        #            if len (labels) == 1:
        #                # we have only one label, it is a high-level organization of some kind. Get the label
        #                label = labels [0]
        #
        #                # blit the label
        #                self.surface.blit ( label, (0, 0, label.get_width(), label.get_height()),
        #                                    (50 + indent * 50, 100 + index * label.get_height(), label.get_width(),
        #                                     label.get_height() ) )
        #            else:
        #                # it is a tuple of labels for a unit
        #                name, type, men, guns = labels
        #
        #                # blit the labels
        #                self.surface.blit ( name, (0, 0, name.get_width(), name.get_height()),
        #                                    (50 + indent * 50, 100 + index * name.get_height(), name.get_width(),
        #                                     name.get_height() ) )
        #                self.surface.blit ( type, (0, 0, type.get_width(), type.get_height()),
        #                                    (100 + indent * 50, 100 + index * type.get_height(), type.get_width(),
        #                                     type.get_height() ) )
        #                self.surface.blit ( men, (0, 0, men.get_width(), men.get_height()),
        #                                    (150 + indent * 50, 100 + index * men.get_height(), men.get_width(),
        #                                     men.get_height() ) )
        #                self.surface.blit ( guns, (0, 0, guns.get_width(), guns.get_height()),
        #                                    (200 + indent * 50, 100 + index * guns.get_height(), guns.get_width(),
        #                                     guns.get_height() ) )
        #
        # create the widget manager
        self.wm = WidgetManager(self.surface)

        # create all widgets
        self.createWidgets()

        # blit out or full surface to the main surface
        #        scenario.sdl.blit ( self.surface, (0, 0, scenario.sdl.getWidth (), scenario.sdl.getHeight () )
        #                            (0, 0,scenario.sdl.getWidth (), scenario.sdl.getHeight () ) )

        # update the whole screen
        scenario.sdl.update_rect((0, 0, scenario.sdl.getWidth(), scenario.sdl.getHeight()))

    def createWidgets(self):
        """
        Creates all widgets for the dialog.
        """
        # create the buttons for the next and previous buttons
        self.wm.register(Button(os.path.join(properties.path_dialogs, "butt-back-moff.png"),
                                os.path.join(properties.path_dialogs, "butt-back-mover.png"),
                                (850, 30), {widget.MOUSEBUTTONUP: self.prevScreen}), K_RETURN)

        # labels
        self.wm.register(TitleLabel("Scenario order of battle ", (20, 10)))

        unionlabel = NormalLabel("Union brigades", (50, 80), color=(255, 255, 0))
        self.wm.register(unionlabel)

        # create the label summarizing the units of the union side
        unionlabel = self.createSummary(constants.UNION, 200, 83)
        self.wm.register(unionlabel)

        # create labels for all union brigades and store the coordinate of the last used y-position
        lasty = self.createBrigadeLabels(constants.UNION, 80 + unionlabel.getHeight() + 30)

        rebellabel = NormalLabel("Rebel brigades", (50, lasty + 30), color=(255, 255, 0))
        self.wm.register(rebellabel)

        # create the label summarizing the units of the rebel side
        rebellabel = self.createSummary(constants.REBEL, 200, lasty + 30 + 3)
        self.wm.register(rebellabel)

        # create labels for all rebel brigades
        unionBrigades = self.createBrigadeLabels(constants.REBEL,
                                                 lasty + 30 + rebellabel.getHeight() + 30)

    def createBrigadeLabels(self, owner, starty):
        """
        Creates labels for all brigades owned by 'owner'.
        """
        index = starty

        # loop over all brigades owned by the correct player
        for brigade in list(scenario.info.brigades[owner].values()):
            # render a label and register it
            label = NormalLabel(brigade.getName(), (150, index), color=(255, 0, 255))

            # register label so that it gets managed
            self.wm.register(label)

            # also create a label with info about the brigade
            # increment the index
            index += label.getHeight() + 20

        # we're done, return the last index we used
        return index

    def createSummary(self, owner, x, y):
        """
        Creates a summary label for all the units of the specified owner.
        """

        companies = []

        # first get all companies of all the brigades
        for brigade in list(scenario.info.brigades[owner].values()):
            companies = companies + brigade.getCompanies()

        # now set some counters
        counts = {constants.INFANTRY: 0,
                  constants.CAVALRY: 0,
                  constants.ARTILLERY: 0}
        guns = 0

        # loop over all companies
        for company in companies:
            # add the men to the proper counter
            counts[company.getType()] += company.getMen()
            guns += company.getGuns()

        # now create a suitable label
        labeltext = "infantry: " + str(counts[constants.INFANTRY]) + ", cavalry: " + str(counts[constants.CAVALRY])
        labeltext += ", artillery (men/guns): " + str(counts[constants.ARTILLERY]) + "/" + str(guns)

        # create and return the label
        return TinyLabel(labeltext, (x, y))

    def run(self):
        """
        Executes the dialog and runs its internal loop until a key is pressed. When that happens
        this dialog is terminated and the method returns.
        """

        # loop forever
        while 1:
            # get next event
            event = sdl.events_wait()

            # see weather the widget manager wants to handle it
            if event != -1:
                # handle event and get the return code that tells us weather it was handled or not
                returncode = self.wm.handle(event)

                # is the event loop done?
                if returncode == widget.DONE:
                    return

    def prevScreen(self, event):
        """
        Callback triggered when the user clicks the 'Previous' button. This method simply cancels
        the event loop for this dialog's widget manager. Basically this dialog quits.
        """

        # we're done
        return widget.DONE
        # loop forever
        while True:
            # get next event
            event = sdl.events_wait()

            # see weather the widget manager wants to handle it
            # TODO self not known??
            if event != -1 and self.wm.handle(event):
                # it's handled, nothing to see here folks
                continue

            # did we gert anything?
            if event != -1 and event.get_type() == sdl.KEYDOWN:
                # we're done here, go away
                return
