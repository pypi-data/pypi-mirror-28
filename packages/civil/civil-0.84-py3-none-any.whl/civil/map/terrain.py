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

from civil import constants

# a dictionary of all terrain types, indexed by a string which is their name
terrainDict = {}


class ImpassableTerrainException(Exception):
    """
    Simple class for an exception that means that a unit has entered impassable terrain. The unit
    should not be there and it means we have a path error or something like that.
    """

    def __init__(self, unit):
        """
        Initialize the exception with a custom string.
        """
        # get unit position
        pos = unit.getPosition()

        # create the string
        str = "unit %d in impassable terrain at (%d,%d)" % (unit.getId(), pos[0], pos[1])

        # now init the exception
        Exception.__init__(self, str)

        # store the unit
        self.unit = unit


class Terrain:
    """
     The terrain type indicates what kind of terrain is dominant in the part of the map that
    the triangle occupies, such as woods, slope, mud etc. The type is used in various
    calculations. A one letter code is also given, it is used to represent the type of the terrain
    where a short code is enough.

    This class also provides easy means to use the terrain in various calculations, as it can return
    a modifier suitable for use in movement, attack and defense value calculations.

    TODO: more info about modifiers when we know how to handle them!

    Every subclass should set the data for the movement speed modifiers list. Every subclass can also
    decide what unit types can enter the terrain by customizing the method canUnitEnter() and
    disallowing certain types of units.

    Probably modifier inquiries should take an optional unit/type field?
    """

    def __init__(self, type, code):
        """
        Initializes the instance. Mainly sets default values for all data so that we don't break
        stuff unnecessarily.
        """

        # store the type and the letter code
        self.type = type
        self.code = code

        # set the movement speed and fatigue modifiers. These are four values that tell how the
        # terrain affects movement for: infantry, cavalry, artillery and headquarters. these must be
        # overridden by subclasses!
        self.movement_speed_mods = (1.0, 1.0, 1.0, 1.0)
        self.movement_fatigue_mods = (1.0, 1.0, 1.0, 1.0)

        # set default attack- and defense modifiers
        self.attack_mod = 1.0
        self.defense_mod = 1.0

        # store ourselves in the global dictionary
        terrainDict[code] = self

    def getType(self):
        """
        Returns the type of terrain for this triangle.
        """
        return self.type

    def getCode(self):
        """
        Returns the code of terrain for this triangle.
        """
        return self.code

    def canUnitEnter(self, unit):
        """
        Returns 1 if the given unit can enter this type of terrain and 0 if not.
        """
        # by default all units can enter all terrain
        return 1

    def movementSpeedModifier(self, unit):
        """
        This method returns a modifier for the movement speed for the given unit over this
        terrain. The modifier is a value that modifies the theoretical maximum speed of the unit,
        so all returned values are <=1.0. The speed also depends on the unit type. If the terrain is
        impassable then 0 is returned.
        """

        # return a speed that depends on the type
        return self.movement_speed_mods[unit.getType()]

    def movementFatigueModifier(self, unit):
        """
        This method returns a modifier for the fatigue the unit gains when moving over the
        terrain. The value is 1.0 if the terrain does not add extra fatigue at all, and >1.0 if the
        terrain is harder to move through. The value 1.0 should be like moving on solid, perfectly
        clear road.

        Different units may gain different amounts of fatigue for different types of terrain.
        """

        # return a speed that depends on the type
        return self.movement_fatigue_mods[unit.getType()]

    def defenseModifier(self):
        """
        Returns the defensive modifiers for this terrain. This value indicates how the terrain
        affects the defensive position. It may either increase or decrease the defensive value. An
        increased value means that the position is good for defense.
        """
        return self.defense_mod

    def attackModifier(self):
        """
        Returns the attack modifier for this terrain. This value indicates how the terrain
        affects the attacker in performing the attack. It may either increase or decrease the
        defensive value. A decreased value means that the position is good for attacking, probably
        very open and allows for easy maneuvers.
        """
        return self.attack_mod

    def visionModifier(self, altitude):
        """
         """
        if altitude > 0:
            return 1.0
        return 0  # Terrain is opaque below ground.

    def loscolor(self):
        """

        Returns:

        """
        return 0x00, 0x00, 0x00


