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


def drawLine(surface, sx, sy, dx, dy, color):
    """
    Draws a line on the passed surface from (sx,sy) to (dx,dy). Uses the normal Bresenham
    algorithm. Throws an exception if the passed parameters are outside the surface dimensions. The
    color is assumed to be a valid pixel value mapped to a RGB(A) color.
    """

    # get the dimensions of the surface
    width, height = surface.get_size()

    # precautions
    if sx < 0 or sy < 0 or dx < 0 or dy < 0:
        raise IndexError("negative coordinates not allowed")

    # more checks
    if sx >= width or sy >= height or dx >= width or dy >= height:
        raise IndexError("coordinates out of range")

    # lock the surface before we begin
    surface.lock()

    delta_y = dy - sy
    delta_x = dx - sx

    if delta_y < 0:
        delta_y = -delta_y
        stepy = -1
    else:
        stepy = 1

    if delta_x < 0:
        delta_x = -delta_x
        stepx = -1
    else:
        stepx = 1

    # double the delta values
    delta_y *= 2
    delta_x *= 2

    # set start pixel
    # TODO raster is unresolved, what is it?
    raster.set_at([sx, sy], color)

    if delta_x > delta_y:
        # same as 2*delta_y - delta_x
        fraction = delta_y - (delta_x / 2)

        while sx != dx:
            if fraction == 0:
                sy += stepy

                # same as fraction -= 2*delta_x
                fraction -= delta_x

            sx += stepx

            # same as fraction -= 2*delta_y
            fraction += delta_y
            raster.set_at([sx, sy], color)

    else:
        fraction = delta_x - (delta_y / 2)

        while sy != dy:
            if fraction == 0:
                sx += stepx
                fraction -= delta_y

            sy += stepy
            fraction += delta_x
            raster.set_at([sx, sy], color)

    # we're done unlock the surface
    surface.unlock()
