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


class Plugin:
    """
    Superclass for all plugins. It mainly defines an interface that inheriting plugins should
    use. A plugin is a class that performs some specific task in response to something the user does
    with the mouse in the map. The plugins can manipulate the map somehow or do something else.


    The methods in this class let the plugin react to various mouse events.
    """

    def __init__(self, name, longExplanation):
        self.name = name
        self.longExplanation = longExplanation

    def leftMousePressed(self):
        """
        Handles an event when the left mouse button has been pressed in the map. Should be
        overridden by the plugin if it wants notification of that event.
        """
        pass

    def midMousePressed(self):
        """
        Handles an event when the mid mouse button has been pressed in the map. Should be
        overridden by the plugin if it wants notification of that event.
        """
        pass

    def rightMousePressed(self):
        """
        Handles an event when the right mouse button has been pressed in the map. Should be
        overridden by  the plugin if it wants notification of that event.
        """
        pass

    def leftMouseReleased(self):
        """
        Handles an event when the left mouse button has been released in the map. Should be
        overridden by the plugin if it wants notification of that event.
        """
        pass

    def midMouseReleased(self):
        """
        Handles an event when the mid mouse button has been released in the map. Should be
        overridden by the plugin if it wants notification of that event.
        """
        pass

    def rightMouseReleased(self):
        """
        Handles an event when the right mouse button has been released in the map. Should be
        overridden by  the plugin if it wants notification of that event.
        """
        pass
