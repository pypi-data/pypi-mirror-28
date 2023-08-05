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
from pygame.locals import *

from civil.ui import widget, button
from civil import properties
from civil.ui.widget import *


class EditField(Widget):
    """
    This class defines a simple edit field where the user may input some text while the widget has
    focus. The editfield has a cursor which shows where current text is inserted or removed.
    """

    # static images for the frame around the editable text
    frameicons = {}

    # names for the icons
    frameiconnames = ['topleft', 'top', 'topright', 'right', 'botright', 'bot', 'botleft', 'left']

    # a shared font
    font = None

    def __init__(self, text="", width=100, position=(0, 0), callbacks=None,
                 color=properties.editfield_font_color, background=properties.editfield_background_color):
        """
        Initializes the widget. Renders the font using the passed data.
        """

        # first call superclass constructor
        Widget.__init__(self, position, callbacks)

        # do we have a font already?
        if EditField.font is None:
            # no, so create it 
            EditField.font = pygame.font.Font(properties.editfield_font_name, properties.editfield_font_size)

        # store the text
        if text is None:
            self.text = ""
        else:
            self.text = text

        # store the cursor position
        self.cursor = len(self.text)

        # store all needed data so that we can create new surfaces later
        self.color = color
        self.background = background
        self.width = width

        # render the text
        self.textrendered = EditField.font.render(text, 1, color)

        # create the background surface to fit the rendered text's height
        self.textsurface = pygame.Surface((width, self.textrendered.get_height() + 3),
                                          HWSURFACE).convert()

        # fill with the proper background color 
        self.textsurface.fill(background)

        # create a surface for the cursor
        self.cursor_image = pygame.Surface((1, self.textrendered.get_height()))

        # draw a vertical line
        pygame.draw.line(self.cursor_image, properties.editfield_font_color, (0, 0),
                         (0, self.cursor_image.get_height() - 1))

        # by default don't show the cursor
        self.show_cursor = 0

        # create the surface with the border in it
        self.createBorder()

        # set our internal callbacks so that we can trap keys
        self.internal = {widget.KEYDOWN: self.keyDown,
                         widget.MOUSEENTEREVENT: self.mouseEnter,
                         widget.MOUSELEAVEEVENT: self.mouseLeave}

    def setText(self, text):
        """
        Sets a new text to be rendered.
        """
        # store new text
        if text is None:
            self.text = ""
        else:
            self.text = text

        # render a new surface
        self.textrendered = EditField.font.render(self.text, 1, self.color)

    def getText(self):
        """
        Returns the text of the editfield. The text is never None, but may be empty if the
        editfield was cleared.
        """
        return self.text

    def paint(self, destination, force=0):
        """
        Method that paints the editfield. This method will simply blit out the surface of the widget
        onto the destination surface.
        """
        # are we dirty or not?
        if not self.dirty and not force:
            # not dirty, nothing to do here
            return 0

        # we're dirty, blit out the frame first
        destination.blit(self.surface, (self.position[0], self.position[1]))

        # now the text background
        destination.blit(self.textsurface, (self.position[0] + self.delta_x, self.position[1] + self.delta_y))

        # and the text if we have any
        if self.textrendered:
            # yep, we have it, get the width we should use
            if self.width < self.textrendered.get_size()[0] + 3:
                width = self.width - 3
            else:
                width = self.textrendered.get_size()[0]

            # now blit out the text
            destination.blit(self.textrendered,
                             (self.position[0] + self.delta_x + 3, self.position[1] + self.delta_y + 3))

        # slm : render cursor
        if self.show_cursor:
            # do we have any text?
            if len(self.text):
                # yes, get the text length 
                cursorx = self.font.size(self.text[0:self.cursor])[0]
            else:
                # no, set it at the start
                cursorx = 0

            # some extra spacing
            cursor_space = self.font.size(" ")[0] / 2

            # blit the cursor 
            destination.blit(self.cursor_image,
                             ((self.position[0] + self.delta_x) + (cursorx + cursor_space),
                              (self.position[1] + self.delta_y + 3)))

        # not dirty anymore
        self.dirty = 0

        # we did something, make sure the widget manager knows that
        return 1

    def keyDown(self, event):
        """
        Callback triggered when the user presses a key inside the editfield. Gets the pressed key
        and modifies the internal string if needed. Renders a new surface too if needed. Some
        special keys are ignored.
        """

        # get the key and the unicode string
        key = event.key

        # Weird fix. This is required on RedHat pygame 1.5.3??
        ev_unicode = event.str
        if type(ev_unicode) == str or type(ev_unicode) == str:
            if ev_unicode == '':
                ev_unicode = 0
            else:
                ev_unicode = ord(ev_unicode)

        value = chr(ev_unicode).encode('latin1')

        # get the old cursor position
        old_pos = self.cursor

        # a special key?
        if key == K_BACKSPACE:
            # are we at the first position and can't delete to the left?
            if self.cursor == 0:
                # yes, nothing to do here
                return HANDLED

            # remove one character to the left
            self.text = self.text[:self.cursor - 1] + self.text[self.cursor:]

            # update cursor position
            self.cursor -= 1
            if self.cursor < 0:
                self.cursor = 0

            # what text should we render?
            if len(self.text) == 0:
                # no text, so use something empty
                text = ' '
            else:
                # we have text, use it
                text = self.text

            # render the new surface
            self.textrendered = EditField.font.render(text, 1, self.color)

            # we're dirty now
            self.dirty = 1
            return HANDLED

        if key == K_DELETE:
            # remove one character from the right
            self.text = self.text[0:self.cursor] + self.text[self.cursor + 1:]

            # what text should we render?
            if len(self.text) == 0:
                # no text, so use something empty
                text = ' '
            else:
                # we have text, use it
                text = self.text

            # render the new surface
            self.textrendered = EditField.font.render(text, 1, self.color)

            # we're dirty now
            self.dirty = 1
            return HANDLED

        if key == K_TAB or key == K_RETURN:
            # remove one character from the right
            print("editfield.keyDown(): tab/return not handled")
            return UNHANDLED

        # arrow handling
        elif key == K_LEFT:
            self.cursor -= 1
            if self.cursor < 0:
                self.cursor = 0

        elif key == K_RIGHT:
            self.cursor += 1
            if self.cursor > len(self.text):
                self.cursor = len(self.text)

        elif key == K_HOME:
            # move to the first position
            self.cursor = 0

        elif key == K_END:
            # move the the last position
            self.cursor = len(self.text)

        elif ev_unicode != 0:
            # a normal key pressed, merge in the text
            self.text = self.text[0:self.cursor] + value + self.text[self.cursor:]

            # update cursor position
            self.cursor += 1

            # do we still have any text left?
            if self.text == "":
                self.textrendered = None
                self.cursor = 0
            else:
                # set the new surface
                self.textrendered = EditField.font.render(self.text, 1, self.color)

            # we're dirty now
            self.dirty = 1

        else:
            # not handled at all
            return UNHANDLED

        # so, has the cursor changed from the position it had when we started this method?
        if old_pos != self.cursor:
            # yes, so we need to repaint
            self.dirty = 1

        # we got this far, it's handled all right
        return HANDLED

    def createBorder(self):
        """
        Creates the border for the widget. Uses the 8 static icons and creates a surface that is
        slightly larger than the text surface (self.textsurface). This method is one ugly thing of
        coordinates and offsets. Don't touch unless you know what you do.
        """
        # load the frame icons
        self.__loadFrameIcons()

        # get the delta values. These are used so that we know where to paint the text surface
        self.delta_x = EditField.frameicons['left'].get_width()
        self.delta_y = EditField.frameicons['top'].get_height()

        # get height and width of new surface
        size = self.textsurface.get_size()
        width = size[0] + self.delta_x + EditField.frameicons['right'].get_width()
        height = size[1] + self.delta_y + EditField.frameicons['bot'].get_height()

        # create the needed surface
        self.surface = pygame.Surface((width, height), HWSURFACE).convert()

        # now some gory details. We need to blit stuff onto our frame surface to create the actual
        # frame. We first blit out the borders and the the corners. the corners then overpaint the
        # borders at proper positions
        top = EditField.frameicons['top']
        bot = EditField.frameicons['bot']
        left = EditField.frameicons['left']
        right = EditField.frameicons['right']
        topleft = EditField.frameicons['topleft']
        topright = EditField.frameicons['topright']
        botleft = EditField.frameicons['botleft']
        botright = EditField.frameicons['botright']

        # top/bottom borders
        x = 0
        while x < width:
            # what width should be used?
            if x + top.get_size()[0] < width:
                # full width of icon
                widthx = top.get_size()[0]
            else:
                # use only the missing part
                widthx = width - x

            # blit it all out
            self.surface.blit(top, (x, 0))
            self.surface.blit(bot, (x, height - bot.get_height()))
            x += widthx

        # left/right borders
        y = 0
        while y < height:
            # what height should be used?
            if y + left.get_size()[1] < height:
                # full height of icon
                heighty = left.get_size()[1]
            else:
                # use only the missing part
                heighty = height - y

            # blit it all out
            self.surface.blit(left, (0, y))
            self.surface.blit(right, (width - right.get_size()[0], y))
            y += heighty

        # top left corner
        self.surface.blit(topleft, (0, 0))

        # top right corner
        self.surface.blit(topright, (width - topright.get_width(), 0))

        # bottom left corner
        self.surface.blit(botleft, (0, height - botleft.get_height()))

        # bottom right corner
        self.surface.blit(botright, (width - botright.get_width(), height - botright.get_height()))

    def mouseEnter(self, event):
        """
        Internal callback triggered when the mouse enters an editfield. This will show the cursor.
        """
        # show cursor
        self.show_cursor = 1

        # we're dirty
        self.dirty = 1

    def mouseLeave(self, event):
        """
        Internal callback triggered when the mouse leaves an editfield. This will hide the cursor.
        """
        # don't show cursor
        self.show_cursor = 0

        # we're dirty
        self.dirty = 1

    def __loadFrameIcons(self):
        """
        Loads the needed icons for the frame from files. The icons are stored in static members
        so that all instances can share the same icons.
        """
        # do we already have icons loaded?
        if EditField.frameicons != {}:
            return

        # base file_name
        base = os.path.join(properties.path_dialogs, 'dialog-widgetFrm-')

        # loop and read all the icons
        for name in EditField.frameiconnames:
            # create the file_name
            file_name = base + name + '.png'

            # load it
            # TODO pygame update problem pygame.image.load not existing anymore
            icon = pygame.image.load(file_name).convert()

            # do we need colorkeying?
            if properties.editfield_use_colorkey:
                # yeah, set it
                button.set_colorkey(properties.editfield_colorkey_color)

            # store it in the map
            EditField.frameicons[name] = icon
