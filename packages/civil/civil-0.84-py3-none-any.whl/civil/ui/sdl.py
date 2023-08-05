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


class SDL:
    """
    This class defines a wrapper around the top-level SDL surface. It manages when the top-level
    surface and takes care of directing all painting requests to the internally kept real SDL
    surface. The reason for this class is to have one centralized class that manages the repainting
    of the entire application.

    This class also initializes all needed pygame resources.

    TODO: this class should also manage the playfield and panel and just let clients register that
    they would be interested in seeing them updated.
    """

    def __init__(self):
        """
        Initializes the surface.
        """

        # get the initial width and height
        width = properties.window_size_x
        height = properties.window_size_y

        # try to set a top level surface using that size
        if not self.setSize(width, height):
            # failed to set the size
            raise RuntimeError("could not initialize video mode (%d,%d)" % (width, height))

        # set a nice caption too
        pygame.display.set_caption(properties.window_caption, properties.window_icon_text)

        # an update is needed
        self.update_needed = 1

    def getSize(self):
        """
        Returns a (x,y) tuple with the size of the top-level surface.
        """
        return self.width, self.height

    def getWidth(self):
        """
        Returns the width of the top-level surface. This is a convenience method.
        """
        return self.width

    def getHeight(self):
        """
        Returns the height of the top-level surface. This is a convenience method.
        """
        return self.height

    def setSize(self, width, height):
        """
        Sets a new size for the top-level surface. This in practice reinits the window at another
        resolution, so care must be taken to only give a dimension that is valid. If the new
        dimension can not be used then nothing will be done and 0 returned. If all is ok then 1 is
        returned.

        Note that this may raise an IndexError if the map is too small to fit in a large mode!
        """

        # try to open the screen centered
        os.environ['SDL_VIDEO_CENTERED'] = 'anything'

        # see weather the desired mode is ok. First we test a hardware mode
        depth = pygame.display.mode_ok([width, height],
                                       properties.window_hwflags, properties.window_depth)

        # did we get anything at all?
        if depth != 0:
            # yep, so initialize this mode
            flags = properties.window_hwflags
            print("initializing hardware accelerated mode.")

        else:
            # that did not work, try safe flags
            depth = pygame.display.mode_ok([width, height],
                                           properties.window_safeflags, properties.window_depth)

            # did we get anything at all?
            if depth != 0:
                # all ok, set the mode
                flags = properties.window_safeflags
                print("initializing safe mode.")

            else:
                # not even the safe mode could be initialized
                print("the needed video mode (%d,%d) can not be initialized!" % (width, height))
                return 0
                # sys.exit ( 1 )

        # all ok, set the mode
        self.sdl = pygame.display.set_mode([width, height], flags, depth)

        # and store the new size
        self.width = width
        self.height = height

        # all ok
        return 1

    def update(self):
        """
        Updates the top-level surface and makes all registered blits active. If nothing has
        changed since the last update this method does nothing.
        """
        # do we need an update?
        if self.update_needed == 0:
            # no update needed
            return

        # update it all
        pygame.display.flip()
        # pygame.display.update ()

        # no update needed anymore
        self.update_needed = 0

    def fill(self, color, rectangle=None):
        """
        Fills the entire top-level surface with the given color. It must be a (r,g,b) tuple. If
        'rectangle' is given it must be a tuple (x,y,w,h) that describes the position and dimensions
        of the filled rectangle.
        """

        # perform fill
        # do we have a rectangle?
        if rectangle is None:
            self.sdl.fill(color)
        else:
            self.sdl.fill(color, rectangle)

        # an update is needed
        self.update_needed = 1

    def blit(self, icon, position, subrect=None):
        """
        Blits out 'icon' at 'position' on the top-level surface. If the four-part tuple 'subrect'
        has been given (normally not) then that rectangle is used to indicate that only a part of


 """

        # do we have a subrect?
        if subrect is None:
            # no rect, blit the entire icon
            self.sdl.blit(icon, position)
        else:
            # use the subrect too
            self.sdl.blit(icon, position, subrect)

        # an update is needed
        self.update_needed = 1

    def drawLine(self, color, start, end):
        """
        Paints a line from 'start' to 'end' using the passed color. The color argument can be
        either a RGB sequence or mapped color integer. The positions are tuples (x,y).
        """

        # paint the line using pygame
        pygame.draw.line(self.sdl, color, start, end)

        # an update is needed
        self.update_needed = 1

    def drawLines(self, lines):
        """
        This is an alternate version provided for painting several lines at the same time. Here
        the parameter lines is an list of tuples (color,start.end), where each element is of the
        type drawLine() above accepts. All lines are drawn at the same time.
        """

        # lock the surface this time
        self.sdl.lock()

        # loop over all lines
        for color, start, end in lines:
            # paint the line using pygame
            pygame.draw.line(self.sdl, color, start, end)

            # we're done, unlock the surface
        self.sdl.unlock()

        # an update is needed
        self.update_needed = 1

    def drawCircle(self, color, position, radius, width):
        """
        Paints a circle with center as 'pos' and which has a radius of 'radius'. The width
        defines how many pixels wide the drawn border is. The position is a tuple (x,y).
        """

        position = [int(x) for x in position]

        # paint the line using pygame
        pygame.draw.circle(self.sdl, color, position, radius, width)

        # an update is needed
        self.update_needed = 1

    def drawRect(self, color, position, width):
        """
        Paints a rectangle at the Rect position with a specified width
        and a specific color. If width is zero the rect is filled.
        """

        # paint the rectangle using pygame
        pygame.draw.rect(self.sdl, color, position, width)

        # an update is needed
        self.update_needed = 1

    def setClip(self, rect):
        """
        Sets the clipping area to the rectangle defined by 'rect'. It must contain four values:
        x, y, width and height.
        """
        # set the clipping
        self.sdl.set_clip(rect)

        # an update is needed
        self.update_needed = 1

    def clearClip(self):
        """
        Clears the clipping and sets it to the entire top-level surface.
        """
        self.sdl.set_clip()

        # an update is needed
        self.update_needed = 1

    def saveScreenshot(self, file_name='snapshot.bmp'):
        """
        Saves the current state of the top-level surface as a screenshot. The name of the
        screenshot will be 'file_name'. Any errors are catched and ignored.
        """
        try:
            # perform the save
            pygame.image.save(self.sdl, file_name)

            # write a message too os the player knows what happened
            scenario.messages.add("Saved screenshot: %s" % file_name)

        except:
            # oops, failed to do the save, catch and ignore
            # write a message too os the player knows what happened
            scenario.messages.add("Could not save screenshot")

    def getSurface(self):
        """
        Returns the raw pygame surface.
        """
        return self.sdl
