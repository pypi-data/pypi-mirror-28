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
import random

from PyQt5 import QtWidgets, QtCore

from civil.editor.editor_map import EditorMap

from civil.model import scenario
from civil.constants import REBEL, UNION
from civil.map.hex import Hex
from civil.model.scenario_info import ScenarioInfo

# icon => (may-be-on-right, may-be-on-down-right, may-be-on-down-left)
__suitable__ = {
    1: ((7, 8, 10, 11, 14), (1, 7, 8, 14), (1, 10)),
    2: ((2, 3, 5, 9, 12), (3, 5, 15), (2, 5, 9, 11, 16)),
    3: ((4, 5, 9, 12, 15, 16), (4, 6, 12, 13, 15, 16), (5, 8, 13, 14, 15, 16)),
    4: ((4, 5, 6, 10, 11, 13, 14, 16), (4, 6, 7, 8, 9, 11, 13, 14, 16), (5, 6, 7, 8, 9, 12, 16)),
    5: ((9, 12, 14, 15, 16), (11, 12, 15, 16), (5, 11, 12, 13, 15, 16)),
    6: ((1, 6, 7, 8, 10, 11, 14, 16), (1, 7, 8, 10, 14), (1, 4, 6, 7, 9, 10, 12, 14)),
    7: ((4, 6, 8, 10, 13, 14, 16), (4, 6, 8, 14, 16), (1, 6, 10, 14, 16)),
    8: ((2, 3, 4, 5, 6, 9, 12, 14, 15, 16), (2, 4, 6, 8, 9, 11, 14, 15, 16), (4, 6, 7, 8, 12, 14, 16)),
    9: ((4, 5, 6, 10, 11, 14), (2, 5, 6, 9, 11, 12, 15, 16), (2, 3, 5, 8, 11, 13, 15, 16)),
    10: ((1, 4, 6, 7, 8, 11, 13, 16), (4, 8, 9, 10, 13, 16), (4, 6, 7, 9, 12, 14)),
    11: ((2, 3, 5, 9, 12, 15), (2, 3, 5, 15, 16), (4, 5, 6, 7, 8, 14)),
    12: ((4, 10, 11, 14, 16), (5, 6, 12, 13, 15, 16), (2, 3, 5, 11, 13, 15, 16)),
    13: ((6, 11, 13, 16), (5, 6, 9, 12, 14, 15, 16), (5, 11, 12, 13, 14, 15, 16)),
    14: ((2, 4, 5, 10, 11, 13, 14, 16), (2, 4, 5, 6, 9, 10, 11, 12, 13, 15, 16), (4, 8, 12, 14, 15, 16)),
    15: ((4, 5, 6, 9, 13, 15, 16), (4, 6, 9, 10, 11, 12, 14, 15, 16), (3, 4, 5, 7, 8, 9, 11, 12, 14,
                                                                       15, 16)),
    16: ((4, 5, 6, 11, 13, 15, 16), (4, 6, 11, 13, 14, 15, 16), (4, 5, 6, 7, 8, 9, 12, 13, 14, 15, 16)),
}

randgen = random.Random()


def getSuitable(left, above_left, above_right):
    """
    Returns suitable grass icon, given the hex id:s
    left of, up left of, and up right of
    our current hex. NOTE: This assumes you fill in the map
    left-to-right, up-to-bottom.
    """
    by_left = []
    by_above_left = []
    by_above_right = []

    musthave = 0

    if left != -1:
        try:
            by_left = __suitable__[left][0]
            musthave += 1
        except:
            pass

    if above_left != -1:
        try:
            by_above_left = __suitable__[above_left][1]
            musthave += 1
        except:
            pass

    if above_right != -1:
        try:
            by_above_right = __suitable__[above_right][2]
            musthave += 1
        except:
            pass

    if musthave == 0:
        return -1

    # every possible hex
    # print left, by_left
    # print above_left, by_above_left
    # print above_right, by_above_right
    all = list(by_left)
    all.extend(by_above_left)
    all.extend(by_above_right)

    candidates = {}

    # Now which hex is approved by all surrounding hexes?
    for i in all:
        if i in candidates:
            continue
        c = all.count(i)
        if c >= musthave:
            candidates[i] = c

    # No suitable hex?
    if len(candidates) == 0:
        return -1

    # Choose one by random, and return it
    return list(candidates.keys())[randgen.randrange(0, len(candidates))]


