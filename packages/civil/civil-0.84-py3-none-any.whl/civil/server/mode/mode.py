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


class Mode:
    """
    This class works as a base class for all modes of the game. A mode is an internal state each
    unit is in. A unit always has a mode, and most orders that are given to a unit require some
    certain mode to be active.

    Each mode has a name and a list of other modes (by name) that can be entered from that
    mode. This builds up a simple state machine the contains the legal actions for a unit. The
    actual mode machine functionality is provided by several 'canX()' methods which indicate weather
    the unit can perform the 'X' action. Use these to check what the unit can do.

    If the unit can enter a mode (i.e. 'canX()' returns 1), then the method 'onX()' will return the
    name of the mode the unit would enter if it changed to doing 'X'. Each subclass should provide
    the names of the modes for those 'on'-values which are possible.

    There are also some methods 'isX()', which return 1 if the mode is a mode that is currently
    doing X, such as isMeleeing() returns 1 if the unit is meleeing.

    There is a field 'self.base_fatigue' that indicates a base fatigue added to units for each step
    they stay in the mode.
    
    This class should be subclassed, and subclasses should set the fields indicating what can be
    done with the mode.
    """

    def __init__(self, name, title):
        """
        Initializes the mode.
        """

        # set the name and title
        self.name = name
        self.title = title

        self.onchangemode = ""
        self.onmove = ""
        self.ondone = ""
        self.onmovefast = ""
        self.onrotate = ""
        self.onhalt = ""
        self.onretreat = ""
        self.onskirmish = ""
        self.onmelee = ""
        self.onassault = ""
        self.onchangepolicy = ""
        self.onwait = ""
        self.onrally = ""
        self.ondisorganize = ""
        self.onrout = "FIXME: all modes need this!"

        # flags indicating what the mode is. by default none of the flags are set. subclasses should
        # set those that are appropriate
        self.ismeleeing = 0

        # set a default and invalid base fatigue. this must be set by subclasses
        self.base_fatigue = None

    def getName(self):
        """
        Returns the name of the mode.
        """
        return self.name

    def getTitle(self):
        """
        Returns the title of the mode. This title is suitable for displaying to the players in
        the panel etc. The name as returned by getName() is more for internal use.
        """
        return self.title

    def canMove(self):
        """
        Returns 1 weather the unit can move. Returns 0 if the action is not allowed.
        """
        if self.onmove == "":
            # can't do it
            return 0

        return 1

    def canMoveFast(self):
        """
        Returns 1 weather the unit can move at double pace. Returns 0 if the action is not allowed.
        """
        if self.onmovefast == "":
            # can't do it
            return 0

        return 1

    def canRotate(self):
        """
        Returns 1 weather the unit can turn. Returns 0 if the action is not allowed.
        """
        if self.onrotate == "":
            # can't do it
            return 0

        return 1

    def canHalt(self):
        """
        Returns 1 weather the unit can halt and stop all actions. Returns 0 if the action is not
        allowed.
        """
        if self.onhalt == "":
            # can't do it
            return 0

        return 1

    def canRetreat(self):
        """
        Returns 1 weather the unit can retreat. Returns 0 if the action is not allowed.
        """
        if self.onretreat == "":
            # can't do it
            return 0

        return 1

    def canSkirmish(self):
        """
        Returns 1 weather the unit can skirmish. Returns 0 if the action is not allowed.
        """
        if self.onskirmish == "":
            # can't do it
            return 0

        return 1

    def canMelee(self):
        """
        Returns 1 weather the unit can set a target and engage in combat. Returns 0 if the action
        is not allowed. This method is merely here for symmetry with the other 'canX()' methods, it
        should never really need to be used. When a unit is close enough to an enemy it will switch
        to melee automatically.
        """
        if self.onmelee == "":
            # can't do it
            return 0

        return 1

    def canAssault(self):
        """
        Returns 1 weather the unit can set a target and assault it. Returns 0 if the action
        is not allowed.
        """
        if self.onassault == "":
            # can't do it
            return 0

        return 1

    def canChangeMode(self):
        """
        Returns 1 weather the unit can change mode. Changing mode means changing from a transport
        mode to a battle mode. Returns 0 if the action is not allowed.
        """
        if self.onchangemode == "":
            # can't do it
            return 0

        return 1

    def canChangePolicy(self):
        """
        Returns 1 weather the unit can change the combat policy. Changing combat policy means
        changing the way a unit reacts to possible targets. Returns 0 if the action is not allowed.
        """
        if self.onchangepolicy == "":
            # can't do it
            return 0

        return 1

    def canWait(self):
        """
        Returns 1 weather the unit can wait. Returns 0 if the action is not allowed.
        """
        if self.onwait == "":
            # can't do it
            return 0

        return 1

    def canRally(self):
        """
        Returns 1 weather the unit can rally. Returns 0 if the action is not allowed. Most modes
        can't rally, only those where the unit is dirorganized.
        """
        if self.onrally == "":
            # can't do it
            return 0

        return 1

    def canDisorganize(self):
        """
        Returns 1 weather the unit can become disorganized. Returns 0 if the action is not
        allowed. Most modes can't disorganize, only those where the unit is routed.
        """
        if self.ondisorganize == "":
            # can't do it
            return 0

        return 1

    def onDone(self):
        """
        Returns the mode this mode would change to when this mode is done
        """
        return self.ondone

    def onMove(self):
        """
        Returns the mode this mode would change to when moving.
        """
        return self.onmove

    def onMoveFast(self):
        """
        Returns the mode this mode would change to when moving fast.
        """
        return self.onmovefast

    def onRotate(self):
        """
        Returns the mode this mode would change to when rotating.
        """
        return self.onrotate

    def onHalt(self):
        """
        Returns the mode this mode would change to when halting.
        """
        return self.onhalt

    def onRetreat(self):
        """
        Returns the mode this mode would change to when retreating.
        """
        return self.onretreat

    def onSkirmish(self):
        """
        Returns the mode this mode would change to when skirmishing.
        """
        return self.onskirmish

    def onMelee(self):
        """
        Returns the mode this mode would change to when meleeing with a unit.
        """
        return self.onmelee

    def onAssault(self):
        """
        Returns the mode this mode would change to when assaulting a unit.
        """
        return self.onassault

    def onChangeMode(self):
        """
        Returns the mode this mode would change to when changing mode. Hmm, this sounds
        silly. The unit can do a simple plan 'change mode' which basically switches between a combat
        and a movement mode.
        """
        return self.onchangemode

    def onWait(self):
        """
        Returns the mode this mode would change to when waiting.
        """
        return self.onwait

    def onRally(self):
        """
        Returns the mode this mode would change to when rallying.
        """
        return self.onrally

    def onDisorganize(self):
        """
        Returns the mode this mode would change to when disorganizing.
        """
        return self.ondisorganize

    def onRout(self):
        """
        Returns the mode this mode would change to when routing.
        """
        return self.onrout

    def isMeleeing(self):
        """
        Returns 1 if this mode is meleeing, and 0 if it is not.
        """
        return self.ismeleeing

    def getBaseFatigue(self):
        """
        This method returns the base fatigue for the mode. This value should reflect how much
        fatigue the unit gains each turn it spends in this mode. Some modes may not give any fatigue
        at all, some may even rest the unit. The value should be a fairly low floating point value
        that can be used as a basis for further calculations. The value should reflect how fatiguing
        it is to stay in the mode for a step, bearing in mind that 100 is the max possible fatigue
        and means the unit does absolutely nothing.

        Subclases should set the member value.
        """

        # precautions
        if self.base_fatigue is None:
            # oops, not set
            raise RuntimeError("mode '%s' has not set self.base_fatigue" % self.getName())

            # return the value
        return self.base_fatigue
