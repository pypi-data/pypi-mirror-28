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

from PyQt5 import QtWidgets, QtGui, QtCore

from civil.editor.editor_map import MapHeightException
from civil.editor import globals
from civil import properties
from civil.model import scenario
from civil.constants import REBEL, UNION, INFANTRY, CAVALRY, ARTILLERY, HEADQUARTER


class MapView(QtWidgets.QWidget):
    """
    This class implements the raw canvas of the map. It is responsible for the actual painting of
    the map.
    """

    def __init__(self, parent, mainwindow):
        QtWidgets.QWidget.__init__(self, parent)

        self.mapview = parent

        # Urgh. Save a reference to the main window.
        self.mainwindow = mainwindow

        # self.setBackgroundMode ( QtWidgets.QWidget.NoBackground )
        self.setBackgroundMode(QtWidgets.QWidget.PaletteDark)

        # show a grid and no vectorized map
        self.showgrid = 1

        # loop over the
        self.uniticons = {REBEL: {},
                          UNION: {}}

        # load the icons
        self.loadUnitIcons()

        # no objectives yet
        self.objectiveicons = []

        # load objectives too
        self.loadObjectiveIcons()

        # load the icon for the selected unit
        self.loadSelectionIcon()

        # No map height errors
        self.height_errors = []

    def pasteIcon(self, x, y, painter=None):
        """

        Args:
            x: 
            y: 
            painter: 

        Returns:

        """
        # Invalid hex
        size = scenario.map.getSize()
        if x >= size[0] or y >= size[1]:
            return

        if painter is None:
            painter = QtGui.QPainter(self)
            # set a white pen
            painter.setPen(QtGui.QPen(QtCore.Qt.white, 2))

        oldpen = painter.pen()

        # get the terrain
        hex = scenario.map.getHexes()[y][x]
        icon = globals.icons[hex.getIconId()]

        if y % 2 == 0:
            # the icon is painted as far left as possible
            posx = x * 48 - 24
            posy = y * 36 - 12

        else:
            # the icon is indented half a hex to the right.
            posx = x * 48
            posy = y * 36 - 12

        # paint icon
        painter.drawPixmap(posx, posy, icon)

        # paint the grid?
        if self.showgrid:
            error = 0
            if (x, y) in self.height_errors:
                # set a red pen
                painter.setPen(QtGui.QPen(QtGui.QColor(255, 128, 128), 3))
                painter.drawRect(posx + 22, posy + 22, 4, 4)
                painter.setPen(oldpen)

                # BUG why doesn't the above line work?
                painter.setPen(QtGui.QPen(QtCore.Qt.white, 2))
            else:
                painter.drawRect(posx + 23, posy + 23, 2, 2)

    def paintEvent(self, event):
        """
        Paints out the map
        """
        # do we have a map now?
        if scenario.map is None:
            # no map, no custom painting
            QtWidgets.QWidget.paintEvent(self, event)
            return

        # get the size of the map
        sizex, sizey = scenario.map.getSize()

        # get the rectangle that is the area that needs repainting
        rect = event.rect()

        # get the coordinates for the update
        updatex1 = rect.x()
        updatey1 = rect.y()
        updatex2 = rect.right()
        updatey2 = rect.bottom()

        # get position of the hex in the upper left corner
        topcorner = scenario.map.pointToHex2((updatex1, updatey1))
        lowcorner = scenario.map.pointToHex2((updatex2, updatey2))

        # blow up the tuples
        updatex1, updatey1 = topcorner
        updatex2, updatey2 = lowcorner

        # fix coordinates to be a little bit more wide
        # fixing by 1 hex unit was not enough in all cases, so
        # I just made it 2 hex units instead => no gfx mess
        updatex1 = max(updatex1 - 2, 0)
        updatey1 = max(updatey1 - 2, 0)

        updatex2 = min(updatex2 + 2, sizex - 1)
        updatey2 = min(updatey2 + 2, sizey - 1)

        # Calculate new rectangle, now that we now how big it will be.
        # This means that units and objectives don't "disappear"
        # when we paint hexes over them, without actually painting
        # the units & objectives.
        xyupleft = scenario.map.hexToPoint((updatex1, updatey1))
        xyupleft = xyupleft[0] - properties.hex_size, xyupleft[1] - properties.hex_size
        xydownright = scenario.map.hexToPoint((updatex2, updatey2))
        xydownright = xydownright[0] + properties.hex_size, xydownright[1] + properties.hex_size

        newrect = QtCore.QRect(xyupleft[0], xyupleft[1], xydownright[1] - xyupleft[0], xydownright[1] - xyupleft[1])

        # start painting
        painter = QtGui.QPainter(self)

        # set a white pen
        painter.setPen(QtGui.QPen(QtCore.Qt.white, 2))

        # loop and paint the icons for the map
        for x in range(updatex1, updatex2 + 1):
            for y in range(updatey1, updatey2 + 1):
                self.pasteIcon(x, y, painter)

        # paint the units, locations and objectives too
        self.paintUnits(newrect, painter)
        self.paintObjectives(newrect, painter)
        self.paintLocations(newrect, painter)

    def paintUnits(self, rect, painter):
        """
        Repaints all units on the map that are inside the rectangle given by the passed
        parameters.
        """

        # enlarge the rect to be a little bigger
        rect = QtCore.QRect(rect.x() - 30, rect.y() - 30, rect.width() + 60, rect.height() + 60)

        # loop over all companies
        for unit in scenario.info.units.values():
            # got a unit, get it's position
            x, y = unit.getPosition()

            # offset the coordinates so that the unit is centered
            x -= 24
            y -= 24

            # BUG: added the "1 or" just to get it ti paint anything at all

            # is it inside?
            if 1 or rect.contains(QtCore.QPoint(int(x), int(y))):

                # get its icon
                icon = self.uniticons[unit.getOwner()][unit.getType()][unit.getFacing()]

                # get the half width/height used to center the icon
                halfwidth = icon.width() / 2
                halfheight = icon.height() / 2

                # is the unit selected?
                if unit == globals.currentunit:
                    # yes, get the half width and height of the icon
                    selection_halfwidth = self.selectionicon.width() / 2
                    selection_halfheight = self.selectionicon.height() / 2

                    # print "sel half", selection_halfwidth, selection_halfheight
                    # print "sel pos",    x + selection_halfwidth, y + selection_halfheight

                    # and draw it
                    painter.drawPixmap(x + selection_halfwidth, y + selection_halfheight, self.selectionicon)

                # draw the unit
                painter.drawPixmap(x - 0, y - 0, icon)
                # painter.drawPixmap ( x - halfwidth, y - halfheight, icon )

    def paintObjectives(self, rect, painter):
        """
        Repaints all objectives on the map that are inside the rectangle given by the passed
        parameters.
        """

        # enlarge the rect to be a little bigger
        rect = QtCore.QRect(rect.x() - 30, rect.y() - 30, rect.width() + 60, rect.height() + 60)

        # loop over all companies
        for objective in scenario.info.objectives:
            # got an objective, get it's position
            x, y = objective.getPosition()

            # is the position valid?
            if x < 0 or y < 0:
                # nope, don't paint
                continue

            # is it inside?
            if rect.contains(QtCore.QPoint(int(x), int(y))):
                # get its icon
                if objective.points >= 10:
                    # gold objective
                    icon = self.objectiveicons[0]
                else:
                    # silver objective
                    icon = self.objectiveicons[1]

                # and draw it
                painter.drawPixmap(x, y, icon)

                # Draw objective name "nicely"
                ty = y + 50
                tx = x
                name = objective.getName()
                painter.setPen(QtCore.Qt.black)
                for _y in range(ty - 1, ty + 2):
                    for _x in range(tx - 1, tx + 2):
                        painter.drawText(_x, _y, name)
                painter.setPen(QtCore.Qt.white)
                painter.drawText(tx, ty, name)

    def paintLocations(self, rect, painter):
        """
        Repaints all locations on the map that are inside the rectangle given by the passed
        parameters.
        """

        # enlarge the rect to be a little bigger
        rect = QtCore.QRect(rect.x() - 30, rect.y() - 30, rect.width() + 60, rect.height() + 60)

        # loop over all locations
        for location in scenario.info.locations:
            # got an location, get it's position
            x, y = location.getPosition()

            # is the position valid?
            if x < 0 or y < 0:
                # nope, don't paint
                continue

            # is it inside?
            if rect.contains(QtCore.QPoint(int(x), int(y))):
                # Draw objective name "nicely"
                ty = y
                tx = x
                name = location.getName()
                painter.setPen(QtCore.Qt.black)
                for _y in range(ty - 1, ty + 2):
                    for _x in range(tx - 1, tx + 2):
                        painter.drawText(_x, _y, name)
                painter.setPen(QtCore.Qt.white)
                painter.drawText(tx, ty, name)

    def toggleGrid(self):
        """
        Toggles the visibility of the grid.
        """
        # invert the value
        if self.showgrid:
            self.showgrid = 0

        else:
            self.showgrid = 1
            self.height_errors = []
            try:
                scenario.map.calculateAbsoluteHeights()
            except MapHeightException as e:
                self.height_errors = e.value

        self.repaintVisible()

    def refresh(self):
        """
        Resets the scenario this view views. All data is repainted and the new data is visualized.
        """
        # get the size
        x, y = scenario.map.getSize()

        # set canvas size
        self.resize(x * 48 - 24, y * 36 - 12)

    def repaintVisible(self):
        """

        """
        # repaint ourselves, but only the part that shows
        self.repaint(self.mapview.contentsX(), self.mapview.contentsY(),
                     self.mapview.visibleWidth(), self.mapview.visibleHeight())

    def mouseMoveEvent(self, event):
        """
        Callback trigegred when the user moves the mouse. Will emit a signal if the mouse is
        dragged, ie left mouse button is pressed while moving.
        """

        # We don't want anybody continuously drawing blocks
        if self.mainwindow.palette.currentPage() == self.mainwindow.blockview:
            return

        # get the position of the click
        x = event.x()
        y = event.y()

        # map the widget coordinate to a hex
        hexx, hexy = scenario.map.pointToHex2((x, y))

        # We can't ask event.button(), it isn't set!
        state = event.state()
        if state & QtCore.Qt.LeftButton:

            self.emit(PYSIGNAL('mapClickedLeft'), (x, y, hexx, hexy))

        elif state & QtCore.Qt.MidButton:
            self.emit(PYSIGNAL('mapClickedMid'), (x, y, hexx, hexy))

        elif state & QtCore.Qt.RightButton:
            self.emit(PYSIGNAL('mapClickedRight'), (x, y, hexx, hexy))

    def mouseReleaseEvent(self, event):
        """
        Callback triggered when the mouse is released. Paints the clicked position with the
        selected icon.
        """

        # get the position of the click
        x = event.x()
        y = event.y()

        # map the widget coordinate to a hex
        hexx, hexy = scenario.map.pointToHex2((x, y))

        # send out a signal to tell the world that we're clicked
        # left button pressed?
        if event.button() == QtCore.Qt.LeftButton:
            self.emit(PYSIGNAL('mapClickedLeft'), (x, y, hexx, hexy))

        elif event.button() == QtCore.Qt.MidButton:
            self.emit(PYSIGNAL('mapClickedMid'), (x, y, hexx, hexy))

        else:
            self.emit(PYSIGNAL('mapClickedRight'), (x, y, hexx, hexy))

    def loadUnitIcons(self):
        """

        """
        # load the icons 
        self.uniticons[REBEL][INFANTRY] = self.loadIcons("unit-type2")
        self.uniticons[REBEL][CAVALRY] = self.loadIcons("unit-type2")
        self.uniticons[REBEL][ARTILLERY] = self.loadIcons("unit-type2")
        self.uniticons[REBEL][HEADQUARTER] = self.loadIcons("unit-type2")

        # and union too
        self.uniticons[UNION][INFANTRY] = self.loadIcons("unit-type1")
        self.uniticons[UNION][CAVALRY] = self.loadIcons("unit-type1")
        self.uniticons[UNION][ARTILLERY] = self.loadIcons("unit-type1")
        self.uniticons[UNION][HEADQUARTER] = self.loadIcons("unit-type1")

    def loadIcons(self, type):
        """

        Args:
            type: 

        Returns:

        """
        # create the basename of the file names
        basename = properties.path_units + type + "-"

        # create the map we'll ultimately return. It is the map of all sizes
        icons = {}

        # loop over all angles from 0 to 35. These should be multiplied by 10 to get the real angle.
        for angle in range(1, 37):
            # convert the angle to a string
            anglestr = str(angle)

            # add necessary padding
            anglestr = "0" * (3 - len(anglestr)) + anglestr

            # create the file_name based on the angle
            file_name = os.path.join(basename, anglestr + ".png")

            # load it
            newicon = QtGui.QPixmap(file_name)

            # create a mask that makes sure we paint only what we want
            newicon.setMask(newicon.createHeuristicMask())

            # convert to our more efficient format and store
            icons[angle - 1] = newicon

        return icons

    def loadObjectiveIcons(self):
        """
        Loads in the icons for the objectives.
        """

        # just do it
        self.objectiveicons = [QtGui.QPixmap(properties.path_units + 'obj-gold.png'),
                               QtGui.QPixmap(properties.path_units + 'obj-silver.png')]

        # and set the masks too
        self.objectiveicons[0].setMask(self.objectiveicons[0].createHeuristicMask())
        self.objectiveicons[1].setMask(self.objectiveicons[1].createHeuristicMask())

    def loadSelectionIcon(self):
        """
        Loads in the icon for the selection. This icon is always shown under the current unit.
        """
        # load it
        self.selectionicon = QtGui.QPixmap(properties.layer_unit_icon_main)

        # and set the mask too
        self.selectionicon.setMask(self.selectionicon.createHeuristicMask())
