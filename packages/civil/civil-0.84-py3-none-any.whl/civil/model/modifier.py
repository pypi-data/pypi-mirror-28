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

# constants that define the current value of a modifier, weather it is in "good shape" or "bad shape"
GOOD = 0
NORMAL = 1
BAD = 2


class Modifier:
    """
    This class is a base class for all possible modifiers in the game. A modifier is a class that
    directly modifies a passed value according to some formula. This formula is defined by
    subclasses.

    Units and leaders use several modifiers to determine the outcomes of battles.
    """

    def __init__(self, value, min=0, max=99):
        """
        Creates the instance of the class and sets the passed value
        """

        # set default limits
        self.min = min
        self.max = max

        # and set it
        self.setValue(value)

    def getValue(self):
        """
        Returns the current value of this modifier.
        """
        return self.value

    def setValue(self, value):
        """
        Sets a new current value of this modifier. If the value is less than min or larger thanmax
        it is set to the limit value.
        """
        # too large or too small?
        if value > self.max:
            self.value = self.max

        elif value < self.min:
            self.value = self.min

        else:
            # normal value in between
            self.value = value

    def addValue(self, value):
        """
        Adds 'value' to the modifier value. The value may be negative to subtract. The value is
        clamped to [min..max].
        """
        # add it
        self.value += value

        # too large or too small?
        if self.value > self.max:
            self.value = self.max

        elif self.value < self.min:
            self.value = self.min

    def evaluateAttack(self, data):
        """
        Evaluates the passed 'data' value from a attacker point of view. This method is merely
        here as a placeholder to remind that the subclasses must overload this method.
        """
        # raise exception
        raise NotImplementedError("Modifier.evaluateAttack: this method must be overridden")

    def evaluateDefense(self, data):
        """
        Evaluates the passed 'data' value from a defender point of view. This method is merely
        here as a placeholder to remind that the subclasses must overload this method.
        """
        # raise exception
        raise NotImplementedError("Modifier.evaluateDefense: this method must be overridden")

    def evaluateMelee(self, data):
        """
        Evaluates the passed 'data' value from a melee point of view. This method is merely
        here as a placeholder to remind that the subclasses must overload this method.
        """
        # raise exception
        raise NotImplementedError("Modifier.evaluateMelee: this method must be overridden")


