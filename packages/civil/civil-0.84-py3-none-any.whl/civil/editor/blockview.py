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

from PyQt5 import QtWidgets, QtGui, QtCore

from civil.editor import globals
from civil.editor import undostack
from civil.editor.block import Block
from civil.model import scenario
from civil.map.hex import Hex


class BlockPreview(QtWidgets.QWidget):
    """
    This class implements the raw canvas of the map.
    """

    def __init__(self, parent):
        QtWidgets.QWidget.__init__(self, parent)

        self.setBackgroundMode(QtWidgets.QWidget.PaletteDark)

        # no previewed block yet
        self.block = None

    def paintEvent(self, event):
        """
        Paints out the preview.
        """

        # do we have a block already?
        if self.block is None:
            # no, nothing to do here
            return

        # start painting
        painter = QtGui.QPainter(self)

        # loop over all icons
        for x, y, id in self.block.getIcons():
            # get the terrain
            icon = globals.icons[id]

            if y % 2 == 0:
                # the icon is painted as far left as possible
                posx = x * 48
                posy = y * 36

            else:
                # the icon is indented half a hex to the right.
                posx = x * 48 + 24
                posy = y * 36

            # paint icon
            painter.drawPixmap(posx, posy, icon)

    def setBlock(self, block):
        """
        Stores a new block to be previewed.
        """
        self.block = block

        # get the block size
        x, y = block.getSize()

        # resize ourselves to fit
        self.resize(x * 48 + 24, y * 48)

        # repaint ourselves
        self.repaint()


class BlockList(QtWidgets.QListView):
    """
    This class extends a normal listbox and provides the possibility to use a popup menu with
    it. When something is selected from the menu a signal is emitted.
    """

    # menu items
    NEW = 10
    EDIT = 11
    DELETE = 12

    def __init__(self, parent):
        """
        Initializes the instance.
        """
        QtWidgets.QListView.__init__(self, parent)

        # create the popup menu
        self.popup = QtWidgets.QMenu(self)

        self.popup.insertItem('New', self.new, QtCore.Qt.CTRL + QtCore.Qt.Key_N, BlockList.NEW)
        self.popup.insertItem('Edit', self.edit, QtCore.Qt.CTRL + QtCore.Qt.Key_E, BlockList.EDIT)
        self.popup.insertItem('Delete', self.delete, QtCore.Qt.CTRL + QtCore.Qt.Key_D, BlockList.DELETE)

    def mousePressEvent(self, event):
        """
        Callback handling the fact that the user has pressed some mouse button. shows the menu on the
        right button.
        """

        # is this the right button?
        if event.button() != QtCore.Qt.RightButton:
            # nope, perform normal stuff
            QtWidgets.QListView.mousePressEvent(self, event)
            return

        # do we have a block selected
        if self.currentItem() == -1:
            # no item, so the listview is empty, disable all items that should not be active
            self.popup.setItemEnabled(BlockList.EDIT, 0)
            self.popup.setItemEnabled(BlockList.DELETE, 0)

        else:
            # an item is selected, enable the items
            self.popup.setItemEnabled(BlockList.EDIT, 1)
            self.popup.setItemEnabled(BlockList.DELETE, 1)

            # show the popup
        self.popup.move(event.globalPos())
        self.popup.show()

    def mouseReleaseEvent(self, event):
        """
        Callback handling the fact that the user has released a mouse button. Hides the menu on the
        right button.
        """

        # is this the right button?
        if event.button() == QtCore.Qt.RightButton:
            # just hide the popup
            self.popup.hide()

        else:
            # perform normal stuff
            QtWidgets.QListView.mouseReleaseEvent(self, event)

    def new(self):
        """
        Callback triggered when a new block should be created. Just emits a signal so that the
        parent can react to it.
        """
        # emit a 'new' signal
        # TODO old style signals, use new style
        self.emit(PYSIGNAL('menuItemNew'), ())

    def edit(self):
        """
        Callback triggered when a block should be edited. Just emits a signal so that the
        parent can react to it.
        """
        # emit a 'edit' signal
        self.emit(PYSIGNAL('menuItemEdit'), ())

    def delete(self):
        """
        Callback triggered when a block should be deleted. Just emits a signal so that the
        parent can react to it.
        """
        # emit a 'delete' signal
        self.emit(PYSIGNAL('menuItemDelete'), ())


############################################################################################### 
class BlockView(QtWidgets.QSplitter):
    """
    This class...
    """

    def __init__(self, parent):
        """
        Initializes the instance.
        """

        QtWidgets.QSplitter.__init__(self, QtCore.Qt.Vertical, parent)

        # create the listbox and the scrollview
        self.blocklist = BlockList(self)
        self.previewcontainer = QtWidgets.QScrollArea(self)

        # create the actual preview too
        self.preview = BlockPreview(self.previewcontainer)

        # no blocks yet
        self.blocks = []

        # loop over all blocks we can find
        for file_name in os.listdir('editor/data/blocks/'):
            # does the file_name end with .xml?
            if file_name.endswith('.xml'):
                # yep, create a new block
                block = Block('editor/data/blocks/' + file_name)

                # yep, add it to the listbox
                self.blocklist.insertItem(block.getName())

                # add to list of blocks
                self.blocks.append(block)

        # connect signals to callbacks
        self.connect(self.blocklist, SIGNAL('selectionChanged()'), self.blockSelected)
        self.connect(self.blocklist, PYSIGNAL('menuItemNew'), self.new)
        self.connect(self.blocklist, PYSIGNAL('menuItemEdit'), self.edit)
        self.connect(self.blocklist, PYSIGNAL('menuItemDelete'), self.delete)

    def blockSelected(self):
        """
        Callback triggered when a new item is selected in the listbox.
        """
        # get the selected block
        block = self.blocks[self.blocklist.currentItem()]

        # assign the block as the previewed block
        self.preview.setBlock(block)

    def mapClickedLeft(self, x, y, hexx, hexy):
        """
        Callback triggered when the map has been clicked. Sets an objective at the map
        position. It gets the currently selected objective (if any) and changes its position to that
        of the clicked hex.
        """

        # get the selected block index (if any)
        index = self.blocklist.currentItem()

        # do we have a selected icon?
        if index == -1:
            # nope, go away
            return

        # ok, get the actual block too
        block = self.blocks[index]

        # Create the undo list
        hexes = []
        for iconx, icony, id in block.getIcons():
            if hexy % 2 == 1 and icony % 2 == 1:
                iconx += 1
            hexes.append((iconx + hexx, icony + hexy))

        # Remember these hexes
        undostack.addUndoList(hexes)

        # loop over all icons in the block
        for iconx, icony, id in block.getIcons():

            # fix the offset for even rows so that we always keep the same "formation". If it's an odd row
            # that was clicked and the icon row is odd then x is offset on hex to the right
            if hexy % 2 == 1 and icony % 2 == 1:
                iconx += 1

            # set the icon for the hex to our selected icon
            scenario.map.getHexes()[icony + hexy][iconx + hexx] = Hex(id)

            # paste in the icon
            globals.mapview.pasteIcon(iconx + hexx, icony + hexy)

    def new(self):
        """
        Callback triggered when a new block should be created.
        """
        print("BlockView.new")

    def edit(self):
        """
        Callback triggered when a block should be edited.
        """
        print("BlockView.edit")

    def delete(self):
        """
        Callback triggered when a block should be deleted. Will delete the currently selected
        block from the list and disk if possible.
        """
        print("BlockView.delete")