class GrassTerrain(Terrain):
    """
      boring short grass
      """

    def __init__(self):
        """
        Initializes the instance. Sets needed parameters.
        """
        Terrain.__init__(self, "grassland", "g")

        # set the movement speed and fatigue modifiers
        self.movement_speed_mods = (1.0, 1.0, 1.0, 1.0)
        self.movement_fatigue_mods = (1.0, 1.0, 1.0, 1.0)

        # set attack- and defense modifiers too
        self.attack_mod = 0.9
        self.defense_mod = 0.6

    def loscolor(self):
        """

        Returns:

        """
        return 0x00, 180, 0x00


class SandTerrain(Terrain):
    """
     sand
     """

    def __init__(self):
        """
        Initializes the instance. Sets needed parameters.
        """
        Terrain.__init__(self, "sand", "s")

        # set the movement speed and fatigue modifiers for (inf,cav,art,hq)
        self.movement_speed_mods = (0.7, 0.8, 0.7, 0.7)
        self.movement_fatigue_mods = (1.0, 1.0, 1.0, 1.0)

        # set attack- and defense modifiers too
        self.attack_mod = 0.8
        self.defense_mod = 0.5


class MudTerrain(Terrain):
    """
     mud
     """

    def __init__(self):
        """
        Initializes the instance. Sets needed parameters.
        """
        Terrain.__init__(self, "mud", "m")

        # set the movement speed and fatigue modifiers for (inf,cav,art,hq)
        self.movement_speed_mods = (0.5, 0.5, 0.5, 0.5)
        self.movement_fatigue_mods = (1.0, 1.0, 1.0, 1.0)

        # set attack- and defense modifiers too
        self.attack_mod = 0.7
        self.defense_mod = 0.5

    def loscolor(self):
        """

        Returns:

        """
        return 85, 65, 33


class CrackedMudTerrain(Terrain):
    """
    Dried up cracked mud.
    """

    def __init__(self):
        """
        Initializes the instance. Sets needed parameters.
        """
        Terrain.__init__(self, "crackedmud", "c")

        # set the movement speed and fatigue modifiers for (inf,cav,art,hq)
        self.movement_speed_mods = (0.7, 0.7, 0.7, 0.7)
        self.movement_fatigue_mods = (1.0, 1.0, 1.0, 1.0)

        # set attack- and defense modifiers too
        self.attack_mod = 0.8
        self.defense_mod = 0.5


class RockTerrain(Terrain):
    """
     rocks
     """

    def __init__(self):
        """
        Initializes the instance. Sets needed parameters.
        """
        Terrain.__init__(self, "rocks", "o")

        # set the movement speed and fatigue modifiers for (inf,cav,art,hq)
        self.movement_speed_mods = (0.5, 0.5, 0.5, 0.5)
        self.movement_fatigue_mods = (1.0, 1.0, 1.0, 1.0)

        # set attack- and defense modifiers too
        self.attack_mod = 0.5
        self.defense_mod = 2.0

    def canUnitEnter(self, unit):
        """
        Returns 1 if the given unit can enter this type of terrain and 0 if not. This disallows
        artillery from entering rocky terrain.
        """
        # is the unit artillery?
        if unit.getType() == constants.ARTILLERY:
            # yes, can't enter
            return 0

        # all others are ok
        return 1

    def visionModifier(self, altitude):
        """

        Args:
            altitude: 

        Returns:

        """
        if 0 < altitude < 5:
            return .8
        return Terrain.visionModifier(self, altitude)

    def loscolor(self):
        """

        Returns:

        """
        return 0xff, 0xff, 0xff


