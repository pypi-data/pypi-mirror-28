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

# TODO this is a big global singleton right now, make it a class

# info about the scenario
info = None

# a list of the currently selected units. Selected units are those that the player has clicked
# on. If several units are selected for some reason they are all in the list
selected = []

# messages to the player
messages = None

# the global map. This map contain all the data about the terrain in the game. It is a
# two-dimensional array of hexes.
map = None

# the handle to the SDL module
sdl = None

# the main playfield .
playfield = None

# signal dispatcher and handler
dispatcher = None

# the connection to the remote player
connection = None

# audio manager
audio = None

# animation manager
animation_manager = None

# the id of the local player, the name of the remote host and a flag indicating weather we're the
# server or a connecting client
local_player_id = None
local_player_name = "Unknown"
remote_player_name = ""

# flag indicating weather the local player is an ai player
local_player_ai = 0

# a handle to the AI code itself.  Will be initialized later if this is the AI.
local_ai = None

# flag indicating weather we're starting a server or not
start_server = 0

# flag indicating weather we're starting an AI player or not. by default we run one
start_ai = 1

# flag indicating that we're playing. When this gets set to 0 then the main loop of the clients
# should be terminated
playing = 1
end_game_type = -1

# flag indicating weather the current turn has ended. valid only for the server
turn_ended = 0

# data for the time
# time = None

# the main engine. This is created and used only by the player acting as server. The other player
# will send data to the other engine
engine = None

# the current state of the game
current_state = None

# stupid hacks here
#

# This is set if we are in quickstart mode
#  0  - not
# 'r' - rebel
# 'u' - union
commandline_quickstart = 0

# This is set if we want sound/music
commandline_sound = 1
