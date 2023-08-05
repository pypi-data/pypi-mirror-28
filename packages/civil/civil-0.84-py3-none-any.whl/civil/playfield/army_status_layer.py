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
from pygame.locals import *

from civil import properties
from civil.model import scenario
from civil.playfield.dialog_layer import DialogLayer


class ArmyStatusLayer(DialogLayer):
    """
    This class defines a layer that plugs into the PlayField. It takes care os showing a dialog with
    info about the player's army. All organizations are shown in a tree fashion along with the
    number of men, guns and casualities. The dialog provides several 'panes' that can be flipped
    through by clicking buttons. As all units don't fit on one dialog the status is broken up into
    several smalles panes.

    Navigation between the panes is performed using two buttons that when clicked move to next and
    previous panes.
    """

    def __init__(self, name):
        """
        Initializes the layer.
        """
        # call superclass constructor. note that that size is totally vapour, we'll fill it in layer
        # in the constructor
        DialogLayer.__init__(self, name, 100, 100, properties.layer_armystatus_button_ok)

        # load the additional up/down buttons
        self.button_up = pygame.image.load(properties.layer_armystatus_button_up).convert()
        self.button_down = pygame.image.load(properties.layer_armystatus_button_down).convert()

        # set the margins we use from the origin. this gives some padding to the border
        self.margin_x = 15
        self.margin_y = 10

        # set the title
        side = ('rebel', 'union')[scenario.local_player_id]
        self.title = self.createLabel("Status of the %s army" % side)

        # amount of indentation
        self.indent_amount = 30
        self.stats_size = 30

    def updateUnits(self):
        """
        Updates the army status. Creates all labels and panes that are needed.
        """

        # create the labels
        labels = self.__createLabels()

        # figure out a size for the panes that suits the widest label
        self.__calculateSize(labels)

        # now all labels are created, so now we can
        self.__createPanes(labels)

        # start with the first pane as current
        self.current_pane_index = 0

    def handleLeftMousePressed(self, click_x, click_y):
        """
        Method that handles a press with the left mouse button. Checks weather any of the buttons
        was clicked, and if so makes the next or previous pane current. Returns 1 if a repaint is
        needed and 0 if not.
        """

        # figure out where the pane goes and add some margin
        x, y, contentwidth, contentheight = self.getContentGeometry()
        x += self.margin_x
        y += self.margin_y + self.title.get_height() + 10

        # get the button dimensions
        buttonw = self.button_up.get_width()
        buttonh = self.button_up.get_height()

        # do we have a "up" button? we do that if the current pane index is small enough
        if self.current_pane_index > 0:
            # yes, up could be clicked, is it clicked?
            if x + contentwidth - buttonw <= click_x <= x + contentwidth and \
                    y <= click_y <= y + buttonw:
                # yes, activate the previous pane
                self.current_pane_index -= 1
                return 1

        # do we have a "down" button? we do that if the current pane index is small enough
        if self.current_pane_index < len(self.panes) - 1:
            # yes, up could be clicked, is it clicked?
            if x + contentwidth - buttonh <= click_x <= x + contentwidth and \
                    y + contentheight - buttonh <= click_y <= y + contentheight:
                # yes, activate the next pane
                self.current_pane_index += 1
                return 1

        # no repaint needed, as no button was clicked
        return 0

    def customPaint(self):
        """
        Paints the layer by painting the title and the checkboxes along with the labels.
        """

        # paint the title. the coordinates are inherited, and refer to the topleft corner of the
        # content area we're given
        if not self.need_internal_repaint:
            scenario.sdl.blit(self.title, (self.x + self.margin_x, self.y + self.margin_y))

        # figure out where the pane goes and add some margin
        x, y, contentwidth, contentheight = self.getContentGeometry()
        x += self.margin_x
        y += self.margin_y + self.title.get_height() + 10

        # repaint the selected pane
        scenario.sdl.blit(self.panes[self.current_pane_index], (x, y))

        # get the button dimensions
        buttonw = self.button_up.get_width()
        buttonh = self.button_up.get_height()

        # do we have a "up" button? we do that if the current pane index is small enough
        if self.current_pane_index > 0:
            # yes, large enough, draw the button
            scenario.sdl.blit(self.button_up, (x + contentwidth - buttonw, y))
            # scenario.sdl.drawRect ( (255,255,255), (x+contentwidth-buttonw, y, 20, 20), 3)

        # do we have a "down" button? we do that if the current pane index is small enough
        if self.current_pane_index < len(self.panes) - 1:
            # yes, small enough, draw the button
            scenario.sdl.blit(self.button_down, (x + contentwidth - buttonw, y + contentheight - buttonh))
            # scenario.sdl.drawRect ( (255,255,255),
            #                        pygame.Rect(x+contentwidth-20, y+contentheight-20, 20, 20), 3 )

    def __calculateSize(self, labels):
        """
        Checks all labels to see which one is the widest. That widest size is then used as the
        width for the panes, with some extra added space for the navigation buttons.
        """

        # use 60% of the height 
        height = int(scenario.sdl.getHeight() * 0.50)
        width = 100

        # loop over all labels that we got
        for indent, labels, skip in labels:
            # is the label wider than the current max?
            if labels[0].get_width() + indent * self.indent_amount > width:
                # yes, so store the new width
                width = labels[0].get_width() + indent * self.indent_amount

        # store the widest label
        self.widest_label = width

        # add some extra width for the buttons and the data labels
        width += 50 + 4 * self.stats_size

        # set the size
        self.setSize(width, height)

    def __createLabels(self):
        """
        Creates all the labels for the panes. Returns a list containing (indent,labels,skip) tuples,
        where indent is the amount of indentation (in steps) that 'label' should be indented when
        drawn. The 'skip' is some extra skip that is added to separate the labels a bit.
        """

        # no labels yet. we add here tuples (indent,label,skip) that represent the indentation level of
        # the label, and the actual rendered label
        labels = []

        # cache the colors. this makes the label making a bit prettier :)
        color_brigade = properties.layer_armystatus_color_brigade
        color_regiment = properties.layer_armystatus_color_regiment
        color_battalion = properties.layer_armystatus_color_battalion
        color_company = properties.layer_armystatus_color_company

        # loop over all brigades we have for the local player
        for brigade in list(scenario.info.brigades[scenario.local_player_id].values()):
            # get the hq
            hq = brigade.getHeadquarter()

            # create a label for the hq 
            unit_labels = self.__createUnitLabels(hq, color_brigade)

            # and add to the labels
            labels.append((0, unit_labels, 10))

            # loop over all regiments for the brigade
            for regiment in brigade.getRegiments():
                # get the hq
                hq = regiment.getHeadquarter()

                # create a label for the hq 
                unit_labels = self.__createUnitLabels(hq, color_regiment)

                # and add to the labels
                labels.append((1, unit_labels, 10))

                # loop over all battalions for the regiments
                for battalion in regiment.getBattalions():
                    # get the hq
                    hq = battalion.getHeadquarter()

                    # create a label for the hq 
                    unit_labels = self.__createUnitLabels(hq, color_battalion)

                    # and add to the labels
                    labels.append((2, unit_labels, 10))

                    # loop over  all companies
                    for company in battalion.getCompanies():
                        # create a label for the company
                        unit_labels = self.__createUnitLabels(company, color_company)

                        # and add to the labels
                        labels.append((3, unit_labels, 0))

                # append all companies
                for company in regiment.getCompanies():
                    # create a label for the company
                    unit_labels = self.__createUnitLabels(company, color_company)

                    # and add to the labels
                    labels.append((2, unit_labels, 0))

        # return the label data that we now have
        return labels

    def __createPanes(self, labels):
        """
        Creates the panes and stores them internally. Each pane contains info about some units as
        all info does not fit on one pane. As many panes as are needed will be created.
        """
        # cache the dimensions we have to play with
        width = self.contentwidth
        height = self.contentheight - self.title.get_height() - 10 - self.margin_y

        # no panes yet
        self.panes = []

        # create the initial pane
        pane = pygame.Surface((width, height), HWSURFACE)

        # add it
        self.panes.append(pane)

        # start from the top
        y = 0

        # loop over all labels that we got
        for indent, labels, skip in labels:
            # explode the labels
            name, men_ok, men_dead, guns_ok, guns_dead = labels

            # does this label still fit on the pane?
            if y + name.get_height() > height:
                # does not fit, create a new pane
                pane = pygame.Surface((width, height), HWSURFACE)

                # add it
                self.panes.append(pane)

                # and start from the top again, and no skip
                y = 0
                skip = 0

            # no we have space for it, render the labels
            pane.blit(name, (indent * self.indent_amount, y + skip))
            pane.blit(men_ok, (self.widest_label + self.stats_size * 1, y + skip))

            # do we have dead guys?
            if men_dead is not None:
                pane.blit(men_dead, (self.widest_label + self.stats_size * 2, y + skip))

            # do we have guns too?
            if guns_ok is not None:
                # yeah, blit them too
                pane.blit(guns_ok, (self.widest_label + self.stats_size * 3, y + skip))

            # do we have destroyed guns?
            if guns_dead is not None:
                # yeah, blit them too
                pane.blit(guns_dead, (self.widest_label + self.stats_size * 4, y + skip))

            # add the height of the label to the total height
            y += name.get_height() + skip

        print("ArmyStatusLayer.__createPanes: got %d panes" % len(self.panes))

    def __createUnitLabels(self, unit, color):
        """
        Creates the labels needed for a unit. This will return five labels, which contain as
        rendered labels: name, men ok, men killed, guns ok and guns destroyed. If the unit has no guns the
        two last labels are returned as None. So the count is always five.
        """
        # create labels for the name
        name = self.createLabel(text=unit.getName(), color=color)

        # and men
        men_ok_count = unit.getMen()
        men_dead_count = unit.getKilled()

        # create the label for the number of ok/dead men
        men_ok = self.createLabel(text="%d" % men_ok_count, color=properties.layer_armystatus_color_data_ok)
        men_dead = self.createLabel(text="%d" % men_dead_count, color=properties.layer_armystatus_color_data_dead)

        # does the unit have guns?
        if unit.hasGuns():
            # yes, guns too
            guns_ok_count = unit.getWeaponCounts()[0]
            guns_dead_count = unit.getWeaponCounts()[1]

            # create the label for ok/destroyed guns
            guns_ok = self.createLabel(text="%d" % guns_ok_count,
                                       color=properties.layer_armystatus_color_data_ok)
            guns_dead = self.createLabel(text="%d" % guns_dead_count,
                                         color=properties.layer_armystatus_color_data_dead)
        else:
            # no guns, use None
            guns_ok = None
            guns_dead = None

        # return all data
        return name, men_ok, men_dead, guns_ok, guns_dead
