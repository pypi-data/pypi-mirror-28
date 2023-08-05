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

import copy

from PyQt5 import QtWidgets, QtCore

from civil.editor import globals
from civil.model import scenario
from civil.editor.unitviewitems import ArtilleryItem, HeadquarterItem, UnitItem
from civil.editor.unitviewitems import BrigadeItem, RegimentItem, BattalionItem, InfantryItem, CavalryItem
from civil.model.leader import Leader
from civil.model.modifier import Experience, Aggressiveness, RallySkill, Motivation
from civil.model.organization import Brigade, Regiment, Battalion
from civil.model.unit import Unit, InfantryCompany, CavalryCompany, ArtilleryBattery, Headquarter
from civil.util.math_utils import calculateAngle
from civil.editor.edit_organization import EditOrganization
from civil.editor.edit_unit import EditUnit


class UnitView(QtWidgets.QListView):
    """

    """
    # a static next id
    nextid = 0

    def __init__(self, parent, player):
        """
        Initializes the instance.
        """

        QtWidgets.QListView.__init__(self, parent)

        # store the player
        self.player = player

        # add the columns
        # TODO AttributeError: 'UnitView' object has no attribute 'addColumn'
        #self.addColumn('Name')
        #self.addColumn('Type')
        #self.addColumn('Men')

        # single selection and decorated root
        # TODO AttributeError: 'UnitView' object has no attribute 'setMultiSelection'
        #self.setMultiSelection(0)
        #self.setRootIsDecorated(1)

        # create the popup menu
        self.popup = QtWidgets.QMenu(self)

        self.popup.addAction('New brigade', self.newBrigade, QtCore.Qt.CTRL + QtCore.Qt.Key_B)
        self.popup.addAction('New regiment', self.newRegiment, QtCore.Qt.CTRL + QtCore.Qt.Key_R)
        self.popup.addAction('New battalion', self.newBattalion, QtCore.Qt.CTRL + QtCore.Qt.Key_A)
        self.popup.addAction('New infantry company', self.newInfantry, QtCore.Qt.CTRL + QtCore.Qt.Key_I)
        self.popup.addAction('New cavalry company', self.newCavalry, QtCore.Qt.CTRL + QtCore.Qt.Key_A)
        self.popup.addAction('New artillery battery', self.newArtillery, QtCore.Qt.CTRL + QtCore.Qt.Key_B)
        self.popup.addSeparator()

        # and the normal functions. note the order of the id:s!
        self.popup.addAction('Copy', self.copy, QtCore.Qt.CTRL + QtCore.Qt.Key_C)
        self.popup.addAction('Paste', self.paste, QtCore.Qt.CTRL + QtCore.Qt.Key_V)
        self.popup.addAction('Edit', self.edit, QtCore.Qt.CTRL + QtCore.Qt.Key_E)
        self.popup.addAction('Delete', self.delete, QtCore.Qt.CTRL + QtCore.Qt.Key_D)

        # make sure we know of all changed items
        self.connect(self, SIGNAL('currentChanged(QtWidgets.QListWidgetItem *)'), self.itemChanged)

        # currently copied organization
        self.copied = None

    def refresh(self):
        """
        This method is called when the view should refresh itself. This means clearing out all items
        that currently are in the tree and regenerate it from scratch. This method can be called after
        some scenario has been loaded or something other big changes to the units has happened.

        This method will simply loop over all structures and create new items.
        """
        # clear all old cruft first
        self.clear()

        # loop over all brigades that are ours
        for brigade in list(scenario.info.brigades[self.player].values()):
            # create a new item for it
            item1 = BrigadeItem(self, brigade)

            # create a new item for the hq too
            HeadquarterItem(item1, brigade.getHeadquarter())

            # get new max ids if needed
            UnitView.nextid = max(UnitView.nextid + 1, brigade.getId() + 1)
            UnitView.nextid = max(UnitView.nextid + 1, brigade.getHeadquarter().getId() + 1)

            # loop over all the regiments of the brigade
            for regiment in brigade.getRegiments():
                # create a new item for it
                item2 = RegimentItem(item1, regiment)

                # create a new item for the hq too
                HeadquarterItem(item2, regiment.getHeadquarter())

                # get new max ids if needed
                UnitView.nextid = max(UnitView.nextid + 1, regiment.getId() + 1)
                UnitView.nextid = max(UnitView.nextid + 1, regiment.getHeadquarter().getId() + 1)

                # loop over all battalions of the regiment
                for battalion in regiment.getBattalions():
                    # create a new item for it
                    item3 = BattalionItem(item2, battalion)

                    # create a new item for the hq too
                    HeadquarterItem(item3, battalion.getHeadquarter())

                    # get new max ids if needed
                    UnitView.nextid = max(UnitView.nextid + 1, battalion.getId() + 1)
                    UnitView.nextid = max(UnitView.nextid + 1, battalion.getHeadquarter().getId() + 1)

                    # loop over all companies of the battalion
                    for company in battalion.getCompanies():
                        # create a new item for it
                        self.createCompanyItem(company, item3)

                        # get new max id if needed
                        UnitView.nextid = max(UnitView.nextid + 1, company.getId() + 1)

                # loop over all companies of the regiment
                for company in regiment.getCompanies():
                    # create a new item for it
                    self.createCompanyItem(company, item2)

                    # get new max id if needed
                    UnitView.nextid = max(UnitView.nextid + 1, company.getId() + 1)

    def createCompanyItem(self, company, parentitem):
        """
        Helper method to create the proper listview item based on the type of the company. Artillery,
        infantry and cavalry have different items.
        """

        # so what do we have here?
        if isinstance(company, InfantryCompany):
            # infantry
            InfantryItem(parentitem, company)

        elif isinstance(company, CavalryCompany):
            # cavalry
            CavalryItem(parentitem, company)

        elif isinstance(company, ArtilleryBattery):
            # artillery
            ArtilleryItem(parentitem, company)

        elif isinstance(company, Headquarter):
            # headquarter
            HeadquarterItem(parentitem, company)

        else:
            # hmm?
            raise RuntimeError("unknown unit type:", type(company))

    def newBrigade(self, copied=None):
        """
        Callback triggered when the user chooses 'New brigade' from the popup menu. Will create a new
        brigade and add it to the global datastructures.
        """
        # do we have something we should copy? we must also check that the 'copied' unit is a real unit,
        # as we will get a numeric menuitem id when called from the popup menu
        if copied and type(copied) != int:
            # we should do a copy
            brigade = copy.deepcopy(copied)

            # TODO: set all id:s for all sub organizations

        else:
            # create a new brigade
            brigade = Brigade(UnitView.nextid, "Brigade %d" % UnitView.nextid, self.player)

        # increment the id
        UnitView.nextid += 1

        # create a new item for the listview
        item = BrigadeItem(self, brigade)

        # add to the global data
        scenario.info.brigades[self.player][brigade.getId()] = brigade

        # create a headquarter for the brigade too
        self.newHeadquarter(brigade, item)

    def copyBrigade(self, original):
        """
        CCopies a wbrigade. Will do a deep copy of the passed 'original', regiments, battalions,
        units and all, and attach the regiment to the currently selected item.
        """
        # do the raw copy
        brigade = copy.deepcopy(original)

        # set id for the copied battalion
        brigade.id = UnitView.nextid
        UnitView.nextid += 1

        # get the current item and make it expandable
        current = self.selectedItem()
        current.setExpandable(1)

        # create a new item for the listview
        item = BrigadeItem(self, brigade)

        # loop over all regiments we have
        for regiment in brigade.getRegiments():
            # set the id and add to the id counter
            regiment.id = UnitView.nextid
            UnitView.nextid += 1

            # create a new item for the listview
            regimentitem = RegimentItem(item, regiment)
            regimentitem.setExpandable(1)

            # create a new item for the
            HeadquarterItem(regimentitem, regiment.getHeadquarter())

            # loop over all companies that the battalion has
            for company in regiment.getCompanies():
                # set the id and add to the id counter
                company.id = UnitView.nextid
                UnitView.nextid += 1

                # add a new item
                self.createCompanyItem(company, item)

            # loop over all battalions
            for battalion in regiment.getBattalions():
                # set the id and add to the id counter
                battalion.id = UnitView.nextid
                UnitView.nextid += 1

                # create a new item for the listview
                battalionitem = BattalionItem(regimentitem, battalion)
                battalionitem.setExpandable(1)

                # create a new item for the
                HeadquarterItem(battalionitem, battalion.getHeadquarter())

                # loop over all companies that the battalion has
                for company in battalion.getCompanies():
                    # set the id and add to the id counter
                    company.id = UnitView.nextid
                    UnitView.nextid += 1

                    # add a new item
                    self.createCompanyItem(company, battalionitem)

        # add to the global data
        scenario.info.brigades[self.player][brigade.getId()] = brigade

        # create a new item for the
        HeadquarterItem(item, brigade.getHeadquarter())

    def newRegiment(self, copied=None):
        """
        Callback triggered when the user chooses 'New regiment' from the popup menu. Will create a new
        regiment and add it to the global datastructures.
        """
        # do we have something we should copy? we must also check that the 'copied' unit is a real unit,
        # as we will get a numeric menuitem id when called from the popup menu
        if copied and type(copied) != int:
            # we should do a copy
            regiment = copy.deepcopy(copied)

            # TODO: set all id:s for all sub organizations

        else:
            # create a new regiment
            regiment = Regiment(UnitView.nextid, "Regiment %d" % UnitView.nextid, self.player)

        # increment the id
        UnitView.nextid += 1

        # get the current item and make it expandable
        current = self.selectedItem()
        current.setExpandable(1)

        # create a new item for the listview
        item = RegimentItem(current, regiment)

        # add to the regiments for the brigade
        current.getBrigade().getRegiments().append(regiment)

        # create a headquarter for the regiment too
        self.newHeadquarter(regiment, item)

    def copyRegiment(self, original):
        """
        Copies a regiment. Will do a deep copy of the passed 'original', battalions, units and all,
        and attach the regiment to the currenttly selected item.
        """
        # do the raw copy
        regiment = copy.deepcopy(original)

        # set id for the copied battalion
        regiment.id = UnitView.nextid
        UnitView.nextid += 1

        # get the current item and make it expandable
        current = self.selectedItem()
        current.setExpandable(1)

        # create a new item for the listview
        item = RegimentItem(current, regiment)

        # loop over all companies that the battalion has
        for company in regiment.getCompanies():
            # set the id and add to the id counter
            company.id = UnitView.nextid
            UnitView.nextid += 1

            # add a new item
            self.createCompanyItem(company, item)

        # loop over all battalions
        for battalion in regiment.getBattalions():
            # set the id and add to the id counter
            battalion.id = UnitView.nextid
            UnitView.nextid += 1

            # create a new item for the listview
            battalionitem = BattalionItem(item, battalion)
            battalionitem.setExpandable(1)

            # create a new item for the
            HeadquarterItem(battalionitem, battalion.getHeadquarter())

            # loop over all companies that the battalion has
            for company in battalion.getCompanies():
                # set the id and add to the id counter
                company.id = UnitView.nextid
                UnitView.nextid += 1

                # add a new item
                self.createCompanyItem(company, battalionitem)

        # add to the regiments for the brigade
        current.getBrigade().getRegiments().append(regiment)

        # create a new item for the
        HeadquarterItem(item, regiment.getHeadquarter())

    def newBattalion(self, copied=None):
        """
        Callback triggered when the user chooses 'New battalion' from the popup menu. Will create a new
        battalion and add it to the global datastructures.
        """
        # create a new battalion
        battalion = Battalion(UnitView.nextid, "Battalion %d" % UnitView.nextid, self.player)

        # increment the id
        UnitView.nextid += 1

        # get the current item and make it expandable
        current = self.selectedItem()
        current.setExpandable(1)

        # create a new item for the listview
        item = BattalionItem(current, battalion)

        # add to the battalions for the regiment
        current.getRegiment().getBattalions().append(battalion)

        # create a headquarter for the battalion too
        self.newHeadquarter(battalion, item)

    def copyBattalion(self, original):
        """
        Copies a battalion. Will do a deep copy of the passed 'original', units and all, and attach
        the battalion to the currenttly selected item.
        """
        # do the raw copy
        battalion = copy.deepcopy(original)

        # set id for the copied battalion
        battalion.id = UnitView.nextid
        UnitView.nextid += 1

        # get the current item and make it expandable
        current = self.selectedItem()
        current.setExpandable(1)

        # create a new item for the listview
        item = BattalionItem(current, battalion)

        # loop over all companies that the battalion has
        for company in battalion.getCompanies():
            # set the id and add to the id counter
            company.id = UnitView.nextid
            UnitView.nextid += 1

            # add a new item
            self.createCompanyItem(company, item)

        # add to the battalions for the regiment
        current.getRegiment().getBattalions().append(battalion)

        # create a new item for the
        HeadquarterItem(item, battalion.getHeadquarter())

    def newHeadquarter(self, organization, item, copied=None):
        """
        Creates a new headquarter company to 'organization'. Adds a new node in the tree and a new
        unit too. Headquarters are never copied!
        """
        # create a new headquarter
        headquarter = Headquarter(UnitView.nextid, "%s HQ" % organization.getName(), self.player)

        # set default data
        headquarter.setWeapon(globals.weapons[globals.defaultweapons['headquarter']])

        # create a commander for the headquarter
        headquarter.setCommander(Leader("Commander name", globals.defaultrank,
                                        Aggressiveness(50), Experience(50),
                                        RallySkill(50), Motivation(50)))

        # add the unit to the global structures
        scenario.info.units[headquarter.getId()] = headquarter

        # increment the id
        UnitView.nextid += 1

        # create a new item for the listview
        newitem = HeadquarterItem(item, headquarter)

        # set this new hq as the hq for the passed organization
        headquarter.setHeadquarterFor(organization)
        organization.setHeadquarter(headquarter)

        # let the world know we have a new unit
        self.emit(PYSIGNAL('currentUnitChanged'), ())

    def newInfantry(self, copied=None):
        """
        Callback triggered when the user chooses 'New infantry company' from the popup menu. Will
        create a new infantry company and add it to the global datastructures.
        """
        # do we have something we should copy? we must also check that the 'copied' unit is a real unit,
        # as we will get a numeric menuitem id when called from the popup menu
        if copied and type(copied) != int:
            # we should do a copy
            infantry = copy.deepcopy(copied)

            # set new id
            infantry.id = UnitView.nextid

        else:
            # create a new infantry
            infantry = InfantryCompany(UnitView.nextid, "Infantry company %d" % UnitView.nextid, self.player)

            # set default data
            # infantry.setMode ()
            infantry.setWeapon(globals.weapons[globals.defaultweapons['infantry']])

            # create a commander for the unit
            infantry.setCommander(Leader("Commander name", globals.defaultrank,
                                         Aggressiveness(50), Experience(50),
                                         RallySkill(50), Motivation(50)))

        # add the unit to the global structures
        scenario.info.units[infantry.getId()] = infantry

        # increment the id
        UnitView.nextid += 1

        # get the current item and make it expandable
        current = self.selectedItem()
        current.setExpandable(1)

        # create a new item for the listview
        item = InfantryItem(current, infantry)

        # what do we have here?
        if isinstance(current, RegimentItem):
            # add to the companies for the regiment
            current.getRegiment().getCompanies().append(infantry)

        else:
            # add to the companies for the battalion
            current.getBattalion().getCompanies().append(infantry)

        # let the world know we have a new unit
        self.emit(PYSIGNAL('currentUnitChanged'), ())

    def newCavalry(self, copied=None):
        """
        Callback triggered when the user chooses 'New cavalry company' from the popup menu. Will
        create a new cavalry company and add it to the global datastructures.
        """
        # do we have something we should copy? we must also check that the 'copied' unit is a real unit,
        # as we will get a numeric menuitem id when called from the popup menu
        if copied and type(copied) != int:
            # we should do a copy
            cavalry = copy.deepcopy(copied)

            # set new id
            cavalry.id = UnitView.nextid

        else:
            # create a new cavalry
            cavalry = CavalryCompany(UnitView.nextid, "Cavalry company %d" % UnitView.nextid, self.player)

            # set default data
            # infantry.setMode ()
            cavalry.setWeapon(globals.weapons[globals.defaultweapons['cavalry']])

            # create a commander for the unit
            cavalry.setCommander(Leader("Commander name", globals.defaultrank,
                                        Aggressiveness(50), Experience(50),
                                        RallySkill(50), Motivation(50)))

        # add the unit to the global structures
        scenario.info.units[cavalry.getId()] = cavalry

        # increment the id
        UnitView.nextid += 1

        # get the current item and make it expandable
        current = self.selectedItem()
        current.setExpandable(1)

        # create a new item for the listview
        item = CavalryItem(current, cavalry)

        # what do we have here?
        if isinstance(current, RegimentItem):
            # add to the companies for the regiment
            current.getRegiment().getCompanies().append(cavalry)

        else:
            # add to the companies for the battalion
            current.getBattalion().getCompanies().append(cavalry)

        # let the world know we have a new unit
        self.emit(PYSIGNAL('currentUnitChanged'), ())

    def newArtillery(self, copied=None):
        """
        Callback triggered when the user chooses 'New artillery battery' from the popup menu. Will
        create a new artillery battery and add it to the global datastructures.
        """
        # do we have something we should copy? we must also check that the 'copied' unit is a real unit,
        # as we will get a numeric menuitem id when called from the popup menu
        if copied and type(copied) != int:
            # we should do a copy
            artillery = copy.deepcopy(copied)

            # set new id
            artillery.id = UnitView.nextid

        else:
            # create a new artillery
            artillery = ArtilleryBattery(UnitView.nextid, "Artillery battery %d" % UnitView.nextid, self.player)

            # set default data
            # infantry.setMode ()
            artillery.setWeapon(globals.weapons[globals.defaultweapons['artillery']])

            # create a commander for the unit
            artillery.setCommander(Leader("Commander name", globals.defaultrank,
                                          Aggressiveness(50), Experience(50),
                                          RallySkill(50), Motivation(50)))

        # add the unit to the global structures
        scenario.info.units[artillery.getId()] = artillery

        # increment the id
        UnitView.nextid += 1

        # get the current item and make it expandable
        current = self.selectedItem()
        current.setExpandable(1)

        # create a new item for the listview
        item = ArtilleryItem(current, artillery)

        # what do we have here?
        if isinstance(current, RegimentItem):
            # add to the companies for the regiment
            current.getRegiment().getCompanies().append(artillery)

        else:
            # add to the companies for the battalion
            current.getBattalion().getCompanies().append(artillery)

        # let the world know we have a new unit
        self.emit(PYSIGNAL('currentUnitChanged'), ())

    def delete(self):
        """
        Callback triggered when the user chooses 'Delete unit' from the popup menu. Will delete the
        currently selected unit.
        """
        # not yet done...
        QtWidgets.QMessageBox.warning(self, "TODO: delete organization", "This feature is not yet implemented!",
                                      "&Uh, ok")

    def copy(self):
        """
        Callback triggered when the user chooses 'Copy' from the popup menu. Will copy the currently
        selected unit/organization for later pasting.
        """
        # get the current item and the company
        current = self.selectedItem()

        # do we have a unit item here?
        if isinstance(current, UnitItem):
            # a company, so store it as the currently copied item
            self.copied = current.getCompany()

            # well, but is it a headquarter then? we can't really copy them
            if isinstance(self.copied, Headquarter):
                # nah, we can't do this after all, clear the copied
                self.copied = None

        else:
            # a higher organization, store it as the currently copied item
            self.copied = current.getOrganization()

    def paste(self):
        """
        Callback triggered when the user chooses 'Paste' from the popup menu. Will paste the
        currently selected unit as a new unit into the currently selected item.
        """
        # precautions
        if not self.copied:
            # oops?
            print("Unitview.paste: nothing to paste, and paste() called?")
            return

        # ok, is it a unit?
        if isinstance(self.copied, ArtilleryBattery):
            # create a copy
            self.newArtillery(self.copied)

        elif isinstance(self.copied, InfantryCompany):
            # create a copy
            self.newInfantry(self.copied)

        elif isinstance(self.copied, CavalryCompany):
            # create a copy
            self.newCavalry(self.copied)

        elif isinstance(self.copied, Battalion):
            # create a copy
            self.copyBattalion(self.copied)

        elif isinstance(self.copied, Regiment):
            # create a copy
            self.copyRegiment(self.copied)

        elif isinstance(self.copied, Brigade):
            # create a copy
            self.copyBrigade(self.copied)

        else:
            print("Unitview.paste: only primitive units can be copied atm")

    def edit(self):
        """
        Callback triggered when the user chooses 'Edit' from the popup menu. This method will bring
        up a dialog  where the properties of the selected organization can be edited.
        """
        # get the current item and the company
        current = self.selectedItem()

        # do we have an organization or a company level unit?
        try:
            # assume it's a company. if this fails it's a higher organization, but we deal with that in
            # the "except" clause
            company = current.getCompany()

            # create and show the dialog
            EditUnit(self, company).exec_loop()

        except:
            # a higher organization, edit it
            EditOrganization(self, current.getOrganization()).exec_loop()

        # update the visualized data
        current.update()

    def itemChanged(self):
        """
        Callback used when the current selected item has changed. Sets up the popup menu so that the
        proper items in it are available, and also stores the current company (if any) in the global
        data.
        """

        # what do we have under the mouse cursor?
        item = self.selectedItem()

        # initially clear the global current unit
        globals.currentunit = None

        # did we get any item?
        if item is None:
            # no item, so the listview is empty, disable all items that should not be active
            self.popup.setItemEnabled(10, 1)
            self.popup.setItemEnabled(11, 0)
            self.popup.setItemEnabled(12, 0)
            self.popup.setItemEnabled(13, 0)
            self.popup.setItemEnabled(14, 0)
            self.popup.setItemEnabled(15, 0)
            self.popup.setItemEnabled(16, 0)
            self.popup.setItemEnabled(17, 0)
            self.popup.setItemEnabled(18, 0)
            self.popup.setItemEnabled(19, 0)

        elif isinstance(item, BrigadeItem):
            # a brigade
            self.popup.setItemEnabled(10, 1)
            self.popup.setItemEnabled(11, 1)
            self.popup.setItemEnabled(12, 0)
            self.popup.setItemEnabled(13, 0)
            self.popup.setItemEnabled(14, 0)
            self.popup.setItemEnabled(15, 0)
            self.popup.setItemEnabled(16, 1)
            self.popup.setItemEnabled(17, 1)
            self.popup.setItemEnabled(18, 1)
            self.popup.setItemEnabled(19, 1)
            self.popup.setItemEnabled(18, 1)

            # can we paste the currently selected thing into this one?
            if isinstance(self.copied, Regiment) or isinstance(self.copied, Brigade):
                # a regiment, all is ok
                self.popup.setItemEnabled(19, 1)
                # print "can paste regiment into brigade"
            else:
                # no, pasting not allowed
                self.popup.setItemEnabled(19, 0)

        elif isinstance(item, RegimentItem):
            # a regiment
            self.popup.setItemEnabled(10, 0)
            self.popup.setItemEnabled(11, 0)
            self.popup.setItemEnabled(12, 1)
            self.popup.setItemEnabled(13, 1)
            self.popup.setItemEnabled(14, 1)
            self.popup.setItemEnabled(15, 1)
            self.popup.setItemEnabled(16, 1)
            self.popup.setItemEnabled(17, 1)
            self.popup.setItemEnabled(18, 1)

            # can we paste the currently selected thing into this one?
            if isinstance(self.copied, Battalion) or isinstance(self.copied, Unit):
                # either a battalion or a company, all ok
                self.popup.setItemEnabled(19, 1)
                # print "can paste battalion/unit into regiment"
            else:
                # no, pasting not allowed
                self.popup.setItemEnabled(19, 0)

        elif isinstance(item, BattalionItem):
            # a battalion
            self.popup.setItemEnabled(10, 0)
            self.popup.setItemEnabled(11, 0)
            self.popup.setItemEnabled(12, 0)
            self.popup.setItemEnabled(13, 1)
            self.popup.setItemEnabled(14, 1)
            self.popup.setItemEnabled(15, 1)
            self.popup.setItemEnabled(16, 1)
            self.popup.setItemEnabled(17, 1)
            self.popup.setItemEnabled(18, 1)

            # can we paste the currently selected thing into this one?
            if isinstance(self.copied, Unit):
                # a company, all ok
                self.popup.setItemEnabled(19, 1)
                # print "can paste unit into battalion"
            else:
                # no, pasting not allowed
                self.popup.setItemEnabled(19, 0)

        else:
            # a company, cavalry or battery
            self.popup.setItemEnabled(10, 0)
            self.popup.setItemEnabled(11, 0)
            self.popup.setItemEnabled(12, 0)
            self.popup.setItemEnabled(13, 0)
            self.popup.setItemEnabled(14, 0)
            self.popup.setItemEnabled(15, 0)
            self.popup.setItemEnabled(16, 1)
            self.popup.setItemEnabled(17, 1)

            # can we copy this one? we don't allow headquarters to be copied
            if isinstance(item, HeadquarterItem):
                # a hq, don't copy this one
                self.popup.setItemEnabled(18, 0)
            else:
                # no hq, copy is ok
                self.popup.setItemEnabled(18, 1)

                # we can't paste anything onto a company, ever
            self.popup.setItemEnabled(19, 0)

            # we have a new company that needs to be set into the global data
            globals.currentunit = item.getCompany()

            # let the world know we have a new unit
            self.emit(PYSIGNAL('currentUnitChanged'), ())

    def contentsMousePressEvent(self, event):
        """
        Callback handling the fact that the user has pressed some mouse button. shows the menu on the
        right button.
        """

        # is this the right button?
        if event.button() != QtCore.Qt.RightButton:
            # nope, perform normal stuff
            QtWidgets.QListView.contentsMousePressEvent(self, event)
            return

        # make sure the menu is up-to-date
        self.itemChanged()

        # show the popup
        self.popup.move(event.globalPos())
        self.popup.show()

    def contentsMouseReleaseEvent(self, event):
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
            QtWidgets.QListView.contentsMouseReleaseEvent(self, event)

    def mapClickedLeft(self, x, y, hexx, hexy):
        """
        Callback triggered when the map has been clicked. It gets the currently selected unit
        (if any) and changes its position to that of the clicked hex. Only companies (hqs, infantry,
        cavalry and artillery can be placed on the map. Brigades etc. are ignored.
        """

        # get the current item and make it expandable
        tmp = self.selectedItem()

        # what do we have here?
        if isinstance(tmp, BrigadeItem) or isinstance(tmp, RegimentItem) or isinstance(tmp, BattalionItem):
            # nothing we can place out
            return

        # get the company in the item
        company = tmp.getCompany()

        oldpos = company.getPosition()

        # assign the new position, the coordinates are offset with -24 to set the unit right over the
        # click position
        company.setPosition((x, y))

        globals.mapview.repaint()

    def mapClickedMid(self, x, y, hexx, hexy):
        """
        Callback triggered when the map has been clicked. It gets the currently selected unit
        (if any) and changes its facing to face towards the position on the map that was clicked. Only
        companies (hqs, infantry, cavalry and artillery can have their facing changed. Brigades etc. are
        ignored.
        """

        # get the current item and make it expandable
        tmp = self.selectedItem()

        # what do we have here?
        if isinstance(tmp, BrigadeItem) or isinstance(tmp, RegimentItem) or isinstance(tmp, BattalionItem):
            # nothing we can place out
            return

        # get the company in the item
        company = tmp.getCompany()

        # get the position of the company
        xpos, ypos = company.getPosition()

        # calculate the facing
        facing = calculateAngle(xpos, ypos, x, y)

        # assign the new position
        company.setFacing(facing)

        # gfx updates
        # globals.mapview.paintEvent(QPaintEvent(QRect(xpos-30, ypos-30, 60, 60)))
        globals.mapview.repaint()

    def validate(self):
        """
        Validates the part of the scenario that this view is responsible for creating. Returns a
        free text report that indicates the validation result or None if all is ok.
        """

        # nothing to do
        return None
