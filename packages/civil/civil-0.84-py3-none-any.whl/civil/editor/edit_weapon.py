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


class EditWeapon(QtWidgets.QDialog):
    """

    """
    def __init__(self, parent, weapon):
        QtWidgets.QDialog.__init__(self, parent, "edit weapon", 1)

        # store the weapon
        self.weapon = weapon

        self.resize(358, 243)
        self.setCaption(self.tr('Edit weapon'))
        EditWeaponLayout = QtWidgets.QVBoxLayout(self)
        EditWeaponLayout.setSpacing(6)
        EditWeaponLayout.setMargin(11)

        Layout4 = QtWidgets.QGridLayout()
        Layout4.setSpacing(6)
        Layout4.setMargin(0)

        self.accuracy = QtWidgets.QSpinBox(self, 'accuracy')
        self.accuracy.setButtonSymbols(QtWidgets.QSpinBox.UpDownArrows)
        self.accuracy.setMaxValue(100)
        self.accuracy.setMinValue(1)
        self.accuracy.setLineStep(1)
        self.accuracy.setValue(10)
        QtWidgets.QToolTip.add(self.accuracy, self.tr('Accuracy in % at max range'))

        Layout4.addWidget(self.accuracy, 4, 1)
        spacer = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        Layout4.addItem(spacer, 4, 2)
        spacer_2 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        Layout4.addItem(spacer_2, 3, 2)

        self.TextLabel4 = QtWidgets.QLabel(self, 'TextLabel4')
        self.TextLabel4.setText(self.tr('Damage:'))

        Layout4.addWidget(self.TextLabel4, 3, 0)

        self.type = QtWidgets.QComboBox(0, self, 'type')
        self.type.insertItem(self.tr('artillery'))
        self.type.insertItem(self.tr('rifle'))
        self.type.insertItem(self.tr('fastrifle'))
        QtWidgets.QToolTip.add(self.type, self.tr('Base type of the weapon'))

        Layout4.addMultiCellWidget(self.type, 1, 1, 1, 2)

        self.TextLabel2 = QtWidgets.QLabel(self, 'TextLabel2')
        self.TextLabel2.setText(self.tr('Type:'))

        Layout4.addWidget(self.TextLabel2, 1, 0)

        self.TextLabel5 = QtWidgets.QLabel(self, 'TextLabel5')
        self.TextLabel5.setText(self.tr('Accuracy:'))

        Layout4.addWidget(self.TextLabel5, 4, 0)

        self.TextLabel3 = QtWidgets.QLabel(self, 'TextLabel3')
        self.TextLabel3.setText(self.tr('Range:'))

        Layout4.addWidget(self.TextLabel3, 2, 0)

        self.TextLabel1 = QtWidgets.QLabel(self, 'TextLabel1')
        self.TextLabel1.setText(self.tr('Name:'))

        Layout4.addWidget(self.TextLabel1, 0, 0)

        self.range = QtWidgets.QSpinBox(self, 'range')
        self.range.setMaxValue(3000)
        self.range.setMinValue(1)
        self.range.setLineStep(10)
        self.range.setValue(200)
        QtWidgets.QToolTip.add(self.range, self.tr('Maximum effective range'))

        Layout4.addWidget(self.range, 2, 1)

        self.damage = QtWidgets.QSpinBox(self, 'damage')
        self.damage.setButtonSymbols(QtWidgets.QSpinBox.UpDownArrows)
        self.damage.setMaxValue(100)
        self.damage.setMinValue(1)
        self.damage.setLineStep(1)
        self.damage.setValue(10)
        QtWidgets.QToolTip.add(self.damage, self.tr('Damage delivered by full hit'))

        Layout4.addWidget(self.damage, 3, 1)

        self.name = QtWidgets.QLineEdit(self, 'name')
        QtWidgets.QToolTip.add(self.name, self.tr('Descriptive name of weapon'))

        Layout4.addMultiCellWidget(self.name, 0, 0, 1, 2)
        spacer_3 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        Layout4.addItem(spacer_3, 2, 2)
        EditWeaponLayout.addLayout(Layout4)
        spacer_4 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        EditWeaponLayout.addItem(spacer_4)

        Layout2 = QtWidgets.QHBoxLayout()
        Layout2.setSpacing(6)
        Layout2.setMargin(0)
        spacer_5 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        Layout2.addItem(spacer_5)

        self.btnok = QtWidgets.QPushButton(self, 'btnok')
        self.btnok.setSizePolicy(QtWidgets.QSizePolicy(0, 0, self.btnok.sizePolicy().hasHeightForWidth()))
        self.btnok.setText(self.tr('&Ok'))
        Layout2.addWidget(self.btnok)
        spacer_6 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        Layout2.addItem(spacer_6)

        self.btncancel = QtWidgets.QPushButton(self, 'btncancel')
        self.btncancel.setSizePolicy(QtWidgets.QSizePolicy(0, 0, self.btncancel.sizePolicy().hasHeightForWidth()))
        self.btncancel.setText(self.tr('&Cancel'))
        Layout2.addWidget(self.btncancel)
        EditWeaponLayout.addLayout(Layout2)

        # connect signals to slots
        self.connect(self.btnok, SIGNAL('clicked()'), self.ok)
        self.connect(self.btncancel, SIGNAL('clicked()'), self, SLOT('reject()'))

        # populate all info into the widgets
        self.populate()

    def populate(self):
        """
        Populates the dialog with data from the weapon. This is a separate unit so that it can be
        easily picked out and improved.
        """

        # set all data
        self.name.setText(self.weapon.getName())
        self.damage.setValue(self.weapon.getDamage())
        self.range.setValue(self.weapon.getRange())
        self.accuracy.setValue(self.weapon.getAccuracy())

        # this is a little bit of a hack, but fairly nice :)
        self.type.setCurrentItem({'artillery': 0, 'rifle': 1, 'fastrifle': 2}[self.weapon.getType()])

    def ok(self):
        """
        Callback triggered when the player clicks Ok. Stores all the data in the weapon and
        closes the dialog.
        """

        # just shove it all in
        self.weapon.setName(str(self.name.text()))
        self.weapon.setType(str(self.type.currentText()))
        self.weapon.setRange(self.range.value())
        self.weapon.setDamage(self.damage.value())
        self.weapon.setAccuracy(self.accuracy.value())

        # close the dialog
        self.accept()
