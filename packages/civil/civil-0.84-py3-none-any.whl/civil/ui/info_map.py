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

import pygame
import pygame.image

from civil.ui import widget, sdl
from civil.ui.button import Button
from civil import properties
from civil.model import scenario
from civil.ui.info_units import InfoUnits
from civil.ui.widget_manager import WidgetManager


class InfoMap:
    """
    This class is used as a dialog for.
    """

    def __init__(self):
        """
        Creates the dialog.
        """

        # create a new surface matching the display
        self.surface = sdl.surface_new(scenario.sdl.getSize(), 1)
        self.surface = self.surface.convert()

        # load the fonts too
        self.titlefont = pygame.font.Font(properties.title_font_name, 24)

        # create the static labels
        self.title = self.titlefont.render("Scenario map ", 1, (255, 0, 0))

        # blit 'em
        self.surface.blit(self.title, (20, 10))

        # get the map
        map = scenario.map

        # get the hexes of the map
        hexes = scenario.map.getHexes()

        # create a new surface for it. It must contain the entire map (2x2 pixels per hex) and be a
        # little wider as every even row is adjusted half a hex to the right
        self.minimap = sdl.surface_new((map.getsize_x() * 4 + 1, map.getsize_y() * 3 + 1), 1)

        # loop over the hexes in the map
        for y in range(map.getsize_y()):
            for x in range(map.getsize_x()):
                # get the hex for that position
                hex = hexes[y][x]

                # get the miniicon for the hex
                icon = hex.getMiniIcon()

                # is this an odd or even row?
                if y % 2:
                    # odd
                    self.minimap.blit(icon, (x * 4 + 2, y * 3))
                else:
                    # even
                    self.minimap.blit(icon, (x * 4, y * 3))

        # calculate the x position for the map
        xpos = scenario.sdl.getWidth() / 2 - (self.minimap.get_size()[0] / 2)

        # blit out the created surface
        self.surface.blit(self.minimap, (xpos, self.title.get_size()[1] + 40))

        # create the widget manager
        self.wm = WidgetManager(self.surface)

        # create all widgets
        self.createWidgets()

        # blit out or full surface to the main surface
        scenario.sdl.blit(self.surface, (0, 0))

        # update the whole screen
        scenario.sdl.update()
        # pygame.display.update ()

    def createWidgets(self):
        """
        Creates all widgets for the dialog.
        """
        # create the buttons for the next and previous buttons
        self.wm.register(Button(os.path.join(properties.path_dialogs, "butt-back-moff.png"),
                                os.path.join(properties.path_dialogs, "butt-back-mover.png"),
                                (284, 650), {widget.MOUSEBUTTONUP: self.prevScreen}))
        self.wm.register(Button(os.path.join(properties.path_dialogs, "butt-forward-moff.png"),
                                os.path.join(properties.path_dialogs, "butt-forward-mover.png"),
                                (528, 650), {widget.MOUSEBUTTONUP: self.nextScreen}))

    def run(self):
        """
        Executes the dialog and runs its internal loop until a key is pressed. When that happens
        shows the dialog InfoUnits. When that dialog is terminated this method also returns.
        """

        # loop forever
        while 1:
            # get next event
            event = pygame.event.wait()

            # see weather the widget manager wants to handle it
            if event != -1:
                # handle event and get the return code that tells us weather it was handled or not
                returncode = self.wm.handle(event)

                # is the event loop done?
                if returncode == widget.DONE:
                    return

    def nextScreen(self, event):
        """
        Callback triggered when the user clicks the 'Next' button. Shows the 'Order of battle'
        dialog. After the dialog has been shown this dialog is repainted.
        """

        # show the dialog
        InfoUnits().run()

        # blit out or full surface to the main surface
        scenario.sdl.blit(self.surface, (0, 0))

        # update the whole screen
        scenario.sdl.update()
        # pygame.display.update ()

        # we've handled the event
        return widget.HANDLED

    def prevScreen(self, event):
        """
        Callback triggered when the user clicks the 'Previous' button. This method simply cancels
        the event loop for this dialog's widget manager. Basically this dialog quits.
        """
        # we're done
        return widget.DONE
