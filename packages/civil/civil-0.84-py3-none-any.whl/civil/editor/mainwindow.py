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

import sys
import traceback
import zipfile

from PyQt5 import QtWidgets, QtCore

from civil.editor.editor_map import MapHeightException
from civil.editor.locationview import LocationView
from civil.editor.mapview import MapView
from civil.editor.unitview import UnitView

from civil.editor import globals
from civil.editor import undostack
from civil.editor.blockview import BlockView
from civil.model import scenario
from civil.constants import REBEL, UNION
from civil.editor.new_scenario import NewScenario, createNewScenario
from civil.map.hex import Hex
from civil.serialization.scenario_parser import ScenarioParser
from civil.serialization.scenario_writer import ScenarioWriter
from civil.editor.iconview import IconView
from civil.editor.objectiveview import ObjectiveView
from civil.editor.pluginview import PluginView
from civil.editor.scenarioview import ScenarioView
from civil.editor.weaponview import WeaponView


class MainWindow(QtWidgets.QMainWindow):
    """
    This is the main window of the application. Contains the palette of tools and the actual
    map.
    """

    def __init__(self):
        # TODO right windowflag and title QtWidgets.QMainWindow.__init__(self, None, 'Civil Scenario Editor', QtCore.Qt.WDestructiveClose)
        QtWidgets.QMainWindow.__init__(self, None)

        # create the menubar
        self.file = QtWidgets.QMenu('&File', self)
        self.view = QtWidgets.QMenu('&View', self)
        self.edit = QtWidgets.QMenu('&Edit', self)
        self.tools = QtWidgets.QMenu('&Tools', self)
        self.help = QtWidgets.QMenu('&Help', self)
        self.menuBar().addMenu(self.file)
        self.menuBar().addMenu(self.edit)
        self.menuBar().addMenu(self.view)
        self.menuBar().addMenu(self.tools)
        self.menuBar().addSeparator()
        self.menuBar().addMenu(self.help)

        # create the menu items for 'File'
        self.file.addAction('&New', self.new, QtCore.Qt.CTRL + QtCore.Qt.Key_N)
        self.file.addAction('&Open', self.open, QtCore.Qt.CTRL + QtCore.Qt.Key_O)
        self.file.addAction('&Save', self.save, QtCore.Qt.CTRL + QtCore.Qt.Key_S)
        self.file.addAction('Save &As', self.saveAs, QtCore.Qt.CTRL + QtCore.Qt.Key_A)
        self.file.addAction('&Quit', self.quit, QtCore.Qt.CTRL + QtCore.Qt.Key_Q)

        # create the menu items for 'Edit'
        self.edit.addAction('&Clear', self.clear)
        self.edit.addAction('&Undo', self.undo, QtCore.Qt.CTRL + QtCore.Qt.Key_Z)

        # create the menu items for 'View'
        self.view.addAction('&Grid', self.viewGrid, QtCore.Qt.CTRL + QtCore.Qt.Key_G)

        # create the menu items for 'Tools'
        self.tools.addAction('&Validate', self.validateScenario, QtCore.Qt.CTRL + QtCore.Qt.Key_V)

        # create the splitter and make it the main widget
        self.splitter = QtWidgets.QSplitter(QtCore.Qt.Horizontal, self)
        self.splitter.setFocus()
        self.setCentralWidget(self.splitter)

        # create the palette
        self.palette = QtWidgets.QTabWidget(self.splitter)

        # and all its tabs
        self.iconview = IconView(self)
        self.unionview = UnitView(self, UNION)
        self.rebelview = UnitView(self, REBEL)
        self.objectiveview = ObjectiveView(self)
        self.locationview = LocationView(self)
        self.blockview = BlockView(self)
        self.weaponview = WeaponView(self)
        self.scenarioview = ScenarioView(self)
        self.pluginview = PluginView(self)

        # add the tabs too
        self.palette.addTab(self.iconview, "Icons")
        self.palette.addTab(self.rebelview, "Rebel units")
        self.palette.addTab(self.unionview, "Union units")
        self.palette.addTab(self.scenarioview, "Scenario info")
        self.palette.addTab(self.objectiveview, "Objectives")
        self.palette.addTab(self.locationview, "Locations")
        self.palette.addTab(self.blockview, "Blocks")
        self.palette.addTab(self.weaponview, "Weapons")
        self.palette.addTab(self.pluginview, "Plugins")

        # disable all tabs
        self.palette.setDisabled(1)

        # create the map view
        self.mapscrollview = QtWidgets.QScrollArea(self.splitter)
        self.mapview = MapView(self.mapscrollview, self)

        # store it globally too
        globals.mapview = self.mapview

        # create the canvas and store it for global access
        self.mapscrollview.addChild(self.mapview, 0, 0)

        self.connect(self.rebelview, PYSIGNAL('currentUnitChanged'), self.mapview, SLOT("repaint()"))
        self.connect(self.unionview, PYSIGNAL('currentUnitChanged'), self.mapview, SLOT("repaint()"))
        self.connect(globals.mapview, PYSIGNAL('mapClickedLeft'), self.mapClickedLeft)
        self.connect(globals.mapview, PYSIGNAL('mapClickedMid'), self.mapClickedMid)
        self.connect(globals.mapview, PYSIGNAL('mapClickedRight'), self.mapClickedRight)
        self.connect(globals.mapview, PYSIGNAL('mapMove'), self.mapMove)

        # we want to know when the date changes so that the weapons can be kept up to date
        self.connect(self.scenarioview, PYSIGNAL('dateChanged'), self.weaponview.refresh)

        # set a default save name
        self.file_name = 'default.civil'

        # set a suitable caption
        self.setCaption('Civil Scenario Editor')
        self.statusBar().message('Ready', 2000)

        # by default create a new scenario
        createNewScenario(self, 40, 40)

        self.show()

    def new(self):
        """
        Callback for the menuitem 'File->New'. Asks the user weather a new scenario should be started
        and discards ny old if wanted.
        """

        # ask the user what to do
        result = QtWidgets.QMessageBox.warning(self, "New scenario", "Really create a new scenario?", "Yes", "No")

        # did we get a 1, which is the second button?
        if result == 1:
            # yep, don't quit
            return

        # create and show the dialog
        if NewScenario(self).exec_loop() == QtWidgets.QDialog.Rejected:
            # nothing done, go away
            return

        # enable menu entries for saving
        self.file.setItemEnabled(MainWindow.ITEM_SAVE, 1)
        self.file.setItemEnabled(MainWindow.ITEM_SAVE_AS, 1)

    def open(self):
        """
        Callback for the menuitem 'File->Open'. Asks the user for the name of a scenario and
        loads it. Does not load the pickled LOS data, as it is enyway regenerated when saving.
        """
        # get file_name
        file_name = str(QtWidgets.QFileDialog.getOpenfile_name(None, "Civil scenarios (*.civil)", self))

        # did we get anything?
        if file_name is None or file_name == '':
            # no file, go away
            return

        # clean up the file_name
        file_name = str(file_name)

        try:
            # open the file as a zip file
            archive = zipfile.ZipFile(file_name)

            # get the main scenario file from the archive
            data = archive.read('scenario.xml')
            info = archive.read('info.xml')

            # note that we do not parse the los data at all, as it is anyway regenerated when saving

            # and close it
            archive.close()

        except:
            # oops parsing failed
            QtWidgets.QMessageBox.warning(self, "Error loading file", "The scenario file %s is invalid." % file_name,
                                          "&Ok")

            # print stack trace
            print("-" * 75)
            traceback.print_exc(file=sys.stdout)
            print("-" * 75)

        # TODO
        # QtWidgets.QMessageBox.warning ( self, "TODO", "TODO: should clear all data first!", "&Yeah" )

        try:
            # parse the file
            ScenarioParser().parseString(data)

            # store new file_name
            self.file_name = file_name

            # add all destroyed units to all of the units. we can while designing have units with 0
            # men, and we should not mark those as 'destroyed', as the parser does. just add them
            scenario.info.units.update(scenario.info.destroyed_units)

            # make sure the mapview  knows the new map 
            self.mapview.refresh()

            # and the unit views need refreshing too
            self.unionview.refresh()
            self.rebelview.refresh()

            # objectives too
            self.objectiveview.refresh()
            self.locationview.refresh()

            # and the scenarioview should be reset too
            self.scenarioview.refresh()

            # enable all tabs
            self.palette.setEnabled(1)

            # enable menu entries for saving
            self.file.setItemEnabled(MainWindow.ITEM_SAVE, 1)
            self.file.setItemEnabled(MainWindow.ITEM_SAVE_AS, 1)

        except:
            # oops parsing failed
            QtWidgets.QMessageBox.warning(self, "Error loading file", "Failed to load the file %s" % file_name, "&Ok")

            # print stack trace
            print("-" * 75)
            traceback.print_exc(file=sys.stdout)
            print("-" * 75)

        globals.mapview.repaintVisible()

    def undo(self):
        """
        Peforms an undo.
        """
        undostack.undo()

    def save(self):
        """
        Callback for the menuitem 'File->Save'. Saves the current scenario with a default name or the
        one used when the scenario was saved using 'File->Save As'.
        """

        # assume the map is valid
        scenario.info.setValid(1)

        # check the heights of the map to make sure all is ok. if the map is supposed to be finished
        # the user will want to know about the errors before saving
        try:
            scenario.map.calculateAbsoluteHeights()

        except MapHeightException as e:
            # oops, we got errors,
            count = len(e.value)

            # make the error text
            text = 'There seems to be %d height errors in the map. The map can not ' % count
            text += 'be used in the game before it is fully valid. Continue with save?'

            # ask the user what to do
            result = QtWidgets.QMessageBox.warning(self, "Map height errors", text, "Yes", "No")

            # did we get a 1, which is the second button?
            if result == 1:
                # yep, don't save
                return

            # the map is not valid
            scenario.info.setValid(0)

        # map is valid, so create the LOS map once and for all
        scenario.map.createLosMap()

        # show message
        self.statusBar().message('Saving scenario to file ' + self.file_name)

        # update the scenario info from the view first so that it's up-to-date in the central
        # ScenarioInfo object too
        self.scenarioview.store()

        # create a new scenario writer and write out the data with the scenario info 
        ScenarioWriter().write(self.file_name)

        self.statusBar().message('Scenario saved', 3000)

    def saveAs(self):
        """
        Callback for the menuitem 'File->Save As'. Saves the current scenario with a name that is
        asked from the user. Stores the used name as the new default name.
        """

        # get file_name
        file_name = str(QtWidgets.QFileDialog.getSavefile_name(None, "Civil scenarios (*.civil)", self))

        # did we get anything?
        if file_name is None or file_name == '':
            # no file, go away
            return

        # clean up the file_name
        self.file_name = str(file_name)

        # call method for saving
        self.save()

    def quit(self):
        """
        Callback for the menuitem 'File->Quit'. Asks the player weather the application should be
        quit, and quits if wanted.
        """
        # ask the user what to do
        result = QtWidgets.QMessageBox.warning(self, "Really quit", "Really quit the application?", "Yes", "No")

        # did we get a 1, which is the second button?
        if result == 1:
            # yep, don't quit
            return

        # quit
        # TODO qApp unresolved
        qApp.quit()

    def viewGrid(self):
        """
        Callback for the menuitem 'View->Grid'. Toggles the visibility of the helper grid in the
        mapview.
        """
        self.mapview.toggleGrid()

    def clear(self):
        """
        Callback for the menuitem 'Edit->Clear'. Asks the player weather the map should be cleared to
        the currently selected icon.
        """
        # ask the user what to do
        result = QtWidgets.QMessageBox.warning(self, "Really clear map", "Really clear the map and fill with " +
                                               "the current icon?", "Yes", "No")

        # did we get a 1, which is the second button? 
        if result == 1:
            # yep, don't do it
            return

        # do we have a selected icon?
        if not globals.icons.hasSelected():
            return

        # get the size of the map
        sizex, sizey = scenario.map.getSize()

        # get selected icon
        icon = globals.icons.getSelected()

        # loop and set the new initial icon (or hex really) for the map
        for x in range(sizex):
            for y in range(sizey):
                scenario.map.getHexes()[y][x] = Hex(x, y, icon)

        # repaint it all
        self.mapview.canvas.repaint()
        # self.mapview.repaint ( 0, 0, self.mapview.width () - 1, self.mapview.height () - 1 )

    def validateScenario(self):
        """
        Validates the current scenario. Checks all the data in the scenario that must be valid
        for the scenario to be valid. Shows a summary to the user about the state of the
        scenario. Marks the map as valid or invalid depending on the result.
        """

        # all the views that are allowed to validate data
        views = ((self.iconview, "Map"),
                 (self.rebelview, "Rebel units"),
                 (self.unionview, "Union units"),
                 (self.scenarioview, "Scenario data"),
                 (self.objectiveview, "Objectives"),
                 (self.locationview, "Locations"),
                 (self.weaponview, "Weapons"))

        # initial message
        report = ""

        # no errors yet
        errors = 0

        # loop over all views and validate them
        for view, name in views:
            # validate the view and get the result
            text = view.validate()

            # do we have errors?
            if text is not None:
                # add the text to the report
                report += '<p><b>%s</b><br/>\n%s</p>\n' % (name, text)

                # we have errors now
                errors = 1

        # all modules traversed and validated, did we get any errors?
        if errors:
            # yep, so add a short blurb about that
            header = "<qt><p>The scenario contains the following errors that must be fixed before the "
            header += "scenario can be used in <em>Civil</em>:</p>"

            # add the header
            report = header + report

            # errors, not valid
            scenario.info.setValid(0)
        else:
            # no errors
            report = "<qt><p>The scenario contains no errors and can be used in <em>Civil</em>.</p></qt>"

            # no errors, ok
            scenario.info.setValid(1)

        # add a footer to the report
        report += "</qt>"

        # show the report to the user
        QtWidgets.QMessageBox.information(self, "Validation summary", report, "&Ok")

    def mapMove(self, x, y, hexx, hexy):
        """
        Callback triggered when the user drags the mouse in the map.
        """
        self.mapClickedLeft(x, y, hexx, hexy)

    def mapClickedLeft(self, x, y, hexx, hexy):
        """
        Callback triggered when the map has been clicked.
        """

        # get current child tab
        child = self.palette.currentPage()

        # try:
        # let the child handle the click
        child.mapClickedLeft(x, y, hexx, hexy)

        # except:
        #    print "MainWindow.mapClickedLeft: child should handle mapClickedLeft():", child

    def mapClickedMid(self, x, y, hexx, hexy):
        """
        Callback triggered when the map has been clicked.
        """

        # get current child tab
        child = self.palette.currentPage()

        try:
            # let the child handle the click
            child.mapClickedMid(x, y, hexx, hexy)

        except:
            print("MainWindow.mapClickedMid: child should handle mapClickedMid():", child)

    def mapClickedRight(self, x, y, hexx, hexy):
        """
        Callback triggered when the map has been clicked.
        """

        # get current child tab
        child = self.palette.currentPage()

        try:
            # let the child handle the click
            child.mapClickedRight(x, y, hexx, hexy)

        except:
            print("MainWindow.mapClickedRight: child should handle mapClickedRight():", child)

        # repaint the map
        self.mapview.repaint(x, y, 1, 1, 1)
        # self.mapview.repaint ( 0 )
