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

from civil.editor import globals
from civil.model import scenario

# Our list of commands that can be used to undo
undoStack = []

# Maximum undo levels
UNDO_LEVELS = 50


def addUndoList(hexes):
    """
    hexes if a list of (hexx, hexy) of hexes that will be overwritten.
    """
    list = []
    for x, y in hexes:
        old = scenario.map.getHexes()[y][x]
        list.append((old, x, y))
    global undoStack
    if len(undoStack) == UNDO_LEVELS:
        undoStack.pop(0)
    assert (len(undoStack) < UNDO_LEVELS)
    undoStack.append(list)


def addUndo(hexx, hexy):
    """

    Args:
        hexx: 
        hexy: 
    """
    global undoStack
    if len(undoStack) == UNDO_LEVELS:
        undoStack.pop(0)
    assert (len(undoStack) < UNDO_LEVELS)

    old = scenario.map.getHexes()[hexy][hexx]
    undoStack.append([(old, hexx, hexy)])


def undo():
    """

    Returns:

    """
    global undoStack
    if len(undoStack) == 0:
        return

    # Take latest hex change
    hexes = undoStack.pop()

    for (hex, hexx, hexy) in hexes:
        # set the icon for the clicked hex to our selected icon
        scenario.map.getHexes()[hexy][hexx] = hex

        # paste in that icon
        globals.mapview.pasteIcon(hexx, hexy)
