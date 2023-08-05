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
import pygame.image

from civil import properties
from civil.model import scenario
from civil.playfield.layer import Layer


class WeaponInfoLayer(Layer):
    """
    This class defines a layer that plugs into the PlayField. It provides code for showing a dialog
    with info about a given weapon. The info includes all info that can be retrieved from the Weapon
    class. The user can using this dialog get a good idea as to what a weapon can do.

    To set the weapon this layer should show call 'setWeapon()'. This layer should be added among
    the last to the playfield, so that it is drawn on top over  everything else.
    """

    def __init__(self, name):
        """
        Initializes the layer.
        """
        # call superclass constructor
        Layer.__init__(self, name)

        # no labels yet
        self.labels = []

        # max width and default borders
        self.maxwidth = 100
        self.borderx = 15
        self.bordery = 15

        # set total height of the labels 
        self.totalheight = 50

        # load a button
        try:
            self.button = pygame.image.load(properties.layer_help_button).convert()
        except:
            # could not load the file
            print("Could not load: " + properties.layer_help_button + ", reason: " + repr(sys.exc_info()[1]))
            sys.exit(1)

    def setWeapon(self, weapon):
        """
        Sets the weapon whose info should be shown. This method will extract data from the weapon
        and generate labels from the data and display them. The labels are pygame labels for the
        texts and resize the dialog to fit the width and height of all the labels. They will be
        drawn justified to the left.
        """

        # no labels yet
        self.labels = []

        # extract data from the weapon
        tmplabels = self.extractData(weapon)

        # set default total height of the labels 
        self.totalheight = self.button.get_height() + self.bordery
        self.maxwidth = 100

        # load the font for the labels
        labelfont = pygame.font.Font(properties.layer_help_font,
                                     properties.layer_help_font_size)

        # loop over the global location labels we have
        for label in tmplabels:
            # create the surface and the shadow
            surface = labelfont.render(label, 1, properties.layer_help_color)

            # is this wider than the maximum width so far? We want to cache this here to avoid
            # having to loop all labels before painting
            if surface.get_width() > self.maxwidth:
                # yes, we have a new maximum width
                self.maxwidth = surface.get_width()

            # add to the total height of the labels 
            self.totalheight += surface.get_height()

            # store the label
            self.labels.append(surface)

    def extractData(self, weapon):
        """
        Extracts all known data about a weapon and creates strings from it. Creates a list with
        the labels and returns it.
        """

        # did we get a weapon at all?
        if weapon is None:
            # no weapon, return a default value
            return "Weapon information", " ", "Unit has no weapon"

        # add the known data
        return ("Weapon information",
                " ",
                "Name: %s" % weapon.getName(),
                "Type: %s" % weapon.getType(),
                "Max range: %d" % weapon.getRange(),
                "Damage: %d" % weapon.getDamage(),
                "Accuracy: %d" % weapon.getAccuracy())

    def paint(self, offset_x, offset_y, dirtyrect=None):
        """
        Paints the layer. Loops and blits out all labels. The offsets are used so that we know how
        much the map has been scrolled.
        """

        # get width and height of the area
        width = self.maxwidth + 2 * self.borderx
        height = self.totalheight + 2 * self.bordery

        # get starting position
        x = scenario.sdl.getWidth() / 2 - width / 2
        y = (scenario.sdl.getHeight() - self.totalheight) / 2

        # fill a part of the background with black so that we have something to paint on
        scenario.sdl.fill((0, 0, 0), (x - 1, y - 1, width + 2, height + 2))

        # paint the border first
        self.paintBorder(x, y, width, height)

        # add the borders before we start painting labels
        x += self.borderx
        y += self.bordery

        # loop over all labels we have
        for label in self.labels:
            # now blit out the label
            scenario.sdl.blit(label, (x, y))

            # increment height
            y += label.get_height()

        # get the button position
        buttonx = scenario.sdl.getWidth() / 2 - self.button.get_width() / 2
        buttony = y + 15

        # blit it out
        scenario.sdl.blit(self.button, (buttonx, buttony))
