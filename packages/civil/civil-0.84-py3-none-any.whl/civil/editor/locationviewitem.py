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

from PyQt5 import QtWidgets


class LocationItem(QtWidgets.QListWidgetItem):
    """
    This class subclasses a normal QtWidgets.QListWidgetItem and adds needed functionality, such as keeping of
    the location the item represents. The location can be retrieved using the 'getLocation()'
    method.
    """

    def __init__(self, parent, location):
        # create the strings for the item
        name = location.getName()
        QtWidgets.QListWidgetItem.__init__(self, parent, name)

        # store the location
        self.location = location

    def getLocation(self):
        """
        Returns the location this item represents.
        """
        return self.location

    def update(self):
        """
        Updates the labels for the item. Can be used if the location has changed.
        """

        # set the new labels
        self.setText(0, self.location.getName())
