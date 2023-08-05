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

import os
import re

from PyQt5 import QtWidgets, QtGui, QtCore

from civil.editor import globals
from civil.editor import undostack
from civil import properties
from civil.model import scenario
from civil.editor.editor_map import MapHeightException
from civil.map.hex import Hex
from civil.editor.icons import Icons


class IconTooltip(QtWidgets.QToolTip):
    """
    This class is used as a dynamic tooltip. It is a tooltip that can query the canvas for a icon
    at the mouse position. This is useful when doing blocks and the id is needed.
    """

    def __init__(self, parent):
        QtWidgets.QToolTip.__init__(self, parent)

    def maybeTip(self, pos):
        """
        Callback called when the tooltip should maybe be called. Creates a new tip and shows it if
        appropriate. The text contains the id of the icon under the cursor.
        """
        # get the icon if and a rect that contains it
        iconid, rect = self.parentWidget().iconAtPos(pos)

        # do we have an icon at that position?
        if iconid == -1:
            # nope, get lost
            return

        # create a text with the id
        text = "Icon %d" % iconid

        # show the tip
        self.tip(rect, text)


class IconCanvas(QtWidgets.QWidget):
    """

    """
    def __init__(self, parent):
        """
        Initializes the instance.
        """
        QtWidgets.QWidget.__init__(self, parent)

        # set a darker background. this same color is used later when erasing the selection rectangle
        # TODO use qss for that
        # self.setBackgroundMode(QtWidgets.QWidget.PaletteDark)

        # nothing selected yet
        self.gui_selectedx = -1
        self.gui_selectedy = -1

        # create the custom dynamic tooltip
        # TODO error TypeError: PyQt5.QtWidgets.QToolTip cannot be instantiated or sub-classed
        # self.tip = IconTooltip(self)

    def paintRect(self, x, y, color, painter=None):
        """
        Paints a rectangle around the icon at (x,y) in the passed color. The position is not
        pixels, but a row/col for the icon. If no painter is passed one is created.
        """

        # did we get a current painter?
        if painter is None:
            painter = QtGui.QPainter(self)

        # make a the custom pen with our wanted color and 3 pixels wide
        painter.setPen(QtGui.QPen(color, 3))

        # Draw rectangle
        painter.drawRect(x * 51 - 1, y * 51 - 1, 54, 54)

    def paintEvent(self, event):
        """
        Paints out all icons.
        """
        # get the width
        width = self.width()

        # get the number of icons that fits in the x-dimension and the required number of rows
        fits_x = int(width / 51)
        fits_y = int(max(globals.icons.keys()) / fits_x) + 1

        # start painting
        painter = QtGui.QPainter(self)
        x = 0
        y = 0

        # get the id of the selected icon
        selected = globals.icons.getSelected()

        # loop over the icons
        for id in range(1, max(globals.icons.keys()) + 1):
            if globals.icons.isInvalid(id):
                pass
            else:
                # it's ok, paint icon
                painter.drawPixmap(2 + x * 51, 2 + y * 51, globals.icons[id])

                # is this the selected icon?
                if id == selected:
                    # yep, paint a red frame
                    self.paintRect(x, y, QtCore.Qt.red, painter)

            # increment x and check overflow
            x += 1
            if x == fits_x:
                x = 0
                y += 1

    def mouseReleaseEvent(self, event):
        """
        Callback triggered when the mouse is released. Selects the current icon that was pressed.
        """

        # left button pressed?
        if event.button() != QtCore.Qt.LeftButton:
            return

        # get the width
        width = self.width()

        # get the number of icons that fits in the x-dimension and the required number of rows
        fits_x = int(width / 51)
        fits_y = int(max(globals.icons.keys()) / fits_x) + 1

        # get the position of the click
        x = event.x()
        y = event.y()

        # get row and column
        row = y / 51
        col = x / 51

        # precautions
        if row >= fits_y or col >= fits_x:
            return

        # get new selected id
        id = row * fits_x + col + 1

        # is that icon valid?
        if globals.icons.isInvalid(id):
            # it's not valid, so don't make it selected
            return

        # it's fully ok, set it as the new selected icon
        globals.icons.setSelected(row * fits_x + col + 1)

        # get the current palette and from it extract the "dark" color so that we can fill the old red
        # rectangle
        pal = self.palette()
        color = pal.color(QtGui.QPalette.Active, QtGui.QColorGroup.Dark)

        # erase the old rectangle
        self.paintRect(self.gui_selectedx, self.gui_selectedy, color)

        # and paint the new one
        self.paintRect(col, row, QtCore.Qt.red)

        # store coordinates for later use
        self.gui_selectedx = col
        self.gui_selectedy = row

    def iconAtPos(self, pos):
        """
        Returns the id of the icon at the given position and a rect that contains it. This is used
        for showing tooltips of the icons.
        """

        # get the width
        width = self.width()

        # get the number of icons that fits in the x-dimension and the required number of rows
        fits_x = int(width / 51)
        fits_y = int(max(globals.icons.keys()) / fits_x) + 1

        # split the position 
        x = pos.x()
        y = pos.y()

        # get row and column
        row = y / 51
        col = x / 51

        # precautions
        if row >= fits_y or col >= fits_x:
            return -1, None

        # get new selected
        return row * fits_x + col + 1, QtCore.QRect(col * 51, row * 51, 51, 51)


