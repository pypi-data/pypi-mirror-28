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

from civil.constants import REBEL, UNION, UNKNOWN


class EditObjective(QtWidgets.QDialog):
    """
    This class provides a dialog which allows the user to graphically edit the properties of
    objectives.
    """

    def __init__(self, parent, objective):
        QtWidgets.QDialog.__init__(self, parent, "edit objective", 1)

        # store the objective
        self.objective = objective

        self.resize(399, 227)
        self.setCaption(self.tr('Edit objective'))
        Edit_objectiveLayout = QtWidgets.QGridLayout(self)
        Edit_objectiveLayout.setSpacing(6)
        Edit_objectiveLayout.setMargin(11)
        spacer = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        Edit_objectiveLayout.addItem(spacer, 3, 1)

        self.points = QtWidgets.QSpinBox(self, 'points')
        self.points.setMaxValue(1000)
        self.points.setMinValue(0)
        QtWidgets.QToolTip.add(self.points, self.tr('The number of victory points the objective is worth'))

        Edit_objectiveLayout.addWidget(self.points, 3, 2)
        spacer_2 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        Edit_objectiveLayout.addItem(spacer_2, 3, 3)

        self.description = QtWidgets.QLineEdit(self, 'description')
        QtWidgets.QToolTip.add(self.description, self.tr('Description of the objective'))

        Edit_objectiveLayout.addMultiCellWidget(self.description, 1, 1, 2, 3)
        spacer_3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        Edit_objectiveLayout.addItem(spacer_3, 1, 1)

        self.owner = QtWidgets.QComboBox(0, self, 'owner')
        self.owner.insertItem(self.tr('Nobody'))
        self.owner.insertItem(self.tr('Rebel'))
        self.owner.insertItem(self.tr('Union'))
        self.owner.setSizePolicy(QtWidgets.QSizePolicy(7, 0, self.owner.sizePolicy().hasHeightForWidth()))
        QtWidgets.QToolTip.add(self.owner, self.tr('Initial owner of the objective'))

        Edit_objectiveLayout.addMultiCellWidget(self.owner, 2, 2, 2, 3)
        spacer_4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        Edit_objectiveLayout.addItem(spacer_4, 2, 1)
        spacer_5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        Edit_objectiveLayout.addItem(spacer_5, 0, 1)

        self.name = QtWidgets.QLineEdit(self, 'name')
        QtWidgets.QToolTip.add(self.name, self.tr('Name of the objective'))

        Edit_objectiveLayout.addMultiCellWidget(self.name, 0, 0, 2, 3)

        self.TextLabel3 = QtWidgets.QLabel(self, 'TextLabel3')
        self.TextLabel3.setSizePolicy(QtWidgets.QSizePolicy(1, 1, self.TextLabel3.sizePolicy().hasHeightForWidth()))
        self.TextLabel3.setText(self.tr('Owner:'))

        Edit_objectiveLayout.addWidget(self.TextLabel3, 2, 0)

        self.TextLabel5 = QtWidgets.QLabel(self, 'TextLabel5')
        self.TextLabel5.setSizePolicy(QtWidgets.QSizePolicy(1, 1, self.TextLabel5.sizePolicy().hasHeightForWidth()))
        self.TextLabel5.setText(self.tr('Points:'))

        Edit_objectiveLayout.addWidget(self.TextLabel5, 3, 0)

        self.TextLabel1 = QtWidgets.QLabel(self, 'TextLabel1')
        self.TextLabel1.setSizePolicy(QtWidgets.QSizePolicy(1, 1, self.TextLabel1.sizePolicy().hasHeightForWidth()))
        self.TextLabel1.setText(self.tr('Name:'))
        self.TextLabel1.setAlignment(QtWidgets.QLabel.AlignVCenter | QtWidgets.QLabel.AlignLeft)

        Edit_objectiveLayout.addWidget(self.TextLabel1, 0, 0)

        self.TextLabel2 = QtWidgets.QLabel(self, 'TextLabel2')
        self.TextLabel2.setSizePolicy(QtWidgets.QSizePolicy(1, 1, self.TextLabel2.sizePolicy().hasHeightForWidth()))
        self.TextLabel2.setText(self.tr('Description:'))

        Edit_objectiveLayout.addWidget(self.TextLabel2, 1, 0)
        spacer_6 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        Edit_objectiveLayout.addItem(spacer_6, 4, 2)

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

        Edit_objectiveLayout.addMultiCellLayout(Layout19, 5, 5, 2, 3)

        # populate all info into the widgets
        self.populate()

        # connect signals to slots
        self.connect(self.cancel, SIGNAL('clicked()'), self, SLOT('reject()'))
        self.connect(self.okbutton, SIGNAL('clicked()'), self.ok)

    def populate(self):
        """
        Populates the dialog with data from the objective. This is a separate unit so
        that it can be easily picked out and improved.
        """

        # basic data
        self.name.setText(self.objective.getName())
        self.description.setText(self.objective.getDescription())
        self.points.setValue(self.objective.getPoints())

        # get the owner
        owner = self.objective.getOwner()

        # set the proper index in the listbox
        self.owner.setCurrentItem({UNKNOWN: 0, REBEL: 1, UNION: 2}[owner])

    def ok(self):
        """
        Callback triggered when the player clicks Ok. Stores all the data in the objective and
        closes the dialog.
        """

        # set all data
        self.objective.setName(str(self.name.text()))
        self.objective.setDescription(str(self.description.text()))
        self.objective.setPoints(self.points.value())

        # get the owner too
        owner = self.owner.currentItem()

        # set it
        self.objective.setOwner({0: UNKNOWN, 1: REBEL, 2: UNION}[owner])

        # close the dialog
        self.accept()
