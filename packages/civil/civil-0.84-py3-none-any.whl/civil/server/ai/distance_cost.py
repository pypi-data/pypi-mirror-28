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

try:
    import dc

    # specify distance cost function with map type
    dc_algorithm = {
        'diamond_v': dc.distance_cost_dv,
        'diamond_h': dc.distance_cost_dh,
        'rectangle': dc.distance_cost_r,
        'square_sg': dc.distance_cost_sg,
        'square_sd': dc.distance_cost_sd,
    }

except:

    from math import floor, ceil

    # Thanks Amit!
    # http://www-cs-students.stanford.edu/~amitp/Articles/HexLOS.html
    # Note: I'm using x,y coord to represent the opposite what amit does
    # This is mainly to allow for more seamless working with Numeric

    # distance cost helper functions
    def same_sign(n, n1):
        """

        Args:
            n: 
            n1: 

        Returns:

        """
        return (n > -1) == (n1 > -1)


    def a2h(xxx_todo_changeme):
        """

        Args:
            xxx_todo_changeme: 

        Returns:

        """
        (x, y) = xxx_todo_changeme
        return int(x - floor(float(y) / 2)), int(x + ceil(float(y) / 2))


    def h2a(xxx_todo_changeme1):
        """

        Args:
            xxx_todo_changeme1: 

        Returns:

        """
        (x, y) = xxx_todo_changeme1
        return int(floor(float(x + y) / 2)), y - x


    # For use with rectangular hex maps - usually a 2D array
    # The a2h and h2a algorithms are transforms needed here and to convert back
    # the path list below (XXX below)
    def r_distance_cost(p, p1):
        """

        Args:
            p: 
            p1: 

        Returns:

        """
        x, y = a2h(p)
        x1, y1 = a2h(p1)
        dx = x1 - x
        dy = y1 - y
        if same_sign(dx, dy):
            return max(abs(dx), abs(dy))
        else:
            return abs(dx) + abs(dy)


    # Diamond shaped maps
    # used for vertically stacked hex maps
    def dv_distance_cost(xxx_todo_changeme2, xxx_todo_changeme3):
        """

        Args:
            xxx_todo_changeme2: 
            xxx_todo_changeme3: 

        Returns:

        """
        (x, y) = xxx_todo_changeme2
        (x1, y1) = xxx_todo_changeme3
        dx = x1 - x
        dy = y1 - y
        if same_sign(dx, dy):
            return max(abs(dx), abs(dy))
        else:
            return abs(dx) + abs(dy)


    # used for horizontally stacked hex maps
    def dh_distance_cost(xxx_todo_changeme4, xxx_todo_changeme5):
        """

        Args:
            xxx_todo_changeme4: 
            xxx_todo_changeme5: 

        Returns:

        """
        (x, y) = xxx_todo_changeme4
        (x1, y1) = xxx_todo_changeme5
        dx = x1 - x
        dy = y1 - y
        if not same_sign(dx, dy):
            return max(abs(dx), abs(dy))
        else:
            return abs(dx) + abs(dy)


    # for square grid maps that don't allow diagonal movement
    def sg_distance_cost(xxx_todo_changeme6, xxx_todo_changeme7):
        """

        Args:
            xxx_todo_changeme6: 
            xxx_todo_changeme7: 

        Returns:

        """
        (x, y) = xxx_todo_changeme6
        (x1, y1) = xxx_todo_changeme7
        dx = x1 - x
        dy = y1 - y
        return abs(dx) + abs(dy)


    # for square grid maps that does allow diagonal movement
    def sd_distance_cost(xxx_todo_changeme8, xxx_todo_changeme9):
        """

        Args:
            xxx_todo_changeme8: 
            xxx_todo_changeme9: 

        Returns:

        """
        (x, y) = xxx_todo_changeme8
        (x1, y1) = xxx_todo_changeme9
        dx = x1 - x
        dy = y1 - y
        return max(abs(dx), abs(dy))


    # specify distance cost function with map type
    dc_algorithm = {
        'diamond_v': dv_distance_cost,
        'diamond_h': dh_distance_cost,
        'rectangle': r_distance_cost,
        'square_sg': sg_distance_cost,
        'square_sd': sd_distance_cost,
    }
