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

# current selected company
currentunit = None

# icons
icons = None

# the map view
mapview = None

# global hash of weapons, indexed by the id
weapons = {}

# default weapons for new units
defaultweapons = {'infantry': -1,
                  'cavalry': -1,
                  'headquarter': -1,
                  'artillery': -1}

# alla available ranks for commanders
ranks = []

# default rank for new units
defaultrank = ""
