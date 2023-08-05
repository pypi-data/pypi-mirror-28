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


class EditOrganization(QtWidgets.QDialog):
    """
    This class lets the user edit an organization. An organization is just a logical entity
    that can't really be seen on the battlefield, such as a brigade or regiment. Only the name can
    be altered.
    """

    def __init__(self, parent, organization):
        QtWidgets.QDialog.__init__(self, parent, "edit organization", 1)

        # store the unit
        self.organization = organization

        self.setCaption(self.tr('Edit organization'))
        EditOrganizationLayout = QtWidgets.QVBoxLayout(self)
        EditOrganizationLayout.setSpacing(6)
        EditOrganizationLayout.setMargin(11)

        Layout5 = QtWidgets.QHBoxLayout()
        Layout5.setSpacing(6)
        Layout5.setMargin(0)

        self.TextLabel1 = QtWidgets.QLabel(self, 'TextLabel1')
        self.TextLabel1.setMinimumSize(QtCore.QSize(80, 0))
        self.TextLabel1.setText(self.tr('&Name:'))
        Layout5.addWidget(self.TextLabel1)

        self.name = QtWidgets.QLineEdit(self, 'name')
        QtWidgets.QToolTip.add(self.name, self.tr('Name of the organization'))
        Layout5.addWidget(self.name)
        EditOrganizationLayout.addLayout(Layout5)
        spacer = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        EditOrganizationLayout.addItem(spacer)

        Layout3 = QtWidgets.QHBoxLayout()
        Layout3.setSpacing(6)
        Layout3.setMargin(0)
        spacer_2 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        Layout3.addItem(spacer_2)

        self.ok_btn = QtWidgets.QPushButton(self, 'ok')
        self.ok_btn.setText(self.tr('&Ok'))
        self.ok_btn.setDefault(1)
        Layout3.addWidget(self.ok_btn)
        spacer_3 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        Layout3.addItem(spacer_3)

        self.cancel = QtWidgets.QPushButton(self, 'cancel')
        self.cancel.setText(self.tr('&Cancel'))
        Layout3.addWidget(self.cancel)
        EditOrganizationLayout.addLayout(Layout3)

        self.connect(self.ok_btn, SIGNAL('clicked()'), self.ok)
        self.connect(self.cancel, SIGNAL('clicked()'), self, SLOT('reject()'))

        self.TextLabel1.setBuddy(self.name)

        self.resize(self.sizeHint())

        # populate all info into the widgets
        self.populate()

    def ok(self):
        """
        Accepts the dialog. Sets the new name.
        """
        # get the name
        newname = self.name.text().latin1()

        # did we get anything?
        if newname == "":
            # no name, set a valid one
            newname = 'unnamed'

        # assign the new name
        self.organization.setName(newname)

        # close the dialog
        self.accept()

    def populate(self):
        """
        Populates the dialog with data from the unit.
        """
        # basic data
        self.name.setText(self.organization.getName())
