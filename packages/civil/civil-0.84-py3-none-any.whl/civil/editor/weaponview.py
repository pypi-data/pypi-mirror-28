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

from PyQt5 import QtWidgets, QtCore

from civil.editor import globals
from civil.model import scenario
from civil.editor.editor_weapon import EditorWeapon
from civil.editor.edit_weapon import EditWeapon
from civil.editor.weaponviewitem import WeaponItem


class WeaponView(QtWidgets.QListView):
    """
    This class is a view that lists all available weapons. It allows the user to edit weapons as
    well as create new ones and delete old weapons.
    """

    # a static next id
    nextid = 0

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
        self.addColumn('Type')
        self.addColumn('Range')
        self.addColumn('Damage')
        self.addColumn('Accuracy')

        # single selection and not decorated root
        self.setMultiSelection(0)
        self.setRootIsDecorated(0)

        # create the popup menu
        self.popup = QtWidgets.QMenu(self)

        self.popup.insertItem('New', self.new, QtCore.Qt.CTRL + QtCore.Qt.Key_N, WeaponView.NEW)
        self.popup.insertItem('Edit', self.edit, QtCore.Qt.CTRL + QtCore.Qt.Key_E, WeaponView.EDIT)
        self.popup.insertItem('Delete', self.delete, QtCore.Qt.CTRL + QtCore.Qt.Key_D, WeaponView.DELETE)

        # loop over all weapons and insert them into the list
        for weapon in list(globals.weapons.values()):
            # create an item and add it
            WeaponItem(self, weapon)

    def refresh(self):
        """
        Sets the weapons that are supposed to be available at the time for the scenario. The
        current date is picked from the scenario data, and all weapons that should not be present
        are removed.
        """
        # clear all weapons
        self.clear()

        # get the date for the scenario. we only need to year and month
        year, month, day, hour, minute = scenario.info.getCurrentDate()

        print(year, month)

        # loop over all weapons and check them
        for weapon in list(globals.weapons.values()):
            # is this a weapon that's present at this time?
            if weapon.isAvailable(year, month):
                # yep, it's available, create an item and add it
                WeaponItem(self, weapon)
                print("ok:", weapon)
            else:
                print("not ok:", weapon)

    def new(self):
        """
        Callback triggered when the user chooses 'New' from the popup menu. Will create a new
        weapon and add it to the global datastructures.
        """
        # create a new weapon
        weapon = EditorWeapon(id=WeaponView.nextid, name="unknown", type="rifle", range=0,
                              damage=0, accuracy=0, start_avail=(1861, 1), end_avail=(1865, 12))

        # increment the id
        WeaponView.nextid += 1

        # create a new item for the listview
        item = WeaponItem(self, weapon)

        # add the weapon to the global data
        globals.weapons[weapon.getId()] = weapon

    def delete(self):
        """
        Callback triggered when the user chooses 'Delete' from the popup menu. Will delete the
        currently selected weapon.
        """
        # what do we have under the mouse cursor?
        item = self.selectedItem()

        # did we get any item?
        if item is None:
            # nothing here
            return

        # get the deleted weapon
        weapon = item.getWeapon()

        # remove the weapon from the global data
        del globals.weapons[weapon.getId()]

        # update display too
        self.takeItem(item)

    def edit(self):
        """
        Callback triggered when the user chooses 'Edit' from the popup menu. This method will bring up a dialog
        where the properties of the selected weapon can be edited.
        """
        # get the current item and the company
        current = self.selectedItem()
        weapon = current.getWeapon()

        # create and show the dialog
        if not EditWeapon(self, weapon).exec_loop():
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
            self.popup.setItemEnabled(WeaponView.EDIT, 0)
            self.popup.setItemEnabled(WeaponView.DELETE, 0)

        else:
            # an item is selected, enable the items
            self.popup.setItemEnabled(WeaponView.EDIT, 1)
            self.popup.setItemEnabled(WeaponView.DELETE, 1)

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

    def validate(self):
        """
        Validates the part of the scenario that this view is responsible for creating. Returns a
        free text report that indicates the validation result or None if all is ok.
        """

        # nothing to do
        return None
