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


class Weapon:
    """
    This class contains all needed information about a weapon in the game. A weapon describes the
    needed data about a weapon that the units have. Weapons include normal rifles, artillery
    etc. The reason for having a separate class is that it is then easy for units to share the same
    type of weapon and its stats etc are in only one place.

    Every unit has one or more weapons, but mainly one primary and one secondary weapon.

    The data about a weapon includes:

    * a unique id, which is used in scenario files when referring to weapons.
    * a descriptive name that is suitable for showing to the players.
    * a type the categorizes the weapon into different types.
    * a range value, which is the max firing range the weapon is able to reach.
    * a damage value used to calculate the damage the weapon does when it hits.
    * an accuracy value describing how well the weapon hits at a specific range.

    """

    def __init__(self, id, name, type, range, damage, accuracy):
        """
        Initializes the instance. Sets the passed data.
        """
        # store data
        self.id = id
        self.name = name
        self.type = type
        self.range = range
        self.damage = damage
        self.accuracy = accuracy

    def getId(self):
        """
        Returns the id of this weapon.
        """
        return self.id

    def getName(self):
        """
        Returns the descriptive name of the weapon.
        """
        return self.name

    def setName(self, name):
        """
        Sets a new name value for the weapon.
        """
        self.name = name

    def getType(self):
        """
        Returns the descriptive type of the weapon.
        """
        return self.type

    def setType(self, type):
        """
        Sets a new type value for the weapon.
        """
        self.type = type

    def isArtillery(self):
        """
        Returns 1 if the weapon is an artillery weapon, ie. used by artillery.
        """
        # is this artillery?
        if self.type == 'artillery':
            # yep
            return 1

        # no artillery
        return 0

    def getRange(self):
        """
        Returns the range value of this weapon.
        """
        return self.range

    def getAccuracy(self):
        """
        Returns the accuracy value of this weapon.
        """
        return self.accuracy

    def getDamage(self):
        """
        Returns the damage value of this weapon.
        """
        return self.damage

    def setDamage(self, damage):
        """
        Sets a new damage value for the weapon. TODO: is this method unnecessary?
        """
        self.damage = damage

    def setRange(self, range):
        """
        Sets a new range value for the weapon. TODO: is this method unnecessary?
        """
        self.range = range

    def setAccuracy(self, accuracy):
        """
        Sets a new accuracy value for the weapon. TODO: is this method unnecessary?
        """
        self.accuracy = accuracy

    def toXML(self):
        """
        Returns a string containing the weapon serialized as XML. The lines are not indented in
        any way, and contain no newline
        """
        # build up the xml
        return '<weapon id="%d" name="%s" type="%s" range="%d" damage="%d" accuracy="%d"/>' % (self.id,
                                                                                               self.name,
                                                                                               self.type,
                                                                                               self.range,
                                                                                               self.damage,
                                                                                               self.accuracy)
