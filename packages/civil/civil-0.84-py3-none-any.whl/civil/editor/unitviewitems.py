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

from PyQt5 import QtWidgets, QtGui


class BrigadeItem(QtWidgets.QListWidgetItem):
    """
    This class subclasses a normal QtWidgets.QListWidgetItem and adds needed functionality, such as keeping of
    the brigade the item represents. Th brigade can be retrieved using the 'getBrigade()' method.
    """

    def __init__(self, parent, brigade):
        QtWidgets.QListWidgetItem.__init__(self, parent, brigade.name, "")

        # store the brigade
        self.brigade = brigade

        # set the item to be open by default
        self.setOpen(1)

        # set the displayed data
        self.update()

    def getOrganization(self):
        """
        Returns the organization that this item contains.
        """
        return self.getBrigade()

    def getBrigade(self):
        """
        Returns the brigade this item represents.
        """
        return self.brigade

    def update(self):
        """
        Updates the labels for the item. Can be used if the objective has changed.
        """
        # set the displayed data
        self.setText(0, self.brigade.getName())


class RegimentItem(QtWidgets.QListWidgetItem):
    """
    This class subclasses a normal QtWidgets.QListWidgetItem and adds needed functionality, such as keeping of
    the regiment the item represents. Th regiment can be retrieved using the 'getRegiment()' method.
    """

    def __init__(self, parent, regiment):
        QtWidgets.QListWidgetItem.__init__(self, parent, regiment.name, "")

        # store the regiment
        self.regiment = regiment

        # set the item to be open by default
        self.setOpen(1)

        # set the displayed data
        self.update()

    def getOrganization(self):
        """
        Returns the organization that this item contains.
        """
        return self.getRegiment()

    def getRegiment(self):
        """
        Returns the regiment this item represents.
        """
        return self.regiment

    def update(self):
        """
        Updates the labels for the item. Can be used if the objective has changed.
        """
        # set the displayed data
        self.setText(0, self.regiment.getName())


class BattalionItem(QtWidgets.QListWidgetItem):
    """
    This class subclasses a normal QtWidgets.QListWidgetItem and adds needed functionality, such as keeping of
    the battalion the item represents. Th battalion can be retrieved using the 'getBattalion()'
    method.
    """

    def __init__(self, parent, battalion):
        QtWidgets.QListWidgetItem.__init__(self, parent, battalion.name, "")

        # store the battalion
        self.battalion = battalion

        # set the item to be open by default
        self.setOpen(1)

        # set the displayed data
        self.update()

    def getOrganization(self):
        """
        Returns the organization that this item contains.
        """
        return self.getBattalion()

    def getBattalion(self):
        """
        Returns the battalion this item represents.
        """
        return self.battalion

    def update(self):
        """
        Updates the labels for the item. Can be used if the objective has changed.
        """
        # set the displayed data
        self.setText(0, self.battalion.getName())


class UnitItem(QtWidgets.QListWidgetItem):
    """
    This class subclasses a normal QtWidgets.QListWidgetItem to provide a common base class for all unit
    items.
    """

    def __init__(self, parent):
        # init superclass
        # TODO unit unknown
        QtWidgets.QListWidgetItem.__init__(self, parent, unit)


class HeadquarterItem(UnitItem):
    """
    This class subclasses a normal QtWidgets.QListWidgetItem and adds needed functionality, such as keeping of
    the company the item represents. The company can be retrieved using the 'getCompany()'
    method.
    """

    # icon
    icon = None

    def __init__(self, parent, hq):
        QtWidgets.QListWidgetItem.__init__(self, parent)

        # store the company
        self.company = hq

        # do we have an icon already?
        if not HeadquarterItem.icon:
            # nope, load it
            HeadquarterItem.icon = QtGui.QPixmap('../gfx/editor/button-hq.png')

        # set the displayed data
        self.update()

    def getCompany(self):
        """
        Returns the company this item represents.
        """
        return self.company

    def update(self):
        """
        Updates the labels for the item. Can be used if the objective has changed.
        """
        # set the displayed data
        self.setText(0, self.company.getName())
        self.setPixmap(1, HeadquarterItem.icon)
        self.setText(2, str(self.company.getMen()))


class InfantryItem(UnitItem):
    """
    This class subclasses a normal QtWidgets.QListWidgetItem and adds needed functionality, such as keeping of
    the company the item represents. The company can be retrieved using the 'getCompany()'
    method.
    """

    # icon
    icon = None

    def __init__(self, parent, company):
        QtWidgets.QListWidgetItem.__init__(self, parent)

        # store the company
        self.company = company

        # do we have an icon already?
        if not InfantryItem.icon:
            # nope, load it
            InfantryItem.icon = QtGui.QPixmap('../gfx/editor/button-head.png')

        # set the displayed data
        self.update()

    def getCompany(self):
        """
        Returns the company this item represents.
        """
        return self.company

    def update(self):
        """
        Updates the labels for the item. Can be used if the objective has changed.
        """
        # set the displayed data
        self.setText(0, self.company.getName())
        self.setPixmap(1, InfantryItem.icon)
        self.setText(2, str(self.company.getMen()))


class CavalryItem(UnitItem):
    """
    This class subclasses a normal QtWidgets.QListWidgetItem and adds needed functionality, such as keeping of
    the company the item represents. Th company can be retrieved using the 'getCompany()'
    method.
    """

    # icon
    icon = None

    def __init__(self, parent, company):
        QtWidgets.QListWidgetItem.__init__(self, parent)

        # store the company
        self.company = company

        # do we have an icon already?
        if not CavalryItem.icon:
            # nope, load it
            CavalryItem.icon = QtGui.QPixmap('../gfx/editor/button-horse.png')

        # set the displayed data
        self.update()

    def getCompany(self):
        """
        Returns the company this item represents.
        """
        return self.company

    def update(self):
        """
        Updates the labels for the item. Can be used if the objective has changed.
        """
        # set the displayed data
        self.setText(0, self.company.getName())
        self.setPixmap(1, CavalryItem.icon)
        self.setText(2, str(self.company.getMen()))


class ArtilleryItem(UnitItem):
    """
    This class subclasses a normal QtWidgets.QListWidgetItem and adds needed functionality, such as keeping of
    the company the item represents. Th company can be retrieved using the 'getCompany()'
    method.
    """

    # icon
    icon = None

    def __init__(self, parent, company):
        QtWidgets.QListWidgetItem.__init__(self, parent)

        # store the company
        self.company = company

        # do we have an icon already?
        if not ArtilleryItem.icon:
            # nope, load it
            ArtilleryItem.icon = QtGui.QPixmap('../gfx/editor/button-gun.png')

        # set the displayed data
        self.update()

    def getCompany(self):
        """
        Returns the company this item represents.
        """
        return self.company

    def update(self):
        """
        Updates the labels for the item. Can be used if the objective has changed.
        """
        # set the displayed data
        self.setText(0, self.company.getName())
        self.setPixmap(1, ArtilleryItem.icon)
        self.setText(2, str(self.company.getMen()))
