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

import pygame


class TimerNode:
    """
    This class is a helper class used to store one single timer callback and the times. It has a
    method for decrementing the delay until it should be called, and it also stores the callback.
    """

    def __init__(self, interval, callback, owner):
        """
        Creates the node, stores all data internally.
        """
        self.interval = interval
        self.callback = callback
        self.owner = owner

        # the current interval is set to max
        self.current = interval

    def decreaseInterval(self, delta):
        """
        Decreases the interval of the node. If the internal interval reaches 0 that means that
        the node's callback should be called. This emthod returns 1 if the call should be done, and
        0 if not. If the callback is ready then the interval is reset to its max value.
        """
        # decrease interval
        self.current -= delta

        # are we ready to be executed?
        if self.current <= 0:
            # yep, reset the interval
            self.current = self.interval

            return 1

        # not yet ready
        return 0

    def getCallback(self):
        """
        Returns the callback of the node, ie. the method/function that should be called when the
        interval has reached 0.
        """
        return self.callback

    def getOwner(self):
        """
        Returns the reference to the the class that owns the callback. This is used to identify
        the callback when removed.
        """
        return self.owner


class Dispatcher:
    """
    This class is used as a central handler for passing signals around to callbacks. Classes can
    register interest in some specified signals and when some other part of Civil emits that signal
    the callbacks get called. This is one way of reducing the number of classes a given class must
    know, as it does not need to care which other parts are interested in a given signal.

    This class also manages timing events. Classes can register interest in having a certain
    callback called at regular intervals.

    To register interest in a signal use the method registerCallback() like this:

        dispatcher.registerCallback ( 'some_signal', self.someCallback )

    To register interest in a timer use the method registerTimerCallback(). This example calls
    someCallback() every 300 ms.

        dispatcher.registerTimerCallback ( 300, self.someCallback )

    The callback should accept one parameter which is a list of parameters passed along with the
    signal. To emit a specified signal use:

        dispatcher.emit ( 'some_signal', (params...) )

    The emitting of a signal takes a optional list of signal dependent parameters. The contents are
    known to those handling the signal. Timer events do not contain any data.
    """

    def __init__(self):
        """
        Creates the instance of the class.
        """
        # no callbacks yet
        self.signal_callbacks = {}
        self.timer_callbacks = []

        # last time we were here
        self.lastcall = pygame.time.get_ticks()

        # the current timer interval to something invalid
        self.interval = -1

    def registerCallback(self, signal, callback):
        """
        Registers a new callback for the given signal. When that signal is emitted the callback
        will be called. Internally a dictionary is stored which maps signals to a list of callbacks.
        """

        # do we already have such a signal?
        if signal not in self.signal_callbacks:
            # no such signal
            self.signal_callbacks[signal] = []

        # just add it into the list of callbacks for that signal
        self.signal_callbacks[signal].append(callback)

    def registerTimerCallback(self, interval, callback, owner):
        """
        Registers a new timer callback that is to be called every 'interval'
        milliseconds. Nothing will guarantee that the callback occurs after exactly that interval,
        it is more like after at least that interval, ie. be prepared that it may be a little
        longer. 

        The minimum allowed callback time is 50 milliseconds, everything smaller will trigger an
        exception.

        Internally a dictionary is stored which maps times to a list of callbacks.
        """

        # precautions
        if interval < 50 or callback is None:
            raise RuntimeError("invalid data: interval=%d, callback=" % interval, callback)

        # just store the callback in a new node
        self.timer_callbacks.append(TimerNode(interval, callback, owner))

        # are we here for the first time?
        if self.interval == -1:
            # yep, so we're now starting the timer for the first time, store the current time
            self.lastcall = pygame.time.get_ticks()

            # use the given interval as our base interval from now on, until some smaller interval
            # is needed
            self.interval = interval

            # enable the timer with the new interval
            pygame.time.set_timer(pygame.USEREVENT + 1, self.interval)

        # is the new interval smaller than the current?
        elif self.interval > interval:
            # yep, we need to use this new interval as our timing interval, otherwise we'll get
            # timer events too rarely
            self.interval = interval

            # enable the timer with the new interval
            pygame.time.set_timer(pygame.USEREVENT + 1, self.interval)

    def deregisterTimerCallback(self, owner):
        """
        Removes all timer callbacks for the given owner.
        """
        # loop over all registered nodes and remove the ones owned by 'owner'
        for node in self.timer_callbacks:
            if node.getOwner() == owner:
                # owned by the caller, delete it
                self.timer_callbacks.remove(node)

    def emit(self, signal, parameters):
        """
        Emits the given signal. The parameters can be filled in with signal dependent data if
        needed.
        """

        # do we have such a signal?
        if signal not in self.signal_callbacks:
            # no such signal
            return

        # loop over all callbacks
        for callback in self.signal_callbacks[signal]:
            # execute it
            callback(parameters)

    def checkTimers(self):
        """
        Callback called when the timer triggers. This decreases the intervals for all registered
        timer nodes, and calls the callbacks for all those that have a timeout.
        """

        # get the current millisecond and calculate how many ms have passed since the last call was made
        millisecond = pygame.time.get_ticks()
        delta = millisecond - self.lastcall

        # loop over all nodes and decrease them
        for node in self.timer_callbacks:
            # decrease the time
            if node.decreaseInterval(delta):
                # we're ready to call the callback, so get it and call it. note the double () below!
                node.getCallback()()

        # store the new last calling time
        self.lastcall = millisecond
