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
import pygame.image

from civil import properties
from civil.model import scenario
from civil.playfield.layer import Layer


class LocationLayer(Layer):
    """
    This class defines a layer that plugs into the PlayField. It provides code for drawing various
    locations as labels on the map. The labels can be for various parts of the map, such as geographical
    features, objectives etc.

    A simple text label is rendered using a font given in the properties file, and painted on the
    map when the layer is painted.
    """

    def __init__(self, name):
        """
        Initializes the layer.
        """
        # call superclass constructor
        Layer.__init__(self, name)

        # setup all labels
        self.createLabels()

    def getLocations(self):
        """
        Returns which locations are valid, and what delta coordinates
        to apply. See also ObjectiveLayer.getLocations().
        """
        return {"locations": scenario.info.locations, "delta_x": 0, "delta_y": 0}

    def createLabels(self):
        """
        Creates all labels. This loops over the labels that were parsed from the scenario file
        and creates tuples into an internal list self.labels. The tuples are of the form
        (x,y,surface) where the surface is the SDL surface ready for blitting out.
        """
        # no labels yet
        self.labels = []

        # load the font for the labels
        labelfont = pygame.font.Font(properties.layer_locations_font,
                                     properties.layer_locations_font_size)

        # loop over the global location labels we have
        h = self.getLocations()
        for location in h["locations"]:
            # create the surface and the shadow
            surface = labelfont.render(location.getName(), 1, properties.layer_locations_color)
            shadow = labelfont.render(location.getName(), 1, properties.layer_locations_shadow)

            # get the position of the label
            x, y = location.getPosition()

            # offset the x and y a little bit so that they get where the middle of the label is, not
            # the left upper corner
            mylabel = pygame.Surface((surface.get_width() + 2, surface.get_height() + 2))
            mylabel.fill((0, 0, 0))

            mylabel.blit(shadow, (0, 0))
            mylabel.blit(shadow, (2, 0))
            mylabel.blit(shadow, (0, 2))
            mylabel.blit(shadow, (2, 2))
            mylabel.blit(surface, (1, 1))

            mylabel.set_colorkey((0, 0, 0), pygame.RLEACCEL)

            x -= mylabel.get_width() / 2
            y -= mylabel.get_height() / 2

            x += h["delta_x"]
            y += h["delta_y"]
            # store the label along with the coordinates. We store them as a tuple
            self.labels.append((x, y, mylabel))

    def paint(self, offset_x, offset_y, dirtyrect=None):
        """
        Paints the layer. Loops and blits out all labels. The offsets are used so that we know how
        much the map has been scrolled.
        """

        # get the tuple with the visible sizes (in hexes) and the current offset (in hexes)
        visible_x, visible_y = scenario.playfield.getVisibleSize()

        # precalculate the min and max possible x and y values
        min_x = offset_x * self.delta_x
        min_y = offset_y * self.delta_y
        max_x = (offset_x + visible_x) * self.delta_x
        max_y = (offset_y + visible_y) * self.delta_y

        # loop over all labels we have
        for labelx, labely, surface in self.labels:

            # is the label visible on the playfield?
            if labelx >= min_x and labelx <= max_x and labely >= min_y and labely <= max_y:
                # yep, translate the position so that it is within the screen
                labelx -= min_x
                labely -= min_y

                # now blit out the actual text in the middle of the outline
                scenario.sdl.blit(surface, (labelx, labely))
