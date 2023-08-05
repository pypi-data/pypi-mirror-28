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

# the players that are connected to the server. The map can be indexed with the player id:s.
# we prefill it with two null values 
players = {constants.REBEL: None, constants.UNION: None}

# a thread safe queue of incoming stuff from the players
incoming = None

# the actual server engine. this is where the server spends all its time.
engine = None

# the current turn. this is a number incremented for each iteration of the main loop that the
# server performs
turn = 0
