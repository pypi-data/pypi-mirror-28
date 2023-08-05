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

import os

import pygame

from civil import properties
from civil.model import scenario
from civil.ui.messages import AUDIO
from civil.playfield.floating_window_layer import FloatingWindowLayer
from civil.playfield.layer import Layer


class AudioLayer(FloatingWindowLayer):
    """
    This class defines a layer that contains the audio controls. It's a small floating dialog
    that contains all needed controls for the player to control playback of the background
    music. The player can control weather to:

    * play the builtin music
    * play music from an audio cd
    * no music at all

    It also contains controls for managing CD playback, ie. the tracks can be selected and playback
    can be paused/stopped.

    The state Audio controls this layer.

    This layer is a floating window layer, which means it can be dragged around the map.
    """

    def __init__(self, name):
        """
        Initializes the layer.
        """
        # call superclass constructor
        FloatingWindowLayer.__init__(self, name)

        # load all icons
        self.play = pygame.image.load(os.path.join(properties.path_dialogs, "butt-play-moff.png")).convert()
        self.stop = pygame.image.load(os.path.join(properties.path_dialogs, "butt-stop-moff.png")).convert()
        self.pause = pygame.image.load(os.path.join(properties.path_dialogs, "butt-pause-moff.png")).convert()
        self.next = pygame.image.load(os.path.join(properties.path_dialogs, "butt-fastforward-moff.png")).convert()
        self.prev = pygame.image.load(os.path.join(properties.path_dialogs, "butt-rewind-moff.png")).convert()
        self.eject = pygame.image.load(os.path.join(properties.path_dialogs, "butt-eject-moff.png")).convert()

        # load the font and set its properties. use the same font as the dialog layer does
        font = pygame.font.Font(properties.layer_dialog_font, properties.layer_dialog_font_size)

        # render the labels we'll need
        self.labels = [font.render("Included music", 1, properties.layer_dialog_color),
                       font.render("No music", 1, properties.layer_dialog_color),
                       font.render("CD", 1, properties.layer_dialog_color)]

        # get width of the drawn border
        borderw, borderh = self.getBorderWidth()

        # and the icon dimensions. we assum they're all of similar size
        self.iconwidth = self.play.get_width()
        self.iconheight = self.play.get_height()

        # some spacing between icons
        self.spacing = 5

        # set the margins we use from the origin. this gives some padding to the border
        self.margin_x = 10
        self.margin_y = 10

        # the area must fit 6 icons with a total of 8 spacings (2 border, 5 between, 1 extra for eject)
        self.width = 1 * self.margin_x + \
                     4 * self.iconwidth + \
                     6 * self.spacing + \
                     1 * self.margin_x

        # create the height. Note that we have no margin above the checkboxes, and they are heigh
        # enough to contain the needed margin
        self.height = 3 * (Layer.checkbox[0].get_height() - 15) + \
                      2 * self.spacing + \
                      1 * self.iconheight + \
                      1 * self.margin_y

        # set default position
        self.x = (scenario.sdl.getWidth() - self.width) / 2
        self.y = scenario.sdl.getHeight() - self.height - borderh - 5

        # what is clicked by default?
        self.selected = 0

        # a dictionary for the coordinates and another for callbacks
        self.coordinates = {}
        self.callbacks = {'stop': self.stopCD,
                          'play': self.playCD,
                          'prev': self.prevCD,
                          'next': self.nextCD,
                          'eject': self.ejectCD}

        # callbacks for the checkboxes. the callbacks are in the same order as the checkboxes
        self.cb_callbacks = [self.playIncluded, self.playNothing, self.playFromCD]

    def handleContentsClick(self, x, y):
        """
        This callback is activated if the player clicks within the contents area, ie. inside the
        borders. This callback will see if any of the buttons was pressed, and if so, do the
        nevessary action. If one of the checkboxes is clicked then the type of played music is
        changed, and if CD playing is enabled then the lower row of CD control buttons is checked too.
        """

        # create coordinates for the checkboxes. we don't have the coordinates for them stored anywhere,
        # so we need to do it this way and "recreate" the rendering
        buttonx1 = self.margin_x
        buttonx2 = buttonx1 + Layer.checkbox[0].get_width()
        buttony1 = 0
        checkheight = Layer.checkbox[0].get_height()

        # translate the x and y coordinates of the click th be within the window
        x -= self.x
        y -= self.y

        # loop over the three checkboxes
        for index in range(3):
            # lower y coordinate of the current button
            buttony2 = buttony1 + checkheight - 15

            # was the click inside this button? if the checkbox is already selected, so we couldn't
            # do any good to activate it again, get out of the loop. note that we don't use the full
            # height for the checkboxes when checking the y coordinate, as they are a bit too high,
            # and partially overlap
            if buttonx1 <= x <= buttonx2 and buttony1 <= y <= buttony2 and index != self.selected:
                # yep, this is it
                self.selected = index

                # call the callback
                self.cb_callbacks[index]()

                # repaint the playfield
                scenario.playfield.needInternalRepaint(self)
                break

            # add to the y coordinate
            buttony1 += checkheight - 15

        # loop over the buttons
        for buttonname in list(self.coordinates.keys()):
            # get the coordinates for this button
            bx, by, bw, bh = self.coordinates[buttonname]

            # is the button hit?
            if bx <= x <= bx + bw and by <= y <= by + bh:
                # yes, inside, call the callback
                self.callbacks[buttonname]()

                # we're done
                break

        # we were handled all right
        return 1

    def paint(self, offset_x, offset_y, dirtyrect=None):
        """
        Paints the layer. Blits out the surfaces for the minimap surrounded by a border.
        """
        # are we minimized?
        if self.isMinimized():
            # yes, paint just the minimized layer, no content, and then go away
            self.paintBorderMinimized(self.x, self.y, self.width)
            return

        # fill the background with black so that we have something to paint on
        scenario.sdl.fill((0, 0, 0), (self.x - 1, self.y - 1, self.width + 2, self.height + 2))

        # paint the border first
        self.paintBorder(self.x, self.y, self.width, self.height)

        # get the upper left corner of the contents area. saves some typing. this includes the
        # spacing above and to the left of the icons
        x = self.x + self.margin_x
        y = self.y  # + self.margin_y

        # width and height of a checkbox
        checkwidth = Layer.checkbox[0].get_width()
        checkheight = Layer.checkbox[0].get_height()
        buttonwidth = self.play.get_width()
        buttonheight = self.play.get_height()

        # loop over the three labels
        for index in range(3):
            # is this checkbox selected?
            if index == self.selected:
                # this one is checked
                use = 1
            else:
                # nope, draw an unchecked
                use = 0

            # create coordinates for exactly where it will be put. we can later use these coordinates to
            # easily check weather a checkbox got clicked
            check_x1 = x
            check_y1 = y
            check_x2 = x + checkwidth + self.spacing

            # get the label associated with the checkbox
            label = self.labels[index]

            # we need some extra offset to the y for the label to align it nicely with the
            # checkbox. 
            extray = checkheight / 2 - label.get_height() / 2

            # do the blit of the checkbox and the label. also 
            scenario.sdl.blit(Layer.checkbox[use], (check_x1, check_y1))
            scenario.sdl.blit(label, (check_x2 + self.spacing, check_y1 + extray))

            # add to the y coordinate
            y += checkheight - 15

        # add some more spacing before the buttons
        y += 2 * self.spacing

        # draw out the buttons, first the play/stop button
        if scenario.audio.isPlayingCD():
            # we're playing at the moment, so we want to show the stop button
            scenario.sdl.blit(self.stop, (x, y))
        else:
            # not playing, show the play button
            scenario.sdl.blit(self.play, (x, y))

        # draw the rest
        scenario.sdl.blit(self.prev, (x + buttonwidth * 1 + self.spacing * 2, y))
        scenario.sdl.blit(self.next, (x + buttonwidth * 2 + self.spacing * 3, y))
        scenario.sdl.blit(self.eject, (x + buttonwidth * 3 + self.spacing * 5, y))

        # do we already have the coordinates stored?
        if self.coordinates == {}:
            # no coordinates, store them for later use. the coordinates are stored as relative to the window
            # position
            self.coordinates['stop'] = (x - self.x, y - self.y, buttonwidth, buttonheight)
            self.coordinates['play'] = (x - self.x, y - self.y, buttonwidth, buttonheight)
            self.coordinates['prev'] = (x - self.x + buttonwidth * 1 + self.spacing * 2, y - self.y,
                                        buttonwidth, buttonheight)
            self.coordinates['next'] = (x - self.x + buttonwidth * 2 + self.spacing * 3, y - self.y,
                                        buttonwidth, buttonheight)
            self.coordinates['eject'] = (x - self.x + buttonwidth * 3 + self.spacing * 5, y - self.y,
                                         buttonwidth, buttonheight)

    def stopCD(self):
        """
        Callback triggered when the player clicks the 'stop' button. Stops playing CD music if it
        is playing. Does nothing if the CD is not used.
        """
        # do we have the CD checkbox selected? if not we don't use this button at all
        if self.selected != 2:
            # not in cd mode, go away
            return

        # this is a little bit of a hack. the 'stop' button is first in the callback list, so it
        # always gets called even if 'play' is actually clicked, as the buttons are painted on the
        # same place. So, if we're not playing cd audio at the moment we'll jump to the 'play'
        # callback instead
        if not scenario.audio.isPlayingCD():
            # not playing, so go run play instead
            self.playCD()
            return

        # stop playing
        scenario.audio.stopCD()

        # repaint the playfield to refresh the buttons
        scenario.playfield.needInternalRepaint(self)

    def playCD(self):
        """
        Callback triggered when the player clicks the 'play' button. Starts playing music from
        the CD if CD audio is enabled, or does nothing if it's not.
        """
        # do we have the CD checkbox selected? if not we don't use this button at all
        if self.selected != 2:
            # not in cd mode, go away
            return

        # start playing
        scenario.audio.playCD()

        # repaint the playfield to refresh the buttons
        scenario.playfield.needInternalRepaint(self)

    def prevCD(self):
        """
        Callback triggered when the player clicks the 'prev' button. Skips one track backward if
        CD audio is enabled, or does nothing if it's not
        """
        # do we have the CD checkbox selected? if not we don't use this button at all
        if self.selected != 2:
            # not in cd mode, go away
            return

        print("AudioLayer.prev")

    def nextCD(self):
        """
        Callback triggered when the player clicks the 'next' button. Skips one track forward if
        CD audio is enabled, or does nothing if it's not
        """
        # do we have the CD checkbox selected? if not we don't use this button at all
        if self.selected != 2:
            # not in cd mode, go away
            return

        print("AudioLayer.next")

    def ejectCD(self):
        """
        Callback triggered when the player clicks the 'eject' button. This will always try to
        eject the CD tray, regardless if there is a CD or not. If music is being played from the CD
        then it is stopped first. Note that this method can always be called, no matter if we're
        currently playing background music or no music at all.
        """
        # just eject the cd. this method may fail to do the ejecting
        scenario.audio.ejectCD()

        scenario.messages.add("No background music", AUDIO)

    def playIncluded(self):
        """
        Starts playing the included background music if it is available.
        """
        # just play it if we have it
        scenario.audio.stopCD()
        scenario.audio.playMusic()

        scenario.messages.add("Playing background music", AUDIO)

    def playNothing(self):
        """
        Plays no background music at all. Stops playing from CD if available and also stops the
        background music.
        """
        # stop cd and audio. we don't need to bother about checking weather they are played at all,
        # that's done by the methods themselves
        scenario.audio.stopMusic()
        scenario.audio.stopCD()

        scenario.messages.add("No background music", AUDIO)

    def playFromCD(self):
        """
        Checks weather we have an audio CD in the drive and if so plays it.
        """
        # do we have an audio cd?
        if not scenario.audio.hasAudioCD():
            # no audio cd
            scenario.messages.add("No audio CD in the drive", AUDIO)
            return

        # stop the music first
        scenario.audio.stopMusic()

        # start playing
        scenario.audio.playCD()

        scenario.messages.add("Playing CD background music", AUDIO)
