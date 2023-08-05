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

from civil import constants
from civil import properties
from civil.model import scenario

# some constants used for colorizing the messages, these should be nuked from here sooner or later,
# and only the ones in constants.py used
NORMAL = constants.NORMAL
CHAT1 = constants.CHAT1
CHAT2 = constants.CHAT2
COMBAT = constants.COMBAT
DESTROYED = constants.DESTROYED
REINFORCEMENT = constants.REINFORCEMENT
ERROR = constants.ERROR
AUDIO = constants.AUDIO
HELP = constants.HELP


class Messages:
    """
    This class keeps track of all messages that the other player or the engine have sent to the
    local player. The messages are normal textual strings that contain some for if textual
    information meant for the player.

    The messages are kept as prerendered surfaces, ready for blitting.
    """

    def __init__(self):
        """
        Creates the instance of the class. Resets all data.
        """
        # no labels yet
        self.labels = []

        # create the colors for the various types of messages
        self.colors = {constants.NORMAL: (255, 255, 255),
                       constants.CHAT1: (255, 255, 0),
                       constants.CHAT2: (0, 255, 255),
                       constants.COMBAT: (128, 255, 255),
                       constants.DESTROYED: (135, 206, 250),
                       constants.REINFORCEMENT: (255, 128, 128),
                       constants.ERROR: (0, 255, 255),
                       constants.AUDIO: (0, 255, 0),
                       constants.HELP: (210, 210, 255)}

        # get the font we should use
        self.font = pygame.font.Font(properties.layer_messages_font_name,
                                     properties.layer_messages_font_size)

        # get the shadow color
        self.shadowcolor = properties.layer_messages_shadow_color

        # get the max width of labels
        self.width = properties.layer_messages_max_width

        # register ourselves with the animation manager. we want to be called regularly, but not too
        # frequently
        scenario.animation_manager.register(properties.messages_animation_interval, self.animate)

    def add(self, message, type=NORMAL):
        """
        Adds a new message. The message is internally stored as a surface ready for blitting
        along with the hour and minute (game time) that tell when the message was received. The
        parameter 'type' indicates the type of message. Various types can have different colors to
        make it easier for the player to visualize the messages. The parameter defaults to NORMAL
        color, which can be used for anything. See the beginning of this file for the other
        types.
        """

        # get the current millisecond
        millisecond = pygame.time.get_ticks()

        tmp = ''
        all = ''

        # get the color we should use
        color = self.colors[type]

        # loop over all words
        for text in message.split(' '):
            # store the current full line
            tmp = all

            # merge a text we use to test the width with. Don't add a ' ' if we only have one word
            # so far
            if all == '':
                test = text
            else:
                test = all + ' ' + text

            # get the size of the label as it would be when rendered
            x, y = self.font.size(test)

            # too wide?
            if x > self.width:
                # yep, os use the last 'good' text that fits and render a label
                self.labels.append((millisecond, self.__renderLabel(all, color)))

                # start with a new full line that is the part that was 'too much'
                all = text

            else:
                # it's ok, append new text to full line
                all = all + ' ' + text

                # still something in 'all' that has not made it into a full line? we add a last (short) line
        # with the extra text
        if all != '':
            self.labels.append((millisecond, self.__renderLabel(all, color)))

        # do we have too many labels?
        if len(self.labels) > properties.messages_max_labels:
            # we need to get rid of a few labels. we slice away as many labels as are too
            # many. simple and efficient
            self.labels = self.labels[len(self.labels) - properties.messages_max_labels:]

        # The messages layer catches this and repaints
        scenario.dispatcher.emit('messages_changed', None)

    def animate(self):
        """
        Callback executed by the animation manager when it's time to perform animation. Actually
        it's no real animation, but just a way to make sure the messages on the playfield silently
        scroll away.
        """

        # ok, do we even have messages here?
        if len(self.labels) == 0:
            # no messages, get lost
            return

        # get the current millisecond
        millisecond = pygame.time.get_ticks()

        # should the first label be removed? we allow them at least 20s on display
        if millisecond - self.labels[0][0] < 20000:
            # too young, don't remove yet
            return

        # just slice away the first message, this removes it
        self.labels = self.labels[1:]

        # The messages layer catches this and repaints
        scenario.dispatcher.emit('messages_changed', None)

    def getLabels(self):
        """
        Returns the prerendered labels, ready for blitting. The text in the messages can no
        longer be obtained from the labels.
        """
        return self.labels

    def __renderLabel(self, text, color):
        """
        Renders the given text using the given color. The label will have a small shadow around
        it to make it easier to read and give better contrast. Or something. The shadow is created
        by first blitting the shadow four times, offset a little bit, and then finally the main
        text.
        """

        # first render the main text and a shadow
        maintext = self.font.render(text, 1, color)
        shadow = self.font.render(text, 1, self.shadowcolor)

        # now we get the size of that surface, as we want a slightly larger final surface
        width = maintext.get_width() + 3
        height = maintext.get_height() + 3

        # now allocate the final surface
        label = pygame.Surface((width, height), pygame.HWSURFACE)

        # fill with a color we can make transparent later
        label.fill((10, 10, 10))

        for x, y in ((0, 0), (1, 0), (2, 0), (0, 1), (2, 1), (0, 2), (1, 2), (2, 2)):
            # blit out the outline offset a few pixels
            label.blit(shadow, (x, y))

        # now blit out the actual text in the middle of the surface
        label.blit(maintext, (1, 1))

        # make blackish pixels transparent
        label.set_colorkey((10, 10, 10))

        # we're done, return our nice label
        return label
