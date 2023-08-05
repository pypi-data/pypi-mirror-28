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

from math import pi, hypot, sin, cos

from civil import properties
from civil.model import scenario


def calculateDistance(sx, sy, dx, dy):
    """
    Returns the distance from (sx,sy) to (dx,dy).
    """
    # get the distance from the source to the destination
    return hypot(float(sx) - float(dx), float(sy) - float(dy))


def calculateMovementSpeed(unit, basespeed):
    """
    Calculates the movements speed of the unit in psotitions (pixels) per turn. Returns the
    result.  Several different types of modifications are performed on the movement speed and base
    delay before commands are actually created. These are:

    * base delay
    * unit state
    * unit fatigue
    * terrain

    This method also calculates the x- and y-deltas the unit moves each turn, as well as the
    facing the unit should have in order to move towards the new position.
    """

    # use the given base speed for the unit
    speed = basespeed

    # use the unit's fatigue to modify the movement speed. A too fatigued unit will be forced to
    # move slower due to exhaustion
    speed = unit.getFatigue().evaluateMovementSpeed(speed)

    # use the terrain to modify the movement speed
    speed = speed * scenario.map.getTerrain(unit.getPosition()).movementSpeedModifier(unit)

    # get the number of steps per turn the unit can do. We use the movement speed per minute for
    # the unit as base for the calculation
    speed = float(speed) / (60.0 / properties.seconds_per_step)

    # print "calculateMovementSpeed: base speed %d, modified speed %.2f:" % (basespeed, speed)

    # we're done
    return speed


def calculatePosAlongFacing(facing, distance):
    """
    Calculates the deltas for a movement 'distance' long in the direction of 'facing'. The data
    returned is a (x,y) tuple, whose values originate from (0,0), so the deltas can be added to any
    coordinate. This function does no precaution checks for coordinates outside the map etc.
    """
    # precaution for the angle
    if facing < 0 or facing > 35:
        # illegal value
        raise RuntimeError("illegal facing %d, valid: [0,35]" % facing)

    # do some black magic with the facing. the reason for this is that we have facing 0 as straight
    # north, and increasing clockwise. the math stuff has 0 at straight west, and increasing
    # counterclockwise. so we need to modify our value to fit those expectations
    facing = 36 - (facing - 9) % 36

    # convert the facing to a radian value
    radian = (facing * 10.0) / 180.0 * pi

    # get the distance values in the x, y directions based on the radian
    delta_x = cos(radian) * distance
    delta_y = sin(radian) * distance

    # return what we got
    return delta_x, delta_y


def calculateMovementDeltas(sx, sy, dx, dy, speed):
    """
    This function calculates movement deltas for the x- and y-direction based on a given speed for
    a unit. The position (sx,sy) is where the unit is right now and (dx,dy) is the destination. A
    tuple (x,y) is returned with the delta values.
    """

    # get the distance from the source to the destination
    distance = calculateDistance(sx, sy, dx, dy)

    # default to invalid delta values
    delta_x = None
    delta_y = None

    # try:
    # how many turns are needed?
    turns_needed = distance / float(speed)

    # also calculate the delta_x and delta_y, i.e. the size of each step
    if turns_needed < 1.0:
        delta_x = float(dx - sx)
        delta_y = float(dy - sy)

    else:
        delta_x = float(dx - sx) / turns_needed
        delta_y = float(dy - sy) / turns_needed

        # return whatever deltas we have
    return delta_x, delta_y
