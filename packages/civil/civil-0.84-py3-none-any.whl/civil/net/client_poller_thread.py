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

import pygame

from civil import constants
from civil import properties
from civil.model import scenario


class ClientPollerThread(Thread):
    """
    This class implements a thread that waits for data on a specific socket connection. It sends
    a USEREVENT with a code and a connection parameter.
    """

    def __init__(self, connection):
        """
        Initializes the thread. connection is the Connection that
        it will listen to
        """
        Thread.__init__(self)
        self.connection = connection

        # allow the event we will use for notification
        pygame.event.set_allowed(pygame.USEREVENT)

        pygame.register_quit(self.__pygameQuitting)

        # we assume that pygame is ok for now. this flag is needed so that we don't later try to
        # post events when the event subsystem is already shot down
        self.pygame_ok = 1

    def run(self):
        """
        Starts and runs the thread
        """

        print("ClientPollerThread.run: starting connection poller thread")

        while scenario.playing == constants.PLAYING and self.pygame_ok:
            # We block with a timeout value
            # so we can detect when the game has ended
            try:
                incoming, out, exceptional = select.select([self.connection], [], [], 1.000)
            except:
                # hmm, seems the other party has died?
                scenario.playing = constants.GAME_ENDED
                scenario.end_game_type = constants.OPPONENT_CRASH

                # terminate ourselves
                break

            # Did we get anything?
            if len(incoming) == 0:
                continue

            # precautions
            if not self.pygame_ok:
                # pygame has gone away, so do we
                print("ClientPollerThread.run: pygame is not ok anymore, we're done")
                break

            try:
                # Create a new event
                e = pygame.event.Event(pygame.USEREVENT, {"code": properties.USEREVENT_DATA_FROM_SOCKET,
                                                          "connection": self.connection})
                # Send it to the main event loop
                pygame.event.post(e)

                # Just in case, also gives time for the main loop to read the packets
                pygame.time.wait(10)
            except:
                # Something broke badly, exit
                print("\nOops, something went wrong. Dumping brain contents: ")
                print("-" * 75)
                traceback.print_exc(file=sys.stdout)
                print("-" * 75)
                break

        # the main loop is done, close the socket and ignore any errors from that
        try:
            self.connection.close()
        except:
            pass

        print("ClientPollerThread.run: stopping connection poller thread")

    def __pygameQuitting(self):
        """
        Callback triggered when Pygame is being shut down. It means that the game has somehow
        ended and that main thread has closed down the Pygame stuff. We can no longer send messages
        anywhere but should instead just exit.
        """
        print("ClientPollerThread.__pygameQuitting")

        # ok, pygame is now down
        self.pygame_ok = 0
