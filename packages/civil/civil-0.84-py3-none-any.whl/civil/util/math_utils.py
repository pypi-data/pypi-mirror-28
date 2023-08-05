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

# we need a magic coefficient for angle calculations. It converts a radian to degrees and
# maps the angle from 0-359 to 0-35
coefficient = 180 / pi / 10


def calculateAngle(sx, sy, dx, dy):
    """
    Calculates the angle between the points (sx, sy) and (dx, dy). Angle 0 is north (12
    o'clock), and the angle goes clockwise. The resulted angle is then divided with 10 to get a
    value between 0 and 35.
    """
    # precautions
    if sx == dx and sy == dy:
        # oops, they are the same
        print("calculateAngle: coordinates are equal, returning default.")
        return 0

    # now calculate the angle using the formula: atan (y/x), performed by atan2 and then
    # converted  to an int in the correct range
    angle = int(floor(atan2(dx - sx, sy - dy) * coefficient) % 36)

    # return the angle
    return angle
