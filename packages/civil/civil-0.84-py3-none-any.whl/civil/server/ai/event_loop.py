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
import select

from civil import constants
from civil import plan
from civil.model import scenario
from civil.server import action
from civil.server.action import factory

# flag indicating weather orders have been done already
orders_done = 0


def crash():
    """
    This function is called when we have a server crash. It prints some info and exits.
    """
    print("AI: crash: server seems to have crashed, exiting")
    print("AI: crash: this should save state or do something intelligent")
    sys.exit(1)


def checkNetEvents(may_sleep_seconds):
    """
    Checks weather there are any network events ready to be received. If there is something to be
    handled it is done. Handled means that a line of data is read from the connection and a new
    command is
    """

    # get a line of data if one is available
    try:
        line = scenario.connection.readLine()
    except:
        # failed to read from the socket, remote host closed down?
        crash()

    # did we get anything?
    if line:
        # print "checkNetEvents: got '%s'" % line

        # split the data
        parts = line.split()

        # did we get any data at all?
        if len(parts) == 0:
            # oops, nothing there?
            raise RuntimeError("AI: checkNetEvents: no parameters at all?")

        # have the action factory try to make an action instance
        act = factory.create(parts)

        # did we get an update?
        if act is not None:
            # yes, it was an update, handle it
            act.execute()
            return

        # no update, have the plan factory make a plan
        newplan = plan.factory.create(parts)

        # print "checkNetEvents: got '%s'" % newplan.toString ().strip ()

    else:
        # Too small values means we don't sleep
        # Note that "== 0" might be bad because this is floating point
        if may_sleep_seconds < 0.01:
            return

        incoming, out, exceptional = select.select([scenario.connection], [], [], may_sleep_seconds)
        # Did we get anything?
        if len(incoming) == 0:
            return

        # We got something, so call us again.
        # Don't sleep again, tho
        checkNetEvents(0.0)


def sendPlans():
    """
    Sends all plans that the units have to the server. As we're the client we need to send
    the number of plans as an immediate update: 'end_turn' so that the server knows how many
    plans to expect
    """

    # all plans
    plans = []

    # loop over all units in the map
    for unit in scenario.info.units.values():
        # is the unit visible
        if unit.getOwner() != scenario.local_player_id:
            # not our unit, get next
            continue

        # add the unit plans
        plans += unit.getPlans()

    # now loop over all plans and send them
    for plan in plans:
        scenario.connection.send(plan.toString())

    print("AI: sendPlans: sent %d plans" % len(plans))


def updateAI():
    """
    This is the main point where the AI should do its work. It gets called very often, i.e. after
    every time that network events have been checked. It should therefore maybe not every call do
    full heavy calculations. Anyway, this is the place.
    """
    global orders_done

    # do stuff
    print("AI: updateAI: should perform AI calculations")
    scenario.local_ai.nextTurn()

    # orders are now given for this orders phase
    orders_done = 1

    # send off all plans first
    sendPlans()


def sendQuit():
    """
    Sends a 'quit' action to the server to tell the server and the other player that we are
    quitting now and will exit immediately.
    """

    #  create a new 'quit' action
    cmd = action.quit_act.QuitAct(scenario.local_player_id)

    # send off a command
    scenario.connection.send(cmd.toString())

    # clean up
    scenario.connection.close()


def eventLoop():
    """
    Main function that handles the entire event loop. Polls events from the SDL event system and
    handles them. Regularly checks weather there is any incoming data to be read.
    """

    global orders_done

    # How many seconds we may select() on the socket
    may_sleep_seconds = 0.0

    # loop forever, or at least while we're playing
    while scenario.playing != constants.GAME_ENDED:
        checkNetEvents(may_sleep_seconds)

        # do ai stuff if not already done. orders will be given only once for each orders phase
        if not orders_done:
            updateAI()
        else:
            may_sleep_seconds = 1.0

    # we're leaving, go away
    sendQuit()

    print("AI: event_loop: main loop terminated, exiting.")
