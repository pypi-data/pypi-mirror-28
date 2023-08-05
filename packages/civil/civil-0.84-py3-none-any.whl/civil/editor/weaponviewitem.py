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


class WeaponItem(QtWidgets.QListWidgetItem):
    """
    This class subclasses a normal QtWidgets.QListWidgetItem and adds needed functionality, such as keeping of
    the weapon the item represents. The weapon can be retrieved using the 'getWeapon()'
    method.
    """

    def __init__(self, parent, weapon):
        # create the strings for the item
        name = weapon.getName()
        type = weapon.getType()
        range = str(weapon.getRange())
        damage = str(weapon.getDamage())
        accuracy = str(weapon.getAccuracy())

        QtWidgets.QListWidgetItem.__init__(self, parent, name, type, range, damage, accuracy)

        # store the weapon
        self.weapon = weapon

    def getWeapon(self):
        """
        Returns the weapon this item represents.
        """
        return self.weapon

    def update(self):
        """
        Updates the labels for the item. Can be used if the weapon has changed.
        """

        # set the new labels
        self.setText(0, self.weapon.getName())
        self.setText(1, self.weapon.getType())
        self.setText(2, str(self.weapon.getRange()))
        self.setText(3, str(self.weapon.getDamage()))
        self.setText(4, str(self.weapon.getAccuracy()))
