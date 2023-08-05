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

from civil.model import scenario
from civil.playfield.layer import Layer
from civil.state import window_move


class FloatingWindowLayer(Layer):
    """
    This class defines a base class for layers that are floating. A floating window is a small area
    with a border around it. Dragging the border can be used to move the window. The actual code for
    checking for events must be done somewhere else, this layer mainly handles the actual click
    position and checks what to do with it.

    This class has methods for getting and setting the position for layers, as well as some
    overloadable methods for handling clicks.
    """

    # the move button
    move = None

    def __init__(self, name):
        """
        Initializes the layer.
        """
        # call superclass constructor
        Layer.__init__(self, name)

        # we want the position too
        self.x = -1
        self.y = -1
        self.width = -1
        self.height = -1

        # not minimized by default
        self.minimized = 0

    def updateForResolutionChange(self, oldwidth, oldheight, width, height):
        """
        This method is overridden from Layer. It makes sure the dimensions of the layer remain
        unchanged. Moves the _floating layers_ relative to the change in resolution, so they are at
        'good' places relative to where they were in the old resolution.

        In practice this means that stuff in a corner still in fact is in that corner.

        (This looks so complicated because the layer's width and height does _not_ scale with the
        resolution.
        """

        # get new and old dimensions
        newwidth = scenario.sdl.getWidth()
        newheight = scenario.sdl.getHeight()

        # Get the bounding box of the layer
        rect = self.getRect()

        # Scale the topleft corner in a reduced rectangle
        # to get the new corner at another resolution
        newx = rect.left * (width - rect.width) / (oldwidth - rect.width)
        newy = rect.top * (height - rect.height) / (oldheight - rect.height)

        # Translate to inner coordinate ( add border left & top size)
        self.x = newx + (self.x - rect.left)
        self.y = newy + (self.y - rect.top)

        print("FloatingWindowLayer.updateForResolutionChange:", self.x, self.y)

    def setPosition(self, x, y):
        """
        Sets a new position for the floating window. This is the position of the upper left part
        of the contents window, not the border.
        """
        # just store the new position
        self.x = x
        self.y = y

    def getPosition(self):
        """
        Returns the position of the upper left corner of the contents part of the window as a
        (x,y) tuple.
        """
        return self.x, self.y

    def isClickable(self):
        """
        Returns 1 as the layer is clickable, i.e. it has a method handleClick(). Normal layers
        are not clickable, but these layers are.
        """
        return 1

    def isMinimized(self):
        """
        Returns 1 if the window is minimized, and 0 if not. A minimized floating window has no
        actual content, just a little border.
        """
        return self.minimized

    def setMinimized(self, minimized=1):
        """
        Sets the minimization status of the floating layer. If 'minimized' is 1 then the layer
        should be minimized, and for a value of 0 it should regain its normal size.
        """
        # store new value
        self.minimized = minimized

        print("FloatingWindowLayer.setMinimized:", self.minimized)

    def handleLeftMousePressed(self, x, y):
        """
        Handles a press in the layer with the left mouse button. Returns a suitable state if
        needed. Checks weather the border has been clicked, and if so starts a state WindowMove,
        which is active as long as the left mouse button is pressed (the window is dragged).

        If the contents is clicked a method that subclasses can overload is called to handle it. If
        the click is outside the window nothing is done.

        The return value should be a tuple (state,handled) where the former is a new state if
        needed, or None if no new state is needed. The latter parameter is a flag indicating weather
        the event was handled or not. This method may have handled an event although a new state was
        not returned.
        """

        # was the move button pressed in the border?
        if self.inBorder(x, y):
            # yes, so activate a new state and give in the current state as a param so that it can
            # be restored later. this is really quite ugly, and should maybe be fixed some day to
            # something a little less hackish
            return window_move.WindowMove(self, scenario.current_state), 1

        # no, was the contents clicked?
        elif self.x <= x <= self.x + self.width and self.y <= y <= self.y + self.height:
            # contents clicked, call optional handler
            handled = self.handleContentsClick(x, y)

            # it was maybe handled, return no new state and the 'handled' flag
            return None, handled

        # nothing clicked, no new state needs to be activated and the event was not handled
        return None, 0

    def handleMidMousePressed(self, x, y):
        """
        Handles a press in the layer with the mid mouse button. Checks if the border was clicked,
        and if so the minimization status of the layer is toggled. Returns a handled status to the
        caller.
        """
        # was the move button pressed in the border?
        if self.inBorder(x, y):
            # yes, so set a new minimization status
            self.minimized = 1 - self.minimized

            # is it now being restored?
            if not self.minimized:
                # make sure the window fits on the screen. it may have been moved to the lower edge,
                # which means that we should move it a bit upwards
                if self.y + self.height > scenario.sdl.getHeight():
                    # too low, set new position
                    self.y = scenario.sdl.getHeight() - self.height - Layer.bot.get_height()
            else:
                # being minimized, make sure it stays inside screen
                borderheight = self.getBorderWidth()[1]
                if self.y < borderheight:
                    self.y = borderheight

            # repaint the playfield now that it has changed
            handled = scenario.playfield.needRepaint()

            # it was maybe handled, return no new state and the 'handled' flag
            return None, handled

        # nothing clicked, no new state needs to be activated and the event was not handled
        return None, 0

    def handleContentsClick(self, x, y):
        """
        This callback is activated if the player clicks within the layer area, ie. inside the
        borders. Layers that want to handle this event can do it, but this default version does
        nothing at all. Returns 0 by default to indicate that nothing actually happened.
        """
        return 0

    def inBorder(self, click_x, click_y):
        """
        Checks weather the mouse click at (x,y) was on the border. Returns 1 if the border was
        clicked and 0 if not.
        """

        # get the border dimensions
        borderwidth, borderheight = self.getBorderWidth()

        # get the coordinates
        x = self.x
        y = self.y
        width = self.width

        # are we minimized?
        if self.isMinimized():
            # yes, so use a 0 height
            height = 0
        else:
            # not minimized
            height = self.height

        # upper border?
        if x - borderwidth <= click_x <= x + width + borderwidth and y - borderheight <= click_y <= y:
            # upper border hit
            return 1

        # lower border?
        elif x - borderwidth <= click_x <= x + width + borderwidth and \
                y + height <= click_y <= y + height + borderheight:
            # lower border hit
            return 1

        # left border?
        elif x - borderwidth <= click_x <= x and y <= click_y <= y + height:
            # left border hit
            return 1

        # right border?
        elif x + width <= click_x <= x + width + borderwidth and y <= click_y <= y + height:
            # left border hit
            return 1

        # not on border
        return 0
