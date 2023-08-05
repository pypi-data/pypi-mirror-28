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

from PyQt5 import QtWidgets, QtCore, QtGui

from civil.editor import globals
from civil.model import scenario
from civil.editor.locationviewitem import LocationItem
from civil.model.location import Location
from civil.editor.edit_location import EditLocation


class LocationView(QtWidgets.QListView):
    """
    This class...
    """

    # menu items
    NEW = 10
    EDIT = 11
    DELETE = 12

    def __init__(self, parent):
        """
        Initializes the instance.
        """

        QtWidgets.QListView.__init__(self, parent)

        # add the columns
        self.addColumn('Name')

        # single selection and not decorated root
        self.setMultiSelection(0)
        self.setRootIsDecorated(0)

        # create the popup menu
        self.popup = QtWidgets.QMenu(self)

        self.popup.insertItem('New', self.new, QtCore.Qt.CTRL + QtCore.Qt.Key_N, LocationView.NEW)
        self.popup.insertItem('Edit', self.edit, QtCore.Qt.CTRL + QtCore.Qt.Key_E, LocationView.EDIT)
        self.popup.insertItem('Delete', self.delete, QtCore.Qt.CTRL + QtCore.Qt.Key_D, LocationView.DELETE)

    def refresh(self):
        """
        Refreshes all locations by clearing the list and regenerating it.
        """
        # clear first
        self.clear()

        # loop over all locations
        for location in scenario.info.locations:
            # create a new item
            LocationItem(self, location)

    def new(self):
        """
        Callback triggered when the user chooses 'New' from the popup menu. Will create a new
        location and add it to the global datastructures.
        """
        # create a new location
        location = Location(-1, -1, "New location")

        # create a new item for the listview
        item = LocationItem(self, location)

        # add the location to the global data
        scenario.info.locations.append(location)

    def delete(self):
        """
        Callback triggered when the user chooses 'Delete' from the popup menu. Will delete the
        currently selected location.
        """
        # what do we have under the mouse cursor?
        item = self.selectedItem()

        # did we get any item?
        if item is None:
            # nothing here
            return

        # get the deleted location
        location = item.getLocation()

        # remove the location from the global data
        scenario.info.locations.remove(location)

        # update display too
        self.takeItem(item)

    def edit(self):
        """
        Callback triggered when the user chooses 'Edit' from the popup menu. This method will
        bring up a dialog  where the properties of the selected location can be edited.
        """
        # get the current item and the company
        current = self.selectedItem()
        location = current.getLocation()

        # create and show the dialog
        if not EditLocation(self, location).exec_loop():
            # dialog was cancelled
            return

        # update the visualized data
        current.update()

    def contentsMousePressEvent(self, event):
        """
        Callback handling the fact that the user has pressed some mouse button. shows the menu on the
        right button.
        """

        # is this the right button?
        if event.button() != QtCore.Qt.RightButton:
            # nope, perform normal stuff
            QtWidgets.QListView.contentsMousePressEvent(self, event)
            return

        # what do we have under the mouse cursor?
        item = self.selectedItem()

        # did we get any item?
        if item is None:
            # no item, so the listview is empty, disable all items that should not be active
            self.popup.setItemEnabled(LocationView.EDIT, 0)
            self.popup.setItemEnabled(LocationView.DELETE, 0)

        else:
            # an item is selected, enable the items
            self.popup.setItemEnabled(LocationView.EDIT, 1)
            self.popup.setItemEnabled(LocationView.DELETE, 1)

            # show the popup
        self.popup.move(event.globalPos())
        self.popup.show()

    def contentsMouseReleaseEvent(self, event):
        """
        Callback handling the fact that the user has released a mouse button. Hides the menu on the
        right button.
        """

        # is this the right button?
        if event.button() == QtCore.Qt.RightButton:
            # just hide the popup
            self.popup.hide()

        else:
            # perform normal stuff
            QtWidgets.QListView.contentsMouseReleaseEvent(self, event)

    def mapClickedLeft(self, x, y, hexx, hexy):
        """
        Callback triggered when the map has been clicked. Sets a location at the map position. It
        gets the currently selected location (if any) and changes its position to that of the clicked hex.
        """

        print("LocationView.mapClickedLeft")

        # what do we have under the mouse cursor?
        current = self.selectedItem()

        # did we get any item?
        if current is None:
            # no location selected, go away
            return

        # get the location from the item
        location = current.getLocation()

        oldpos = location.getPosition()

        # set the new position for it
        location.setPosition((x - 16, y - 16))

        # gfx updates
        globals.mapview.paintEvent(QtGui.QPaintEvent(QtCore.QRect(oldpos[0] - 30, oldpos[1] - 30, 60, 60)))
        globals.mapview.paintEvent(QtGui.QPaintEvent(QtCore.QRect(x - 30, y - 30, 60, 60)))

    def validate(self):
        """
        Validates the part of the scenario that this view is responsible for creating. Returns a
        free text report that indicate the validation result or None if all is ok.
        """

        # nothing to do
        return None
