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

import queue
import datetime
import time

# executor modules
from civil.server.engine.executor import factory as executor_factory
from civil import constants
from civil.model import scenario
# needed action
from civil.server.action.done_act import DoneAct
from civil.server.action.time_act import TimeAct
from civil.server import globals as server_globals
from civil.server import properties as server_properties
# AI modules
from civil.server.engine.ai.assign_targets import AssignTargets
from civil.server.engine.ai.check_los import CheckLOS
from civil.server.engine.ai.check_reinforcements import CheckReinforcements
from civil.server.engine.ai.clear_targets import ClearTargets
from civil.server.engine.ai.morale import Morale
from civil.server.engine.ai.rally import Rally
from civil.server.engine.ai.resolve_melee import ResolveMelee
from civil.server.engine.ai.rest import Rest
from civil.server.engine.ai.units_destroyed import UnitsDestroyed
from civil.server.poller_thread import PollerThread


class Engine:
    """
    This class is the main logic of the entire application. It works as the game engine and
    processes all commands the players have given and sends out what actually should happen. It
    takes care of issues such as:

    * movement of units
    * all combat resolution
    * line of sight
    * status changes for units
    * a lot more

    It loops through all the plans that the players have issued to units, and calculates the
    action.

    """

    def __init__(self):
        """
        Initializes the instance. Sets default values for all needed members.
        """

        # initialize the modules
        self.modules = [AssignTargets(),
                        ClearTargets(),
                        # ResolveCombat (),
                        ResolveMelee(),
                        Rally(),
                        Rest(),
                        UnitsDestroyed(),
                        Morale(),
                        CheckLOS(),
                        CheckReinforcements()]

        # no executors yet
        self.executors = {}

        # create the queue of incoming packets
        server_globals.incoming = queue.Queue()

        # create the poller thread and start it. let it operate on our players and the dedicated
        # queue for incoming data
        PollerThread(server_globals.incoming).start()

        # we are playing now
        scenario.playing = constants.PLAYING

        print("Engine.init: engine initialized")

    def mainLoop(self):
        """
        The main loop of the server. This is entered when the server starts up starts to actually
        simulate the game. This method will sleep for the most of the time, and once every second it
        wakes up and performs the calculations for that 'turn'. After the action has been calculated
        and sent out to the players the server will resume sleeping.
        """

        # handle events while we are playing. this will quit as soon as the game ends and thus not
        # give the players a chance to chat after the game. this should be changed to something
        # like:
        #    ... == constants.ALL_PLAYERS_QUIT
        while scenario.playing == constants.PLAYING:
            # sleep for some time
            time.sleep(1)

            # print "Engine.mainLoop: running update"

            # get all events and apply them
            # print "Engine.mainLoop: incoming plans:", server_globals.incoming.qsize ()

            # distribute all plans that have arrived while we were sleeping
            self.__distributePlans()

            # update action for the turn
            self.__update()

            # update the time too
            self.__updateTime()

        # the game has ended
        print("Engine.mainLoop: game has ended, exiting")

    def __distributePlans(self):
        """
        Gets all plans that have arrived from the players and distributes them to the proper
        units. The plans are just appended last among the unit's plans. Plans are not sent to other
        players.
        """
        # loop over all plans
        while server_globals.incoming.qsize() > 0:
            # get a plan without blocking. well, it should never block unless some other part of the
            # engine removes plans too
            plan = server_globals.incoming.get(block=0)

            # do we have such a unit?
            if plan.getunit_id() not in scenario.info.units:
                # no such unit, just log and then ignore the plan
                print("server: Engine.__distributePlans: no such unit: %d, ignoring plan for it" % plan.getunit_id())
                continue

            # add the plan to the unit
            scenario.info.units[plan.getunit_id()].getPlans().append(plan)

            # print "server: Engine.__distributePlans: %d got plan:" % plan.getunit_id(), plan

    def __update(self):
        """
        This method is the main workhorse of the entire engine. It checks all plans that should
        be processed this actual turn and processes them.  Executes active plans for all units by
        looping through all units and checks weather they have any plans that are currently being
        executed by an executor If they have such a plan executor it is executed. Finished executors
        are removed.

        If the unit has no active executor the delay for the first plan is checked to see if it can
        be started. For a plan that can be executed a new Executor instance is created for that
        particular plan. A plan that can not yet be executed (delay not 0), the delay is just
        decremented.

        """

        print("Engine.__update: starting calculations for turn %d" % server_globals.turn)

        actiondata = []

        # loop over all units and see weather the plans they have should be run
        for unit in list(scenario.info.units.values()):
            # Unit died before the iteration reached it?
            if unit.getId() not in scenario.info.units:
                continue
            # do we have an active executor for this unit, i.e. a plan that is currently being
            # executed? try to get it
            plan_exec = self.__getExecutor(unit)

            # is it valid?
            if plan_exec is not None:
                # it is valid, is it executing already or has its waiting delay been decremented
                # enough so that it is ready? we decrement with as many seconds as the engine
                # handles per update
                if plan_exec.isExecuting() or plan_exec.decrementDelay(server_properties.speedup_factor):
                    # yes, it is being executed or just got ready. execute!
                    self.__runExecutor(plan_exec, unit, actiondata)

                continue

            # the unit has no current executor, so we need to check weather the unit has any plans at
            # all and create an executor for it

            # get the unit's current active plan
            active = unit.getActivePlan()

            # has it any plans?
            if active is None:
                # no plans at all, next unit
                continue

            # create a new plan executor for the active plan
            plan_exec = executor_factory.create(unit, active)

            # make this executor the default for the unit
            self.executors[unit.getId()] = plan_exec

            # set a delay for the executor. TODO: any additional delays needed?
            plan_exec.setDelay(unit.getBaseDelay())

        # all units handled, send out the action that was created
        self.__sendToPlayers(actiondata)

        # all unit plans are now executed, time to execute all AI modules that are registered, and
        # that need to be executed this turn
        self.__executeAI()

        # now we need to clear out dangling executors for units that have been destroyed. if we
        # don't do this then we may have problems

        # loop over all existing executors
        for tmpexec in list(self.executors.values()):
            # get the unit the executor has and see if it's destroyed
            if tmpexec.getUnit().isDestroyed():
                # oh, it has gone away, so this executor shouldn't be here either
                del self.executors[tmpexec.getUnit().getId()]

    def __getExecutor(self, unit):
        """
        Finds the currently active executor for the given unit. If the executor does not exist or
        has been cancelled then None is returned. If all is ok a valid executor is returned.
        """
        # do we have an executor at all?
        if unit.getId() not in self.executors:
            # no executor
            return None

        # get the executor
        planexec = self.executors[unit.getId()]

        # get the ids of all the plans that the unit already has
        ids = [p.getId() for p in unit.getPlans()]

        # has the executor been cancelled from the outside, ie. has a some module or similar
        # removed the unit's plans?
        if not planexec.getPlan().getId() in ids:
            # the executor isn't among the plans for the unit, so it has been cancelled
            # somehow
            print("Engine.__getExecutor: *** executor has been cancelled:", planexec.getPlan().getName())
            print("Engine.__getExecutor: *** plan ids", ids)
            print("Engine.__getExecutor: *** plan id", planexec.getPlan().getId())

            # TODO: this nukes all executors for the unit and not only the current cancelled
            # plan. is this good?
            del self.executors[unit.getId()]

            # we're done
            return None

        # all is ok, this executor is valid
        return planexec

    def __runExecutor(self, planexec, unit, actiondata):
        """
        Executes the given executor. If the plan becomes finished after execution, then the
        executor is removed.
        """

        # TODO: send plans and action only to the player that needs them. Not all action needs to be sent to both players?

        # let it execute the plan if the planexec isn't already finished
        if not planexec.isFinished():
            # execute it
            planexec.execute()

        # is it finished now? note that this can not be an "else", as the plan may have been
        # finished during execution
        if planexec.isFinished():
            # yep, remove it from the dictionary of active executors. we're now supposed to
            # start working on the next plan for the unit. the new plan will be activated
            # next turn
            print("Engine.__runExecutor: executor finished:", planexec.getPlan().getName())
            del self.executors[unit.getId()]

            # remove the plan from the unit too. this is the first plan, so some nice
            # slicing will work just fine
            unit.setPlans(unit.getPlans()[1:])

            # print "Engine.__runExecutor: unit plans:", unit.getPlans ()

            # the plan is done, send data to the player that owns the unit. we do not need to send
            # to both players, as only one player actually knows the plans
            actiondata.append(DoneAct(unit.getId()), unit.getOwner())

    def __executeAI(self):
        """
        This method performs various simple automatic AI tasks for this turn. It loops over all
        loaded modules and checks weather they want to be executed at this turn. Not all modules are
        executed every turn.

        Modules return a list of actions that they want to have sent to the clients. The action is
        added to the internal list of action.
        """

        # get the current turn
        turn = server_globals.turn

        # no actiondata yet
        actiondata = []

        # loop over all modules
        for module in self.modules:
            # is the module ready to run?
            if module.isReady():
                # yep, execute
                module.execute(actiondata)

        # send the optional action data to the players
        self.__sendToPlayers(actiondata)

    def __sendToPlayers(self, actiondata):
        """
        Sends the given action to both the connected players. The 'action' should be a list or
        tuple of Action instances. The action can be targeted at one or both players.
        """
        # no action at all?
        if actiondata is None:
            # no action at all, so nothing to do here
            return

        # a list or tuple?
        if type(actiondata) is tuple or type(actiondata) is list:
            # send a list of items
            for actionitem in actiondata:
                # send it
                self.__sendOneItemToPlayers(actionitem)

        else:
            # a single item
            self.__sendOneItemToPlayers(actiondata)

    def __sendOneItemToPlayers(self, actionitem):
        """
         """
        # get receiver
        receiver = actionitem.getReceiver()

        # send to both?
        try:
            if receiver == constants.BOTH:
                # send to both players
                for player in list(server_globals.players.values()):
                    player.getConnection().send(actionitem.toString())

            else:
                # send to only one player
                server_globals.players[receiver].getConnection().send(actionitem.toString())

        except:
            # failed to send to either player
            print("server: Engine.__sendOneItemToPlayers: failed to send data, ending game")
            scenario.playing = constants.GAME_ENDED
            raise RuntimeError()

    def __updateTime(self):
        """
        Updates the internal time of the server. The clock is advanced as much as one turn
        takes. The new time is sent as a TimeAct to the players.
        """

        # one more turn done
        server_globals.turn += 1

        # create a delta time
        delta = datetime.timedelta(seconds=server_properties.speedup_factor)

        # set the new time
        scenario.info.setCurrentDate(scenario.info.getCurrentDate() + delta)

        # send to players an updated time
        self.__sendToPlayers(TimeAct(server_properties.speedup_factor))

        # has the game ended?
        if scenario.info.hasEnded():
            # the game has ended, send out the action
            # TODO EndGameAct unknown
            self.__sendToPlayers(EndGameAct(constants.TIMEOUT))

            # we're not playing anymore, set the flags that put the server into 'end game' mode 
            scenario.playing = constants.GAME_ENDED
            scenario.end_game_type = constants.TIMEOUT