class Morale(Modifier):
    """
    

    """
    # the possible string values for this modifier
    strings = ['panic', 'terrified', 'broken', 'shaken', 'worried',
               'ok', 'good', 'very good', 'superb', 'excellent']

    def evaluate(self, data):
        """
        Evaluates the modifier against the passed value. The new modified value is returned to
        the caller.
        """
        return data

    def toString(self):
        """
        Returns a string representation of the numerical value of this modifier. There are ten
        different strings that can be returned, and they are suitable for showing to the player. The
        strings are all lowercase.
        """
        # nope, use div to get a value 0-9
        return Morale.strings[self.value // 10]

    def checkSkirmish(self):
        """
        This checks weather the unit's morale is good enough for the unit to skirmish. Returns 1
        if all is ok and 0 if not.

        The limit for a failure is 30.
        """
        # do we fail?
        if self.value < 30:
            # yep, failed
            return 0

        # all ok, morale holds
        return 1

    def checkAssault(self):
        """
        This checks weather the unit's morale is good enough for an assault. This assault is the
        part where the unit double times towards the enemy, not the final storming. Returns 1 if all
        is ok and 0 if not.

        The limit for a failure is 40.
        """
        # do we fail?
        if self.value < 40:
            # yep, failed
            return 0

        # all ok, morale holds
        return 1

    def checkFinalAssault(self):
        """
        This checks weather the unit's morale is good enough for the final storming part of an
        assault. This is when the unit runs the final distance to the enemy unit. The morale has to
        be fairly high for this thing to work out. Returns 1 if all is ok and 0 if not.

        The limit for a failure is 50.
        """
        # do we fail?
        if self.value < 50:
            # yep, failed
            return 0

        # all ok, morale holds
        return 1

    def getStatus(self):
        """
        Returns one of the GOOD, NORMAL or BAD constants depending on the value of the
        modifier. The constant reflects the general value of it.

        0-30  = BAD
        31-70 = NORMAL
        71-99 = GOOD
        """
        # so, what do we have?
        if 0 <= self.value <= 30:
            return BAD

        elif 31 <= self.value <= 70:
            return NORMAL

        # must be good
        return GOOD


class Fatigue(Modifier):
    """
    This class is a modifier that manages the unit fatigue. A unit that is tired performs worse
    than a rested unit. This modifier has several methods that can disallow a unit from performing
    certain actions when the fatigue is too high. These methods are the check_xXX() methods.

    This modifier has a value range [0..999] instead of the default [0..99].
    """

    # the possible string values for this modifier
    strings = ['rested', 'rested', 'ok', 'ok', 'tired',
               'tired', 'weary', 'weary', 'exhausted', 'exhausted']

    def __init__(self, value):
        """
        Creates the instance of the class and sets the passed value. This class has another value
        range so we need this constructor
        """
        Modifier.__init__(self, value, 0, 999)

    def checkSkirmish(self):
        """
        This checks weather the unit is too fatigued to skirmish. Returns 1 if all is ok and 0 if
        not. 

        The limit for a failure is 700 or above.
        """
        # do we fail?
        if self.value >= 700:
            # yep, failed
            return 0

        # all ok, fatigue is not too high
        return 1

    def checkAssault(self):
        """
        This checks weather the unit's fatigue is too high for an assault. This assault is the
        part where the unit double times towards the enemy, not the final storming. Returns 1 if all
        is ok and 0 if not.

        The limit for a failure is 500 or above.
        """
        # do we fail?
        if self.value >= 500:
            # yep, failed
            return 0

        # all ok, fatigue is not too high
        return 1

    def checkChangeMode(self):
        """
        This checks weather the unit's fatigue is too high for it to do a mode change. Returns 1
        if all is ok and 0 if not. 

        The limit for a failure is 800 or above.
        """
        # do we fail?
        if self.value >= 800:
            # yep, failed
            return 0

        # all ok, fatigue is not too high
        return 1

    def checkRotate(self):
        """
        This checks weather the unit's fatigue is too high for a rotate. Returns 1 if all is ok and
        0 if not. 

        The limit for a failure is 800 or above.
        """
        # do we fail?
        if self.value >= 800:
            # yep, failed
            return 0

        # all ok, fatigue is not too high
        return 1

    def checkRetreat(self):
        """
        This checks weather the unit's fatigue is too high for a retreat. Returns 1 if all is ok and
        0 if not. 

        The limit for a failure is 600 or above.
        """
        # do we fail?
        if self.value >= 600:
            # yep, failed
            return 0

        # all ok, fatigue is not too high
        return 1

    def checkMove(self):
        """
        This checks weather the unit's fatigue is too high for a move. Returns 1 if all is ok and
        0 if not. 

        The limit for a failure is 600 or above.
        """
        # do we fail?
        if self.value >= 600:
            # yep, failed
            return 0

        # all ok, fatigue is not too high
        return 1

    def checkMoveFast(self):
        """
        This checks weather the unit's fatigue is too high for a fast  move. Returns 1 if all is
        ok and 0 if not. 

        The limit for a failure is 500 or above.
        """
        # do we fail?
        if self.value >= 500:
            # yep, failed
            return 0

        # all ok, fatigue is not too high
        return 1

    def evaluateAttack(self, data):
        """
        Evaluates the modifier against the passed value. The new modified value is returned to
        the caller. A fatigue of 300 or less is neutral, more fatigue decreases the the damage
        done. At 999 fatigue the damage is 0.2. range: 0.2 to 1.0.

        Formula: data * ((100 - fatigue) / 100 + 0.2)
        """

        # the damage done. at 999 fatigue the damage is 0.2. range: 0.2 to 1.0
        if self.value > 300:
            # modify the value and return
            return data * ((1000 - self.value) / 1000 + 0.2)

            # no change
        return data

    def evaluateMelee(self, data):
        """
        Evaluates the passed 'data' value from a meleee point of view. This method will calculate
        a new value based on the fatigue value. If a unit is vary fatigued then this value is
        reduced, as the unit just does not have the energy to fight.

        A fatigue of 500 or less is neutral, more fatigue decreases the the damage done. At 999
        fatigue the damage is 0.2. range: 0.2 to 1.0.
        """

        # the damage done. at 999 fatigue the damage is 0.2. range: 0.2 to 1.0
        if self.value > 500:
            # modify the value and return
            return data * ((1000 - self.value) / 1000 + 0.2)

            # no change
        return data

    def evaluateTurningSpeed(self, data):
        """
        Evaluates the passed 'data' value from a turning speed point of view. This method will
        calculate a new value based on the fatigue value. If a unit is vary fatigued then this value is
        reduced, as the unit just does not have the energy to rotate at normal speed.

        A fatigue of 600 or less is neutral, more fatigue decreases the speed. At 999 fatigue the
        rate is 0.4. range: 0.4 to 1.0.
        """

        # at 999 fatigue the damage is 0.4. range: 0.4 to 1.0
        if self.value > 600:
            # modify the value and return
            return data * ((1000 - self.value) / 1000 + 0.4)

            # no change
        return data

    def evaluateMovementSpeed(self, data):
        """
        Evaluates the passed 'data' value from a movement speed point of view. This method will
        calculate a new value based on the fatigue value. If a unit is vary fatigued then this value is
        reduced, as the unit just does not have the energy to move at normal speed.

        A fatigue of 600 or less is neutral, more fatigue decreases the speed. At 999 fatigue the
        speed is 0.4. range: 0.3 to 1.0.
        """

        # at 999 fatigue the damage is 0.3. range: 0.3 to 1.0
        if self.value > 600:
            # modify the value and return
            return data * ((1000.0 - self.value) / 1000.0 + 0.3)

        # no change
        return data

    def toString(self):
        """
        Returns a string representation of the numerical value of this modifier. There are ten
        different strings that can be returned, and they are suitable for showing to the player. The
        strings are all lowercase.
        """
        # use div to get a value 0-99
        return Fatigue.strings[self.value // 100]

    def getStatus(self):
        """
        Returns one of the GOOD, NORMAL or BAD constants depending on the value of the
        modifier. The constant reflects the general value of it.

        0-300  = GOOD
        301-700 = NORMAL
        701-999 = BAD
        """
        # so, what do we have?
        if 0 <= self.value <= 300:
            return GOOD

        elif 301 <= self.value <= 700:
            return NORMAL

        # must be bad
        return BAD


class Experience(Modifier):
    """

    """
    # the possible string values for this modifier
    strings = ['conscript', 'green', 'novice', 'normal', 'normal',
               'well trained', 'seasoned', 'experienced', 'veteran', 'elite']

    def evaluateAttack(self, data):
        """
        Evaluates the modifier against the passed value. The new modified value is returned to
        the caller. A skill of 50 is neutral. less decreases the value and more increases the damage
        value. the modifier range: 0.5 to 1.5

        Formula: data * ((experience + 50) / 100)
        """
        return data * ((self.value + 50) / 100)

    def evaluateMelee(self, data):
        """
        Evaluates the modifier against the passed value. The new modified value is returned to
        the caller. A skill of 50 is neutral. less decreases the value and more increases the damage
        value. the modifier range: 0.5 to 1.5

        Formula: data * ((experience + 50) / 100)
        """
        return data * ((self.value + 50) / 100)

    def toString(self):
        """
        Returns a string representation of the numerical value of this modifier. There are ten
        different strings that can be returned, and they are suitable for showing to the player. The
        strings are all lowercase.
        """
        # use div to get a value 0-9
        return Experience.strings[self.value // 10]

    def getStatus(self):
        """
        Returns one of the GOOD, NORMAL or BAD constants depending on the value of the
        modifier. The constant reflects the general value of it.

        0-30  = BAD
        31-70 = NORMAL
        71-99 = GOOD
        """
        # so, what do we have?
        if 0 <= self.value <= 30:
            return BAD

        elif 31 <= self.value <= 70:
            return NORMAL

        # must be good
        return GOOD


class Aggressiveness(Modifier):
    """

    """

    # the possible string values for this modifier
    strings = ['coward', 'careful', 'careful', 'agg3', 'agg4',
               'moderate', 'moderate', 'aggressive', 'aggressive', 'wild']

    def evaluate(self, data):
        """
        Evaluates the modifier against the passed value. The new modified value is returned to
        the caller.
        """
        return data

    def toString(self):
        """
        Returns a string representation of the numerical value of this modifier. There are ten
        different strings that can be returned, and they are suitable for showing to the player. The
        strings are all lowercase.
        """
        # use div to get a value 0-9
        return Aggressiveness.strings[self.value // 10]


class RallySkill(Modifier):
    """

    """
    # the possible string values for this modifier
    strings = ['craven', 'cowardly', 'timid', 'apprehensive', 'careful',
               'hostile', 'offensive', 'pugnacious', 'aggressive', 'bellicose']

    def evaluate(self, data):
        """
        Evaluates the modifier against the passed value. The new modified value is returned to
        the caller.
        """
        return data

    def toString(self):
        """
        Returns a string representation of the numerical value of this modifier. There are ten
        different strings that can be returned, and they are suitable for showing to the player. The
        strings are all lowercase.
        """
        # use div to get a value 0-9
        return RallySkill.strings[self.value // 10]


class Motivation(Modifier):
    """
    This modifier reflects a leaders ability to motivate his troops to battle. A high rating makes
    the troops like the leader better and follows his orders more thoroughly. The units are more
    likely to actually follow a leader with a high motivation modifier into battle and less likely
    to disobey orders.
    """

    # the possible string values for this modifier
    strings = ['apathetic', 'phlegmatic', 'indolent', 'inert', 'indifferent',
               'stimulated', 'motivated', 'determined', 'inspired', 'resolute']

    def evaluate(self, data):
        """
        Evaluates the modifier against the passed value. The new modified value is returned to
        the caller.
        """
        return data

    def toString(self):
        """
        Returns a string representation of the numerical value of this modifier. There are ten
        different strings that can be returned, and they are suitable for showing to the player. The
        strings are all lowercase.
        """
        # nope, use div to get a value 0-9
        return Motivation.strings[self.value // 10]
