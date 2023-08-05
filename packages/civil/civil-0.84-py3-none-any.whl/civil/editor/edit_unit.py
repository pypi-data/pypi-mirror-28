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


class EditUnit(QtWidgets.QDialog):
    """

    """
    def __init__(self, parent, unit):
        QtWidgets.QDialog.__init__(self, parent, "edit unit", 1)

        # store the unit
        self.unit = unit

        self.resize(571, 637)
        self.setCaption(self.tr('Edit unit'))
        EditUnitLayout = QtWidgets.QHBoxLayout(self)
        EditUnitLayout.setSpacing(6)
        EditUnitLayout.setMargin(11)

        Layout9 = QtWidgets.QVBoxLayout()
        Layout9.setSpacing(6)
        Layout9.setMargin(0)

        self.GroupBox1 = QtWidgets.QGroupBox(self, 'GroupBox1')
        self.GroupBox1.setTitle(self.tr('Basic'))
        self.GroupBox1.setColumnLayout(0, QtCore.Qt.Vertical)
        self.GroupBox1.layout().setSpacing(0)
        self.GroupBox1.layout().setMargin(0)
        GroupBox1Layout = QtWidgets.QGridLayout(self.GroupBox1.layout())
        GroupBox1Layout.setAlignment(QtCore.Qt.AlignTop)
        GroupBox1Layout.setSpacing(6)
        GroupBox1Layout.setMargin(11)

        self.type = QtWidgets.QLabel(self.GroupBox1, 'type')

        GroupBox1Layout.addMultiCellWidget(self.type, 2, 2, 1, 2)

        self.TextLabel1_3 = QtWidgets.QLabel(self.GroupBox1, 'TextLabel1_3')
        self.TextLabel1_3.setMinimumSize(QtCore.QSize(100, 0))
        self.TextLabel1_3.setText(self.tr('Type:'))

        GroupBox1Layout.addWidget(self.TextLabel1_3, 2, 0)

        self.TextLabel2_3 = QtWidgets.QLabel(self.GroupBox1, 'TextLabel2_3')
        self.TextLabel2_3.setMinimumSize(QtCore.QSize(100, 0))
        self.TextLabel2_3.setText(self.tr('Men:'))

        GroupBox1Layout.addWidget(self.TextLabel2_3, 1, 0)
        spacer = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        GroupBox1Layout.addItem(spacer, 1, 2)

        self.men = QtWidgets.QSpinBox(self.GroupBox1, 'men')
        self.men.setSuffix(self.tr(''))
        self.men.setSpecialValueText(self.tr(''))
        self.men.setButtonSymbols(QtWidgets.QSpinBox.UpDownArrows)
        self.men.setMaxValue(200)
        self.men.setMinValue(1)
        self.men.setValue(50)
        QtWidgets.QToolTip.add(self.men, self.tr('Number of men in the unit'))

        GroupBox1Layout.addWidget(self.men, 1, 1)

        self.name = QtWidgets.QLineEdit(self.GroupBox1, 'name')
        QtWidgets.QToolTip.add(self.name, self.tr('Name of the unit'))

        GroupBox1Layout.addMultiCellWidget(self.name, 0, 0, 1, 2)

        self.TextLabel1 = QtWidgets.QLabel(self.GroupBox1, 'TextLabel1')
        self.TextLabel1.setMinimumSize(QtCore.QSize(100, 0))
        self.TextLabel1.setText(self.tr('Name:'))

        GroupBox1Layout.addWidget(self.TextLabel1, 0, 0)
        Layout9.addWidget(self.GroupBox1)

        self.GroupBox2 = QtWidgets.QGroupBox(self, 'GroupBox2')
        self.GroupBox2.setTitle(self.tr('Modifiers'))
        self.GroupBox2.setColumnLayout(0, QtCore.Qt.Vertical)
        self.GroupBox2.layout().setSpacing(0)
        self.GroupBox2.layout().setMargin(0)
        GroupBox2Layout = QtWidgets.QGridLayout(self.GroupBox2.layout())
        GroupBox2Layout.setAlignment(QtCore.Qt.AlignTop)
        GroupBox2Layout.setSpacing(6)
        GroupBox2Layout.setMargin(11)
        spacer_2 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        GroupBox2Layout.addItem(spacer_2, 2, 2)
        spacer_3 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        GroupBox2Layout.addItem(spacer_3, 1, 2)
        spacer_4 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        GroupBox2Layout.addItem(spacer_4, 0, 2)

        self.experience = QtWidgets.QSpinBox(self.GroupBox2, 'experience')
        self.experience.setSuffix(self.tr(''))
        self.experience.setSpecialValueText(self.tr(''))
        self.experience.setButtonSymbols(QtWidgets.QSpinBox.UpDownArrows)
        self.experience.setMaxValue(99)
        self.experience.setMinValue(0)
        self.experience.setValue(50)
        QtWidgets.QToolTip.add(self.experience, self.tr('Unit experience'))

        GroupBox2Layout.addWidget(self.experience, 1, 1)

        self.fatigue = QtWidgets.QSpinBox(self.GroupBox2, 'fatigue')
        self.fatigue.setSuffix(self.tr(''))
        self.fatigue.setSpecialValueText(self.tr(''))
        self.fatigue.setButtonSymbols(QtWidgets.QSpinBox.UpDownArrows)
        self.fatigue.setMaxValue(999)
        self.fatigue.setMinValue(0)
        self.fatigue.setValue(50)
        QtWidgets.QToolTip.add(self.fatigue, self.tr('Unit fatigue'))

        GroupBox2Layout.addWidget(self.fatigue, 2, 1)

        self.morale = QtWidgets.QSpinBox(self.GroupBox2, 'morale')
        self.morale.setSuffix(self.tr(''))
        self.morale.setSpecialValueText(self.tr(''))
        self.morale.setButtonSymbols(QtWidgets.QSpinBox.UpDownArrows)
        self.morale.setMaxValue(99)
        self.morale.setMinValue(0)
        self.morale.setValue(50)
        QtWidgets.QToolTip.add(self.morale, self.tr('Unit morale'))

        GroupBox2Layout.addWidget(self.morale, 0, 1)

        self.TextLabel6 = QtWidgets.QLabel(self.GroupBox2, 'TextLabel6')
        self.TextLabel6.setMinimumSize(QtCore.QSize(100, 0))
        self.TextLabel6.setText(self.tr('Fatigue:'))

        GroupBox2Layout.addWidget(self.TextLabel6, 2, 0)

        self.TextLabel5 = QtWidgets.QLabel(self.GroupBox2, 'TextLabel5')
        self.TextLabel5.setMinimumSize(QtCore.QSize(100, 0))
        self.TextLabel5.setText(self.tr('Experience:'))

        GroupBox2Layout.addWidget(self.TextLabel5, 1, 0)

        self.TextLabel4 = QtWidgets.QLabel(self.GroupBox2, 'TextLabel4')
        self.TextLabel4.setMinimumSize(QtCore.QSize(100, 0))
        self.TextLabel4.setText(self.tr('Morale:'))

        GroupBox2Layout.addWidget(self.TextLabel4, 0, 0)
        Layout9.addWidget(self.GroupBox2)

        self.GroupBox3 = QtWidgets.QGroupBox(self, 'GroupBox3')
        self.GroupBox3.setTitle(self.tr('Commander'))
        self.GroupBox3.setColumnLayout(0, QtCore.Qt.Vertical)
        self.GroupBox3.layout().setSpacing(0)
        self.GroupBox3.layout().setMargin(0)
        GroupBox3Layout = QtWidgets.QGridLayout(self.GroupBox3.layout())
        GroupBox3Layout.setAlignment(QtCore.Qt.AlignTop)
        GroupBox3Layout.setSpacing(6)
        GroupBox3Layout.setMargin(11)
        spacer_5 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        GroupBox3Layout.addItem(spacer_5, 2, 2)
        spacer_6 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        GroupBox3Layout.addItem(spacer_6, 3, 2)
        spacer_7 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        GroupBox3Layout.addItem(spacer_7, 4, 2)
        spacer_8 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        GroupBox3Layout.addItem(spacer_8, 5, 2)

        self.motivation = QtWidgets.QSpinBox(self.GroupBox3, 'motivation')
        self.motivation.setSuffix(self.tr(''))
        self.motivation.setSpecialValueText(self.tr(''))
        self.motivation.setButtonSymbols(QtWidgets.QSpinBox.UpDownArrows)
        self.motivation.setMaxValue(99)
        self.motivation.setMinValue(0)
        self.motivation.setValue(50)
        QtWidgets.QToolTip.add(self.motivation, self.tr('Commander motivational skill'))

        GroupBox3Layout.addWidget(self.motivation, 5, 1)

        self.rallyskill = QtWidgets.QSpinBox(self.GroupBox3, 'rallyskill')
        self.rallyskill.setSuffix(self.tr(''))
        self.rallyskill.setSpecialValueText(self.tr(''))
        self.rallyskill.setButtonSymbols(QtWidgets.QSpinBox.UpDownArrows)
        self.rallyskill.setMaxValue(99)
        self.rallyskill.setMinValue(0)
        self.rallyskill.setValue(50)
        QtWidgets.QToolTip.add(self.rallyskill, self.tr('Commander rallying skill'))

        GroupBox3Layout.addWidget(self.rallyskill, 4, 1)

        self.aggressiveness = QtWidgets.QSpinBox(self.GroupBox3, 'aggressiveness')
        self.aggressiveness.setSuffix(self.tr(''))
        self.aggressiveness.setSpecialValueText(self.tr(''))
        self.aggressiveness.setButtonSymbols(QtWidgets.QSpinBox.UpDownArrows)
        self.aggressiveness.setMaxValue(99)
        self.aggressiveness.setMinValue(0)
        self.aggressiveness.setValue(50)
        QtWidgets.QToolTip.add(self.aggressiveness, self.tr('Commander aggressiveness'))

        GroupBox3Layout.addWidget(self.aggressiveness, 3, 1)

        self.rank = QtWidgets.QComboBox(0, self.GroupBox3, 'rank')
        self.rank.setSizePolicy(QtWidgets.QSizePolicy(7, 0, self.rank.sizePolicy().hasHeightForWidth()))
        QtWidgets.QToolTip.add(self.rank, self.tr('Commander rank'))

        GroupBox3Layout.addMultiCellWidget(self.rank, 1, 1, 1, 2)

        self.name2 = QtWidgets.QLineEdit(self.GroupBox3, 'name2')
        QtWidgets.QToolTip.add(self.name2, self.tr('Name of commander'))

        GroupBox3Layout.addMultiCellWidget(self.name2, 0, 0, 1, 2)

        self.experience2 = QtWidgets.QSpinBox(self.GroupBox3, 'experience2')
        self.experience2.setSuffix(self.tr(''))
        self.experience2.setSpecialValueText(self.tr(''))
        self.experience2.setButtonSymbols(QtWidgets.QSpinBox.UpDownArrows)
        self.experience2.setMaxValue(99)
        self.experience2.setMinValue(0)
        self.experience2.setValue(50)
        QtWidgets.QToolTip.add(self.experience2, self.tr('Commander experience'))

        GroupBox3Layout.addWidget(self.experience2, 2, 1)

        self.TextLabel1_2 = QtWidgets.QLabel(self.GroupBox3, 'TextLabel1_2')
        self.TextLabel1_2.setMinimumSize(QtCore.QSize(100, 0))
        self.TextLabel1_2.setText(self.tr('Name:'))

        GroupBox3Layout.addWidget(self.TextLabel1_2, 0, 0)

        self.TextLabel2_2 = QtWidgets.QLabel(self.GroupBox3, 'TextLabel2_2')
        self.TextLabel2_2.setMinimumSize(QtCore.QSize(100, 0))
        self.TextLabel2_2.setText(self.tr('Rank:'))

        GroupBox3Layout.addWidget(self.TextLabel2_2, 1, 0)

        self.TextLabel4_2 = QtWidgets.QLabel(self.GroupBox3, 'TextLabel4_2')
        self.TextLabel4_2.setMinimumSize(QtCore.QSize(100, 0))
        self.TextLabel4_2.setText(self.tr('Experience:'))

        GroupBox3Layout.addWidget(self.TextLabel4_2, 2, 0)

        self.TextLabel5_2 = QtWidgets.QLabel(self.GroupBox3, 'TextLabel5_2')
        self.TextLabel5_2.setMinimumSize(QtCore.QSize(100, 0))
        self.TextLabel5_2.setText(self.tr('Aggressiveness:'))

        GroupBox3Layout.addWidget(self.TextLabel5_2, 3, 0)

        self.TextLabel6_2 = QtWidgets.QLabel(self.GroupBox3, 'TextLabel6_2')
        self.TextLabel6_2.setMinimumSize(QtCore.QSize(100, 0))
        self.TextLabel6_2.setText(self.tr('Rally skill:'))

        GroupBox3Layout.addWidget(self.TextLabel6_2, 4, 0)

        self.TextLabel6_2_2 = QtWidgets.QLabel(self.GroupBox3, 'TextLabel6_2_2')
        self.TextLabel6_2_2.setMinimumSize(QtCore.QSize(100, 0))
        self.TextLabel6_2_2.setText(self.tr('Motivation:'))

        GroupBox3Layout.addWidget(self.TextLabel6_2_2, 5, 0)
        Layout9.addWidget(self.GroupBox3)

        self.GroupBox4 = QtWidgets.QGroupBox(self, 'GroupBox4')
        self.GroupBox4.setTitle(self.tr('Weapon'))
        self.GroupBox4.setColumnLayout(0, QtCore.Qt.Vertical)
        self.GroupBox4.layout().setSpacing(0)
        self.GroupBox4.layout().setMargin(0)
        GroupBox4Layout = QtWidgets.QGridLayout(self.GroupBox4.layout())
        GroupBox4Layout.setAlignment(QtCore.Qt.AlignTop)
        GroupBox4Layout.setSpacing(6)
        GroupBox4Layout.setMargin(11)
        spacer_9 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        GroupBox4Layout.addItem(spacer_9, 1, 2)

        self.count = QtWidgets.QSpinBox(self.GroupBox4, 'count')
        self.count.setSuffix(self.tr(''))
        self.count.setSpecialValueText(self.tr(''))
        self.count.setButtonSymbols(QtWidgets.QSpinBox.UpDownArrows)
        self.count.setMaxValue(300)
        self.count.setMinValue(0)
        self.count.setValue(0)
        QtWidgets.QToolTip.add(self.count, self.tr('Number of weapons of the above type'))

        GroupBox4Layout.addWidget(self.count, 1, 1)

        self.weapontype = QtWidgets.QComboBox(0, self.GroupBox4, 'weapontype')
        self.weapontype.setSizePolicy(QtWidgets.QSizePolicy(7, 0, self.weapontype.sizePolicy().hasHeightForWidth()))
        QtWidgets.QToolTip.add(self.weapontype, self.tr('Main type of weapon for the unit'))

        GroupBox4Layout.addMultiCellWidget(self.weapontype, 0, 0, 1, 2)

        self.TextLabel1_2_2 = QtWidgets.QLabel(self.GroupBox4, 'TextLabel1_2_2')
        self.TextLabel1_2_2.setMinimumSize(QtCore.QSize(100, 0))
        self.TextLabel1_2_2.setText(self.tr('Type:'))

        GroupBox4Layout.addWidget(self.TextLabel1_2_2, 0, 0)

        self.TextLabel1_2_2_2 = QtWidgets.QLabel(self.GroupBox4, 'TextLabel1_2_2_2')
        self.TextLabel1_2_2_2.setMinimumSize(QtCore.QSize(100, 0))
        self.TextLabel1_2_2_2.setText(self.tr('Number:'))

        GroupBox4Layout.addWidget(self.TextLabel1_2_2_2, 1, 0)
        Layout9.addWidget(self.GroupBox4)
        EditUnitLayout.addLayout(Layout9)

        Layout10 = QtWidgets.QVBoxLayout()
        Layout10.setSpacing(6)
        Layout10.setMargin(0)

        self.okbtn = QtWidgets.QPushButton(self, 'ok')
        self.okbtn.setText(self.tr('&Ok'))
        self.okbtn.setDefault(1)
        Layout10.addWidget(self.okbtn)

        self.cancel = QtWidgets.QPushButton(self, 'cancel')
        self.cancel.setText(self.tr('&Cancel'))
        Layout10.addWidget(self.cancel)
        spacer_10 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        Layout10.addItem(spacer_10)
        EditUnitLayout.addLayout(Layout10)

        self.connect(self.okbtn, SIGNAL('clicked()'), self.ok)
        self.connect(self.cancel, SIGNAL('clicked()'), self, SLOT('reject()'))
        self.connect(self.men, SIGNAL('valueChanged(int)'), self.menChanged)

        # populate all info into the widgets
        self.populate()

    def populate(self):
        """
        Populates the dialog with data from the unit.
        """
        # basic data
        self.name.setText(self.unit.getName())
        self.type.setText(self.unit.getTypeString())
        self.men.setValue(self.unit.getMen())

        # modifiers
        self.experience.setValue(self.unit.getExperience().getValue())
        self.fatigue.setValue(self.unit.getFatigue().getValue())
        self.morale.setValue(self.unit.getMorale().getValue())

        # commander data
        commander = self.unit.getCommander()

        self.name2.setText(commander.getName())
        self.aggressiveness.setValue(commander.getAggressiveness().getValue())
        self.experience2.setValue(commander.getExperience().getValue())
        self.rallyskill.setValue(commander.getRallySkill().getValue())
        self.motivation.setValue(commander.getMotivation().getValue())

        # loop over all ranks and insert them into the list
        correctindex = -1
        for index in range(len(globals.ranks)):
            # get the rank
            rank = globals.ranks[index]

            # add an item to the combo
            self.rank.insertItem(self.tr(rank))

            # is this the same rank as the commander's?
            if rank == commander.getRank():
                # yep, store it
                correctindex = index

        # no assign the correct index for the combo
        self.rank.setCurrentItem(correctindex)

        # weapon data
        self.count.setValue(self.unit.getWeaponCounts()[0])

        # loop over all weapons and insert them into the list
        for weapon in list(globals.weapons.values()):
            # create an item and add it
            self.weapontype.insertItem(self.tr(weapon.getName()))

            # is this the weapon the unit has?
            if weapon.getId() == self.unit.getWeapon().getId():
                # yep, store the index
                weaponindex = self.weapontype.count() - 1

        # now make the weapon for the unit current
        self.weapontype.setCurrentItem(weaponindex)

    def menChanged(self):
        """
        Callback triggered when the user changes the number of men in the unit. Sets the number
        of men as the new max number of weapons. Avoids having a unit with more weapons than men.
        """
        # set the new max count
        self.count.setMaxValue(self.men.value())

    def ok(self):
        """
        Callback that is called when the user clicks the Ok button. Stores all changed data about
        the unit and closes the dialog. The unit also checked for some common flaws, and if
        something is found then the user is alerted to the fact and is given a chance to fix it.
        """

        # validate whatever the user has input. tries to make sure that we get sane units
        error, control = self.__validate()

        # did we get an error?
        if error is not None:
            result = QtWidgets.QMessageBox.warning(self, "Edit unit", "The unit is not complete, " +
                                                   error + ", do you still want to proceed?", "Yes", "No",
                                                   None, 1)

            # did we get a 1, which is the second button?
            if result == 1:
                # yep, don't ok. set focus to the offending control and go away
                control.setFocus()
                return

        # store basic data
        self.unit.setName(self.name.text().latin1())
        self.unit.setMen(self.men.value())

        # store modifiers
        self.unit.getExperience().setValue(self.experience.value())
        self.unit.getFatigue().setValue(self.fatigue.value())
        self.unit.getMorale().setValue(self.morale.value())

        # store commander data
        commander = self.unit.getCommander()

        commander.setName(self.name2.text().latin1())
        commander.setRank(str(self.rank.currentText()))
        commander.getAggressiveness().setValue(self.aggressiveness.value())
        commander.getExperience().setValue(self.experience2.value())
        commander.getRallySkill().setValue(self.rallyskill.value())
        commander.getMotivation().setValue(self.motivation.value())

        # store weapon data. it is assumed to have no destroyed weapons yet
        self.unit.setWeaponCounts(self.count.value(), 0)

        # get the name of the weapon
        weaponname = str(self.weapontype.currentText())

        # loop over all weapons and check weather the weapon is the one that was assigned to the unit
        for weapon in list(globals.weapons.values()):
            # is this it?
            if weapon.getName() == weaponname:
                # found it
                self.unit.setWeapon(weapon)
                break

        # close the dialog
        self.accept()

    def __validate(self):
        """
        Validates the data that has been input for the unit. Some basic checks are made to make
        sure that the unit isn't useless. If something is found to be missing then an error text is
        returned along with the widget that controls the value. If all is ok (None,None) is
        returned.
        """

        # check name
        if self.name.text().latin1() == '':
            # no name given
            return "it has no name", self.name

        # check men
        if self.men.value() <= 1:
            # not enough men
            return "it does not have enough men", self.men

        # check weapons
        if self.count.value() == 0:
            # no weapons
            return "it has no weapons", self.count

        # check commander name
        if self.name2.text().latin1() == '':
            # no commander name given
            return "the commander has no name", self.name2
