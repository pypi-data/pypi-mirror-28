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

from civil.model import scenario


class AnimationManager:
    """
    This class is the central handler for all animation in Civil. It takes care of:

    * letting interested classes register themselves as animatable
    * call a method at regular intervals to provide animation

    Interested parties should call the method register() to register themselves for animation. The
    parameters for the method are all that is needed for the animation.

    The method animate() should be called regularly, or as often as possible. The smallest time
    available for animatable objects is 250ms or 4fps.
    """

    def __init__(self):
        """
        Initializes the class.
        """
        # no animatables yet
        self.animatable = {}

        # last time we were here
        self.lastcall = pygame.time.get_ticks()

        # make sure we get events every now and then
        scenario.dispatcher.registerTimerCallback(150, self.animate, self)

    def animate(self):
        """
        Checks which objects are ready for animation. Calls the callback for those objects and
        updates their last animated time.
        """

        # get the current millisecond
        millisecond = pygame.time.get_ticks()

        # loop over all callbacks
        for callback in list(self.animatable.keys()):
            # get the data
            interval, last = self.animatable[callback]

            # should we animate?
            if millisecond - last > interval:
                # yes, call the callback
                callback()

                # update the last animated time
                self.animatable[callback] = (interval, millisecond)

    def register(self, interval, callback):
        """
        Registers a callback for animation. The 'callback' is called when the animation should be
        performed. It is not given any parameters. The parameter 'interval' is the *minimum* number
        of milliseconds between animation calls, but most likely it is larger, depending on system
        load.
        """

        # get the current millisecond
        millisecond = pygame.time.get_ticks()

        # add the callback along with the last update and interval. we use the callback as the key
        # (is that smart?) and store a tuple with the interval and the last update. we consider this
        # registration moment as the last update
        self.animatable[callback] = (interval, millisecond)

    def deregister(self, callback):
        """
        Removes the given callback from the internal structures of animatable objects.
        """

        # just remove, but make sure it is actually there
        if callback in self.animatable:
            del self.animatable[callback]
