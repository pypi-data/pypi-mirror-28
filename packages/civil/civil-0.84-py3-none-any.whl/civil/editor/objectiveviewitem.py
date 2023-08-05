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


class ObjectiveItem(QtWidgets.QListWidgetItem):
    """
    This class subclasses a normal QtWidgets.QListWidgetItem and adds needed functionality, such as keeping of
    the objective the item represents. The objective can be retrieved using the 'getObjective()'
    method.
    """

    def __init__(self, parent, objective):
        # create the strings for the item
        name = objective.getName()
        points = str(objective.getPoints())
        owner = {UNKNOWN: "unknown", REBEL: "rebel", UNION: "union"}[objective.getOwner()]

        QtWidgets.QListWidgetItem.__init__(self, parent, name, points, owner)

        # store the objective
        self.objective = objective

    def getObjective(self):
        """
        Returns the objective this item represents.
        """
        return self.objective

    def update(self):
        """
        Updates the labels for the item. Can be used if the objective has changed.
        """

        # set the new labels
        self.setText(0, self.objective.getName())
        self.setText(1, str(self.objective.getPoints()))
        self.setText(2, {UNKNOWN: "unknown", REBEL: "rebel", UNION: "union"}[self.objective.getOwner()])