class WaterTerrain(Terrain):
    """
     deep water
     """

    def __init__(self, type="water", code="a"):
        """
        Initializes the instance. Nothing can move through water.
        """
        Terrain.__init__(self, type, code)

        # no overridden settings needed

    def canUnitEnter(self, unit):
        """
        Returns 1 if the given unit can enter this type of terrain and 0 if not.
        """
        # by default no units can enter water
        return 0

    def movementSpeedModifier(self, unit):
        """
        Overridden modifier method that raises an exception. A unit can not enter water, so if
        this method is called for this terrain type we have an error.
        """

        # can't do this
        raise ImpassableTerrainException(unit)

    def movementFatigueModifier(self, unit):
        """
        Overridden modifier method that raises an exception. A unit can not enter water, so if
        this method is called for this terrain type we have an error.
        """

        # can't do this
        raise ImpassableTerrainException(unit)

    def defenseModifier(self):
        """
        Overridden modifier method that raises an exception. A unit can not be in water, so if
        this method is called for this terrain type we have an error.
        """

        # can't do this
        # TODO unit unknown
        raise ImpassableTerrainException(unit)

    def attackModifier(self):
        """
        Overridden modifier method that raises an exception. A unit can not be in water, so if
        this method is called for this terrain type we have an error.
        """

        # can't do this
        # TODO unit unknown
        raise ImpassableTerrainException(unit)

    def loscolor(self):
        """

        Returns:

        """
        return 23, 23, 178


class RiverTerrain(WaterTerrain):
    """
    Impassable deep river, no units can enter.
    """

    def __init__(self):
        """
        Initializes the instance. Sets needed parameters.
        """
        WaterTerrain.__init__(self, "river", "r")

        # no modifiers needed, can't enter rivers


class WoodsTerrain(Terrain):
    """
     deep woods
     """

    def __init__(self):
        """
        Initializes the instance. Sets needed parameters.
        """
        Terrain.__init__(self, "woods", "w")

        # set the movement speed and fatigue modifiers for (inf,cav,art,hq)
        self.movement_speed_mods = (0.5, 0.4, 0.2, 0.5)
        self.movement_fatigue_mods = (1.0, 1.0, 1.0, 1.0)

        # set attack- and defense modifiers too
        self.attack_mod = 0.8
        self.defense_mod = 1.5

    def canUnitEnter(self, unit):
        """
        Returns 1 if the given unit can enter this type of terrain and 0 if not. This disallows
        artillery from entering woods.
        """
        # is the unit artillery?
        if unit.getType() == constants.ARTILLERY:
            # yes, can't enter
            return 0

        # all others are ok
        return 1

    def visionModifier(self, altitude):
        """

        Args:
            altitude: 

        Returns:

        """
        if 0 < altitude < 10:
            return 0.2
        return Terrain.visionModifier(self, altitude)

    def loscolor(self):
        """

        Returns:

        """
        return 0x00, 0x40, 0x00


class FordTerrain(Terrain):
    """
    Crossable river, ie. a ford. Very disadvantageous terrain.
    """

    def __init__(self):
        """
        Initializes the instance. Sets needed parameters.
        """
        Terrain.__init__(self, "ford", "f")

        # set the movement speed and fatigue modifiers for (inf,cav,art,hq)
        self.movement_speed_mods = (0.2, 0.2, 0.1, 0.2)
        self.movement_fatigue_mods = (1.0, 1.0, 1.0, 1.0)

        # set attack- and defense modifiers too
        self.attack_mod = 0.2
        self.defense_mod = 0.5


class RoadTerrain(Terrain):
    """
     road.
     """

    def __init__(self):
        """
        Initializes the instance. Sets needed parameters.
        """
        Terrain.__init__(self, "road", "p")

        # set the movement speed and fatigue modifiers for (inf,cav,art,hq)
        self.movement_speed_mods = (1.0, 1.0, 1.0, 1.0)
        self.movement_fatigue_mods = (1.0, 1.0, 1.0, 1.0)

        # set attack- and defense modifiers too
        self.attack_mod = 1.0
        self.defense_mod = 0.3

    def loscolor(self):
        """

        Returns:

        """
        return 170, 132, 67


"""
This probably isn't the best way to do this, but I'm too lazy to figure out the smart way right
now. See gfx/terrains/terrains.txt
"""
GrassTerrain()
WaterTerrain()
WoodsTerrain()
SandTerrain()
MudTerrain()
RockTerrain()
CrackedMudTerrain()
FordTerrain()
RoadTerrain()
RiverTerrain()

##         grass   g
##         water   a
##         woods   w
##         sand    s
##         mud     m
##         rock    o
##         river   r
##         road    p
##         ford    f
##         crackedmud c
