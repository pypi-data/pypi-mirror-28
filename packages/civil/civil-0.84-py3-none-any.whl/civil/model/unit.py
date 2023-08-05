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

from math import sqrt

from civil import constants
from civil.model import scenario
from civil.server.mode.formation import Formation
from civil.server.mode.mounted import Mounted
from civil.server.mode.unlimbered import Unlimbered
from civil.model.organization import Organization
from civil.plan.general_move_command import GeneralMoveCommand
from civil.model.modifier import Morale, Fatigue, Experience
from civil.util.math_utils import calculateAngle


class Unit(Organization):
    """
    This class is a base class for all actual fighting units in the game. The unit is the basic
    fighting force in the game. Actual used units are subclasses of this class. This class provides
    some additional needed functionality that all actual units will need.

    Data contained for a unit is mainly the number of men/guns, the morale, experience and
    fatigue as well as the number of movement points. Other data includes the name of the unit, a
    unique id and the leader (inherited from Organization).

    Each unit also has a facing. The facing indicated which is the primary direction the unit
    currently looks in. This is a degree value where 0 is to the north (12 o'clock) and the going
    clockwise all the way to 359 in steps of 10 degrees. Fractions are not used, so there are 36
    different facings that are possible.

    Every unit has four possible movement speeds: normal, fast, assault and rout. These must be set
    by the concrete subclasses of Unit. If the unit can not assault the value should be -1.
    
    This organizational unit has no suborganizations.

    Each unit always has a position on the map. That position is not given in hexes, but in absolute
    pixel coordinates.

    All units also have a weapon that they use for combat.
    """

    def __init__(self, id, name, owner, position=(-1, -1)):
        """
        Creates the instance of the class. Sets default values of all members. They should be set
        manually to their correct values later. The type of the unit must have been set before
        calling this constructor.
        """

        # call super constructor
        Organization.__init__(self, id, name, owner)

        # no commander yet
        self.commander = None

        # set default values for all members
        self.morale = Morale(100)
        self.fatigue = Fatigue(100)
        self.experience = Experience(100)

        # make unit look in a default direction from the given position
        self.facing = 0
        self.position = position

        # set default number of men 
        self.men = 0
        self.killed = 0

        # not dead yet!
        self.destroyed = 0

        # no weapon yet
        self.weapon = None

        # no weapons yet
        self.weaponsok = 0
        self.weaponsdestroyed = 0

        # default and invalid movement speeds. set by subclasses! the value is a tuple that consists
        # of two values: a slow speed, a fast speed, assault speed and rout speed
        self.movementspeed = (-1, -1, -1, -1)

        # default invalid turning speed
        self.turning_speed = -1

        # default invalid mode change delay in seconds
        self.mode_change_delay = -1

        # the max range in meters that the unit can see
        self.sightRange = 2000

        # by default the unit is not visible
        self.visible = 0

        # by default the unit has no plans enqueued
        self.plans = []

        # no current mode
        self.mode = None

        # default combat policy
        self.combatpolicy = constants.FIREATWILL

        # default field of fire as a deviation from the facing of the unit
        self.fieldoffire = 3

        # no target yet
        self.target = None

    def getMorale(self):
        """

        Returns:

        """
        return self.morale

    def setMorale(self, morale):
        """

        Args:
            morale: 
        """
        self.morale = morale

    def getWeapon(self):
        """
        Returns the weapon the unit uses for fighting. This is an instance of the class Weapon.
        """
        return self.weapon

    def setWeapon(self, weapon):
        """
        Sets a new main weapon.
        """
        self.weapon = weapon

    def getWeaponCounts(self):
        """
        Returns the the number of weapons that the unit has. The value is a tuple of 

 """
        return self.weaponsok, self.weaponsdestroyed

    def setWeaponCounts(self, ok, destroyed):
        """
        Setsnew main weapons counts.
        """
        self.weaponsok = ok
        self.weaponsdestroyed = destroyed

        # precautions
        if self.weaponsok < 0:
            # this should not happen
            raise RuntimeError("Unit.setWeaponCounts: negative number of of weapons")

    def getDamage(self):
        """
        Returns the maximum unmodified damage of the unit. This is the damage of the main weapon
        multiplied with the number of those weapons.
        """

        # figure out the damage and return it
        return self.weaponsok * self.weapon.getDamage()

    def getFatigue(self):
        """

        Returns:

        """
        return self.fatigue

    def setFatigue(self, fatigue):
        """

        Args:
            fatigue: 
        """
        self.fatigue = fatigue

    def getExperience(self):
        """

        Returns:

        """
        return self.experience

    def setExperience(self, experience):
        """

        Args:
            experience: 
        """
        self.experience = experience

    def getFacing(self):
        """
        Returns the current facing of the unit.
        """
        return self.facing

    def setFacing(self, facing):
        """
        Sets a new facing for the unit. The facing must be in the range 0 to 35.
        """
        self.facing = facing

    def getFieldOfFire(self):
        """
        Returns the field of fire of the unit. The value is the number of 'steps' to any side of
        the current facing the unit where the target may be. The effective field of fire is 
        field-of-fire * 20 degrees, + 10 degress.  (0 FOF= 10 degrees, 1 = 30 degrees, 2 = 50
        degrees, etc.)
        """
        return self.fieldoffire

    def getPosition(self):
        """
        Returns a (x,y) tuple with the current position of the unit. Note that the position is
        not given in hexes, but in absolute pixel coordinates.
        """
        return self.position

    def setPosition(self, position):
        """
        Sets a new position. The parameter must be a (x,y) tuple with the new position. TODO:
        make sure we check the type of parameter here!
        """
        self.position = position

    def getMen(self):
        """
        Returns the number of men in the unit.
        """
        return self.men

    def setMen(self, men):
        """
        Sets a new number of men in the unit.
        """
        self.men = int(men)

    def getKilled(self):
        """
        Returns the number of killed men in the unit.
        """
        return self.killed

    def setKilled(self, killed):
        """
        Sets a new number of killed men in the unit.
        """
        self.killed = int(killed)

    def getMode(self):
        """
        Returns the current mode for the unit. Returns None if no mode has been set at all. This
        mode can be used to either print out the mode or use with the mode machine to change the
        current mode of the unit.
        """
        return self.mode

    def setMode(self, mode):
        """
        Sets a new current mode for the unit. No checks are done, the mode is assumed to be ok
        for the unit.
        """

        # precautions...
        assert (mode != '')

        # ok, all is ok, set the new mode
        self.mode = mode

    def getNormalMovementSpeed(self):
        """
        Returns the normal movement speed for the unit.
        """
        return self.movementspeed[0]

    def getFastMovementSpeed(self):
        """
        Returns the fast movement speed for the unit.
        """
        return self.movementspeed[1]

    def getAssaultMovementSpeed(self):
        """
        Returns the assault movement speed for the unit.
        """
        return self.movementspeed[2]

    def getRoutMovementSpeed(self):
        """
        Returns the rout movement speed for the unit.
        """
        return self.movementspeed[3]

    def getTurningSpeed(self):
        """
        Returns the turning speed for the unit. This is the number of turning steps per minute
        that the unit can perform. 36 steps is a full rotation (360 degrees).
        """
        return self.turning_speed

    def getModeChangeDelay(self):
        """
        This returns the delay in seconds for the unit to change its main mode. The mode change
        can be for instance mounted->dismounted, limbered->unlimbered and vice versa. The delay is
        the amount of time the unit needs to perform the change and be ready in the new mode.
        """
        return self.mode_change_delay

    def getCombatPolicy(self):
        """
        Returns the combat policy of this unit. The return value is one of the policies defined
        in the begining of this file.
        """
        return self.combatpolicy

    def setCombatPolicy(self, policy):
        """
        Sets a new combat policy.
        """
        self.combatpolicy = policy

        print("Unit.setCombatPolicy: %d has policy %d" % (self.id, policy))

    def getTarget(self):
        """


 """
        return self.target

    def setTarget(self, target):
        """
        Sets a new target unit. If the unit should have no target then pass in 'None' here.
        """
        self.target = target

    def setDestroyed(self, destroyed=1):
        """
        Marks the unit as destroyed (or non-destroyed if 'destroyed' is 0.
        """
        self.destroyed = destroyed

    def isDestroyed(self):
        """
        Returns 1 if the unit is destroyed, and 0 otherwise.
        """
        return self.destroyed

    def isVisible(self):
        """
        Returns the visibility of the unit. A value of 1 means the unit is visible, a value of 0
        means it is not visible to the local player. Visibility is always seen from the eyes of the


 """

        # just return the visibility flag
        return self.visible

    def setVisible(self, visible=1):
        """
        Marks the unit as visible (1) or hidden (0).
        """
        self.visible = visible

    def inRange(self, target):
        """
        Is the target in range? Returns 1 if it is in range for the unit's weapon and 0 if not.
        """

        x1, y1 = self.getPosition()
        x2, y2 = target.getPosition()

        # do a simple squared range calculation (no square roots)
        if ((x2 - x1) ** 2 + (y2 - y1) ** 2) > self.getWeapon().getRange() ** 2:
            # out of range
            return 0

        # we're in range
        return 1

    def seesEnemy(self, target):
        """
        Is the target visible? Returns 1 if 'target' is visible and 0 if not.
        """
        # check LOS to the target
        return self.calcViewSingle(target)

    def pointedAt(self, target):
        """
        Checks weather we are aimed more or less at the target? Returns 1 if the target is in the
        field of fire for the unit (can fire) and 0 if not.
        """
        x1, y1 = self.getPosition()
        x2, y2 = target.getPosition()

        diff = self.facing - calculateAngle(x1, y1, x2, y2)
        diff = min(abs(diff), abs(36 - diff))

        # check the difference against the field of fire for the unit. The FOF is given as a
        # deviation from the unit's facing
        if diff > self.fieldoffire:
            # we're not facing that way.  Can't fire.
            return 0

        # all ok, fire at will
        return 1

    def distance(self, target, simple=0):
        """
        Calculates the distance to 'target'. The returned value is a float. If the parameter
        'simple' is given any other value than 0 the returned value is the distance squared, i.e. a
        sqrt() is not performed before returning. In that case the value is an integer.
        """
        # get the distance from the source to the destination
        sx, sy = self.getPosition()
        dx, dy = target.getPosition()

        # calculate and return, depending on the simpleness wanted
        if simple == 0:
            # return an exact value
            return sqrt((sx - dx) * (sx - dx) + (sy - dy) * (sy - dy))

        else:
            # return a simplified value
            return (sx - dx) * (sx - dx) + (sy - dy) * (sy - dy)

    def applyDamage(self, type, count):
        """
         really stupid damage handling.  Fix or override this, eventually...
        
        Takes care of managing the killed and ok men as well as moving a destroyed unit to the map


 """

        # what type of damage did we get?
        if type == constants.KILLED:
            # guys died, check the number of killed. can't be more than the number of men
            killed = int(min(self.men, count))
            self.men -= killed
            self.killed += killed

            print("Unit.applyDamage: id: %d, %d killed, %d left" % (self.id, killed, self.men))

            # any men still left?
            if self.men < 1:
                print("Unit.applyDamage: unit %d is destroyed" % self.id)

                # no, we're destroyed now, remove the unit from the global structure of active units
                del scenario.info.units[self.id]

                # and instead add ourselves to the map of destroyed units
                scenario.info.destroyed_units[self.id] = self

                print("Unit.applyDamage: %d ok, %d destroyed" % (len(list(scenario.info.units.keys())),
                                                                 len(list(scenario.info.destroyed_units.keys()))))

                # handy-dandy we're destroyed flag and not visible anymore either
                self.destroyed = 1
                self.visible = 0

                print("Unit.applyDamage:", self)

                # all weapons of the unit are destroyed too
                self.weaponsdestroyed += self.weaponsok
                self.weaponsok = 0


        elif type == constants.GUNSDESTROYED:
            # reduce the number of guns/weapons for the unit
            self.weaponsdestroyed += count
            self.weaponsok -= count

        else:
            raise RuntimeError("Unit.applyDamage: unknown damage type: %d" % type)

    def calcViewSingle(self, unit):
        """
        Recalculates LoS/Visiblity from us to the passed unit. Returns 0 if 'unit' can not be
        seen and 1 if it can be seen.
        """
        # is the unit already destroyed?
        if unit.destroyed or self.destroyed:
            # yep, dead men can't see
            return 0

        sightSquared = self.sightRange ** 2
        x, y = self.getPosition()
        x2, y2 = unit.getPosition()
        canSeeIt = 0

        # square roots are expensive, so don't bother to take the
        # root of each side for the actual distance, just compare.
        if (x - x2) ** 2 + (y - y2) ** 2 < sightSquared:  # it might be close enough to see
            # check weather the unit can see the other based on its max seeing range
            return scenario.map.checkLos((x, y), (x2, y2), self.sightRange)

        print("Unit.calcViewSingle: too far", sightSquared, (x - x2) ** 2 + (y - y2) ** 2)

        # unit can't see
        return 0

    def updateVisibility(self):
        """
        Recalculates all lines-of-sight for this unit. A local unit is always visible. Checks all
        the enemy units and traces LOS to them, marks those that it can see as visible.
        """

        # is the unit an enemy unit?
        if self.owner != scenario.local_player_id:
            # this unit's an enemy unit
            return

        # loop over all units in the map
        for tmp_unit in scenario.info.units.values():
            # local player's unit?
            if tmp_unit.getOwner() == self.owner:
                # yep, make sure the unit is visible
                tmp_unit.visible = 1
                continue

            # now we have an enemy unit, is it visible? calculate from the 'current' unit to the
            # temporary enemy unit 
            tmp_unit.visible = self.calcViewSingle(tmp_unit)

    def hasGuns(self):
        """
        Returns 1 if this is a type of unit that has guns, and 0 if not.
        """
        return self.weapon.isArtillery()

    def hasPlans(self):
        """
        Returns 1 if the unit has any plans queued up for it and 0 if not.
        """
        if self.plans is None or len(self.plans) == 0:
            # no plans
            return 0

        return 1

    def getPlans(self):
        """
        Returns all the plans the unit has enqueued. The plans are in the list in the order of
        execution, i.e. the first plan is the one executed first. The list can be modified
        externally if needed.
        """
        return self.plans

    def setPlans(self, plans):
        """
        Sets a new list of plans for the unit. This method can be used if the list of plans needs
        to be modified externally. You can the first get the plans with 'getPlans()', modify the
        list and then call this method.
        """
        self.plans = plans

    def getActivePlan(self):
        """
        Returns the currently active plan, i.e. the one the unit is either currently executing or
        is starting to execute. If the unit has no plans then None is returned.
        """
        # precautions
        if self.destroyed == 1:
            # this should never happen
            raise RuntimeError("Unit.getActivePlan: getting active plan for destroyed unit.")

        # do we have any plans at all?
        if len(self.plans) == 0:
            # no plans
            return None

        # return the first plan
        return self.plans[0]

    def getLatestPlan(self):
        """
        Returns the latest plan that the unit has scheduled. If the unit has no plans then None
        is returned. If the unit is destroyed an error is raised.
        """
        # precautions
        if self.destroyed == 1:
            # this should never happen
            raise RuntimeError("Unit.getLatestPlan: getting latest plan for destroyed unit.")

        # do we have any plans at all?
        if len(self.plans) == 0:
            # no plans
            return None

        # return the latest plan
        return self.plans[-1]

    def getLatestPosition(self):
        """
        Returns the latest position from the plans. We need this so pathfinding starts from the
        latest part, not from where the unit originated...
        """

        # Default our current position
        latest_x, latest_y = self.getPosition()

        # would be easier to go in reverse...
        for plan in self.plans:
            if isinstance(plan, GeneralMoveCommand):
                latest_x, latest_y = plan.target_x, plan.target_y

        return latest_x, latest_y

    def getType(self):
        """
        Returns the type of unit.
        """
        return self.type

    def getTypeString(self):
        """
        Returns a string with the type of unit. If the type of the unit is invalid then an
        exception is raised.
        """

        if self.type == constants.INFANTRY:
            return "Infantry"

        elif self.type == constants.CAVALRY:
            return "Cavalry"

        elif self.type == constants.ARTILLERY:
            return "Artillery"

        elif self.type == constants.HEADQUARTER:
            return "Headquarter"

        else:
            raise ValueError("unit %s has invalid type" % self.getName())

    def getCommander(self):
        """
        Returns the commander of this organization.
        """
        return self.commander

    def setCommander(self, commander):
        """
        Sets a new commander for the organization.
        """
        # precautions
        if commander is None:
            raise RuntimeError("Organization.getCommander: commander is None")

        self.commander = commander

    def getSuperiorCommander(self):
        """
        Returns the commander of the unit. This is just a convenience method and makes it easier
        to dig out the commander of a unit.
        """
        # dig out the commander and return it
        return self.getParentOrganization().getHeadquarter().getCommander()

    def getSuperiors(self):
        """
        Returns all superior commanders for the unit and the their position. The return
        value is a list containing the hq companies the commander is in. If the unit has no superiors
        then the list is empty. A top-level organization will have no superiors, all others should
        have at least 1.
        """

        # so far no superior commanders. It may well be that a unit ends up with no commanders in which
        # case the list will remain empty. The unit is then the superior commander for its
        # organization (at least as we model it)
        commanders = []

        # start from our parent organization
        current = self.getParentOrganization()

        # loop as long as we find valid higher organizations
        while current is not None:
            # get the headquarter for this org. The hq is always in a company and the commander is
            # "placed" in that hq
            headquarter = current.getHeadquarter()

            # get the commander and position for that organization and append it
            commanders.append(headquarter)

            # get this organizations parent organization
            current = current.getParentOrganization()

        # return the list
        return commanders

    def getBaseDelay(self):
        """
        Calculates the base command delay for the unit in seconds. This is the time before it can
        start to accept new orders. The time is not an absolute time, but should be treated as a
        relative time added to the current turn, and only applicable if the unit does not perform
        any other plan at the moment. The base delay is built up from:

        * commander distance
        * unit mode
        * unit stats

        The commander distance is a value directly proportional to the total distance from the unit
        through all it's superior commanders. Longer distance means longer time.

        IDEA: if a very high superior commander is very near then its distance should be used
        instead? A commander that is moving around the battlefield and 'cheers' on the units and
        gives direct orders.
        
        The returned value is always an int. All values are always seconds

        TODO: most modifiers not yet used.
        """

        # get a base delay in seconds that is always applied
        delay = 30

        # TODO: modify with the unit's fatigue

        # TODO: modify with the unit's experience

        # TODO: modify with the unit's morale

        # TODO: modify with the unit's state

        print(self, self.getParentOrganization())

        # does it have a parent organization? the unit may be a high enough unit with no parent organizations
        if self.getParentOrganization() is not None:
            # yes, get the hq unit for the unit
            hq = self.getParentOrganization().getHeadquarter()

            # get our and the hq's position
            x1, y1 = self.getPosition()
            x2, y2 = hq.getPosition()

            # calculate distance from the unit to its superior
            distance = int(sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2) * constants.METERS_PER_PIXEL)

            # total command distance is known, calculate a delay for the distance and add it. this is just a
            # value that means how many seconds it takes to move the total distance given that orders
            # "travel" at COMMAND_DELAY_SPEED m/s
            delay += int(distance / constants.COMMAND_DELAY_SPEED)

        # modify with the commander's delay
        delay = self.getCommander().modifyBaseDelay(delay)

        print("Unit.getBaseDelay: total delay: %ds" % int(delay))

        # return it
        return int(delay)

        # find out all superior leaders and their locations

    ##         hqs = self.getSuperiors ()

    ##         # get our position
    ##         x1, y1 = self.getPosition ()

    ##         # do we have any leaders at all?
    ##         if len ( hqs ) == 0:
    ##             # no leaders, the unit is a headquarter for a top-level organization
    ##             print "getBaseDelay: unit has no superior commanders"

    ##         # so far no distance
    ##         totaldistance = 0.0

    ##         # loop over all superior commander companies
    ##         for hq in hqs:
    ##             # get the leader and pos
    ##             leader = hq.getCommander ()
    ##             x2, y2 = hq.getPosition ()

    ##             # calculate distance from the current unit to its superior
    ##             distance = int ( sqrt ( (x1 - x2) ** 2 + (y1 - y2) ** 2 ) * constants.METERS_PER_PIXEL )

    ##             # add to the current total distance
    ##             totaldistance += distance

    ##             #print "leader: %s at (%d,%d) dist: %d m" % (leader.getName (), x2, y2, distance)

    ##             x1, y1 = x2, y2

    ##         # total distance is known, calculate a delay for the distance and add it. this is just a
    ##         # value that means how many seconds it takes to move the total distance given that orders
    ##         # "travel" at COMMAND_DELAY_SPEED m/s
    ##         distancedelay = int ( totaldistance / constants.COMMAND_DELAY_SPEED )
    ##         delay += distancedelay

    # print "Unit.getBaseDelay: hqs: %d, distance: %d, delay: %ds" % ( len (hqs),
    #                                                                 totaldistance,
    #                                                                 distancedelay )

    def __str__(self):
        """
        Returns a string representation of the unit. This string is descriptive and can not be
        used to recreate the unit later. Used for debugging.
        """
        return "%d: %s %s %s" % (self.id, self.getTypeString(), self.getName(),
                                 ['ok', 'destroyed'][self.destroyed])

    def toXML(self, indent, level):
        """
        Returns a string containing the headquarter serialized as XML. The lines are not indented in
        any way, and contain no newline.
        """

        # get the type as a lowercase string
        type = self.getTypeString().lower()

        # build up the xml
        xml = indent * level + '<company id="%d" type="%s" name="%s">\n' % (self.id, type, self.name)

        # serialize the commander
        xml += self.commander.toXML(indent, level + 1)

        # add all data
        xml += indent * (level + 1) + '<pos x="%d" y="%d"/>\n' % self.position
        xml += indent * (level + 1) + '<men ok="%d" killed="%d"/>\n' % (self.men, self.killed)
        xml += indent * (level + 1) + '<facing value="%d"/>\n' % self.facing
        xml += indent * (level + 1) + '<morale value="%d"/>\n' % self.morale.getValue()
        xml += indent * (level + 1) + '<fatigue value="%d"/>\n' % self.fatigue.getValue()
        xml += indent * (level + 1) + '<experience value="%d"/>\n' % self.experience.getValue()
        xml += indent * (level + 1) + '<weapon id="%d" ok="%d" destroyed="%d"/>\n' % (self.weapon.getId(),
                                                                                      self.weaponsok,
                                                                                      self.weaponsdestroyed)

        # does the unit have a target?
        if self.target is not None:
            # yep, add the id of the target
            xml += indent * (level + 1) + '<target id="%d"/>\n' % self.target.getId()

        # close the tag and return our nice string
        xml += indent * level + '</company>\n'

        return xml


