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
import pygame.image
from pygame.locals import *

from civil import properties
from civil.model import scenario
from civil.constants import REBEL, UNION, INFANTRY, CAVALRY, ARTILLERY, HEADQUARTER
from civil.playfield.layer import Layer


class UnitLayer(Layer):
    """
    This class defines a base class for a layer that is used for showing all the units of the
    game. Both friendly and enemy units can be shown. A parameter to the constructor informs which
    units the layer draws.
    
    The icons for the units are in the static shared map 'icons'. There is one icon for each type of
    unit and for every 10 degrees facing and in 5 sizes. This makes it a total of 36*5*3 = 540
    icons. This map is shared among all instances of this class (static member).
    
    All friendly units are always shown, but only visible enemy units are shown. Each unit is drawn
    on the map using its own icon, which shows facing, size and type.

    Selected units are shown with a 'selection marker' under them.
    """

    # a map of the unit icons. It is organized in the following way. First there are 2 different
    # "sides", i.e. rebel and union. The map is indexed first with REBEL or UNION to get a map with
    # 4 map entries, the inf, cav, art and hq units. These maps contains 36 angles and finally 5 sizes
    icons = {REBEL: {},
             UNION: {}}

    # A map of the graphical unit icons (the nice-looking dudes :)
    picticons = {REBEL: {},
                 UNION: {}}

    # static icons for the selection markers. These is loaded only once and shared between all
    # instances of this class. The 'main' version is used for the primary selected unit, and 'extra'
    # for all 'slave' units
    selection_icon_main = None
    selection_icon_extra = None

    # a static strength icons
    strength = {}

    def __init__(self, name, player):
        """
        Initializes the layer.
        """
        # call superclass constructor
        Layer.__init__(self, name)

        # store the player
        self.player = player

        # by default we paint the nice icons and symbols
        self.paint_nice_guys = 1
        self.paint_symbols = 1

        try:

            # do we have a selection marker already loaded?
            if UnitLayer.selection_icon_main is None:
                # nope, so load it
                iconmain = pygame.image.load(properties.layer_unit_icon_main).convert()
                iconextra = pygame.image.load(properties.layer_unit_icon_extra).convert()

                # set the transparent colors for the icons
                iconmain.set_colorkey((255, 255, 255), RLEACCEL)
                iconextra.set_colorkey((255, 255, 255), RLEACCEL)

                # store them
                UnitLayer.selection_icon_main = iconmain
                UnitLayer.selection_icon_extra = iconextra

                # create the strength icons
                self.__createStrengthIcons()

                # load the icons too
                UnitLayer.icons[REBEL][INFANTRY] = self.__loadIcons("unit-type2")
                UnitLayer.icons[REBEL][CAVALRY] = self.__loadIcons("unit-type2")
                UnitLayer.icons[REBEL][ARTILLERY] = self.__loadIcons("unit-type2")
                UnitLayer.icons[REBEL][HEADQUARTER] = self.__loadIcons("unit-type2")

                # and union too
                UnitLayer.icons[UNION][INFANTRY] = self.__loadIcons("unit-type1")
                UnitLayer.icons[UNION][CAVALRY] = self.__loadIcons("unit-type1")
                UnitLayer.icons[UNION][ARTILLERY] = self.__loadIcons("unit-type1")
                UnitLayer.icons[UNION][HEADQUARTER] = self.__loadIcons("unit-type1")

                # The nice unit-pict-types :)
                # Rebel
                UnitLayer.picticons[REBEL][INFANTRY] = self.__loadPictIcons("unit-pict-type2")
                UnitLayer.picticons[REBEL][CAVALRY] = self.__loadPictIcons("unit-pict-type4", 2)
                UnitLayer.picticons[REBEL][ARTILLERY] = self.__loadPictIcons("unit-pict-type6", 2)
                UnitLayer.picticons[REBEL][HEADQUARTER] = self.__loadPictIcons("unit-pict-type8", 2)

                # Union
                UnitLayer.picticons[UNION][INFANTRY] = self.__loadPictIcons("unit-pict-type1")
                UnitLayer.picticons[UNION][CAVALRY] = self.__loadPictIcons("unit-pict-type3", 2)
                UnitLayer.picticons[UNION][ARTILLERY] = self.__loadPictIcons("unit-pict-type5", 2)
                UnitLayer.picticons[UNION][HEADQUARTER] = self.__loadPictIcons("unit-pict-type7", 2)

        except:
            # failed to load icon
            print("failed to load icons for unit layer, exiting.")
            raise

        # register ourselves to receive 'unitselected' signals
        scenario.dispatcher.registerCallback('unit_selected', self.unitSelected)

    def unitSelected(self, parameters):
        """
        Signal callback triggered when a unit has changed. Forces a repaint of the playfield.
        """
        scenario.playfield.needRepaint()

    def showUnitIcons(self, visible):
        """
        Sets the icon representation to be shown if 'visible' is 1 and hidden if 0.
        """
        self.paint_nice_guys = visible

    def showUnitSymbols(self, visible):
        """
        Sets the symbol representation to be shown if 'visible' is 1 and hidden if 0.
        """
        self.paint_symbols = visible

    def unitIconsShown(self):
        """
        Returns 1 if the icon representation is used and 0 if not.
        """
        return self.paint_nice_guys

    def unitSymbolsShown(self):
        """
        Returns 1 if the symbol representation is used and 0 if not.
        """
        return self.paint_symbols

    def paint(self, offset_x, offset_y, dirtyrect=None):
        """
        Paints the layer. Loops and blits out all units. The offsets are used so that we know how
        much the map has been scrolled.
        """

        # are any of the units shown?
        if self.paint_nice_guys == 0 and self.paint_symbols == 0:
            # no units should be shown, we're done here
            return

        # get the tuple with the visible sizes (in hexes)
        visible_x, visible_y = scenario.playfield.getVisibleSize()

        # precalculate the min and max possible x and y values
        min_x = offset_x * self.delta_x
        min_y = offset_y * self.delta_y
        max_x = (offset_x + visible_x) * self.delta_x
        max_y = (offset_y + visible_y) * self.delta_y

        # now paint the selection markers. These are painted before the actual unit so that they are
        # under the unit
        self.paintSelectionMarkers(min_x, max_x, min_y, max_y)

        # Unit graphical representation
        # Contains tuples of (icon, (x, y))
        nice_guys = []

        # strength icons
        # Contains tuples of (icon, (x,y))
        strengths = []

        # loop over all units in the map
        for unit in scenario.info.units.values():
            # is the unit visible
            if not unit.isVisible():
                # not visible, so don't paint either
                continue

            # get its position 
            unitx, unity = unit.getPosition()

            # is the unit visible on the playfield?
            if min_x <= unitx <= max_x and min_y <= unity <= max_y:
                # yes it it, get its icon
                owner = unit.getOwner()
                men = unit.getMen()

                # calculate the index for the size icon. we have 3 sizes, and the number of men
                # determines the icon index. the max index is thus 2. if the unit has 0-29 men the
                # smallest size is used, for 30-59 medium size and for 60+ the largest size
                index = min(2, men / 30)
                angle = unit.getFacing()
                icon = UnitLayer.icons[owner][unit.getType()][angle][int(index)]

                # calculate the half width/height of the icon, used for making sure the units are
                # painted with their midpoint on the exact position, not with their left upper
                # corner on the position 
                halfwidth = icon.get_width() / 2
                halfheight = icon.get_height() / 2

                # translate the unit position so that it is within the screen
                unitx -= (min_x + halfwidth)
                unity -= (min_y + halfheight)

                # are symbols used?
                if self.paint_symbols:
                    # yes, so perform the actual blitting of the icon
                    scenario.sdl.blit(icon, (unitx, unity))

                # are we painting the local player's units?
                if self.player == scenario.local_player_id:
                    # yep, calculate the strength index, ie. which icon to use
                    # 8.0 is no good, we only have 8 icons [0..7]
                    index = int(men / float(men + unit.getKilled()) * 7.9)

                else:
                    # we're painting the enemies, calculate the strength index, ie. which icon to
                    # use. use a more coarse icon scheme here
                    # 4.0 is no good, we only have 8 icons [0..7]
                    index = int(men / float(men + unit.getKilled()) * 3.9) * 2

                # Decide where to paste the nice graphical unit
                if self.paint_nice_guys:

                    # ASSUME
                    # l != 10 means we only have right/left guys
                    # Otherwise, we try to paint formations
                    l = len(list(UnitLayer.picticons[owner][unit.getType()].keys()))

                    # TODO: for python2.2 we want the // version, as / will be converted
                    # to "real" division in the future, not just integer division. so as soon as 2.2
                    # can be safely used we should use the // version. there are a few others in
                    # this same file too.
                    #
                    # Already changed, 2.2 can be assumed to be standard now.

                    # if index <= len(UnitLayer.strength) / 3 or l != 10:
                    if index <= len(UnitLayer.strength) // 3 or l != 10:
                        #
                        # Unit is so weak it should be shown as one
                        #
                        i = 2  # Default left
                        if angle < 18:
                            # Right
                            i = 1
                    else:
                        #
                        # Show stuff with three units
                        #

                        # Map the angle to one of
                        # (this is static and constant, could be moved outside)
                        unit_three_face_mapping = [5, 9, 10, 7, 8, 4, 3, 6]
                        #
                        # 36 angles mapped to 8 faces.
                        # 36/8 == 4.5
                        #
                        # Magic offset
                        # angle += int (4.5/2)
                        angle += 4.5 // 2
                        if angle >= 36:
                            angle -= 36

                        # Calculate the actual facing
                        # i = int(angle / 4.5)
                        i = int(angle // 4.5)

                        # And map it to get the right icon
                        i = unit_three_face_mapping[i]

                    # BUG: really bad offsets. :(

                    nice_icon = UnitLayer.picticons[owner][unit.getType()][i]

                    nx, ny = unit.getPosition()
                    nx -= (min_x + nice_icon.get_width() / 2)

                    # BUG: why the -13 ? Should center nicely without, but...
                    ny -= (min_y + nice_icon.get_height() - 13)
                    nice_guys.append((nice_icon, (nx, ny)))

                # now paint the strength bar
                # Perhaps these should also be painted afterwards?
                y = unity
                if self.paint_nice_guys:
                    # Nice guys take up space, move strength bar up
                    y = ny - 1
                strengths.append((UnitLayer.strength[index], (unitx + halfwidth, y)))

        if self.paint_nice_guys:
            # Paste the nice graphical representations
            for (icon, xy) in nice_guys:
                scenario.sdl.blit(icon, xy)

        # Paint strength bars last so we can see them
        for (icon, xy) in strengths:
            scenario.sdl.blit(icon, xy)

    def paintSelectionMarkers(self, min_x, max_x, min_y, max_y):
        """
        Paints all the selection markers that are for selected units within the currently visible
        are of the map. This method should be called before painting the units so that the markers


 """

        first = 1

        # get the icon
        iconmain = UnitLayer.selection_icon_main
        iconextra = UnitLayer.selection_icon_extra

        # get the half width and height of the icon
        halfwidth = iconmain.get_width() / 2
        halfheight = iconmain.get_height() / 2

        # loop over all units in the map
        for selected in scenario.selected:
            # is this one of this layer's units?
            if selected.getOwner() != self.player:
                # not same owner, go away and do next unit
                continue

            # get the unit position
            unitx, unity = selected.getPosition()

            # is the unit visible on the playfield?
            if min_x <= unitx <= max_x and min_y <= unity <= max_y:
                # translate the position so that it is within the screen
                unitx -= (min_x + halfwidth)
                unity -= (min_y + halfheight)

                # now perform the actual blitting with the correct icon
                if first:
                    # use main icon
                    scenario.sdl.blit(iconmain, (unitx, unity))
                else:
                    # use extra icon
                    scenario.sdl.blit(iconextra, (unitx, unity))

                # not first unit anymore
                first = 0

    def __loadPictIcons(self, type, amount=10):
        """
        Load the nice-looking graphical unit representation.
        """
        h = {}
        for i in range(1, amount + 1):
            file_name = os.path.join(properties.path_units, '%s-%03d.png' % (type, i))
            icon = self.__loadIconAndConvert(file_name)
            h[i] = icon

        return h

    def __loadIcons(self, type):
        """
        Loads icons for the units of 'type', where the given type is the string representation of
        the type of the unit. This method will loop over all 36 angles * 3 sizes for the given type
        and load 108 icons. A map which has the 36 facings as keys and a list of three sizes as the
        values is returned.
        """

        # create the map we'll ultimately return. It is the map of all sizes
        icons = {}

        # the valid sizes
        sizes = ('s', 'm', '')

        # loop over all angles from 0 to 35. These should be multiplied by 10 to get the real angle.
        for angle in range(1, 37):

            # make a default empty list
            icons[angle - 1] = []

            # loop over the three sizes
            for size in range(3):
                # create the file_name based on the angle
                file_name = os.path.join(properties.path_units, '%s%s-%03d.png' % (type, sizes[size], angle))

                # load icon
                icons[angle - 1].append(self.__loadIconAndConvert(file_name))

        # return the map
        return icons

    def __createStrengthIcons(self):
        """
        Creates icons for use as strength bars. The icons will be 3 (from properties) pixels high
        and have widths from 4 pixels up to 16 pixels in 2 pixel increments. The icons are stored
        locally. This means that we have 8 strength icons.
        """

        # get the height and color
        height = properties.layer_unit_strength_height

        index = 0

        # loop over all the valid sizes
        for width in range(4, 20, 2):
            # create a new surface with the given width
            surface = pygame.Surface((width, height), HWSURFACE)

            if width < 9:
                color = properties.layer_unit_strength_color_poor
            elif width < 15:
                color = properties.layer_unit_strength_color_good
            else:
                color = properties.layer_unit_strength_color_excellent

            # fill it with the color
            surface.fill(color)

            # draw black rectangle around it, so it won't blurred with the background too much
            pygame.draw.rect(surface, (0, 0, 0), (0, 0, width, height), 1)

            # and store it in our shared dictionary
            UnitLayer.strength[index] = surface

            index += 1

    def __loadIconAndConvert(self, file_name):
        """
        Load a picture, set the pure white color to transparent, and return it in an optimized
        format. This routine could be moved to some generic place.
        """

        # load it and set the transparent color (white)
        newicon = pygame.image.load(file_name)
        newicon.set_colorkey((255, 255, 255), RLEACCEL)

        # convert to our more efficient format and return
        return newicon.convert()
