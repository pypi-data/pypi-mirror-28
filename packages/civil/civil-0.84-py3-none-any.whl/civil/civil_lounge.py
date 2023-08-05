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
This file contains most of the logic for the Civil Lounge server. It is a standalone console-
based application that when run acts as a simple scenario and chat lounge. The player can by
clicking the "Lounge" button connect to this server and then browse/download scenarios and
chat to other connected players. The lounge server is no essential part of playing Civil, it
need not be run at all, that only removes the lounge functionality, no in-game functionality.

As the lounge can serve scenarios too it must when started be given the name of an index file
containing scenario data. These scenarios are then the ones that connecting clients can download
to their own systems and use. Any number of index files can be given on the commandline. This
makes it possible to have separate indexes for different types of scenarios.
"""

import string
import traceback
import sys
import socket
import select

from civil import properties
from civil.serialization.scenario_manager import ScenarioManager
from civil.lounge.guest import Guest

# list of sockets we have connected
guests = []
insocket = None

scenario_manager = None


def readScenarioIndex(file_name):
    """
    Reads the scenario index file from the given path.
    """
    global scenario_manager

    # create a scenario manager if we don't already have one. This will read the scenarios from
    # the server
    scenario_manager = ScenarioManager()

    # read in all scenario info:s
    try:
        scenario_manager.loadScenarioIndex(file_name) # TODO loadScnearioIndex does not exist anymore
    except:
        # failed to read the index file
        print("\nOoops...\n\nFailed to read the index file: %s" % file_name)
        print("Please make sure that the given parameter is really an index file.\n")
        sys.exit(1)

    print("index %s contains %d scenarios" % (file_name, len(scenario_manager.getScenarios())))


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

    # listen for guests
    s.listen(5)

    print("listening on port %d" % port)

    # return the socket which is ready to listen on
    return s


def handle(guest):
    """
    Handles an event from a guest. This function reads one line of data and broadcasts it out to
    all other guests. On errors the guest is removed.
    """
    global guests, scenario_manager

    # read what there is to read
    try:
        line = guest.getConnection().readLine()
    except:
        # failed to read from the guest
        print("failed to read from", guest)
        line = ''

    print("got: '%s'" % line)

    # did we get anything?
    if line is None or line == '':
        # probably eof
        guests.remove(guest)

        # loop over all guests
        for tmp in guests:
            tmp.send('leave %s\n' % guest.getName())

        return

    # split the line so that we get the command and the 'payload'
    data = line.split()
    cmd = data[0]
    payload = "".join(data[1:])

    # what did we get?
    if cmd == 'join':
        # the guest is now officially joining the server
        print('guest %s is joining' % payload)

        # set new name
        guest.setName(payload.strip())

        # let all others know of the new guest
        for tmp in guests:
            if tmp != guest:
                # let the old guest know of the new player
                tmp.send('join %s\n' % guest.getName())

            # also let the new guest know of the old players
            guest.send('in %s\n' % tmp.getName())

    elif cmd == 'msg':
        # message from the guest
        print('message %s from %s' % (payload, guest.getName()))

        # write out data to all guests, including ourselves
        for tmp in guests:
            # and send the line
            tmp.send(line + '\n')
            print("send to", tmp)

    elif cmd == 'leave':
        # probably eof
        guests.remove(guest)

        # loop over all guests. the leaving guest isn't there anymore
        for tmp in guests:
            tmp.send('leave %s\n' % guest.getName())


    elif cmd == 'get_scenarios':
        # the guest wants the scenario index
        scenario_manager.sendScenarioInfo(guest.getConnection())

    elif cmd == 'scenario':
        # the guest wants a full scenario , get the id
        scenarioid = payload.strip()

        # and send off the scenario
        scenario_manager.sendScenario(guest.getConnection(), scenarioid)


def checkEvents():
    """

    Returns:

    """
    global guests, insocket

    # print "selecting:", guests + [insocket]

    # perform the select. We're only interested in incoming events. wait forever
    incoming, out, exceptional = select.select(guests + [insocket], [], [])

    # was there something on the incoming socket that we listen on?
    if insocket in incoming:
        # yep, we need to accept the new guest
        newsock, addr = insocket.accept()

        print("new guest from; %s" % addr[0])

        # create a new guest
        guest = Guest(newsock)

        # add the guest to our list of guests
        guests.append(guest)
        return

    # loop over all guests
    for guest in guests:
        # is this guest active?
        if guest in incoming:
            # yep, there's data from this guest. handle it
            handle(guest)


def main():
    """
    Runs the main part of the server. Creates the incoming socket and handles all requests.
    """
    global insocket

    # did we get any index files?
    if len(sys.argv) == 1:
        # no index file
        print("Ooops...\n\nNo index file given.")
        print("Usage: %s scenarioindex.xml" % sys.argv[0])
        sys.exit(1)

    # read scenarios from all indexes
    for index in sys.argv[1:]:
        readScenarioIndex(index)

    # create our incoming socket
    insocket = initSocket(properties.lounge_port)

    print("waiting for guests")

    # handle events forever
    while 1:
        checkEvents()


def start():
    """
    Starting point for the application, simply runs main() and checks for errors and
    finally quits the application.
    """
    main()

# starting point if run directly on the commandline
if __name__ == '__main__':
    start()