def createNewScenario(mainwindow, width, height):
    """

    Args:
        mainwindow: 
        width: 
        height: 
    """
    randgen = random.Random()
    # create new scenario info
    scenario.info = ScenarioInfo()

    # set the scenario info
    scenario.info.setName('No name')
    scenario.info.setDescription(['No description'])
    scenario.info.setMission(UNION, ['No union mission'])
    scenario.info.setMission(REBEL, ['No rebel mission'])
    scenario.info.setLocation('No location')
    scenario.info.setMaxTurns(30)
    scenario.info.setDate(datetime.datetime(1862, 1, 1, 9, 0, 0))

    # create the map
    scenario.map = EditorMap(width, height)

    print("NewScenario.ok:", scenario.map.getSize())

    # loop and set initial icons for the map
    hexes = scenario.map.getHexes()
    cur_hex = randgen.randrange(1, 17)
    hexes[0][0] = Hex(cur_hex)
    for y in range(height):
        for x in range(width):
            if y == 0 and x == 0:
                continue
            above_left = -1
            above_right = -1
            left = -1
            if x != 0:
                left = hexes[y][x - 1].template.id
            if y != 0:
                if y % 2 == 0:
                    if x != 0:
                        above_left = hexes[y - 1][x - 1].template.id
                        above_right = hexes[y - 1][x].template.id
                    else:
                        if x != width - 1:
                            above_right = hexes[y - 1][x + 1].template.id
                else:
                    above_left = hexes[y - 1][x].template.id
                    if x != width - 1:
                        above_right = hexes[y - 1][x + 1].template.id

            cur_hex = getSuitable(left, above_left, above_right)
            if cur_hex == -1:
                cur_hex = 17  # so we notice errors

            hexes[y][x] = Hex(cur_hex)

    # # "Suitable" grass icons
    # mapper = [2,2,2,2,2,2,3,3,3,3,5,12]

    # # loop and set initial icons for the map
    # for y in range (height):
    #    for x in range (width):
    #        scenario.map.getHexes () [y][x] = Hex ( mapper[ randgen.randrange(0, len(mapper)) ] )

    # Make sure everything knows we have new scenario
    mainwindow.mapview.refresh()
    mainwindow.unionview.refresh()
    mainwindow.rebelview.refresh()
    mainwindow.objectiveview.refresh()
    mainwindow.blockview.refresh()
    mainwindow.weaponview.refresh()
    mainwindow.scenarioview.refresh()

    # enable all tabs
    mainwindow.palette.setEnabled(1)