class InfantryCompany(Unit):
    """
    This class defines the smallest base type of actual visible infantry, the company. Instances of this
    class are what the player will usually work with when using infantry, and it contains no other
    suborganizations (although things such as platoons could be possible). Larger organizations
    contain no actual visible and movable units, but are merely an organizational aid.

    The normal size of an infantry company is 100 men.
    """

    def __init__(self, id, name, owner):
        """
        Initializes the instance.
        """
        # set the type before we call the superclass
        self.type = constants.INFANTRY

        # pass the id to superclass
        Unit.__init__(self, id, name, owner)

        # set default mode
        self.mode = Formation()

        # override the movement and turning speeds
        self.movementspeed = (10, 20, 25, 20)
        self.turning_speed = 10

        # set the mode change delay (in seconds)
        self.mode_change_delay = 120


class CavalryCompany(Unit):
    """
    This class defines the smallest base type of actual visible cavalry, the company. Instances of
    this class are what the player will usually work with when using cavalry, and it contains no
    other suborganizations. Larger organizations contain no actual visible and movable units, but
    are merely an organizational aid.

    The normal size of an cavalry company is 100 men.
    """

    def __init__(self, id, name, owner):
        """
        Initializes the instance.
        """
        # set the type before we call the superclass
        self.type = constants.CAVALRY

        # pass the id to superclass
        Unit.__init__(self, id, name, owner)

        # set default mode
        self.mode = Mounted()

        # override the movement and turning speeds
        self.movementspeed = (20, 30, 40, 30)
        self.turning_speed = 8

        # set the mode change delay (in seconds)
        self.mode_change_delay = 120


