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


class Plan:
    """
    This class is a base class for all available types of plans the player can give to units. The
    plans contain no actual game logic, merely the data needed for execution by some other party and
    for visualization. This class and subclasses are mostly used on the client side for organizing
    the orders for units.

    A plan is something the player performs with a unit. It contains the overall goal the player
    wants to do with the unit, such as move somewhere, change state etc. A plan is the executed by
    some facility when the action is computed by the server player.

    All other plans should subclass this class and implement the abstract methods. 
    
    Every plan contains a name which is a short lowercase string that identifies the plan. The
    name is unique only among classes, not instances. The name can be used to recognize the plan
    when in deep debug mode.

    All plans also have a member for a label. This is only used for the GUI client. See 'getLabel()'
    for more info.

    Plans are also visualized on the playfield using a custom playfield layer. If a plan can not be
    visualized there it should set the member 'showonplayfield' to 0. By default the member is set
    to 1.
    """

    # a shared font
    font = None

    # a plan id counter. note that this is only unique for one player, both players have this reset
    # to 0 when the game starts. this id is thus not unique for the whole game, only for one player
    plan_id = 0

    def __init__(self, name, unit_id):
        """
        Initializes the instance. Stores the turn the plan was issued and the id:s
        """
        # store the name and unit id
        self.name = name
        self.unit_id = unit_id

        # the label for the plan, by default it's uninitialized
        self.label = None

        # a nice text for the label, we use a default here. subclasses should override it
        self.labeltext = name + " has no label text"

        # by default all plans can be shown on the playfield
        self.showonplayfield = 1

        # the id is invalid by default
        self.id = Plan.plan_id

        # next plan id please
        Plan.plan_id += 1

    def getId(self):
        """
        Returns the unique id of this plan.
        """
        return self.id

    def getName(self):
        """
        Returns the name of the plan. This is a string that can be used to identify the
        plan.
        """
        return self.name

    def getLabel(self):
        """
        Returns a pygame surface that can be used as a label describing the plan. This should be
        a simple thing, such as 'move', or 'wait 2 min', in some color suitable for displaying in
        the panel or similar. The text is set by each subclass in the member 'self.labeltext'.

        The label should be cached in the plan itself. The label is rendered using the font
        'getFont()'.
        """

        # do we have a label?
        if self.label is None:
            # no label, so create one
            self.label = self.getFont().render(self.labeltext, 1, self.getColor())

        # we have a label, here you go
        return self.label

    def getFont(self):
        """
        Returns a suitable font used to render all label descriptions. A plan may override this
        to provide for an alternate font if that for some reason is wanted.
        """
        # do we have a font already?
        if Plan.font is None:
            # get the font we should use
            Plan.font = pygame.font.Font(properties.plan_font_name, properties.plan_font_size)

        # it's done, return it
        return Plan.font

    def getColor(self):
        """
        Returns a color that should be used to render the label for the plan. Plans should
        override the method if they want another color.
        """
        return 255, 255, 255

    def showOnPlayfield(self):
        """
        This method returns 1 if the plan is something that can be visualizable in the playfield,
        i.e. graphically. Some plans can be shown as some kind of line or similar, but not all can
        be shown. This is just an optimization to make the selection of visualizable plans
        faster.
        """
        return self.showonplayfield

    def getunit_id(self):
        """
        Returns the id of the unit the plan should be attached to.
        """
        return self.unit_id

    def extract(self, parameters):
        """
        Extracts all data from the data coming from the network. This method is used whenever
        the plan has been written to the socket and an instance needs to be recreated from textual
        data.  This method should be overridden to perform whatever is needed. The 'parameters' is a
        list of all the parameters passed with the packet.
        """

        raise NotImplementedError("Plan.extract: this method must be overridden")

    def __cmp__(self, other):
        """
        Overridden comparison operator that compares this plan with 'other'. Behaves according to
        spec wrt return value.
        """
        # precautions
        if not other:
            return 1

        # just do the comparisons
        if self.id == other.id:
            return 0

        elif self.id < other.id:
            return -1

        else:
            # has to be larger
            return 1
