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

from pygame.locals import *

from civil.state import assault_unit
from civil.state import change_combat_policy
from civil.ui import messages
from civil.state import move_unit
from civil.state import move_unit_fast
from civil.state import retreat
from civil.state import rotate_unit
from civil.state import skirmish_unit
from civil.state import state
from civil.state import weapon_info
from civil.model import scenario
from civil.plan.change_mode import ChangeMode
from civil.plan.wait import Wait
from civil.model.unit import Headquarter


class OwnUnit(state.State):
    """
    This class is a state that provides basic handling of own units. This state should be activated
    when the player clicks on an own unit or some other way makes an own unit active. From this
    state the player can perform various other actions with a unit.

    This state paints all available information about the current unit in the panel.

    This state will activate the following other states:

    * idle if the player clicks in the terrain somewhere.
    * enemy_unit if an enemy unit is clicked.

    * own_unit is kept if another own unit is clicked on.
    """

    def __init__(self):
        """
        Initializes the instance. Sets default values for all needed members.
        """

        # call superclass constructor
        state.State.__init__(self)

        # set default cursor
        self.setDefaultCursor()

        # set defaults
        self.name = "own_unit"

        # now setup the unit we have so that the proper keymap and helptexts are shown
        self.setupKeymapAndHelp()

    def setupKeymapAndHelp(self):
        """
        Sets up the internal keymap and the help text depending on the mode the selected unit is
        in. All types of orders can not be given at all times. This method will check the current
        mode of the unit and the possible modes that can be entered from it and builds up the keymap
        and helptexts from that info.

        This method also creates the menu keymap that is sent to the popup menu.
        """

        # TODO: we can have many units selected at the same time, so the available commands should
        # be those that all units can perform, otherwise we can end up with illegal orders for some
        # units 

        # TODO: this should be changed to be onDone() of the last plan of the unit

        # get the mode of the current unit
        unit = self.getSelectedUnit()
        mode = unit.getMode()

        # add the default part of the keymap, i.e the commands that can always be given, no matter
        # what mode the unit is in
        self.keymap[(K_i, KMOD_NONE)] = self.showWeaponInfo
        self.keymap[(K_h, KMOD_NONE)] = self.activateHeadquarter
        self.keymap[(K_a, KMOD_SHIFT)] = self.activateAll
        self.keymap[(K_TAB, KMOD_NONE)] = self.center
        self.keymap[(K_BACKSPACE, KMOD_NONE)] = self.cancel
        self.keymap[(K_1, KMOD_ALT)] = self.toggleAIDebug
        # self.keymap [ ( K_l,         KMOD_NONE  ) ] = self.toggleLOS

        # setup an initial menu keymap
        self.menukeymap = [("cancel last order", K_BACKSPACE, KMOD_NONE),
                           ("find unit HQ", K_h, KMOD_NONE),
                           ("activate all", K_a, KMOD_SHIFT),
                           ("center around unit", K_TAB, KMOD_NONE),
                           ("weapon info", K_i, KMOD_NONE)]

        # ( "toggle line of sight", K_l,         KMOD_NONE  ),

        # define the default part of the help help text too
        self.helptext.append(" ")

        # can the unit move?
        if mode.canMove() and unit.getFatigue().checkMove():
            # yep, moving is possible
            self.keymap[(K_m, KMOD_NONE)] = self.move
            self.menukeymap.append(("move unit", K_m, KMOD_NONE))
            self.helptext.append("m - move unit")

        # can the unit move fast?
        if mode.canMoveFast() and unit.getFatigue().checkMoveFast():
            # yep, moving fast is possible
            self.keymap[(K_f, KMOD_NONE)] = self.moveFast
            self.menukeymap.append(("move unit fast march", K_f, KMOD_NONE))
            self.helptext.append("f - move unit fast march")

        # can the unit change facing?
        if mode.canRotate() and unit.getFatigue().checkRotate():
            # yep, changing facing is possible
            self.keymap[(K_o, KMOD_NONE)] = self.rotate
            self.menukeymap.append(("change facing", K_o, KMOD_NONE))
            self.helptext.append("o - change facing")

        # can the unit retreat?
        if mode.canRetreat() and unit.getFatigue().checkRetreat():
            # yep, retreating is possible
            self.keymap[(K_r, KMOD_NONE)] = self.retreat
            self.menukeymap.append(("retreat", K_r, KMOD_NONE))
            self.helptext.append("r - retreat")

        # can the unit skirmish?
        if mode.canSkirmish() and unit.getFatigue().checkSkirmish():
            # yep, skirmishing is possible
            self.keymap[(K_s, KMOD_NONE)] = self.skirmish
            self.menukeymap.append(("skirmish", K_s, KMOD_NONE))
            self.helptext.append("s - skirmish")

        # can the unit assault?
        if mode.canAssault() and unit.getFatigue().checkAssault():
            # yep, assaulting is possible
            self.keymap[(K_x, KMOD_NONE)] = self.assault
            self.menukeymap.append(("assault", K_x, KMOD_NONE))
            self.helptext.append("x - assault")

        # can the unit change mode?
        if mode.canChangeMode() and unit.getFatigue().checkChangeMode():
            # yep, changing mode is possible
            self.keymap[(K_c, KMOD_NONE)] = self.changeMode
            self.menukeymap.append(("change unit mode", K_c, KMOD_NONE))
            self.helptext.append("c - change unit mode")

        # can the unit change combat policy?
        if mode.canChangePolicy():
            # yep, changing mode is possible
            self.keymap[(K_w, KMOD_NONE)] = self.wait
            self.menukeymap.append(("wait", K_w, KMOD_NONE))
            self.helptext.append("w - wait 1 minute")

        # can the unit wait?
        if mode.canWait():
            # yep, waiting is possible
            self.keymap[(K_p, KMOD_NONE)] = self.changeCombatPolicy
            self.menukeymap.append(("change combat policy", K_p, KMOD_NONE))
            self.helptext.append("p - change combat policy")

        # now add the rest of the help texts that should be last
        self.helptext.append("h - get unit hq")
        self.helptext.append("A - activate all units")
        self.helptext.append("i - show weapon info")
        self.helptext.append("l - check unit line of sight")
        self.helptext.append("tab - center map")
        self.helptext.append("del - cancel last order")

    def cancel(self):
        """
        Callback triggered when the player presses the 'cancel' key. This attempts to cancel the
        last issued plan to the currently selected units. The last plan is removed and the unit
        modes are updated to whatever becomes current.
        """

        # loop over all selected unit
        for unit in self.getSelectedUnits():
            # get all the plans for the unit
            plans = unit.getPlans()

            # any plans at all for the unit?
            if not plans:
                # no plans, so we can't really cancel anything either
                continue

            # get the current plan, i.e. the last one
            currentplan = plans[len(plans) - 1]

            # and the old mode, i.e the mode that the unit had before that plan got applied
            # oldmode = currentplan.getOldMode ()

            # TODO: send request to the server to have the plan removed

            print("*** OwnUnit.cancel: send plan to server!")

            # send off the plan to the server
            # scenario.connection.send ( Cancel ().toString () )

            # just pop off the most recently added plan. We simply slice off the last plan
            # unit.setPlans ( unit.getPlans () [:-1] )

            # set it as the new current mode
            # unit.setMode ( oldmode )

        # now the keymap and help stuff needs to be reset
        self.setupKeymapAndHelp()

        # we have changed some units
        scenario.dispatcher.emit('units_changed', self.getSelectedUnits())

    def move(self):
        """
        Callback triggered when the user presses the key 'm' for moving the unit. This callback
        sets the internal state to be 'MoveUnit'.
        """

        # just activate a new state
        return move_unit.MoveUnit()

    def moveFast(self):
        """
        Callback triggered when the user presses the key 'f' for moving the unit fast. This callback
        sets the internal state to be 'MoveUnitFast'.
        """

        # just activate a new state
        return move_unit_fast.MoveUnitFast()

    def retreat(self):
        """
        Callback triggered when the user presses the key 'r' for retreating the unit. This callback
        sets the internal state to be 'Retreat'.
        """

        # just activate a new state
        return retreat.Retreat()

    def rotate(self):
        """
        Callback triggered when the user presses the key 'o' for rotating the. This callback
        sets the internal state to be 'RotateUnit'.
        """

        # just activate a new state
        return rotate_unit.RotateUnit()

    def changeMode(self):
        """
        Callback triggered when the user presses the key 'c' for changing the unit mode. This callback


 """

        # loop over all selected unit
        for unit in self.getSelectedUnits():
            # can the unit change its mode?
            if not unit.getMode().canChangeMode() or not unit.getFatigue().checkChangeMode():
                # nope, the unit mode or fatigue prohibits it, next unit
                scenario.messages.add('%s can not change mode' % unit.getName(), messages.ERROR)
                continue

            # create a new mode for the unit
            # mode = createMode ( createMode ( unit.getMode ().onChangeMode () ).onDone () )

            # assign it too
            # unit.setMode ( mode )

            # create a new 'change mode' plan
            plan = ChangeMode(unit_id=unit.getId())

            # send off the plan to the server
            scenario.connection.send(plan.toString())

            # add the plan last among the unit's plans
            unit.getPlans().append(plan)

        # now the keymap and help stuff needs to be reset
        self.setupKeymapAndHelp()

        # we have changed some units
        scenario.dispatcher.emit('units_changed', self.getSelectedUnits())

        # no new state
        return None

    def changeCombatPolicy(self):
        """
        Callback triggered when the user presses the key 'p' for changing the unit combat policy
        mode. This callback will activate the internal state 'ChangeCombatPolicy' if the unit can
        change the policy from its current state, and let it take care of the bussiness.
        """

        # just activate a new state
        return change_combat_policy.ChangeCombatPolicy()

    def wait(self):
        """
        Callback triggered when the user presses the key 'w' for having the unit wait for a
        certain time. A new plan 'wait' is added to all selected units.
        """
        # loop over all selected units
        for unit in self.getSelectedUnits():
            # create a new 'wait' plan for waiting 60 seconds. TODO: is this too little?
            # plan = Wait(delay=60, unit_id=unit.getId())
            # TODO TypeError: __init__() got an unexpected keyword argument 'delay'
            plan = Wait(unit_id=unit.getId())

            # add it to the plans for the unit
            unit.getPlans().append(plan)

            # create a new mode for the unit
            # mode = createMode ( createMode ( unit.getMode ().onWait () ).onDone () )

            # assign it too
            # unit.setMode ( mode )

        # now the keymap and help stuff needs to be reset
        self.setupKeymapAndHelp()

        # we have changed some units
        scenario.dispatcher.emit('units_changed', self.getSelectedUnits())

        # no new state
        return None

    def skirmish(self):
        """
        Callback triggered when the user presses the key 's' for setting a skirmish target for the
        unit. This callback sets the internal state to be 'SkirmishUnit'.
        """

        return skirmish_unit.SkirmishUnit()

    def assault(self):
        """
        Callback triggered when the user presses the key 'XXX' for setting an assault target for the
        unit. This callback sets the internal state to be 'AssaultUnit'.
        """

        return assault_unit.AssaultUnit()

    def showWeaponInfo(self):
        """
        Callback triggered when the user presses the 'i' key. This method will bring up a small
        dialog that shows information about the weapon used by the current unit.
        """

        # create and return a new state showing our labels
        return weapon_info.WeaponInfo(self.getSelectedUnit().getWeapon(), self)

    def center(self):
        """
        Callback triggered when the player presses the key 'TAB' for centering the screen around
        a unit. The playfield will be scrolled so that it is as centered around the unit as
        possible. If the unit is on the edge of the playfield then it is scrolled as far as
        possible. The same unit is kept selected. If multiple units are selected then the scrolling
        is done wrt the main selected unit.
        """
        # get the selected unit
        selected = self.getSelectedUnit()

        # get the hex the unit is in 
        xhex, yhex = scenario.map.pointToHex2(selected.getPosition())

        # and the visible size of the map as well as the offsets
        xoff, yoff = scenario.playfield.getOffset()
        xvis, yvis = scenario.playfield.getVisibleSize()

        # we want to center the map by making the offsets for the map be:
        # unit position - half visible size
        xdelta = xvis / 2
        ydelta = yvis / 2

        # and now calculate the new offsets we want to scroll to
        xscrollto = xhex - xdelta
        yscrollto = yhex - ydelta

        # make sure they are not negative, we can't scroll further away than (0,0)
        if xscrollto < 0:
            xscrollto = 0

        if yscrollto < 0:
            yscrollto = 0

        # perform the scrolling and see weather we actually did anything
        if scenario.playfield.setOffset(xscrollto, yscrollto):
            # repaint the playfield now that it has changed
            scenario.playfield.needRepaint()

        # no new state
        return None

    def activateHeadquarter(self):
        """
        Finds the headquarter for the unit and makes it the current unit. If the unit has no
        headquarter this method will do nothing. It will first find the parent organization and then
        get the headquarter for that.
        """

        # get the selected unit
        selected = self.getSelectedUnit()

        # get the parent organization for the current unit
        parent = selected.getParentOrganization()

        # do we have a parent?
        if parent is None:
            # no parent, show message
            scenario.messages.add('unit has no headquarter', messages.ERROR)

            return None

        # parent organization was ok, get its hq
        hq = parent.getHeadquarter()

        # is the hq still alive? we can't activate it if it's destroyed
        if hq.isDestroyed():
            # it's destroyed, what should we do now?
            scenario.messages.add('headquarter is destroyed', messages.ERROR)
            return None

        # make it the new current selected unit
        self.setSelectedUnit(unit=hq)

        # setup the unit we have so that the proper keymap and helptexts are shown 
        self.setupKeymapAndHelp()

        # and have the map center around the new unit
        self.center()

        # we have a new selected unit
        scenario.dispatcher.emit('unit_selected', self.getSelectedUnit())

    def activateAll(self):
        """
        Activates all units that belong to the same organization as the selected unit. This is
        useful mainly for battalions and regiments. Makes the headquarter the current selected
        unit.
        """

        # get the selected unit
        selected = self.getSelectedUnit()

        # is that a headquarter?
        if isinstance(selected, Headquarter):
            # a headquarter, make it the current unit
            self.setSelectedUnit(unit=selected)

            # get the organization the hq is hq for
            org = selected.getHeadquarterFor()
        else:
            # a non-hq unit, get its parent organization
            org = selected.getParentOrganization()

            # make the hq selected
            self.setSelectedUnit(unit=org.getHeadquarter())

        # now get the companies for the organization and add them too as selected units
        for tmp in org.getCompanies():
            # do not clear the old ones
            self.setSelectedUnit(unit=tmp, clearfirst=0)

        # setup the unit we have so that the proper keymap and helptexts are shown 
        self.setupKeymapAndHelp()

        # and have the map center around the new unit
        self.center()

        # we have a new selected unit
        scenario.dispatcher.emit('unit_selected', self.getSelectedUnit())