class NewScenario(QtWidgets.QDialog):
    """
    This class is a dialog that takes care of createing a new scenario. It will query the user
    for the size of the map and if accepted initialize a new empty map and reset the scenario info.
    All other scneario data it set afterwards in the special dedicated tab, so data such as the
    scenario name, description etc are given default values here.
    """

    def __init__(self, parent):
        # create a new modal dialog
        QtWidgets.QDialog.__init__(self, parent, 'NewScenario', 1)

        self.setSizeGripEnabled(0)

        NewScenarioLayout = QtWidgets.QVBoxLayout(self, 11, 10, "NewScenarioLayout")

        self.groupBox2 = QtWidgets.QGroupBox(self, "groupBox2")
        self.groupBox2.setSizePolicy(QtWidgets.QSizePolicy(5, 7, 0, 0, self.groupBox2.sizePolicy().hasHeightForWidth()))
        self.groupBox2.setColumnLayout(0, QtCore.Qt.Vertical)
        self.groupBox2.layout().setSpacing(6)
        self.groupBox2.layout().setMargin(11)
        groupBox2Layout = QtWidgets.QHBoxLayout(self.groupBox2.layout())
        groupBox2Layout.setAlignment(QtCore.Qt.AlignTop)

        self.textLabel1 = QtWidgets.QLabel(self.groupBox2, "textLabel1")
        self.textLabel1.setSizePolicy(
            QtWidgets.QSizePolicy(5, 7, 0, 0, self.textLabel1.sizePolicy().hasHeightForWidth()))
        self.textLabel1.setAlignment(QtWidgets.QLabel.WordBreak | QtWidgets.QLabel.AlignVCenter)
        groupBox2Layout.addWidget(self.textLabel1)

        self.theatre = QtWidgets.QComboBox(0, self.groupBox2, "theatre")
        groupBox2Layout.addWidget(self.theatre)
        NewScenarioLayout.addWidget(self.groupBox2)
        spacer = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.MinimumExpanding)
        NewScenarioLayout.addItem(spacer)

        self.groupBox1 = QtWidgets.QGroupBox(self, "groupBox1")
        self.groupBox1.setColumnLayout(0, QtCore.Qt.Vertical)
        self.groupBox1.layout().setSpacing(6)
        self.groupBox1.layout().setMargin(11)
        groupBox1Layout = QtWidgets.QVBoxLayout(self.groupBox1.layout())
        groupBox1Layout.setAlignment(QtCore.Qt.AlignTop)

        self.TextLabel1 = QtWidgets.QLabel(self.groupBox1, "TextLabel1")
        self.TextLabel1.setAlignment(
            QtWidgets.QLabel.WordBreak | QtWidgets.QLabel.AlignVCenter | QtWidgets.QLabel.AlignLeft)
        groupBox1Layout.addWidget(self.TextLabel1)

        Layout3 = QtWidgets.QGridLayout(None, 1, 1, 0, 10, "Layout3")

        self.TextLabel2 = QtWidgets.QLabel(self.groupBox1, "TextLabel2")
        self.TextLabel2.setSizePolicy(
            QtWidgets.QSizePolicy(3, 1, 0, 0, self.TextLabel2.sizePolicy().hasHeightForWidth()))

        Layout3.addWidget(self.TextLabel2, 0, 0)
        spacer_2 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        Layout3.addItem(spacer_2, 0, 2)

        self.width = QtWidgets.QSpinBox(self.groupBox1, "width")
        self.width.setSizePolicy(QtWidgets.QSizePolicy(3, 0, 0, 0, self.width.sizePolicy().hasHeightForWidth()))
        self.width.setMaxValue(500)
        self.width.setMinValue(10)

        Layout3.addWidget(self.width, 0, 1)
        spacer_3 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        Layout3.addItem(spacer_3, 1, 2)

        self.height = QtWidgets.QSpinBox(self.groupBox1, "height")
        self.height.setSizePolicy(QtWidgets.QSizePolicy(3, 0, 0, 0, self.height.sizePolicy().hasHeightForWidth()))
        self.height.setMaxValue(500)
        self.height.setMinValue(10)

        Layout3.addWidget(self.height, 1, 1)

        self.TextLabel3 = QtWidgets.QLabel(self.groupBox1, "TextLabel3")
        self.TextLabel3.setSizePolicy(
            QtWidgets.QSizePolicy(3, 1, 0, 0, self.TextLabel3.sizePolicy().hasHeightForWidth()))

        Layout3.addWidget(self.TextLabel3, 1, 0)
        groupBox1Layout.addLayout(Layout3)
        NewScenarioLayout.addWidget(self.groupBox1)
        spacer_4 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.MinimumExpanding)
        NewScenarioLayout.addItem(spacer_4)

        Layout4 = QtWidgets.QHBoxLayout(None, 0, 10, "Layout4")
        spacer_5 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        Layout4.addItem(spacer_5)

        self.btnok = QtWidgets.QPushButton(self, "btnok")
        self.btnok.setDefault(1)
        Layout4.addWidget(self.btnok)

        self.btncancel = QtWidgets.QPushButton(self, "btncancel")
        Layout4.addWidget(self.btncancel)
        NewScenarioLayout.addLayout(Layout4)

        self.languageChange()

        self.resize(QtCore.QSize(494, 364).expandedTo(self.minimumSizeHint()))

        self.connect(self.btnok, SIGNAL("clicked()"), self.ok)
        self.connect(self.btncancel, SIGNAL("clicked()"), self.cancel)

    def languageChange(self):
        """
        Sets all strings and captions for the entire dialog. Having them in one handy place makes
        it easier to i18n them if needed.
        """

        # raw stuff...
        self.setCaption(self.tr("Create a new scenario"))
        self.groupBox2.setTitle(self.tr("Theatre"))
        self.textLabel1.setText(self.tr("Choose the theatre of war. This defines where the battles will take place."))
        self.theatre.clear()
        self.theatre.insertItem(self.tr("US Civil War"))
        self.groupBox1.setTitle(self.tr("Map size"))
        self.TextLabel1.setText(self.tr("Enter the wanted width and height of the new map in hexes. "))
        self.TextLabel2.setText(self.tr("Width:"))
        self.TextLabel3.setText(self.tr("Height:"))
        self.btnok.setText(self.tr("&Ok"))
        self.btncancel.setText(self.tr("&Cancel"))

    def cancel(self):
        """
        Callback triggered when the Cancel button is pressed. Simply rejects the dialog without
        any further actions.
        """

        # reject the dialog
        self.reject()

    def ok(self):
        """
        Callback triggered when the Ok button is pressed. Accepts the dialog and creates a new
        map and resets all scenario info.
        """

        createNewScenario(self.parent(), self.width.value(), self.height.value())

        # accept ourselves
        self.accept()
