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

import pygame
from pygame.locals import *

from civil.server.action import factory as action_factory
from civil.server.action import quit_act
from civil.net import client_poller_thread
from civil.plan import factory as plan_factory
from civil.state import error, idle
from civil import constants
from civil import properties
from civil.model import scenario
from civil.ui.end_game import EndGame
from civil.net.connection import ConnectionClosed


def endGame():
    """
    This function is called when the main loop has ended and the end screen should be shown. This
    function will take care of creating and handling the end dialog and eventually quit the
    application. Also terminates the music. If the ending was a crash then this will just exit the
    game.
    """

    # how did the game end?
    if scenario.end_game_type == constants.CRASH:
        # we crashed, abandon ship, abandon ship
        sys.exit(1)

    # create and run the dialog
    EndGame().run()

    # stop the music
    scenario.audio.stopMusic()


def quit():
    """
    This function sends a QuitAct action to the server so that it knows that we are quitting
    immediately. Sets the internal flag that tells the poller thread that the game is over.
    """
    # create the action
    cmd = quit_act.QuitAct(scenario.local_player_id)

    # send off a command over the net
    scenario.connection.send(cmd.toString())

    # not playing anymore, this will terminate the poller thread too
    scenario.playing = constants.GAME_ENDED


def crash():
    """
    This function is called when we have a server crash. It prints some info and exits.
    """
    print("crash: server seems to have crashed, exiting")
    print("crash: this should save state or do something intelligent")
    sys.exit(1)


def updateDisplay():
    """
    Updates the main display if there are any suitable events in the event queue. If there are
    they are applied and then the display is repainted to reflect the new changes. This method will
    periodically take care of animating stuff on the screen. This is also the sole point of the main
    running application where the actual screen is visible updated. This is good as we then don't
    have updates all around the sources, leading to duplicate updates.
    """

    # repaint the playfield if needed. This is the only location in the entire event loop
    # the playfield is really repainted, all other places merely register interest int having
    # something painted
    scenario.playfield.paint()

    # now update the display to reflect all changes
    scenario.sdl.update()


def handleAction(act):
    """
    Handles an action that has arrived on the network. The action is immediately executed so that
    it can affect the state of the game in whatever way needed. the current game state is also given
    a chance to look at the action, and if the current state indicates that a new state should be
    activated then is will be done.
    """

    # execute it in case it has something meaningful
    act.execute()

    # let the current state handle it
    newstate = scenario.current_state.handleAction(act)

    # do we have a new state that should be active
    if newstate:
        # yep, set it
        scenario.current_state = newstate


def checkNetEvents():
    """
    Checks weather there are any network events ready to be received. If there is something to be
    handled it is done. Handled means that one or more lines of data is read from the connection and
    actions/plans are created. If a critical error is encountered (i.e. can't read from socket) then
    crash() is called.
    """

    # get a line of data while there is one to be read
    while 1:
        try:
            line = scenario.connection.readLine()

        except ConnectionClosed:
            # the server closed the connection
            print("checkNetEvents: server closed the connection")
            scenario.current_state = error.Error()
            return

        except IOError:
            # failed to read from the socket, some kind of serious error
            scenario.current_state = error.Error()
            return
            # crash ()

        # did we get anything?
        if line is None or line == '':
            # no data, we're done
            return

        # we have data, split the data into words
        parts = line.split()

        # print "checkNetEvents: got '%s'" % parts[0]

        # did we get any data at all?
        if len(parts) == 0:
            # oops, nothing there?
            raise RuntimeError("checkNetEvents: no parameters at all?")

        # is it an action?
        if action_factory.isAction(parts[0]):
            # have the action_factory make an action instance
            act = action_factory.create(parts)

            # handle it
            handleAction(act)
        else:
            # no action, it must be a plan. have the plan_factory make a plan
            newplan = plan_factory.create(parts)

            # add the plan to the unit it belongs to
            scenario.info.units[newplan.getunit_id()].getPlans().append(newplan)


def nextEvent():
    """
    Waits and returns the next event from pygame. If it is a mouse motion event, take all those
    events and only use the last one.  This means the engine doesn't get every single mouse motion
    event, and makes refreshing smoother when moving the mouse quickly.
    """

    event = pygame.event.wait()
    if event.type == MOUSEMOTION:
        mousemoves = pygame.event.get(MOUSEMOTION)

        # any old mouse motion events?
        if mousemoves:
            # yeah, get the last one
            event = mousemoves[-1]
    return event


def event_loop():
    """
    Main function that handles the entire event loop for the human player. Polls events from the
    Pygame event system and handles them. Regularly checks weather there is any incoming data to be
    read. Performs repainting when needed and ends the game when that time comes.
    """

    # set the default state
    scenario.current_state = idle.Idle()
    newstate = None

    # pre-paint the playfield
    scenario.sdl.fill((0, 0, 0))
    scenario.playfield.paint()

    # update it all
    scenario.sdl.update()

    # Create the thread that listens for incoming client/server data
    connthread = client_poller_thread.ClientPollerThread(scenario.connection)
    connthread.start()

    # read_net = 0

    # Pump pygame event queue when we otherwise wouldn't be in the main loop
    # scenario.dispatcher.registerCallback("engine_execute_iteration", pumpPygame )
    # scenario.dispatcher.registerCallback("send_action_data", pumpPygame )

    # loop forever
    while scenario.playing != constants.GAME_ENDED:
        # This is quite a bad hack.
        # The problem is that we send one USEREVENT from
        # net.ClientPollerThread, even though
        # there might be several events arriving
        # while read_net:
        #    #print "Check net events"
        #    if not checkNetEvents ():
        #        read_net = 0

        # get next event
        event = pygame.event.wait()

        # Currently, NOEVENT is used for the State.callMeSoon() logic

        if event.type == pygame.QUIT:
            # user wants to quit the application, so do it by returning from the main event loop
            quit()
            return

        elif event.type == pygame.USEREVENT:
            # do we have any network events ready?  TODO: should this be called more often? Now we
            # potentially repaint for every net event we get, and that is bad. Indent one more step?

            # Perhaps timestamp messages and send them when a) a buffer is full, or b) a
            # certain timeout has been exceeded ? Then the receiver can take several
            # messages between two refreshes
            if event.code == properties.USEREVENT_DATA_FROM_SOCKET:
                # Read network events later, there might be several!
                # read_net = 1
                # read all network events
                checkNetEvents()
            else:
                raise RuntimeError("BUG - Undefined USEREVENT")

        elif event.type == pygame.USEREVENT + 1:
            # a timer event, let the dispatcher handle all optional timer callbacks
            scenario.dispatcher.checkTimers()

        # workaround to handle mouse movements. this is true if the mouse has been moved AND the
        # state wants the movement events OR it's another event type
        elif (event.type == pygame.MOUSEMOTION and scenario.current_state.wantMouseMotion()) or \
                event.type != pygame.MOUSEMOTION:

            # handle the event and get the possible changed state
            newstate = scenario.current_state.handleEvent(event)

            # do we have a new state that should be active?
            if newstate:
                # yep, set it
                scenario.current_state = newstate

        # update the display
        updateDisplay()

    # game ended, show what needs to be shown
    endGame()