class IconView(QtWidgets.QScrollArea):
    """
    This class defines the actual palette of the selectable icons.
    """

    def __init__(self, parent):
        """
        Initializes the instance.
        """
        QtWidgets.QScrollArea.__init__(self, parent)

        # no icons yet
        globals.icons = Icons()

        # load the icons
        self.loadIcons(properties.path_terrains)

        # create the canvas
        self.canvas = IconCanvas(self)
        # TODO AttributeError: 'IconView' object has no attribute 'addChild'
        # self.addChild(self.canvas, 0, 0)

        # TODO AttributeError: 'IconView' object has no attribute 'setVScrollBarMode'
        #self.setVScrollBarMode(QtWidgets.QScrollArea.AlwaysOn)

    def loadIcons(self, path):
        """
        Loads the icons from the given path and stores internally.
        """

        # get a list of all files in the icons directory
        allFiles = os.listdir(path)

        # create the regular expression for matching the id in the name
        iconExp = re.compile('^t-.+([0-9]{3}).png$')

        # load a mask for transparency
        mask = QtGui.QBitmap('editor/mask.png')

        # loop over all files in the directory
        for file in allFiles:
            # attempt to match the expression
            match = iconExp.search(file)

            # did it match?
            if match:
                # yep, load it
                icon = QtGui.QPixmap(properties.path_terrains + file)

                # set a mask
                # TODO: does not work
                icon.setMask(mask)

                # store it
                globals.icons[int(match.group(1))] = icon

        print("loadIcons: loaded %d icons" % len(globals.icons))

    def resizeEvent(self, event):
        """
        Overloaded resize event so that we can resize the contents of the canvas.
        """

        # get the number of icons that fits in the x-dimension and the required number of rows
        fits_x = int((self.width() - self.verticalScrollBar().width()) / 51)
        fits_y = int(max(globals.icons.keys()) / fits_x) + 1

        # resize the canvas
        self.canvas.resize(self.width() - self.verticalScrollBar().width(), fits_y * 51)

        # deliver the event further
        QtWidgets.QScrollArea.resizeEvent(self, event)

    def pasteNoUndo(self, selected, hexx, hexy):
        """

        Args:
            selected: 
            hexx: 
            hexy: 
        """
        new = Hex(selected)

        # set the icon for the clicked hex to our selected icon
        scenario.map.getHexes()[hexy][hexx] = new

        # paste in that icon
        globals.mapview.pasteIcon(hexx, hexy)

    def paste(self, selected, hexx, hexy):
        """

        Args:
            selected: 
            hexx: 
            hexy: 

        Returns:

        """
        # do we have a selected icon?
        if selected == -1:
            # nope, go away
            return

        old = scenario.map.getHexes()[hexy][hexx]
        new = Hex(selected)

        # Already set this hex, don't set again..
        if old == new:
            return

        # Note the undo is done here, after the return
        # Even though this is illogical, we avoid the case
        # when LMB is down and the user pastes the same icon
        # over and over again. Grr..
        undostack.addUndo(hexx, hexy)

        # set the icon for the clicked hex to our selected icon
        scenario.map.getHexes()[hexy][hexx] = new

        # paste in that icon
        globals.mapview.pasteIcon(hexx, hexy)

    def validate(self):
        """
        Validates the part of the scenario that this view is responsible for creating. Returns a
        free text report that indicates the validation result or None if all is ok.
        """

        # check the heights of the map to make sure all is ok. if the map is supposed to be finished
        # the user will want to know about the errors before saving
        try:
            scenario.map.calculateAbsoluteHeights()

            # all is ok
            return None

        except MapHeightException as e:
            # oops, we got errors,
            count = len(e.value)

            # make the error text
            text = 'there seems to be %d height errors in the map.' % count

            # return the error
            return text

    def mapClickedLeft(self, x, y, hexx, hexy):
        """
        Callback triggered when the map has been clicked. Sets the selected hex as the hex for the
        position (hexx,hexy) in the map.
        """

        # get the selected icon (if any)
        selected = globals.icons.getSelected()

        self.paste(selected, hexx, hexy)
