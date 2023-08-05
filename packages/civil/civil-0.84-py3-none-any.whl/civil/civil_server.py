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
This file is the main Civil server file. It starts up all needed logic on the server side
and runs the main loop. The main tasks are waiting for the players to join and then run
the game loop.
"""

import os.path
import socket
import sys
import select

from civil import constants
from civil import properties
from civil.net.connection import Connection
from civil.serialization.scenario_manager import ScenarioManager
from civil.server import globals as server_globals
from civil.server.engine import engine as server_engine
from civil.server.player import Player

# list of sockets we have connected
insocket = None

# the base scenario name
scenario_basename = ''

# the scenario type
scenario_type = ''


def initSocket(port):
    """
    This function initializes a socket on the passed 'port' for listening. If something fails
    (such as the port being in use) the method returns None.
    """

    # create the socket
    s = socket.socket()

    # allow bind()ing while a previous socket is still in TIME_WAIT.
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # bind our socket for incoming requests
    s.bind(('', port))

    # listen for players
    s.listen(5)

    print("server: listening for players on port %d" % port)

    # return the socket which is ready to listen on
    return s


def sendSetupData():
    """
    Sends setup data to both players. This is the needed data so that both players can start
    their actual games. Each player is sent the name of the scenario that is to be played and the
    type. The type tells the player where the scenario can be found. The player is also sent the
    data of the other player. The second player that did not start the server gets its own id this
    way.
    """

    # loop over both players
    for id in (constants.UNION, constants.REBEL):
        # get the player
        player_data = server_globals.players[id]

        # and the player that we send to
        target_player = server_globals.players[1 - player_data.getId()]

        # send the scenario data
        target_player.getConnection().send(scenario_type + " " + scenario_basename + "\n")

        # send the player data
        data = "%d %s\n" % (player_data.getId(), player_data.getName())
        target_player.getConnection().send(data)

        # now the players know that the game can start


def waitForPlayers():
    """
    Waits for the two players to join. This is a custom loop that just waits for the two players
    to join and makes sure they get proper id:s. Once the players have joined the incoming socket is
    closed.
    """
    global insocket

    first_player = None

    print("server: waiting for two players")

    # loop twice and accept two incoming players
    index = 0
    while index < 2:
        # perform the select. We're only interested in incoming events. wait forever
        incoming, out, exceptional = select.select([insocket], [], [])

        # was there something on the incoming socket that we listen on?
        if insocket in incoming:
            # yep, we need to accept the new guest
            new_socket, addr = insocket.accept()

            # read a line of data from the player
            data = new_socket.makefile().readline().split()

            # is this the player that performed the setup action and thus knows its id?
            if data[0] == 'setup':
                # yes, extract the extra data
                player_id = int(data[1])
                player_name = "".join(data[2:])
            else:
                # no, this is the second player that did not do the setup (AI or human player), and
                # who thus does not know any id for itself. first we need to find the other player
                # using a little ugly 'if'
                if server_globals.players[constants.REBEL] is None:
                    other_player = server_globals.players[constants.UNION]
                else:
                    other_player = server_globals.players[constants.REBEL]

                # figure out the id for this player based on the other player's id
                # TODO this is a problem because server_globals.players is never set
                player_id = [constants.UNION, constants.REBEL][other_player.getId()]

                # get the name
                player_name = "".join(data)

            # create a new player with a connection from the socket
            server_globals.players[player_id] = Player(Connection(new_socket), player_id, player_name)

            print("server: new player '%s', id: %d from; %s" % (player_name, player_id, addr[0]))

            # one more player done
            index += 1

        else:
            # huh?
            print("server: nothing on incoming socket? weird...")

    print("server: two players have joined")

    # close the incoming socket
    insocket.close()


def loadScenario(file_name):
    """
    Loads a scenario from the given file name. Returns 1 if all is ok and 0 on error.
    """

    print("server: loading scenario:", file_name)

    # create a scenario manager 
    scenario_manager = ScenarioManager()

    # load in the raw XML and los map
    if not scenario_manager.loadScenario(file_name):
        # error loading the scenario
        print("server: error loading scenario:", file_name)
        return 0

    print("server: scenario loaded ok")

    return 1


def main():
    """
    Runs the main part of the server. Checks passed parameters and creates the incoming socket
    and waits for players to join. Once the players have joined the engine is initialized and the
    players notified that the game is on. Finally the main event loop is started which handles all
    the game logic as long as the game runs.
    """
    global insocket, scenario_basename, scenario_type

    # check passed args
    if len(sys.argv) != 4:
        # oops, missing args?
        print("bad parameters.")
        print("usage: %s scenariofile type port" % sys.argv[0])
        sys.exit(1)

    try:
        # get the scenario file_name and type
        scenario_basename = sys.argv[1]
        scenario_type = sys.argv[2]

        # get the full path to this type of files
        path = {'standard': properties.path_scenarios,
                'saved': properties.path_saved_games,
                'custom': properties.path_custom_scenarios}[scenario_type]

        # add it to our path
        file_name = os.path.join(path, scenario_basename)

        # validate it
        if not os.path.exists(file_name):
            raise RuntimeError("invalid file_name")
    except:
        # oops, bad port
        print("invalid file_name: ", sys.argv[1])
        print("usage: %s scenariofile type port" % sys.argv[0])
        sys.exit(1)

    # validate the type
    if not scenario_type in ['standard', 'saved', 'custom']:
        # invalid type
        print("invalid scenario type: '%s'" % scenario_type)
        print("the type is one of: standard, saved or custom")
        print("usage: %s scenariofile type port" % sys.argv[0])
        sys.exit(1)

    try:
        port = int(sys.argv[3])

        # validate it
        if not 1 <= port <= 65535:
            raise RuntimeError("invalid port")
    except:
        # oops, bad port
        print("invalid port number: ", sys.argv[3])
        print("usage: %s scenariofile type port" % sys.argv[0])
        sys.exit(1)

    # load the scenario
    if not loadScenario(file_name):
        # loading failed, not too much we can do about that
        print("server: error loading scenario, aborting")
        sys.exit(1)

    # create our incoming socket
    insocket = initSocket(port)

    # wait for two players
    waitForPlayers()

    # send setup data
    sendSetupData()

    # create the engine
    server_globals.engine = server_engine.Engine()

    # run the engine!
    server_globals.engine.mainLoop()

    # we got here, so the game has ended
    print("server: game ended, exiting")


def start():
    """
    Starting point for the application, simply runs main() and checks for errors and
    finally quits the application.
    """

    main()


# starting point if run directly on the commandline
if __name__ == '__main__':
    start()
