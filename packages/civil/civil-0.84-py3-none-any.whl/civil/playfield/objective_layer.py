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
from pygame.locals import *

from civil import properties
from civil.model import scenario
from civil.constants import UNION, REBEL, UNKNOWN
from civil.playfield.location_layer import LocationLayer


class ObjectiveLayer(LocationLayer):
    """
    This class defines a layer that is used for showing all the objectives on the map. An objective
    will be drawn as a symbol on a hex. As there are relatively few objectives (normally) this layer
    is not a full surface, but instead single small icons are blitted out.

    Separate icons are used for when the objective is owned by union or rebel forces, or if the
    owner is unknown or neutral.

    Objectives are not painted withing hexes, i.e. their positions are exact pixel positions.

    NOTE: We are a subclass of LocationLayer, in the same way that Objectives are a subclass
    of Location. See self.getLocations()
    """

    def __init__(self, name):
        """
        Initializes the layer. Loads the icons for the objectives from files. If the loading fails
        the method will exit the application.
        """
        # call superclass constructor
        LocationLayer.__init__(self, name)

        self.icons = {}

        try:
            # load the icon for the objectives
            union = pygame.image.load(properties.layer_objective_icon_union).convert()
            rebel = pygame.image.load(properties.layer_objective_icon_rebel).convert()
            unknown = pygame.image.load(properties.layer_objective_icon_unknown).convert()

            # set the transparent color for the icons
            union.set_colorkey((255, 255, 255), RLEACCEL)
            rebel.set_colorkey((255, 255, 255), RLEACCEL)
            unknown.set_colorkey((255, 255, 255), RLEACCEL)

            # store in a hash for later access. Use the owner as the key
            self.icons[UNION] = union
            self.icons[REBEL] = rebel
            self.icons[UNKNOWN] = unknown

        except:
            # failed to load icons
            print("failed to load icons for objectives, exiting.")
            sys.exit(1)

    def getLocations(self):
        """
        Return which locations are valid for the layer, and the delta coordinates
        to apply for the label text. Because Objectives paint a star at
        the exact location, so the text must be slightl right and a lot down...
        """
        return {"locations": scenario.info.objectives, "delta_x": 16, "delta_y": 40}

    def paint(self, offset_x, offset_y, dirtyrect=None):
        """
        Paints the layer. Loops and blits out all objectives.
        """
        # get the tuple with the visible sizes and extract the x- and y-dimensions
        visible_x, visible_y = scenario.playfield.getVisibleSize()

        # precalculate the min and max possible x and y values
        min_x = (offset_x - 1) * self.delta_x
        max_x = (offset_x + visible_x + 1) * self.delta_x
        min_y = (offset_y - 1) * self.delta_y
        max_y = (offset_y + visible_y) * self.delta_y

        # loop over all objectives we have
        for obj in scenario.info.objectives:
            # get its position
            x, y = obj.getPosition()

            # is the objective visible currently?
            if min_x <= x <= max_x:
                if min_y <= y <= max_y:
                    # yep, it's visible so decide the icon to use
                    icon = self.icons[obj.getOwner()]

                    # yep, it's visible now perform the actual raw blit of the icon
                    scenario.sdl.blit(icon, (x - offset_x * self.delta_x, y - offset_y * self.delta_y))

        LocationLayer.paint(self, offset_x, offset_y, dirtyrect)
