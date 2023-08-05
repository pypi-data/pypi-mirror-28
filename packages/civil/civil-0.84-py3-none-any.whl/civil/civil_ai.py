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

import getopt
import os
import traceback
import sys
import socket

from civil.server.ai.aiMinimal import aiMinimal
from civil.server.ai.event_loop import eventLoop
from civil import constants
from civil import properties
from civil.model import scenario
from civil.constants import UNKNOWN
from civil.net.connection import Connection
from civil.serialization.scenario_manager import ScenarioManager

# host and port of server
host = 'localhost'
port = 20000

# our ai object will be initialized later
ai = ''


def usage(code):
    """
    Prints out usage for the ai client. This is called when the user gives the commandline
    parameter -h or --help, and if the parameters are wrong. It then exits using the passed error
    code.
    """

    print(
    """
Usage:
    --host=<host>    - connect to <host> (default: localhost)
    --port=<port>    - connect using port <port> (default: 20000)
    """
    )

    # go away
    sys.exit(code)


###############################################################################################  
def parseCommandline(args):
    """
    Parses the commandline options and make sure they are valid. Exits the application on error
    and prints an error message.
    """

    global host, port

    # set default values
    scenario.local_player_id = UNKNOWN

    try:
        # get options an their arguments
        options, arguments = getopt.getopt(args, "h:p:", ["host=", "port="])

    except getopt.GetoptError as message:
        # oops, invalid parameters
        print("AI: invalid parameters: " + str(message))
        usage(2)

    # loop over all options
    for option, arg in options:
        # is this the port argument?
        if option in ("-p", "--port"):
            # store the port
            try:
                port = int(arg)

                # verify validness of port
                if port < 1 or port > 65535:
                    # invalid port
                    raise RuntimeError()
            except:
                # not an id, print error and exit
                print("\nAI: invalid port number. Valid range: 1-65535")
                usage(1)

        # is this the host argument?
        elif option in ("-p", "--host"):
            # store the host
            host = arg

        # is this the help argument?
        elif option in ("-?", "--help"):
            # show usage and exit
            usage(0)


def initNetwork():
    """
    Initializes the network connection using the passed parameters. Attempts to connect to a
    server running on 'host' which listens on 'port'. If all is ok and the connection was formed
    ok then the connection is stored and None is returned. On error a string with an error
    message is returned.
    """

    global host, port

    try:
        # create the socket
        new_socket = socket.socket()

        # connect to the remote system
        new_socket.connect((host, port))

        # all ok, store the new and connected socket and the extra info
        scenario.connection = Connection(new_socket)

        # send our name
        scenario.connection.send("Mr Computer\n")

    except socket.error as data:
        # explode the error 
        code, message = data.args[:2]
        print("AI: error creating socket to '%s' on port %d: %s" % (host, port, message))

        # was it a refused connection?
        if code == 111:
            # yes, warn the player
            print("AI: please ensure that a player acting as server is already running.")
            print("AI: the AI client can not act as a server.")

        sys.exit()

    except:
        print("AI: error creating socket: ")
        traceback.print_exc(file=sys.stdout)
        sys.exit()

        # we got this far, so all is ok. The socket is now connected and the server has given us
        # permission to continue with setting up the game


def loadScenario(path):
    """
    Loads the scenario in 'path' and stores all needed data. Returns 1 if all is ok and 0 on error.
    """

    # create a scenario manager 
    scenario_manager = ScenarioManager()

    print("AI: loading scenario... ")

    # load in the raw XML and los map
    if not scenario_manager.loadScenario(path):
        # error loading the scenario
        print("AI: error loading scenario:", path)
        return 0

    print("AI: scenario loaded ok")
    return 1


def readConfig():
    """
    Receives config data from the server. This data contains the player the AI should play, the
    name of the scenario file that should be loaded and the name of the other player. Returns the
    path to the scenario that should be loaded
    """

    # get data about the scenario from the server
    scenario_line = scenario.connection.readLine(-1)

    # get data about the opponent from the server
    player_line = scenario.connection.readLine(-1)

    # split up the data
    scenario_parts = scenario_line.split()
    player_parts = player_line.split()

    # get the scenario data
    type = scenario_parts[0]
    base_path = scenario_parts[1]

    # get the id of the local player. it is the opposite of that of the remote player whose id we
    # got sent
    scenario.local_player_id = (constants.UNION, constants.REBEL)[int(player_parts[0])]

    # and the remote player name
    scenario.remote_player_name = "".join(player_parts[1:])

    # get the full path to the scenario file of the given type
    path = {'standard': properties.path_scenarios,
            'saved': properties.path_saved_games,
            'custom': properties.path_custom_scenarios}[type]

    # create a full path
    file_name = os.path.join(path, base_path)

    print("AI: scenario is %s" % file_name)
    print("AI: our id is: %d" % scenario.local_player_id)

    return file_name


def main():
    """
    Main function of the game. Initializes everything and the runs the main event loop. Creates
    internal datastructures and loads the scenario.
    """
    # we're an ai client
    scenario.local_player_ai = 1

    # parse commandline options
    parseCommandline(sys.argv[1:])

    # init the network
    initNetwork()

    # read config data
    scenario_file_name = readConfig()

    # is the scenario ok?
    if scenario_file_name is None or scenario_file_name == '':
        # hm, not a valid name?
        print("AI: error receiving scenario data, aborting")
        return

    # all is ok, load the scenario
    if not loadScenario(scenario_file_name):
        # loading failed, not too much we can do about that
        print("AI: error loading scenario, aborting")
        sys.exit(1)

    # now we're playing!
    scenario.playing = constants.PLAYING

    # initialize the actual AI
    scenario.local_ai = aiMinimal()

    # start the main event loop
    eventLoop()


def start():
    """
    Starting point for the application, simply runs main() and checks for errors and
    finally quits the application.
    """
    # run, civil, run!
    main()


# starting point if run directly on the commandline
if __name__ == '__main__':
    start()
