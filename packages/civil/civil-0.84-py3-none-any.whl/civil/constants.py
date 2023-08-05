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
This file contains various constants that can be used throughout the game. They should not be
changed, and basically should work like the C/C++ 'enum' type.
"""

# the armies
REBEL = 0
UNION = 1
UNKNOWN = 2
BOTH = 3

# define the possible unit types
INFANTRY = 0
CAVALRY = 1
ARTILLERY = 2
HEADQUARTER = 3

# current game state
PLAYING = 0
GAME_ENDED = 1

# define some constants that indicate how a game ends.
UNION_SURRENDER = 0
UNION_DESTROYED = 1
UNION_DEMORALIZED = 2
UNION_QUIT = 3
REBEL_SURRENDER = 4
REBEL_DESTROYED = 5
REBEL_DEMORALIZED = 6
REBEL_QUIT = 7
BOTH_QUIT = 8
BOTH_DESTROYED = 9
CEASE_FIRE = 10
OPPONENT_CRASH = 11
GAME_SAVED = 12
TIMEOUT = 13
CRASH = 14

# define some constants that indicate the battle result
UNION_MAJOR_VICTORY = 0
UNION_MINOR_VICTORY = 1
DRAW = 2
REBEL_MINOR_VICTORY = 3
REBEL_MAJOR_VICTORY = 4

# some constants used for colorizing messages
NORMAL = 0
CHAT1 = 1
CHAT2 = 2
COMBAT = 3
DESTROYED = 4
REINFORCEMENT = 5
ERROR = 6
AUDIO = 7
HELP = 8

# constants indicating what type of game we are playing
STANDARD = 0
SAVED = 1
CUSTOM = 2

# combat policies
HOLDFIRE = 0
DEFENSIVEFIRE = 1
FIREATWILL = 2

# define the possible types of damage
KILLED = 0
GUNSDESTROYED = 1

# map and physics constants
# constant used for pixel to meter conversions
METERS_PER_PIXEL = 1.5

# constant used for calculating the command delay for each meter. This is given as a speed in
# m/s. We just assume that 10m/s is realistic.
COMMAND_DELAY_SPEED = 10.0
