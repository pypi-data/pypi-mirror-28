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

import operator
import os
from functools import reduce

import pygame

from civil import properties
from civil.model import scenario
from civil.serialization.simple_dom_parser import SimpleDOMParser
from civil.playfield.dialog_layer import DialogLayer


class HelpBrowserLayer(DialogLayer):
    """
    This class defines a layer that plugs into the PlayField. It is used when the server is
    calculating the action data. It simply shows the user a static screen. Nothing fancy. Reacts to
    nothing.
    """

    def __init__(self, name):
        """
        Initializes the layer.
        """
        # call superclass constructor, but with no button
        DialogLayer.__init__(self, name, 600, 100, properties.layer_help_browser_button)

        # load the title font and set its properties
        self.titlefont = pygame.font.Font(properties.layer_help_browser_font,
                                          properties.layer_help_browser_font_size)
        self.seealsofont = pygame.font.Font(properties.layer_help_browser_font,
                                            properties.layer_help_browser_font_size - 2)

    def setTopic(self, topic):
        """
        Sets the topic that the help browser is supposed to show. Reads in the topic from a file
        and create all the contents of the layer.
        """

        # the window should be 600 pixels wide, unless the window is smaller. in that case we use
        # 90% of the window width
        width = min(600, int(scenario.sdl.getWidth() * 0.90))

        # read the topic data
        self.readTopicData(topic, width)

        # a map that maps link id:s to the coordinates. this is used when a link is clicked to that
        # we can check which link was selected. the list needs to be cleared each time a new topic
        # is read, so that wa always have fresh coordinates
        self.coordinates = []

        # do we need a "see also" section?
        if len(self.seealsos) > 0:
            # yep, create the labels
            self.see = self.createLabel("See also:", self.seealsofont, properties.layer_help_browser_color2)

        # calculate a new size for the dialog. this is actually a little practise in functional
        # programming, and if it works as I think it will, then all is well :)
        # it should get a list of the label heights and add each of those heights into a single number
        height = self.title.get_height() + \
                 self.bordery + \
                 reduce(operator.add, [x.get_height() + 3 for x in self.labels]) + \
                 self.bordery

        # do we also have 'see also' labels?
        if len(self.seealsos) > 0:
            # yep, add some more height
            height += reduce(operator.add, [x[1].get_height() + 3 for x in self.seealsos]) + \
                      self.bordery

        # set the new size
        self.setSize(width, height)

        # What link should be highlighted
        self.highlighted = None

        # What link is highlighted
        self.gui_highlighted = None

    def overLink(self, x, y):
        """
        Returns over what link key (x,y) is.
        """
        # loop over all link id:s and coordinates
        for linkid, x1, y1, x2, y2 in self.coordinates:

            # is this clicked?
            if x1 <= x <= x2 and y1 <= y <= y2:
                # yep, this id was clicked
                return linkid

        return None

    def handleMouseMotion(self, x, y):
        """
        Handles the highlightning of links.
        """
        self.highlighted = self.overLink(x, y)

        # Same links or both no links, no need to do anything
        if self.highlighted == self.gui_highlighted:
            return

        # Otherwise, signal we need a repaint
        scenario.playfield.needInternalRepaint(self)

    def handleLeftMousePressed(self, click_x, click_y):
        """
        Method that handles a press with the left mouse button. Checks if any of the links have
        been clicked, and if so, 'follows' the link by making it the new current topic.
        """

        linkid = self.overLink(click_x, click_y)

        if linkid:
            # set it as the new topic
            self.setTopic(linkid)

            # we're done, we have changed something so make sure we get repainted
            return 1

        # nothing here, no repaint needed
        return 0

    def customPaint(self):
        """
        Paints the layer by painting the contents and the calling the superclass method for doing
        the frame painting.
        """

        # where to start with the labels
        y = self.y + self.bordery

        if not self.need_internal_repaint:
            # paint the title. the coordinates are inherited, and refer to the topleft corner of the
            # content area we're given
            scenario.sdl.blit(self.title, (self.x + self.borderx, y))

        # add some extra offset
        y += self.title.get_height() + self.bordery

        # loop and paint all the main text labels too
        for label in self.labels:
            # blit it out
            if not self.need_internal_repaint:
                scenario.sdl.blit(label, (self.x + self.borderx, y))

            # add to the offset for the next label
            y += label.get_height() + 3

        # do we need a "see also" section?
        if len(self.seealsos) == 0:
            # nope, we're done here
            return

        # now add some extra spacing for the "see also" title
        y += self.bordery

        # blit it out
        if not self.need_internal_repaint:
            scenario.sdl.blit(self.see, (self.x + self.borderx, y))

        # we want to blit out the labels to the right of the 'see also' title
        x = self.x + self.borderx + self.see.get_width() + self.borderx

        # The coordinates are recreated. Quite useless perhaps, but just in case
        # Anyway, this stops self.coordinates from growing every time customPaint
        # is called
        self.coordinates = []

        # loop and paint all the "see also" text labels too
        for key, label, label_active in self.seealsos:
            # On internal repaints, only link highlighting
            if self.need_internal_repaint:

                # The currently highlighted link is deactivated
                if key == self.gui_highlighted:
                    # Clear first
                    scenario.sdl.fill((0, 0, 0), (x, y, label.get_width(), label.get_height()))
                    # Blit text
                    scenario.sdl.blit(label, (x, y))

                # The new link is highlighted
                if key == self.highlighted:
                    # Clear first
                    scenario.sdl.fill((0, 0, 0), (x, y, label.get_width(), label.get_height()))
                    # Blit text
                    scenario.sdl.blit(label_active, (x, y))

            # Ordinary blit routine
            if not self.need_internal_repaint:
                # blit it out
                scenario.sdl.blit(label, (x, y))

            # add an entry to the coordinates so that we later can identify this link
            self.coordinates.append((key, x, y, x + label.get_width(), y + label.get_height()))

            # add to the offset for the next label
            y += label.get_height() + 3

        # Update gui information, last!
        self.gui_highlighted = self.highlighted

    def readTopicData(self, topic, width):
        """
        Reads in all data about the given topic. The topic data is in an XML file in a special
        directory. This file is read and parsed into its components. The data that is parsed is:

        * the title
        * all the paragraphs
        * optionally some 'see also' links

        Labels are generated for all the texts and stored in members.
        """

        # create a new parser
        domparser = SimpleDOMParser()

        # design the file_name
        file_name = os.path.join(properties.path_help, "%s.xml" % (topic))

        try:
            # parse the data
            root = domparser.parseFile(file_name)
        except:
            # hmm, failed? maybe the file doesn't exist or it's just malformed
            print("HelpBrowserLayer.readTopicData: failed to read: %s" % file_name)

            # set some data for this error situation
            self.setErrorText(file_name, width)
            return

        # read the title and create the label
        self.title = self.createLabel(root.getChild('title').getData(), self.titlefont,
                                      properties.layer_help_browser_color)

        # no paragraphs nor see also:s yet
        self.labels = []
        self.seealsos = []

        # loop over all paragraphs
        count = 1
        all_paragraphs = root.getChild('body').getChildren()
        for paragraph in all_paragraphs:
            # create the needed labels for the paragraph and save it
            self.labels.extend(self.createParagraphLabels(paragraph.getData(), width))

            # should we add an empty row?
            if count < len(all_paragraphs):
                # yes, at least one more, add an empty row
                self.labels.append(self.createLabel(" "))

            count += 1

        # get the see-also nodes
        seealso_child = root.getChild('seealso')

        # did we get anything?
        if not seealso_child:
            # nope, we're done
            return

        # loop over all 'see also' links
        for link in seealso_child.getChildren():
            # get some data
            id = link.getAttribute('id')
            text = link.getData()
            # store the label generated from the link indexed by the id
            self.seealsos.append((id,
                                  self.createLabel(text, None, properties.layer_help_browser_color_link),
                                  self.createLabel(text, None, properties.layer_help_browser_color_activelink)))

    def setErrorText(self, file_name, width):
        """
        This method is used if the wanted help topic file could not be opened. This method will
        set a help text that tells the player that the help file is missing. This aids is
        development a little bit.
        """

        # set an error title
        self.title = self.createLabel("Could not open help topic!", self.titlefont,
                                      properties.layer_help_browser_color)

        # add a few error paragraphs
        self.labels = self.createParagraphLabels("Failed to open the file for the " +
                                                 "wanted help topic. Seems Civil is " +
                                                 "not correctly installed or one of " +
                                                 "the developers has goofed.", width)

        # add an empty row and the file_name label
        self.labels.append(self.createLabel(" "))
        self.labels.extend(self.createParagraphLabels("The missing topic is:", width))

        # add an empty row and the file_name
        self.labels.append(self.createLabel(" "))
        self.labels.append(self.createLabel(file_name))

        # add a link to the top-level index
        self.seealsos = [('index',
                          self.createLabel("Index", None, properties.layer_help_browser_color_link),
                          self.createLabel("Index", None, properties.layer_help_browser_color_activelink))]
