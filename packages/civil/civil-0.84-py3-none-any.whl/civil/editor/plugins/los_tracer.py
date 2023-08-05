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

from civil.editor.plugins.creator import *


class LosTracer(Plugin):
    """
    This class lets the user trace LOS (Line of sight). The start and endpoints for the trace are
    set using the mouse. By clicking the left mouse button in the map the start position is set, and
    the right button sets the end point. The line of sight is then traced from the start towards the
    end point, as long as visible.
    """

    def __init__(self):
        Plugin.__init__(self, "Los tracer", "Trace line of sight between two positions")

        # start and end positions
        self.start = None
        self.end = None

    def mapClickedLeft(self, x, y, hexx, hexy):
        """
        Handles an event when the left mouse button has been pressed in the map. Stores the
        position as the new starting point.
        """
        print("LosTracer.mapClickedLeft", x, y, hexx, hexy)

        # store the position
        self.start = (x, y)

    def mapClickedRight(self, x, y, hexx, hexy):
        """
        Handles an event when the right mouse button has been pressed in the map. Stores the
        position as the new ending point.
        """
        print("LosTracer.mapClickedRight", x, y, hexx, hexy)

        # store the position
        self.end = (x, y)


def new(iconview):
    """
    Constructor function.
    """
    return LosTracer()
