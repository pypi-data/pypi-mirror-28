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

from civil.model import scenario
from civil.playfield.dialog_layer import DialogLayer


class CalculateActionLayer(DialogLayer):
    """
    This class defines a layer that plugs into the PlayField. It is used when the server is
    calculating the action data. It simply shows the user a static screen. Nothing fancy. Reacts to
    nothing.
    """

    def __init__(self, name):
        """
        Initializes the layer.
        """
        # call superclass constructor, but with no button
        DialogLayer.__init__(self, name, 300, 100)

        # set a nice title
        self.title = self.createLabel("Computing action... 0%")

    def updateProgress(self, percentage):
        """
        Updates the progress value of the title.
        """
        # set a nice new title
        self.title = self.createLabel("Computing action... %d%%" % percentage)

        print("CalculateActionLayer.updateProgress: computing action... %d%%" % percentage)

        # repaint the playfield to refresh the buttons
        scenario.playfield.needInternalRepaint(self)

    def customPaint(self):
        """
        Paints the layer by painting the contents and the calling the superclass method for doing
        the frame painting.
        """

        # get the content geometry
        x, y, width, height = self.getContentGeometry()

        # clear the old label first and fill the whole dialog to black
        scenario.sdl.fill((0, 0, 0), (x, y, width, height))

        # paint the title. the coordinates are inherited, and refer to the topleft corner of the
        # content area we're given
        scenario.sdl.blit(self.title, (self.x + self.borderx, self.y + self.bordery))