class ArtilleryBattery(Unit):
    """
    This is a subclass of Unit that implements behaviour needed for a unit of type artillery.

    A battery consists of 4 to 6 guns with roughly 20 men for each gun as its service.
    """

    def __init__(self, id, name, owner):
        """
        Initializes the instance.
        """
        # set the type before we call the superclass
        self.type = constants.ARTILLERY

        # pass the id to superclass
        Unit.__init__(self, id, name, owner)

        # set default mode
        self.mode = Unlimbered()

        # reduced field of fire
        self.fieldoffire = 2

        # override the movement and turning speeds
        self.movementspeed = (8, 15, -1, 15)
        self.turning_speed = 4

        # set the mode change delay (in seconds)
        self.mode_change_delay = 240


class Headquarter(Unit):
    """
    This class defines a headquarter class. A headquarter is a small unit that contains the
    commander for some organization above company, i.e. for battalions and up. A headquarter is a
    separate unit on the battlefield and can be controlled just like any other unit. It should be
    kept near the companies it controls or somewhat close to the suborganizations it controls.

    A headquarter also contains a commander, which is basically the only reason the the existence of
    the headquarter! The commander can be retrieved with getCommander().
    
    The normal size of a headquarter is 10 men.
    """

    def __init__(self, id, name, owner):
        """
        Initializes the instance.
        """
        # set the type before we call the superclass
        self.type = constants.HEADQUARTER

        # pass the id to superclass
        Unit.__init__(self, id, name, owner)

        # set default mode
        self.mode = Formation()

        # improved field of fire
        self.fieldoffire = 3

        # override the movement and turning speeds
        self.movementspeed = (10, 20, 25, 20)
        self.turning_speed = 12

        # set the mode change delay (in seconds)
        self.mode_change_delay = 60

    def getHeadquarterFor(self):
        """
        Returns the organization this unit is headquarter for, if any. If the unit is not a hq
        for any organization this method returns None. The organization is something above company
        level if valid.
        """
        return self.organization

    def setHeadquarterFor(self, organization):
        """
        Sets this unit as a headquarter for some organization.
        """
        self.organization = organization

    def toXML(self, indent, level):
        """
        Returns a string containing the headquarter serialized as XML. The lines are not indented in
        any way, and contain no newline.
        """

        # build up the xml
        xml = indent * level + '<headquarter id="%d" name="%s">\n' % (self.id, self.name)

        # serialize the commander
        xml += self.commander.toXML(indent, level + 1)

        # add all data
        xml += indent * (level + 1) + '<pos x="%d" y="%d"/>\n' % self.position
        xml += indent * (level + 1) + '<facing value="%d"/>\n' % self.facing
        xml += indent * (level + 1) + '<men ok="%d" killed="%d"/>\n' % (self.men, self.killed)
        xml += indent * (level + 1) + '<morale value="%d"/>\n' % self.morale.getValue()
        xml += indent * (level + 1) + '<fatigue value="%d"/>\n' % self.fatigue.getValue()
        xml += indent * (level + 1) + '<experience value="%d"/>\n' % self.experience.getValue()
        xml += indent * (level + 1) + '<weapon id="%d" ok="%d" destroyed="%d"/>\n' % (self.weapon.getId(),
                                                                                      self.weaponsok,
                                                                                      self.weaponsdestroyed)

        # close the tag and return our nice string
        xml += indent * level + '</headquarter>\n'

        return xml
