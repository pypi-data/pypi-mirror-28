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

from civil import properties
from civil.model import scenario
from civil.playfield.floating_window_layer import FloatingWindowLayer


class UnitInfoViewLayer(FloatingWindowLayer):
    """
    This class defines a layer that shows various info in a window. The information is:

    o all known info about a current unit. If friendly it shows all unit data.
    o weapon info for the current unit.
    o commander info.
    o the current time.
    o a button that can be clicked to popup a menu.

    The time is always shown, even if no unit is selected.

    This class has a callback for the following signals:

         o unit_selected
         o units_changed
         
    This layer is a floating window layer, which means it can be dragged around the map.
    """

    def __init__(self, name):
        """
        Initializes the layer.
        """
        # call superclass constructor
        FloatingWindowLayer.__init__(self, name)

        # register ourselves to receive 'unitselected' signals
        scenario.dispatcher.registerCallback('unit_selected', self.unitSelected)
        scenario.dispatcher.registerCallback('units_changed', self.unitsChanged)
        scenario.dispatcher.registerCallback('unit_destroyed', self.unitDestroyed)

        # load the font for all the info
        self.hdg_font = pygame.font.Font(properties.layer_unit_info_font_name,
                                         properties.layer_unit_info_heading_font_size)
        self.info_font = pygame.font.Font(properties.layer_unit_info_font_name,
                                          properties.layer_unit_info_main_font_size)

        # no labels yet
        self.labels = []

        # no shown unit yet
        self.shown_unit = None

        # set the margins we use from the origin. this gives some padding to the border
        self.margin_x = 10
        self.margin_y = 5

        # get the border dimensions
        borderw, borderh = self.getBorderWidth()

        # set default dimensions. we want to take the border into account and then also leave a few
        # pixels space before the edges. makes it a bit more "airy"
        self.width = 340
        self.height = 135
        self.x = borderw + 5
        self.y = scenario.sdl.getHeight() - borderh - self.height - 5

        # no offset yet
        self.offset = 0

        # create the game time font and letters
        self.createGameTime()

        # create static labels
        self.createStaticLabels(self.info_font)

        # load the icon for the waypoint
        self.menu_icon = pygame.image.load(properties.layer_unit_info_menu_button).convert()

        # register ourselves to receive 'time_changed' signals
        scenario.dispatcher.registerCallback('time_changed', self.timeChanged)

    def timeChanged(self, parameters):
        """
        Signal callback triggered when the time has changed. Forces a repaint of at least this layer.
        """

        # we need a repaint
        scenario.playfield.needRepaint()

    def paint(self, offset_x, offset_y, dirtyrect=None):
        """
        Paints the layer. Blits out the orders for the unit surrounded by a border. If the
        selected unit is an enemy unit then no orders are shown.
        """
        # are we minimized?
        if self.isMinimized():
            # yes, paint just the minimized layer, no content, and then go away
            self.paintBorderMinimized(self.x, self.y, self.width)
            return

        # fill a part of the background with black so that we have something to paint on
        scenario.sdl.fill((0, 0, 0), (self.x - 1, self.y - 1, self.width + 2, self.height + 2))

        # paint the border first
        self.paintBorder(self.x, self.y, self.width, self.height)

        # start from our top-level position
        x = self.x + self.margin_x
        y = self.y + self.margin_y

        # paint the menu button. first get the position
        menux, menuy = properties.layer_unit_info_menu_pos

        # and do the blit
        scenario.sdl.blit(self.menu_icon, (x + menux, y + menuy))

        # loop over all labels 
        for label, pos in self.labels:
            # explode the position
            lx, ly = pos

            # and do the blit
            scenario.sdl.blit(label, (x + lx, y + ly))

        # paint the time display too
        self.paintTime()

        # the rest is only blitted for friendly unit
        if self.shown_unit is None or self.shown_unit.getOwner() != scenario.local_player_id:
            # enemy unit
            return

        # loop over all static precreated labels
        for label, pos in self.static_labels:
            # explode the position
            lx, ly = pos

            # and do the blit
            scenario.sdl.blit(label, (x + lx, y + ly))

    def isMenuButtonClicked(self, position):
        """
        Checks weather the menu button in the upper right corner is pressed. Returns 1 if it is
        and 0 if not.
        """

        # ok, is the layer even visible?
        if not self.isVisible():
            # not visible, so menu can't be clicked either
            return 0

        # explode the positions
        x, y = position
        mx, my = properties.layer_unit_info_menu_pos

        mx += self.x + self.margin_x
        my += self.y + self.margin_y

        # ok, inside or not?
        if mx <= x <= mx + self.menu_icon.get_width() and my <= y <= my + self.menu_icon.get_height():
            # inside
            return 1

        # outside
        return 0

    def paintTime(self):
        """
        Paints the time as a series of separate letters.
        """

        # get the hour, minute and second
        date = scenario.info.getCurrentDate()
        hourtmp = date.hour
        mintmp = date.minute
        sectmp = date.second

        # split up the hours an minutes in 10:s and 1:s
        hour10 = hourtmp // 10
        hour1 = hourtmp % 10
        min10 = mintmp // 10
        min1 = mintmp % 10
        sec10 = sectmp // 10
        sec1 = sectmp % 10

        # get the five needed icons
        hour10icon = self.letters[hour10]
        hour1icon = self.letters[hour1]
        min10icon = self.letters[min10]
        min1icon = self.letters[min1]
        sec10icon = self.letters[sec10]
        sec1icon = self.letters[sec1]
        colonicon = self.letters[10]

        # get the x and y-coordinates of where we start painting the labels
        x, y = properties.layer_unit_info_time_pos

        # add our offsets and margins
        x += self.x + self.margin_x
        y += self.y + self.margin_y

        # blit out the tens of hours icon and add to the x coordinate
        scenario.sdl.blit(hour10icon, (x, y))
        x += hour10icon.get_width()

        # blit out the single hour icon and add to the x coordinate
        scenario.sdl.blit(hour1icon, (x, y))
        x += hour1icon.get_width()

        # blit out the colon and add to the x coordinate
        scenario.sdl.blit(colonicon, (x, y))
        x += colonicon.get_width()

        # blit out the tens of mins icon and add to the x coordinate
        scenario.sdl.blit(min10icon, (x, y))
        x += min10icon.get_width()

        # blit out the single min icon and add to the x coordinate
        scenario.sdl.blit(min1icon, (x, y))
        x += min1icon.get_width()

        # blit out the colon and add to the x coordinate
        scenario.sdl.blit(colonicon, (x, y))
        x += colonicon.get_width()

        # blit out the tens of secs icon and add to the x coordinate
        scenario.sdl.blit(sec10icon, (x, y))
        x += sec10icon.get_width()

        # blit out the single sec icon and add to the x coordinate
        scenario.sdl.blit(sec1icon, (x, y))
        x += sec1icon.get_width()

    def createGameTime(self):
        """
        Creates the data needed for displaying the current time. Loads the needed font and
        renders some characters. Each needed character: 0 to 9 and : are rendered into a dictionary
        and stored for later use.
        """

        # load a font
        font = pygame.font.Font(properties.textfont, 14)

        # start with an empty map
        self.letters = []

        # loop over all numbers from 0 to 9, as well as ':'
        for text in ("0", "1", "2", "3", "4", "5", "6", "7", "8", "9", ":"):
            # create and append a new surface
            self.letters.append(font.render(text, 1, (255, 255, 255)))

    def unitSelected(self, parameters):
        """
        Callback triggered when a new unit has been selected. This updates the orders data for
        the unit if it's a friendly unit. For enemy units nothing is shown. The orders are rendered
        as a set of labels, one label for each order.
        """

        # clear the orders
        self.labels = []

        # get the unit, it may be none to indicate that no unit is selected
        self.shown_unit = parameters

        # create new labels
        self.createLabels(self.shown_unit)

        scenario.playfield.needInternalRepaint(self)

    def unitsChanged(self, parameters):
        """
        Callback triggered when an unit has been changed. This updates the orders data for
        the currently selected unit if it is among the changed units. If it is not there then
        nothing will be done.
        """

        # is our unit among the changed?
        if not self.shown_unit in parameters:
            # nah, go away
            return

        # yes, it has changed, update all orders labels for it. send the unit we show as a parameter
        self.unitSelected(self.shown_unit)

        scenario.playfield.needInternalRepaint(self)

    def unitDestroyed(self, parameters):
        """
        Callback triggered when an unit has been destroyed. If the view was showing the destroyed
        unit then the view is cleared.
        """
        # did our unit get destroyed?
        if self.shown_unit in parameters:
            # yep, it's there, don't show uit anymore
            self.shown_unit = None

            # no labels anymore
            self.labels = []

            # we need an internal repaint of ourselves
            scenario.playfield.needInternalRepaint(self)

    def createLabels(self, unit):
        """
        Creates new labels for showing the unint info if needed. Creates different labels if no
        unit is selected, or an own or an enemy unit is selected. Populates the internal list
        self.labels with tuples (label, (x,y)), where label is the prerendered SDL label, and (x,y)
        is the position for the label. The is quite ugly, but makes for more readable code
        elsewhere.
        """

        # no labels for now
        self.labels = []

        # do we have a unit at all?
        if unit is None:
            # nope, so nothing to create
            return

        # cache the font 
        font1 = self.info_font
        font2 = self.hdg_font

        # create label for name, type and mode
        name = font2.render(unit.getName(), 1, properties.layer_unit_info_font_name_color)
        type = font2.render(unit.getTypeString(), 1, properties.layer_unit_info_font_type_color)
        mode = font2.render(unit.getMode().getTitle(), 1, properties.layer_unit_info_font_mode_color)

        # add them too
        self.labels.append((name, properties.layer_unit_info_name_pos))
        self.labels.append((type, properties.layer_unit_info_type_pos))

        # for the 'mode' we need to put it to the right of the 'type' label
        x, y = properties.layer_unit_info_type_pos

        # now add it too
        self.labels.append((mode, (x + type.get_width() + 20, y)))

        if unit.getOwner() != scenario.local_player_id:
            # enemy unit
            return

        # it's an own unit, create extra labels not shown for enemy units. First get the numeric
        # values for the unit modifiers
        mor = unit.getMorale().getValue()
        exp = unit.getExperience().getValue()
        fat = unit.getFatigue().getValue()
        men = unit.getMen()
        killed = unit.getKilled()

        # get the colors too
        color = properties.layer_unit_info_font_color
        weaponcolor = properties.layer_unit_info_font_weapon_color
        statuscolors = properties.layer_unit_info_font_status_colors

        # number of men and total
        x, y = properties.layer_unit_info_men_pos
        self.labels.append((font1.render('%d / %d' % (men, men + killed), 1, color),
                            (x + 50, y)))

        # create the labels that depend on modifier status. we get the start of the label (where the
        # static info part starts) and add a little x offset. we also use a custom color for the label
        x, y = properties.layer_unit_info_morale_pos
        self.labels.append((font1.render('%s (%d)' % (unit.getMorale().toString(), mor),
                                         1, statuscolors[unit.getMorale().getStatus()]),
                            (x + 50, y)))

        x, y = properties.layer_unit_info_fatigue_pos
        self.labels.append((font1.render('%s (%d) ' % (unit.getFatigue().toString(), fat),
                                         1, statuscolors[unit.getFatigue().getStatus()]),
                            (x + 50, y)))

        x, y = properties.layer_unit_info_experience_pos
        self.labels.append((font1.render('%s (%d)' % (unit.getExperience().toString(), exp),
                                         1, statuscolors[unit.getExperience().getStatus()]),
                            (x + 50, y)))

        # data for the terrain info
        x, y = properties.layer_unit_info_terrain_pos
        terrain_type = scenario.map.getTerrain(unit.getPosition()).getType()

        self.labels.append((font1.render('%s' % terrain_type, 1, properties.layer_unit_info_font_mode_color),
                            (x + 50, y)))

        # add a label for the headquarter status of the unit
        # self.createHqLabel ( name.get_width (), font2, properties.layer_unit_info_font_name_color )

        # get the commander of the unit
        cmdr = unit.getCommander()
        exp = cmdr.getExperience().getValue()
        agg = cmdr.getAggressiveness().getValue()
        rally = cmdr.getRallySkill().getValue()
        mot = cmdr.getMotivation().getValue()

        # render the commander labels. we get the start of the label (where the static info part
        # starts) and add a little x offset
        self.labels.append((font2.render(cmdr.getName(), 1, properties.layer_unit_info_font_name_color),
                            properties.layer_unit_info_cmdr_name_pos))

        x, y = properties.layer_unit_info_cmdr_exp_pos
        self.labels.append((font1.render('%s (%d)' % (cmdr.getExperience().toString(), exp),
                                         1, color), (x + 50, y)))

        x, y = properties.layer_unit_info_cmdr_agg_pos
        self.labels.append((font1.render('%s (%d)' % (cmdr.getAggressiveness().toString(), agg),
                                         1, color), (x + 50, y)))

        x, y = properties.layer_unit_info_cmdr_rally_pos
        self.labels.append((font1.render('%s (%d)' % (cmdr.getRallySkill().toString(), rally),
                                         1, color), (x + 50, y)))

        x, y = properties.layer_unit_info_cmdr_motivation_pos
        self.labels.append((font1.render('%s (%d)' % (cmdr.getMotivation().toString(), mot),
                                         1, color), (x + 50, y)))

        # get the weapon of the unit
        weapon = unit.getWeapon()
        ok, destroyed = unit.getWeaponCounts()

        # render the weapon labels. we get the start of the label (where the static info part
        # starts) and add a little x offset
        x, y = properties.layer_unit_info_weapon_name_pos
        self.labels.append((font1.render(weapon.getName(), 1, weaponcolor), (x + 50, y)))

        x, y = properties.layer_unit_info_weapon_range_pos
        self.labels.append((font1.render(str(weapon.getRange()), 1, weaponcolor), (x + 50, y)))

        x, y = properties.layer_unit_info_weapon_num_pos
        self.labels.append((font1.render('%d / %d' % (ok, destroyed), 1, weaponcolor), (x + 50, y)))

    def createStaticLabels(self, font):
        """
        Creates a series of static labels and stores them in a list along with the position they
        should be blitted out. Each element is a tuple (label,x,y).
        """
        # no labels yet
        self.static_labels = []

        # get the colors too
        color = properties.layer_unit_info_font_color
        weaponcolor = properties.layer_unit_info_font_weapon_color

        # create the static unit info labels
        self.static_labels.append((font.render('Men:', 1, color), properties.layer_unit_info_men_pos))
        self.static_labels.append((font.render('Mor:', 1, color), properties.layer_unit_info_morale_pos))
        self.static_labels.append((font.render('Fat:', 1, color), properties.layer_unit_info_fatigue_pos))
        self.static_labels.append((font.render('Exp:', 1, color), properties.layer_unit_info_experience_pos))
        self.static_labels.append((font.render('Ter:', 1, color), properties.layer_unit_info_terrain_pos))

        # commander labels
        self.static_labels.append((font.render('Exp:', 1, color), properties.layer_unit_info_cmdr_exp_pos))
        self.static_labels.append((font.render('Agg:', 1, color), properties.layer_unit_info_cmdr_agg_pos))
        self.static_labels.append((font.render('Rally:', 1, color), properties.layer_unit_info_cmdr_rally_pos))
        self.static_labels.append((font.render('Mot:', 1, color), properties.layer_unit_info_cmdr_motivation_pos))

        # weapon labels
        self.static_labels.append((font.render('Weapon:', 1, weaponcolor),
                                   properties.layer_unit_info_weapon_name_pos))

        self.static_labels.append((font.render('Range:', 1, weaponcolor),
                                   properties.layer_unit_info_weapon_range_pos))

        self.static_labels.append((font.render('Number:', 1, weaponcolor),
                                   properties.layer_unit_info_weapon_num_pos))
