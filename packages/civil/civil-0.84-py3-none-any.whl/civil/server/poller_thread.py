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

import sys
import traceback
from threading import *
import select

from civil.plan import factory as plan_factory
from civil.server.action import factory as action_factory
from civil.server import globals as server_globals
from civil import constants
from civil.model import scenario
from civil.net.connection import ConnectionClosed


class PollerThread(Thread):
    """
    This class implements a thread that waits for data from the two players. It reads the data
    and appends it to a queue of incoming data. The incoming data can then be read by the main
    engine when it has time.
    """

    def __init__(self, queue):
        """
        Initializes the thread. connection is the Connection that
        it will listen to
        """
        Thread.__init__(self)

        # the queue of incoming data
        self.queue = queue

    def run(self):
        """
        Starts and runs the thread. Waits for data from the two given players. When data arrives
        it is read and put onto the queue. A tuple with (id,data) is appended.
        """

        print("PollerThread.run: starting connection poller thread")

        # loop as long as we're said to be playing and there are any players left
        while scenario.playing == constants.PLAYING and len(server_globals.players) > 0:
            try:
                # We block with a timeout value so we can detect when the game has ended. the map
                # just avoids us having to create a loop or refer with hardcoded indexes 0,1
                # (hardcoded indexes are bad if one player happens to have quit)
                incoming, out, exceptional = select.select([p.getConnection() for p in list(server_globals.players.values())],
                                                    [], [], 1.000)
            except:
                # hmm, seems the other party has died?
                scenario.playing = constants.GAME_ENDED
                scenario.end_game_type = constants.OPPONENT_CRASH
                traceback.print_exc(file=sys.stdout)

                # terminate ourselves
                break

            # Did we get anything?
            if len(incoming) == 0:
                continue

            sender = None

            # loop over all incoming sockets, ie those that have data
            for connection in incoming:
                # find the player owning the connection
                for tmp_player in list(server_globals.players.values()):
                    # this player's connection?
                    if connection == tmp_player.getConnection():
                        # yep
                        sender = tmp_player
                        break

                # precautions
                if sender is None:
                    # oops?
                    print("PollerThread.run: sender is None, should not happen?")
                    break

                # read all the data. there is a loop here as the readLine() reads and buffers internally
                while 1:
                    try:
                        data = connection.readLine()
                    except ConnectionClosed:
                        # the player has disconnected
                        print("PollerThread.run: player %d %s has closed connection" % (sender.getId(),
                                                                                        sender.getName()))
                        # remove the offender if it still is with us
                        if sender.getId() in server_globals.players:
                            del server_globals.players[sender.getId()]
                        break

                    # we got data, what is it?
                    if data is None:
                        # no data, we're done for this connection
                        break

                    # handle the data
                    self.__handleData(sender, data)

        print("PollerThread.run: stopping connection poller thread")

        # make sure the main thread knows we're gone and the game can't continue
        scenario.playing = constants.GAME_ENDED
        scenario.end_game_type = constants.BOTH_QUIT

    def __handleData(self, sender, data):
        """
        Handles the read data. Checks weather it is some kind of action or a new plan. Action is
        immediately relayed to the other player and plans are put on the internal queue for handling
        by the engine.
        """

        # is the data some kind of action
        if action_factory.isAction(data.split()[0]):
            # data is an incoming action
            print("PollerThread.__handleData: got action: '%s'" % data)

            # figure out the player that should receive the action
            receiver_id = (constants.UNION, constants.REBEL)[sender.getId()]

            # does that player still exist?
            if receiver_id in server_globals.players:
                # yes, send the data
                receiver = server_globals.players[receiver_id]

                # send the action to the other player
                receiver.getConnection().send(data + '\n')

            # is it something that concerns the server in some way?
            if data.split()[0] == "quit_act":
                print("PollerThread.__handleData: removing %d" % sender.getId())
                # self.__removePlayer ( sender.getId() )
                del server_globals.players[sender.getId()]

        else:
            # create a new plan
            newplan = plan_factory.create(data.strip().split())

            # add the pan to the queue
            self.queue.put(newplan)
