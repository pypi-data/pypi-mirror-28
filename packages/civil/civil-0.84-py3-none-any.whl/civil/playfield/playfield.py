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


def compareLayers(layer1, layer2):
    """
    Helper function to compare two layers. The layer with the lower id is considered to be before
    the other layer. This method is used when setting layers visible.
    """

    # less than?
    if layer1.id < layer2.id:
        return -1

    # equal? should not happen
    elif layer1.id == layer2.id:
        return 0

    # ok, it is larger
    else:
        return 1


class Playfield:
    """
    This class defines a drawable area on the screen. It consists of a number of layers that perform
    the actual drawing. This class in itself draws nothing, it just manages the layers. Layers are
    added using the method addLayer().

    When the playfield needs to be repainted this class calls the paint() methods of all registered
    layers, starting from the lowest layer. The lowest layer is the one that was added first. so we
    have a 'first come, first paint' policy here.

    Each layer in the playfield can be set as visible or hidden. This is not done in the Layer
    class, but here, using the method setVisible().

    This class also maintains a list of components that should be animated. The method animate()
    should be called regularly to perform animation. The method animate() then animates all
    components that have been registered as animatable. Normal layers are never animated by
    default. Use addAnimatable() and removeAnimatable() to add/remove components from the animation
    list.

    To minimize unnecessary repaints the method needRepaint() should be called when a part of the
    game wants to have the playfield repainted. This does no actual repaint, just sets a flag. The
    method repaint() then checks that flag and does nothing unless it is set. The method repaint()
    should be called only at one palce in the application, or a few at most to minimize unnecessary
    updates.

    """

    def __init__(self):
        """
        Initializes the playfield.
        """
        # set the layers to be an empty list
        self.layers = []

        # a list of visible layers
        self.visible = []

        # a list of clickable layers
        self.clickable = []

        # current offsets
        self.offset_x = 0
        self.offset_y = 0

        # we do need a repaint
        self.need_repaint = 1
        # Some layers need an internal repaint
        self.need_internal_repaint = 0

        # The dirty areas of the playfield.
        # Currently can contain Rects
        self.dirtyAreas = []

        # Prints out debugging info
        self.debug_gfx = 0

    def paint(self):
        """
        Paints the playfield, using a quite complicated algorithm. XXX

        This method does nothing unless needRepaint() or needInternalRepaint()
        has been called since the last repaint.

        The dirty areas to be painted are taken from self.dirtyAreas, also honoring
        the wishes of any internalPaint requests.
        """

        # do we need an update, or do we just force it?
        if not self.need_repaint and not self.need_internal_repaint and self.dirtyAreas == []:
            # nothing to do here
            return

        if self.debug_gfx:
            print("*** Paint")
        start_ticks = pygame.time.get_ticks()
        dirtyrect = None
        wholearea = pygame.Rect(0, 0, scenario.sdl.getWidth(), scenario.sdl.getHeight())
        # Use the full playfield as the dirty area if a full
        # repaint is required.
        if self.need_repaint:
            # use the full playfield
            scenario.sdl.setClip(wholearea)
            dirtyrect = wholearea
        else:
            # Combine all dirty areas into one big dirty rectangle
            areas = self.dirtyAreas
            if len(areas) > 0:
                dirtyrect = areas.pop()
                while len(areas) > 0:
                    dirtyrect = dirtyrect.union(areas.pop())
                if self.debug_gfx:
                    print("Going to update only one big dirty rectangle")
                    print(dirtyrect)
                scenario.sdl.setClip(dirtyrect)

        # Whatever we do, we won't have any dirty areas left
        self.dirtyAreas = []

        # loop over all layers, and paint only those that need painting

        # NOTE! This code should notice the case when
        # we have set self.need_repaint, layer.need_internal_repaint
        # but do not hit the dirty rectangle. This happens
        # when several layers ask for internal updates.
        for layer in self.visible:
            # Should we paint the whole layer?
            # Check if it collides with the dirty rectangle
            # gathered so far
            layer_rect = layer.getRect()
            addthis = 0
            if layer.need_internal_repaint:
                addthis = 1
            if dirtyrect and dirtyrect.colliderect(layer_rect):
                # Important to zero this so no layer thinks it is only
                # supposed to do an internal repaint
                layer.need_internal_repaint = 0

                # Repaint the dirty rectangle
                if self.debug_gfx:
                    print("Repaint of " + layer.name + " " + str(dirtyrect))
                layer.paint(self.offset_x, self.offset_y, dirtyrect)

            elif layer.need_internal_repaint:
                # Ok, layer has asked for an internal repaint
                if self.debug_gfx:
                    print("Internal repaint of " + layer.name)

                # An internal update is not inside the dirtyrect
                scenario.sdl.setClip(wholearea)
                layer.paint(self.offset_x, self.offset_y, None)

                # Mark the internal repaint done
                layer.need_internal_repaint = 0

            else:
                # Nothing, this was a layer that didn't change,
                # and no layers under it painted anything on
                # top of it
                continue

            # The layer was painted (no matter if it was an internal
            # or a whole repaint), so update the dirtyrect to contain
            # this new layers total area
            # Note the layer's rectangle can be different now
            # BUG if it became smaller, bad refresh
            if addthis:
                add_dirty = pygame.Rect(layer.getRect())
                if dirtyrect:
                    dirtyrect = dirtyrect.union(add_dirty)
                else:
                    dirtyrect = add_dirty
                # Use the updated clipping information
                scenario.sdl.setClip(dirtyrect)

        # turn off clipping
        scenario.sdl.setClip(wholearea)

        # we don't need a repaint anymore
        self.need_repaint = 0
        self.need_internal_repaint = 0
        end_ticks = pygame.time.get_ticks()
        if self.debug_gfx:
            print("Milliseconds " + str(end_ticks - start_ticks))
            print()

    def needRepaint(self, dirtyrect=None):
        """
        Method to register that the playfield needs an update. This merely sets a flag internally
        which is chekced by repaint().
        """

        if self.need_repaint:
            # We are anyway going to repaint all layers.
            return

        # Default behaviour for layers that haven't been updated is
        # to repaint everything
        if dirtyrect is None:
            # set the flag
            self.need_repaint = 1
            return

        # Now the interesting stuff!
        # Add the dirty area to our list. The paint()
        # method will then update these areas.
        self.dirtyAreas.append(dirtyrect)

    def needInternalRepaint(self, layer):
        """
        Method to register that a specific layer requests an internal
        graphical update.
        """
        layer.need_internal_repaint = 1
        self.need_internal_repaint = 1

    def setVisible(self, layer, visible=1):
        """
        Sets 'layer' to be visible if 'visible' is 1 and hidden if it is 0. A hidden layer is not
        repainted at all.
        """
        # hide or show?
        if not visible:
            # hide it, first check if it is visible at all
            if layer in self.visible:
                # repaint needed
                self.needRepaint(layer.getRect())

                # sure is visible, hide
                self.visible.remove(layer)

        else:
            # should be shown, not already shown?
            if not layer in self.visible:
                # sure is hidden, add to the shown layers
                self.visible.append(layer)

                # resort the list so that it is in good order again
                from functools import cmp_to_key
                self.visible.sort(key=cmp_to_key(compareLayers))

                # repaint needed
                self.needRepaint(layer.getRect())

        # set the layer visibility flag too. this is a bit ugly, but should work ok
        layer.visible = visible

    def toggleVisibility(self, layer):
        """
        Toggles the visibility of the layer. If it is visible it is set to hidden and vice
        versa.
        """
        # are we visible?
        if layer in self.visible:
            # hide layer
            self.setVisible(layer, 0)
        else:
            # show layer
            self.setVisible(layer)

    def updateForResolutionChange(self, oldwidth, oldheight, width, height):
        """
        Method used to let the playfield know that the size of the top-level surface (the screen)
        has changed. This method will update the layers so that they can respond to the event.
        """
        # Check that we don't try to paint out of the real map size
        # Happens with small maps and big resolutions
        #
        # This moves the offsets appropriately so we get as much of
        # the map as possible without any user intervention.
        #
        # Note that we still can have problems, so other methods
        # (like terrain_layer.paintTerrain) still have to check
        # against 'visible + offset > mapsize' or, preferably,
        # use getVisibleSizeClamped ()
        visiblesize = self.getVisibleSize()
        mapsize = scenario.map.getSize()
        offset_x, offset_y = self.getOffset()

        # Clamp high
        if visiblesize[0] + offset_x > mapsize[0]:
            offset_x = mapsize[0] - visiblesize[0]
        if visiblesize[1] + offset_y > mapsize[1]:
            offset_y = mapsize[1] - visiblesize[1]
        # Remember to check below too :)
        if offset_x < 0:
            offset_x = 0
        if offset_y < 0:
            offset_y = 0

        print(offset_x, offset_y)
        self.setOffset(offset_x, offset_y)

        # loop over all layers
        for tmplayer in self.layers:
            # update the layer
            tmplayer.updateForResolutionChange(oldwidth, oldheight, width, height)

    def getLayers(self):
        """
        Returns all the available layers in a list.
        """
        return self.layers

    def getLayer(self, name):
        """
        Returns the layer with 'name' from the list of layers. If no layer can be found then None
        is returned.
        """

        # loop over all layers
        for layer in self.layers:
            # is this the correct layer
            if layer.getName() == name:
                # this is it
                return layer

        # no layer found
        return None

    def getClickableLayers(self):
        """
        Returns all the clickable layers in a list. A clickable layer is a layer that can handle clicks.
        """
        return self.clickable

    def addLayer(self, layer, visible=1):
        """
        Adds a new layer as the topmost layer.
        """
        # simply add the new layer
        self.layers.append(layer)

        # is it clickable?
        if layer.isClickable():
            # yep, add to the proper list of those layers. we add it first, so that later layer
            # (most probably also higher up in the layer stack) are put first in the list. this
            # guarantees that when we look for clicks in the layers the topmost layers get checked
            # first 
            self.clickable = [layer] + self.clickable

        # is it visible too?
        if visible:
            # set it to be visible
            self.setVisible(layer)

    def getOffset(self):
        """
        Returns the a tuple with thecurrent  (x,y) offset. The offset is in hexes, not pixels.
        """
        return self.offset_x, self.offset_y

    def getoffset_x(self):
        """
        Returns the current x offset. The offset is in hexes, not pixels.
        """
        return self.offset_x

    def getoffset_y(self):
        """
        Returns the current y offset. The offset is in hexes, not pixels.
        """
        return self.offset_y

    def setOffset(self, offset_x, offset_y):
        """
        Convenience method that sets both offsets at the same time. Same as calling setoffset_x()
        and setoffset_y().
        """
        # use other methods for the grunt work
        change1 = self.setoffset_x(offset_x)
        change2 = self.setoffset_y(offset_y)

        # did we change?
        if change1 or change2:
            # yep
            return 1

        # no change
        return 0

    def setoffset_x(self, offset_x):
        """
        Sets a new current x offset. Negative values are not accepted. The offset is in hexes,
        not pixels. Returns 1 if the offset was actually changed and 0 otherwise.
        """
        # get the visible size
        visible_x = self.getVisibleSizeClamped()[0]
        mapsizex = scenario.map.getsize_x()

        # does the new offset fall within ok limits?
        if offset_x >= 0 and offset_x + visible_x <= mapsizex and offset_x != self.offset_x:
            # yep, store new offset
            self.offset_x = offset_x

            # we did change
            return 1

        # no change
        return 0

    def setoffset_y(self, offset_y):
        """
        Sets a new current y offset. Negative values are not accepted. The offset is in hexes,
        not pixels. Returns 1 if the offset was actually changed and 0 otherwise.
        """
        # get the visible size
        visible_y = self.getVisibleSizeClamped()[1]
        mapsizey = scenario.map.getsize_y()

        # does the new offset fall within ok limits?
        if offset_y >= 0 and offset_y + visible_y <= mapsizey and offset_y != self.offset_y:
            # yep, store new offset
            self.offset_y = offset_y

            # we did change
            return 1

        # no change
        return 0

    def getVisibleSize(self):
        """
        Returns a tuple (x,y) with the visible size of the map. This is the number of hexes in
        both the x- and y-dimensions that can be painted on the map. We add one in both directions
        to make sure we paint a little over the size, in order to avoid jagged edges. The panel will
        be painted over the part the goes to low, and the part that goes to much to the right is
        clipped anyway.
        """

        # get the number of visible icons int x- and y-dimensions
        return (scenario.sdl.getWidth() / properties.hex_size + 1,
                scenario.sdl.getHeight() / properties.hex_delta_y + 1)

    def getVisibleSizeClamped(self):
        """
        Returns the visible size, but clamped so we don't go out
        of the map boundaries.
        """
        # Check that we don't try to paint out of the real map size
        # Happens with small maps and big resolutions

        mapsize = scenario.map.getSize()
        visible_x, visible_y = self.getVisibleSize()
        offset_x, offset_y = self.getOffset()

        # clamp high
        if visible_x + offset_x > mapsize[0]:
            visible_x = mapsize[0] - offset_x
        if visible_y + offset_y > mapsize[1]:
            visible_y = mapsize[1] - offset_y

        return visible_x, visible_y
