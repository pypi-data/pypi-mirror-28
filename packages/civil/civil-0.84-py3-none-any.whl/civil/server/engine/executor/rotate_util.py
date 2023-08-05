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

from math import floor, pi, atan2

from civil import properties

# we need a magic coefficient for angle calculations. It converts a radian to degrees and
# maps the angle from 0-359 to 0-35
coefficient = 180 / pi / 10


def rotate(currentfacing, targetfacing, turnspeed):
    """
    Performs one step of a rotation. Performs all calculations. The rotation is not assumed to be
    finished, i.e. no checks are done to see weather currentfacing==targetfacing. Returns the new
    facing value. The value returned is an int.
    """

    # calculate the distance and direction
    distance, up = calculateTurnDistance(currentfacing, targetfacing)

    # print "rotate_util.rotate: data:",distance, up,turnspeed,currentfacing

    # is the distance less than what the unit would rotate in one turn?
    if turnspeed >= distance:
        # yep
        # print "rotate_util.rotate: do final small rotation"

        # return the final facing
        return int(targetfacing)

    # should we rotate up or down (cw or ccw)?
    if up:
        # need to increment
        newfacing = currentfacing + turnspeed

        # wrapping check
        if newfacing > 35:
            newfacing -= 36

    else:
        # down, decrement
        newfacing = currentfacing - turnspeed

        # wrapping check
        if newfacing < 0:
            newfacing += 36

    # print "rotate_util.rotate: new facing:", newfacing

    # we have a new facing now, return it
    return int(newfacing)


def calculateAngle(sx, sy, dx, dy):
    """
    Calculates the angle between the points (sx, sy) and (dx, dy). Angle 0 is north (12
    o'clock), and the angle goes clockwise. The resulted angle is then divided with 10 to get a
    value between 0 and 35.
    """

    # precautions
    if sx == dx and sy == dy:
        # oops, they are the same
        # print "calculateAngle: coordinates are equal, returning default."
        return 0

    # now calculate the angle using the formula: atan (y/x), performed by atan2 and then
    # converted  to an int in the correct range
    angle = int(floor(atan2(dx - sx, sy - dy) * coefficient) % 36)

    # return the angle
    return angle


def calculateReverseFacing(facing):
    """
    Calculates the reverse facing for the given 'facing'. The reverse facing is something that
    looks in the opposite direction.
    """

    # we simply add 18 and mod with 36
    return (facing + 18) % 36


def calculateTurnSpeed(unit):
    """
    Calculates the turning speed of the unit in steps (angles) per turn. Returns the result.

    Several different types of modifications are performed on the turning speed and base delay
    before commands are actually created. These are:

    * base delay
    * delay for other commands
    * leader experience
    * unit state
    * unit fatigue
    * terrain
        """

    # turning speed of the unit in steps per minute
    speed = unit.getTurningSpeed()

    # use the unit's current state (normal, routed etc) to modify the turning speed.
    # TODO: this is probably not necessary, as the unit already gives the base speed, and routed
    # units already have an own speed as given by the unit. SEE: move_util.py
    # speed = speed * 1.0

    # use the unit's fatigue to modify the turning speed. A too fatigued unit will be forced to
    # turn slower due to exhaustion
    speed = unit.getFatigue().evaluateTurningSpeed(speed)

    # use the terrain to modify the turning speed
    speed *= 1.0

    # get the number of turning steps per game steps the unit can do. We use the turning speed
    # per minute for the unit as base for the calculation
    speed = float(speed) / (60 / properties.seconds_per_step)

    # print "rotate_util.calculateTurnSpeed: speed:", speed

    # return the final speed
    return speed


def calculateTurnDistance(start, stop):
    """
    Calculates the distance of the rotation in steps and the direction that should be taken
    to reach the 'stop' value. The returned value is a tuple (distance,up) where the first value
    is the distance and the second is a flag indicating weather we should rotate up or down.
    """

    # parameters for the distance calculations. We simply loop clockwise until we find 'stop',
    # and at the same time calculate the distance. If the distance is > 18 then we should really
    # go counterclockwise
    distance = 0

    # make sure we handle integers here, otherwise our loop checks get fubar
    tmp = int(start)
    stop = int(stop)

    while tmp != stop:
        # one more step
        distance += 1
        tmp += 1

        # should we wrap from 36 to 0?
        if tmp >= 36:
            tmp = 0

    # ok, was the distance > 18
    if distance > 18:
        # yep, get the ccw distance and set the 'not up' flag
        distance = 36 - distance
        up = 0

    else:
        # we're going cw
        up = 1

    # return our data
    return distance, up


def isFlankAttack(attacker, target, max):
    """
    Checks weather fire from 'attacker' would be a flank attack on 'target'. The value 'max' sets
    the max deviation from the unit's facing that is allowed before an attack. Returns 1 if the
    attack is a flank attack and 0 if not.
    """
    # get the positions
    attackx, attacky = attacker.getPosition()
    target_x, target_y = target.getPosition()

    # first get the angle from the target to the attacker. note the way. this makes it easier to
    # check for a flank attack
    angle_to_attacker = calculateAngle(target_x, target_y, attackx, attacky)

    # now use the convenient function above and calculate the distance between the target's facing
    # and the angle to the attacker
    distance, dumy = calculateTurnDistance(angle_to_attacker, target.getFacing())

    print("isFlankAttack: %d %d %d = " % (angle_to_attacker, target.getFacing(), distance), end=' ')

    # so, is it a flank attack?
    if distance > max:
        # yep, flank attack, the distance is large
        print("flank")
        return 1

    print("not flank")
    # no flank attack
    return 0
