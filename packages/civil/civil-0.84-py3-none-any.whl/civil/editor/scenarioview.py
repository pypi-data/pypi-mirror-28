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

import datetime

from PyQt5 import QtWidgets, QtCore

from civil.model import scenario
from civil.constants import REBEL, UNION


class ScenarioView(QtWidgets.QWidget):
    """
    This view is used as a general view for all misc scenario info. It lets the user change data
    such as the scenario name, description, date, missions etc.
    """

    def __init__(self, parent):
        QtWidgets.QWidget.__init__(self, parent)

        self.setCaption(self.tr('Form1'))
        ScenarioViewLayout = QtWidgets.QVBoxLayout(self)
        ScenarioViewLayout.setSpacing(10)
        ScenarioViewLayout.setMargin(11)

        self.GroupBox1 = QtWidgets.QGroupBox(self, 'GroupBox1')
        self.GroupBox1.setTitle(self.tr('Basic information'))
        self.GroupBox1.setColumnLayout(0, QtCore.Qt.Vertical)
        self.GroupBox1.layout().setSpacing(0)
        self.GroupBox1.layout().setMargin(0)
        GroupBox1Layout = QtWidgets.QGridLayout(self.GroupBox1.layout())
        GroupBox1Layout.setAlignment(QtCore.Qt.AlignTop)
        GroupBox1Layout.setSpacing(10)
        GroupBox1Layout.setMargin(11)

        self.TextLabel1 = QtWidgets.QLabel(self.GroupBox1, 'TextLabel1')
        self.TextLabel1.setText(self.tr('Name:'))

        GroupBox1Layout.addWidget(self.TextLabel1, 0, 0)

        self.TextLabel2 = QtWidgets.QLabel(self.GroupBox1, 'TextLabel2')
        self.TextLabel2.setText(self.tr('Description:'))

        GroupBox1Layout.addWidget(self.TextLabel2, 1, 0)

        self.TextLabel3 = QtWidgets.QLabel(self.GroupBox1, 'TextLabel3')
        self.TextLabel3.setText(self.tr('Geographic location:'))

        GroupBox1Layout.addWidget(self.TextLabel3, 2, 0)

        self.description = QtWidgets.QTextEdit(self.GroupBox1, 'description')
        self.description.setWordWrap(QtWidgets.QTextEdit.WidgetWidth)
        # Lame QT 2.3/3.0 compatibility

        try:
            wordwrap = QtWidgets.QTextEdit.AtWhiteSpace
        except:
            pass

        try:
            wordwrap = QtWidgets.QTextEdit.AtWordBoundary
        except:
            pass

        self.description.setWrapPolicy(wordwrap)

        QtWidgets.QToolTip.add(self.description, self.tr('Short description of what the scenario is about'))

        GroupBox1Layout.addMultiCellWidget(self.description, 1, 1, 1, 4)

        self.name = QtWidgets.QLineEdit(self.GroupBox1, 'name')
        QtWidgets.QToolTip.add(self.name, self.tr('Name of the scenario'))

        GroupBox1Layout.addMultiCellWidget(self.name, 0, 0, 1, 4)

        self.TextLabel4 = QtWidgets.QLabel(self.GroupBox1, 'TextLabel4')
        self.TextLabel4.setText(self.tr('Date:'))

        GroupBox1Layout.addWidget(self.TextLabel4, 3, 0)

        self.month = QtWidgets.QSpinBox(self.GroupBox1, 'month')
        self.month.setMaxValue(12)
        self.month.setMinValue(1)
        QtWidgets.QToolTip.add(self.month, self.tr('Month of the battle'))

        GroupBox1Layout.addWidget(self.month, 3, 2)

        self.minute = QtWidgets.QSpinBox(self.GroupBox1, 'minute')
        self.minute.setMaxValue(59)
        QtWidgets.QToolTip.add(self.minute, self.tr('Minute of the battle'))

        GroupBox1Layout.addWidget(self.minute, 4, 2)

        self.hour = QtWidgets.QSpinBox(self.GroupBox1, 'hour')
        self.hour.setMaxValue(23)
        QtWidgets.QToolTip.add(self.hour, self.tr('Hour of the battle'))

        GroupBox1Layout.addWidget(self.hour, 4, 1)

        self.TextLabel6 = QtWidgets.QLabel(self.GroupBox1, 'TextLabel6')
        self.TextLabel6.setText(self.tr('Time:'))

        GroupBox1Layout.addWidget(self.TextLabel6, 4, 0)
        spacer = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        GroupBox1Layout.addItem(spacer, 3, 4)

        self.year = QtWidgets.QSpinBox(self.GroupBox1, 'year')
        self.year.setMaxValue(1865)
        self.year.setMinValue(1861)
        self.year.setValue(1861)
        QtWidgets.QToolTip.add(self.year, self.tr('Year of the battle'))

        GroupBox1Layout.addWidget(self.year, 3, 1)

        self.location = QtWidgets.QLineEdit(self.GroupBox1, 'location')
        QtWidgets.QToolTip.add(self.location, self.tr('Name of the place for the battle'))

        GroupBox1Layout.addMultiCellWidget(self.location, 2, 2, 1, 4)

        self.day = QtWidgets.QSpinBox(self.GroupBox1, 'day')
        self.day.setMaxValue(31)
        self.day.setMinValue(1)
        QtWidgets.QToolTip.add(self.day, self.tr('Day of the battle'))

        GroupBox1Layout.addWidget(self.day, 3, 3)

        self.TextLabel1_2 = QtWidgets.QLabel(self.GroupBox1, 'TextLabel1_2')
        self.TextLabel1_2.setText(self.tr('Turns:'))

        GroupBox1Layout.addWidget(self.TextLabel1_2, 5, 0)

        self.turns = QtWidgets.QSpinBox(self.GroupBox1, 'turns')
        self.turns.setMaxValue(999)
        self.turns.setMinValue(1)
        QtWidgets.QToolTip.add(self.turns, self.tr('Number of turns in the scenario'))

        GroupBox1Layout.addWidget(self.turns, 5, 1)
        spacer_2 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        GroupBox1Layout.addItem(spacer_2, 5, 2)
        spacer_3 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        GroupBox1Layout.addItem(spacer_3, 4, 3)
        spacer_4 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        GroupBox1Layout.addItem(spacer_4, 5, 3)
        spacer_5 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        GroupBox1Layout.addItem(spacer_5, 4, 4)
        spacer_6 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        GroupBox1Layout.addItem(spacer_6, 5, 4)
        ScenarioViewLayout.addWidget(self.GroupBox1)

        self.GroupBox2 = QtWidgets.QGroupBox(self, 'GroupBox2')
        self.GroupBox2.setTitle(self.tr('Missions'))
        self.GroupBox2.setColumnLayout(0, QtCore.Qt.Vertical)
        self.GroupBox2.layout().setSpacing(0)
        self.GroupBox2.layout().setMargin(0)
        GroupBox2Layout = QtWidgets.QVBoxLayout(self.GroupBox2.layout())
        GroupBox2Layout.setAlignment(QtCore.Qt.AlignTop)
        GroupBox2Layout.setSpacing(10)
        GroupBox2Layout.setMargin(11)

        self.TextLabel7 = QtWidgets.QLabel(self.GroupBox2, 'TextLabel7')
        self.TextLabel7.setText(self.tr('Union mission information:'))
        GroupBox2Layout.addWidget(self.TextLabel7)

        self.unionmission = QtWidgets.QTextEdit(self.GroupBox2, 'unionmission')
        self.unionmission.setWordWrap(QtWidgets.QTextEdit.WidgetWidth)
        self.unionmission.setWrapPolicy(wordwrap)
        QtWidgets.QToolTip.add(self.unionmission, self.tr('Description about what the union player should accomplish'))
        GroupBox2Layout.addWidget(self.unionmission)

        self.TextLabel7_2 = QtWidgets.QLabel(self.GroupBox2, 'TextLabel7_2')
        self.TextLabel7_2.setText(self.tr('Rebel mission information::'))
        GroupBox2Layout.addWidget(self.TextLabel7_2)

        self.rebelmission = QtWidgets.QTextEdit(self.GroupBox2, 'rebelmission')
        self.rebelmission.setWordWrap(QtWidgets.QTextEdit.WidgetWidth)
        self.rebelmission.setWrapPolicy(wordwrap)
        QtWidgets.QToolTip.add(self.rebelmission, self.tr('Description about what the rebel player should accomplish'))
        GroupBox2Layout.addWidget(self.rebelmission)
        ScenarioViewLayout.addWidget(self.GroupBox2)

        self.GroupBox3 = QtWidgets.QGroupBox(self, 'GroupBox3')
        self.GroupBox3.setTitle(self.tr('Author info'))
        self.GroupBox3.setColumnLayout(0, QtCore.Qt.Vertical)
        self.GroupBox3.layout().setSpacing(0)
        self.GroupBox3.layout().setMargin(0)
        GroupBox3Layout = QtWidgets.QGridLayout(self.GroupBox3.layout())
        GroupBox3Layout.setAlignment(QtCore.Qt.AlignTop)
        GroupBox3Layout.setSpacing(10)
        GroupBox3Layout.setMargin(11)

        self.TextLabel8 = QtWidgets.QLabel(self.GroupBox3, 'TextLabel8')
        self.TextLabel8.setText(self.tr('Name:'))

        GroupBox3Layout.addWidget(self.TextLabel8, 0, 0)

        self.TextLabel9 = QtWidgets.QLabel(self.GroupBox3, 'TextLabel9')
        self.TextLabel9.setText(self.tr('Email:'))

        GroupBox3Layout.addWidget(self.TextLabel9, 1, 0)

        self.authorname = QtWidgets.QLineEdit(self.GroupBox3, 'authorname')
        QtWidgets.QToolTip.add(self.authorname, self.tr('Name of the scenario author'))

        GroupBox3Layout.addWidget(self.authorname, 0, 1)

        self.email = QtWidgets.QLineEdit(self.GroupBox3, 'email')
        QtWidgets.QToolTip.add(self.email, self.tr('Email of the scenario author'))

        GroupBox3Layout.addWidget(self.email, 1, 1)

        self.TextLabel11 = QtWidgets.QLabel(self.GroupBox3, 'TextLabel11')
        self.TextLabel11.setText(self.tr('Comment:'))

        GroupBox3Layout.addWidget(self.TextLabel11, 3, 0)

        self.comment = QtWidgets.QTextEdit(self.GroupBox3, 'comment')
        QtWidgets.QToolTip.add(self.comment, self.tr('Comment about the scenario'))

        GroupBox3Layout.addWidget(self.comment, 3, 1)

        self.TextLabel10 = QtWidgets.QLabel(self.GroupBox3, 'TextLabel10')
        self.TextLabel10.setText(self.tr('URL:'))

        GroupBox3Layout.addWidget(self.TextLabel10, 2, 0)

        self.url = QtWidgets.QLineEdit(self.GroupBox3, 'url')
        QtWidgets.QToolTip.add(self.url, self.tr('Url to a homepage for the scenario'))

        GroupBox3Layout.addWidget(self.url, 2, 1)
        ScenarioViewLayout.addWidget(self.GroupBox3)

        # make sure we know of changes
        self.connect(self.year, SIGNAL('valueChanged(int)'), self.dateChanged)
        self.connect(self.month, SIGNAL('valueChanged(int)'), self.dateChanged)

    def dateChanged(self):
        """
        This callback is triggered when the user changes the year or the month of the
        scenario. It will set the new date and then emit a signal telling the rest of the
        application that we have a new date.
        """
        # get the date data
        year = self.year.value()
        month = self.month.value()
        day = self.day.value()
        hour = self.hour.value()
        minute = self.minute.value()
        second = 0

        # set the new changed date
        scenario.info.setDate(datetime.datetime(year, month, day, hour, minute, second))

        # let the world know that we have a new date
        self.emit(PYSIGNAL('dateChanged'), ())

    def refresh(self):
        """
        Refreshes all the scenario info data. This method should be used when a new scenario has
        been loaded or created. It will get all data from the central ScenarioInfo instance and
        populate this widget with it.
        """

        # set all simple data
        self.name.setText(scenario.info.getName())
        self.location.setText(scenario.info.getLocation())
        self.turns.setValue(scenario.info.getMaxTurns())

        # set the date
        year, month, day, hour, minute = scenario.info.getStartDate()
        self.year.setValue(year)
        self.month.setValue(month)
        self.day.setValue(day)
        self.hour.setValue(hour)
        self.minute.setValue(minute)

        self.description.clear()
        self.unionmission.clear()
        self.rebelmission.clear()

        # loop over all paragraphs and set the description
        for para in scenario.info.getDescription():
            # add the line, followed by an empty line
            self.description.insertLine(para)
            self.description.insertLine("")

        # loop over all paragraphs and set the union mission
        for para in scenario.info.getMission(UNION):
            # add the line, followed by an empty line
            self.unionmission.insertLine(para)
            self.unionmission.insertLine("")

        # loop over all paragraphs and set the rebel mission
        for para in scenario.info.getMission(REBEL):
            # add the line, followed by an empty line
            self.rebelmission.insertLine(para)
            self.rebelmission.insertLine("")

    def store(self):
        """
        Stores all data from the controls of this view in the global object for scenario info
        data. This method should be called before a scenario is saved.
        """

        # get all data
        name = str(self.name.text())
        description = str(self.description.text())
        unionmission = str(self.unionmission.text())
        rebelmission = str(self.rebelmission.text())
        location = str(self.location.text())
        turns = self.turns.value()
        year = self.year.value()
        month = self.month.value()
        day = self.day.value()
        hour = self.hour.value()
        minute = self.minute.value()
        second = 0

        # TODO: should we validate the data too, or just assume it's ok?

        # set the scenario info
        scenario.info.setName(name)
        scenario.info.setDescription([description])
        scenario.info.setMission(UNION, [unionmission])
        scenario.info.setMission(REBEL, [rebelmission])
        scenario.info.setLocation(location)
        scenario.info.setMaxTurns(turns)
        scenario.info.setDate(datetime.datetime(year, month, day, hour, minute, second))

    def validate(self):
        """
        Validates the part of the scenario that this view is responsible for creating. Returns a
        free text report that indicates the validation result or None if all is ok.
        """

        # the default empty text
        text = ''

        # check the name
        if str(self.name.text()).strip() == '':
            # no name given
            text += 'the scenario has no name.<br/>'

        # check the description
        if str(self.description.text()).strip() == '':
            # no description given
            text += 'the scenario has no description.<br/>'

        # check the location
        if str(self.location.text()).strip() == '':
            # no location given
            text += 'the scenario has no location.<br/>'

        # check the union mission
        if str(self.unionmission.text()).strip() == '':
            # no union mission given
            text += 'the scenario has no mission for the Union player.<br/>'

        # check the rebel mission
        if str(self.rebelmission.text()).strip() == '':
            # no rebel mission given
            text += 'the scenario has no mission for the Rebel player.<br/>'

        # did we get any errors?
        if text == '':
            # no errors
            return None

        # we have something to report on
        return text

