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


class EditLocation(QtWidgets.QDialog):
    """
    This class provides a dialog which allows the user to graphically edit the properties of
    locations.
    """

    def __init__(self, parent, location):
        QtWidgets.QDialog.__init__(self, parent, "edit location", 1)

        # store the location
        self.location = location

        self.resize(399, 127)
        self.setCaption(self.tr('Edit location'))
        Edit_locationLayout = QtWidgets.QGridLayout(self)
        Edit_locationLayout.setSpacing(6)
        Edit_locationLayout.setMargin(11)
        spacer = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        Edit_locationLayout.addItem(spacer, 3, 1)

        self.name = QtWidgets.QLineEdit(self, 'name')
        QtWidgets.QToolTip.add(self.name, self.tr('Name of the location'))

        Edit_locationLayout.addMultiCellWidget(self.name, 0, 0, 2, 3)

        self.TextLabel1 = QtWidgets.QLabel(self, 'TextLabel1')
        self.TextLabel1.setSizePolicy(QtWidgets.QSizePolicy(1, 1, self.TextLabel1.sizePolicy().hasHeightForWidth()))
        self.TextLabel1.setText(self.tr('Name:'))
        self.TextLabel1.setAlignment(QtWidgets.QLabel.AlignVCenter | QtWidgets.QLabel.AlignLeft)

        Edit_locationLayout.addWidget(self.TextLabel1, 0, 0)

        Layout19 = QtWidgets.QHBoxLayout()
        Layout19.setSpacing(6)
        Layout19.setMargin(0)
        spacer_7 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        Layout19.addItem(spacer_7)

        self.okbutton = QtWidgets.QPushButton(self, 'ok')
        self.okbutton.setText(self.tr('&Ok'))
        Layout19.addWidget(self.okbutton)
        spacer_8 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        Layout19.addItem(spacer_8)

        self.cancel = QtWidgets.QPushButton(self, 'cancel')
        self.cancel.setText(self.tr('&Cancel'))
        Layout19.addWidget(self.cancel)

        Edit_locationLayout.addMultiCellLayout(Layout19, 5, 5, 2, 3)

        # populate all info into the widgets
        self.populate()

        # connect signals to slots
        self.connect(self.cancel, SIGNAL('clicked()'), self, SLOT('reject()'))
        self.connect(self.okbutton, SIGNAL('clicked()'), self.ok)

    def populate(self):
        """
        Populates the dialog with data from the location. This is a separate unit so
        that it can be easily picked out and improved.
        """

        # basic data
        self.name.setText(self.location.getName())

    def ok(self):
        """
        Callback triggered when the player clicks Ok. Stores all the data in the location and
        closes the dialog.
        """

        # set all data
        self.location.setName(str(self.name.text()))

        # close the dialog
        self.accept()
