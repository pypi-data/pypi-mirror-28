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

import civil.ui.messages as messages
from civil import constants
from civil import properties
from civil.model import scenario
from civil.server.action import action, cease_fire_act, surrender_act, quit_act
from civil.serialization.scenario_writer import ScenarioWriter


class State:
    """
    This class is the base class for all states in the game. A state is a state :-) of the game that
    handles all input and determines what to do when something happens. An event can make a state
    activate another state, thus forming a state machine. This is done by having a event handler
    return a new state if needed.

    Each state is required to provide:

    * name.
    * a keymap of handlers for pressed keys.
    * overridden methods for the types of events it wants to receive.
    * a cursor if needed.
    * a map with custom event handlers.
    
    If a handler should activate another state the new state should be returned by the event
    handler. A return value of None indicates that no new state should be activated.

    When creating subclasses of this class always use fully qualified import paths, such as
    state.basestate, and use the full names in code, such as state.basestate.State. This avoids
    circular imports, but makes the code a little longer to write.

    Custom events are events that are internally posted onto the pygame event queue. They are
    handled by this class which will call registered callbacks if needed. The subclasses register
    callbacks by adding values to the member 'self.customevents'. The key should be the name of the
    event in lowercase, and the value should be the callback.
    
    States can have a custom help page shown when the player activates the online help. This is done
    by setting a member to the name of the help file name, see below for more docs.
    """

    # define a shared base cursor
    defaultcursor = None

    def __init__(self):
        """
        Initializes the instance. Sets default values for all needed members.
        """

        # set defaults
        self.name = "unknown"

        # set a default help file topic. This is the name of the wanted help file, without any path
        # and without the '.xml' extension. subclasses can set this to something custom.
        self.help_topic = 'index'

        # do we have a default cursor already?
        if not State.defaultcursor:
            # nope, so load it. First get the file names
            datafile = properties.state_base_cursor_data
            maskfile = properties.state_base_cursor_mask

            # now load it
            State.defaultcursor = pygame.cursors.load_xbm(datafile, maskfile)

        # no mouse motion wanted by default. if wanted then set this in the subclass' constructor
        self.wantmousemotion = 0

        # setup a default keymap of stuff that is available to all subclasses and thus all states in
        # the game. subclasses with custom needs should create an own version of this map

        # by default we have no popup menu keymap and thus no popup menu at all
        self.menukeymap = ()

        # define the help texts for the default keymap
        self.helptext = ["These are the currently available keys:",
                         " ",
                         "arrow keys - scroll map",
                         "0 - send message to player",
                         "F1 - help browser",
                         "F2 - show keyboard shortcuts",
                         "F3 - select shown features",
                         "F4 - show army status",
                         "F5 - toggle minimap on/off",
                         "F6 - toggle unit info window on/off",
                         "F7 - toggle unit orders window on/off",
                         "F8 - toggle unit line of sight on/off",
                         "F9 - toggle audio controls window on/off",
                         "F10 - toggle fullscreen mode",
                         "F11 - set screen resolution",
                         "F12 - save a screenshot",
                         " ",
                         # "Alt e - end turn/action",
                         "Alt s - save game",
                         "Alt c - request a cease fire",
                         "Alt u - surrender the battle",
                         "Alt g - toggle graphics debugging",
                         "Alt q - quit the game"]

        # build up the admin menu. this is the extra commands that can be triggered from the little
        # admin menu in the unit info window
        self.adminmenukeymap = [('send message to player', K_0, KMOD_NONE),
                                ('help browser', K_F1, KMOD_NONE),
                                ('keyboard shortcuts', K_F2, KMOD_NONE),
                                ('select shown features', K_F3, KMOD_NONE),
                                ('show army status', K_F4, KMOD_NONE),
                                ('toggle minimap on/off', K_F5, KMOD_NONE),
                                ('toggle unit info window on/off', K_F6, KMOD_NONE),
                                ('toggle unit orders window on/off', K_F7, KMOD_NONE),
                                ('toggle unit LOS outline', K_F8, KMOD_NONE),
                                ('toggle audio controls', K_F9, KMOD_NONE),
                                ('toggle fullscreen mode', K_F10, KMOD_NONE),
                                ('set screen resolution', K_F11, KMOD_NONE),
                                ('save a screenshot', K_F12, KMOD_NONE),

                                ('check terrain type', K_c, KMOD_SHIFT),

                                ('save game', K_s, KMOD_ALT),
                                ('request a cease fire', K_c, KMOD_ALT),
                                ('surrender the battle', K_u, KMOD_ALT),
                                ('quit the game', K_q, KMOD_ALT)]

        # setup a default keymap of stuff that is available to all subclasses and thus all states in
        # the game. subclasses with custom needs should create an own version of this map
        self.keymap = {(K_UP, KMOD_NONE): self.scrollUp,
                       (K_DOWN, KMOD_NONE): self.scrollDown,
                       (K_LEFT, KMOD_NONE): self.scrollLeft,
                       (K_RIGHT, KMOD_NONE): self.scrollRight,

                       (K_0, KMOD_NONE): self.chat,
                       (K_1, KMOD_ALT): self.toggleAIDebug,

                       (K_F1, KMOD_NONE): self.helpBrowser,
                       (K_F2, KMOD_NONE): self.help,
                       (K_F3, KMOD_NONE): self.showFeaturesDialog,
                       (K_F4, KMOD_NONE): self.showArmyStatus,
                       (K_F5, KMOD_NONE): self.toggleMinimap,
                       (K_F6, KMOD_NONE): self.toggleInfoView,
                       (K_F7, KMOD_NONE): self.toggleOrdersView,
                       (K_F8, KMOD_NONE): self.toggleLosOutline,
                       (K_F9, KMOD_NONE): self.toggleAudioControls,
                       (K_F10, KMOD_NONE): self.toggleFullscreen,
                       (K_F11, KMOD_NONE): self.setResolution,
                       (K_F12, KMOD_NONE): self.saveScreenshot,

                       (K_c, KMOD_SHIFT): self.checkTerrain,

                       (K_q, KMOD_ALT): self.quit,
                       (K_c, KMOD_ALT): self.ceaseFire,
                       (K_u, KMOD_ALT): self.surrender,
                       (K_s, KMOD_ALT): self.saveGame
                       }

        # are we debugging stuff?
        if properties.debug:
            # yes, add some extra options
            self.adminmenukeymap.append(('debug graphics', K_g, KMOD_ALT))
            self.adminmenukeymap.append(('debug LOS maps', K_d, KMOD_ALT))

            # and the callbacks too
            self.keymap[(K_g, KMOD_ALT)] = self.toggleDebugGfx
            self.keymap[(K_d, KMOD_ALT)] = self.toggleDebugLOS

        # do we have audio available?
        if not scenario.audio.hasAudio():
            # no audio, so don't allow audio to be toggled either
            # del self.adminmenukeymap[K_F8]
            # del self.helptext[9]

            # TODO: plenty to fix here!
            pass

    def getName(self):
        """
        Returns the name of the state. The name is a cleartext readable name meant mainly for
        debugging purposes.
        """
        return self.name

    def setDefaultCursor(self):
        """
        Sets the default cursor for the states. This is a normal arrow that can be used in most
        parts of the game. States that don't need an own cursor can call this method to make sure
        the default one is used.
        """
        # set system default cursor
        pygame.mouse.set_cursor(*State.defaultcursor)

    def callMeSoon(self):
        """
        Posts a dummy event so that we will be called soon. Used by various states which
        can't return anything in the constructor.
        """
        pygame.event.post(pygame.event.Event(pygame.NOEVENT))

    def handleEvent(self, event):
        """
        Handles all events. Calls handlers depending on the type of event. Subclasses of this
        class can override the needed handlers.
        """

        # get the event type. this may be needed for a workaround for keyboard handling on osx. and
        # it doesn't harm to get rid of a lot of "dots" either
        type = event.type

        # do we have a mouse motion?
        if type == MOUSEMOTION:
            # yep, handle it
            return self.handleMouseMotion(event)

        # do we have a mouse button pressed?
        if type == MOUSEBUTTONDOWN:
            # yep, handle the proper button
            if event.button == 1:
                # left button
                return self.handleLeftMousePressed(event)

            elif event.button == 2:
                # middle button
                return self.handleMidMousePressed(event)

            elif event.button == 3:
                # right button
                return self.handleRightMousePressed(event)

        # do we have a mouse button released?
        if type == MOUSEBUTTONUP:
            # yep, handle it
            if event.button == 1:
                # left button
                return self.handleLeftMouseReleased(event)

            elif event.button == 2:
                # middle button
                return self.handleMidMouseReleased(event)

            elif event.button == 3:
                # right button
                return self.handleRightMouseReleased(event)

        # do we have a key pressed pressed?
        if type == KEYDOWN:
            # yep, handle it
            return self.handleKeyDown(event)

        # do we have a key released pressed?
        if type == KEYUP:
            # yep, handle it
            return self.handleKeyUp(event)

        # print "State.handleEvent: we got an event we didn't want to handle:", event

        # we gor this far, so nothing we wanted to handle
        return None

    def handleMouseMotion(self, event):
        """
        This method handles mouse motion events. It is only activated if mouse motion events are
        wanted, i.e. when the middle button is pressed. Checks the movement of the mouse to see if
        it has moved more than 10 pixels in any direction. If so the playfield will be scrolled and
        the repainted. 

        Returns None to indicate that a new state should not be activated.
        """

        # get new updated mouse position
        x, y = pygame.mouse.get_pos()

        # do we have any reason to do anything?
        if abs(x - self.mousepos[0]) > 10 or abs(y - self.mousepos[1]) > 10:
            # scrolling is needed

            # get the deltas
            delta_x = (self.mousepos[0] - x) / 10
            delta_y = (self.mousepos[1] - y) / 10

            # scroll the playfield and get the flags that indicate weather we need to repaint or not
            repaint1 = scenario.playfield.setoffset_x(scenario.playfield.getoffset_x() - delta_x)
            repaint2 = scenario.playfield.setoffset_y(scenario.playfield.getoffset_y() - delta_y)

            # is a repaint needed?
            if repaint1 or repaint2:
                # repaint the playfield now that it has changed
                scenario.playfield.needRepaint()

            # store new last position
            self.mousepos = (x, y)

        return None

    def handleLeftMousePressed(self, event):
        """
        Default method for handling when the left mousebutton is pressed. Overload if you want to
        handle this event. This default handler tries to see if any playfield layer wants to handle
        the click, and if not it tries to activate a unit under the click position..
        """

        # TODO: fix this using some proper mechanism
        from . import menu

        # find the question layer
        unit_info_layer = scenario.playfield.getLayer("info_view")

        # is the menu button in that layer clicked?
        if unit_info_layer.isMenuButtonClicked(event.pos):
            # it's clicked, so activate a state to handle the menu
            key, modifier = menu.Menu(self.adminmenukeymap, event.pos).run()

            # did we get a valid key?
            if key is not None:
                # precautions
                if (key, modifier) not in self.keymap:
                    # no such key, so we've somehow got a modifier that has no callback
                    print("State.handleLeftMousePressed: no callback for: ", (key, modifier))

                # get the proper callback. we assume the modifier is ok
                return self.keymap[(key, modifier)]()

        # not in the menu, get the pos of the click
        x, y = event.pos

        # get all layers from the playfield that are clickable
        clickable = scenario.playfield.getClickableLayers()

        # loop over all clickable layers and see if any of them wants to handle the click
        for layer in clickable:
            # is it visible? we don't allow invisible layers to be clicked
            if not layer.isVisible():
                # hidden, so ignore it
                continue

            # handle it and see weather it did something with it. if it has handled the click we stop
            # the traversing
            newstate, handled = layer.handleLeftMousePressed(x, y)

            # did we get a new state?
            if newstate:
                # it handled it and gave us a new state
                return newstate

            # ok, no new state, was it handled anyway?
            if handled:
                # yes, it was handled, we're done
                return

        # get the clicked global coordinate
        globalx, globaly = self.toGlobal(event.pos)

        # activate a unit (if any) at the position and return a possible new state
        return self.activateUnit(globalx, globaly, x, y)

    def handleLeftMouseReleased(self, event):
        """
        Dummy method for handling when the lef mousebutton is released. Overload if you want to
        handle this event. This default handler does nothing and returns None to indicate
        that a new state should not be activated.
        """
        return None

    def handleMidMousePressed(self, event):
        """
        Dummy method for handling when the middle mousebutton is pressed. Overload if you want to
        handle this event. This default handler does nothing and returns None to indicate
        that a new state should not be activated.
        """

        # get the pos of the click
        x, y = event.pos

        # get all layers from the playfield that are clickable
        clickable = scenario.playfield.getClickableLayers()

        # loop over all clickable layers and see if any of them wants to handle the click
        for layer in clickable:
            # is it visible? we don't allow invisible layers to be clicked
            if not layer.isVisible():
                # hidden, so ignore it
                continue

            # handle it and see weather it did something with it. if it has handled the click we stop
            # the traversing
            newstate, handled = layer.handleMidMousePressed(x, y)

            # did we get a new state?
            if newstate:
                # it handled it and gave us a new state
                return newstate

            # ok, no new state, was it handled anyway?
            if handled:
                # yes, it was handled, we're done
                return

        # we want mouse motion events now
        self.wantmousemotion = 1

        # get current mouse position. this is the initial from which the drag is started
        self.mousepos = pygame.mouse.get_pos()

        return None

    def handleMidMouseReleased(self, event):
        """
        This method provides default handling of a middle mouse pressed events. The default is to
        start scrolling the map when the mouse is moved while the button is kept pressed.

        Returns None to indicate that a new state should not be activated.
        """

        # no more mouse motion events
        self.wantmousemotion = 0

        return None

    def handleRightMousePressed(self, event):
        """
        This method provides default handling of a right mouse press events. Shows a popup menu
        if one is available.
        """

        # do we have a menu at all?
        if self.menukeymap == ():
            # no keymap, so why show the menu then
            return None

        # TODO: fix this using some proper mechanism
        from . import menu

        # just activate a new state
        key, modifier = menu.Menu(self.menukeymap, event.pos).run()

        # did we get a valid key?
        if key is None:
            # no key
            return None

        # call the proper callback
        return self.keymap[(key, modifier)]()

    def handleRightMouseReleased(self, event):
        """
        Dummy method for handling when the right mousebutton is released. Overload if you want to
        handle this event. This default handler does nothing and returns None to indicate
        that a new state should not be activated.
        """
        return None

    def handleKeyDown(self, event):
        """
        Handles a key down event. Checks which key was pressed and weather the state has a handler for
        that particular key. Returns a possible new state or None if no new state should be
        activated.
        """

        # get key and active modifiers
        key = event.key
        mods = pygame.key.get_mods()

        # make sure we don't get the num lock key in here. it screws up all the modifier checks
        # below, as it's a modifier itself
        if mods & KMOD_NUM:
            # yeah, we have it, clear it
            mods = mods ^ KMOD_NUM

        # fix left/right shift/alt so that we have the proper modifier, not the Lx or Rx ones
        if mods & KMOD_SHIFT:
            mods = KMOD_SHIFT

        elif mods & KMOD_ALT:
            mods = KMOD_ALT

        # now, do we have a callback for the combination of key/modifier that we currently have?
        if (key, mods) in self.keymap:
            # yes, call the callback and return whatever new state it gives
            return self.keymap[(key, mods)]()

        # no key we're interested in
        return None

    def handleKeyUp(self, event):
        """
        Handles a key up event. Does nothing and returns None to indicate that a new state should


 """
        return None

    def handleTimerEvent(self):
        """
        Handles a timer event when the state has enabled timers and a timer fires. This should be 
        overridden by subclasses to provide the needed code.
 """
        # by default we do nothing
        raise NotImplementedError("State.handleTimerEvent: this method should be overridden")

    def handleAction(self, action):
        """
        Event handler that lets a state handle an incoming action packet. The update has been
        read from the network connection and at this point already executed. States that need to be
        able to react to some action can override this method to provide the custom handling. But
        care should be taken to handle all action that can come, or then call this method to handle
        unknown/uninteresting action. This method will return a new state if needed and None if


 """

        # do nothing by default, no new state needed
        return None

    def wantMouseMotion(self):
        """
        This method returns 1 if the state is interested in receiving mouse motion events and 0
        if not. This system is done because having to track and handle each mose movement consumnes
        a lot of resources and slows down Civil a lot. So, a state that wants the mouse movements
        should override this method to return 1. This implementation defaults to returning 0 (set in
        the constructor).
        """

        # return the value
        return self.wantmousemotion

    def latestMousemove(self, event):
        """
        If the given event is a mouse motion event, take all those events and only use the last
        one.  This means the engine doesn't get every single mouse motion event, and makes


  """

        # mouse motion? if so get only the last one
        if event.type == MOUSEMOTION:
            mousemoves = pygame.event.get(MOUSEMOTION)

            # more events than only one?
            if mousemoves:
                # get only the last one
                event = mousemoves[-1]

        # return whatever event we got
        return event

    def toGlobal(self, xxx_todo_changeme):
        """
        Helper method to convert a position on the playfield given as a tuple (x,y) to its
        correct global position. The playfield may be offset a certain amount, and this amount needs
        to be added to the passed coordinates. A tuple (x,y) is returned.
        """
        (x, y) = xxx_todo_changeme
        delta_x = properties.hex_delta_x
        delta_y = properties.hex_delta_y

        # get the tuple with the current playfield offset (in hexes)
        offset_x, offset_y = scenario.playfield.getOffset()

        # calculate the minimum and maximum x-, y-coordinates for the visible area and simply return
        # them. These values are in pixels, not hexes
        min_x = offset_x * delta_x
        min_y = offset_y * delta_y

        # we're done, return the data
        return x + min_x, y + min_y

    def scrollUp(self):
        """
        Handles the event when the user presses the 'up' arrow keys. This callback will scroll
        the map up and repaint it if needed.
        """
        # perform the scrolling and see weather we actually did anything
        if scenario.playfield.setoffset_y(scenario.playfield.getoffset_y() - 1):
            # repaint the playfield now that it has changed
            scenario.playfield.needRepaint()

        # no new state
        return None

    def scrollDown(self):
        """
        Handles the event when the user presses the 'down' arrow keys. This callback will scroll
        the map down and repaint it if needed.
        """
        # perform the scrolling and see weather we actually did anything
        if scenario.playfield.setoffset_y(scenario.playfield.getoffset_y() + 1):
            # repaint the playfield now that it has changed
            scenario.playfield.needRepaint()

        # no new state
        return None

    def scrollLeft(self):
        """
        Handles the event when the user presses the 'left' arrow keys. This callback will scroll
        the map left and repaint it if needed.
        """
        # perform the scrolling and see weather we actually did anything
        if scenario.playfield.setoffset_x(scenario.playfield.getoffset_x() - 1):
            # repaint the playfield now that it has changed
            scenario.playfield.needRepaint()

        # no new state
        return None

    def scrollRight(self):
        """
        Handles the event when the user presses the 'right' arrow keys. This callback will scroll
        the map right and repaint it if needed.
        """
        # perform the scrolling and see weather we actually did anything
        if scenario.playfield.setoffset_x(scenario.playfield.getoffset_x() + 1):
            # repaint the playfield now that it has changed
            scenario.playfield.needRepaint()

        # no new state
        return None

    def toggleObjectives(self):
        """
        This callback is triggered when the player presses the key that is used to toggle the
        objectives on/off. If the playfield layer which shows objectives is visible it is hidden and
        vice versa.
        """
        # find the layer and toggle the visibility
        scenario.playfield.toggleVisibility(scenario.playfield.getLayer("objectives"))

    def toggleLabels(self):
        """
        This callback is triggered when the player presses the key that is used to toggle the
        labels on/off. If the playfield layer which shows labels is visible it is hidden and
        vice versa.
        """
        # find the layer and toggle the visibility
        scenario.playfield.toggleVisibility(scenario.playfield.getLayer("locations"))

    def toggleCommanders(self):
        """
        This callback is triggered when the player presses the key that is used to toggle the
        showing of commanders on/off. If the playfield layer which shows superior commanders is
        visible it will be hidden and vice versa.
        """

        # find the layer and toggle the visibility
        scenario.playfield.toggleVisibility(scenario.playfield.getLayer("unit_commanders"))

    def toggleWeaponRanges(self):
        """
        This callback is triggered when the player presses the key that is used to toggle the
        showing of weapon ranges on/off. If the layer which shows the info is visible it will be
        hidden and vice versa.
        """

        # find the layer and toggle the visibility
        scenario.playfield.toggleVisibility(scenario.playfield.getLayer("weapon_ranges"))

    def toggleOrders(self):
        """
        This callback is triggered when the player presses the key that is used to toggle the
        visualization of unit orders on/off. If the playfield layer which shows orders is visible it
        is hidden and vice versa.
        """

        # find the layer and toggle the visibility
        scenario.playfield.toggleVisibility(scenario.playfield.getLayer("unit_orders"))

    def toggleLosOutline(self):
        """
        Toggles the LOS outline for a unit on/off.
        """

        # find the layer and toggle the visibility
        scenario.playfield.toggleVisibility(scenario.playfield.getLayer("unit_los"))

    def toggleOwnUnits(self):
        """
        This callback is triggered when the player presses the key that is used to toggle the
        own units on/off. If the playfield layer which shows the own units is visible it is hidden
        and vice versa. The layer showing enemy units is not affected.
        """
        # find the layer and toggle the visibility
        scenario.playfield.toggleVisibility(scenario.playfield.getLayer("own_units"))

    def toggleEnemyUnit(self):
        """
        This callback is triggered when the player presses the key that is used to toggle the
        enemy units on/off. If the playfield layer which shows the enemy units is visible it is
        hidden and vice versa. The layer showing own units is not affected.
        """
        # find the layer and toggle the visibility
        scenario.playfield.toggleVisibility(scenario.playfield.getLayer("enemy_units"))

    def toggleAIDebug(self):
        """
        Toggles the AI debugging layers on and off. If they are shown they will be hidden and
        vice versa. These layers should normally not be visible.
        """
        # find the layer and toggle the visibility
        scenario.playfield.toggleVisibility(scenario.playfield.getLayer("ai_debug"))

    def toggleOrdersView(self):
        """
        This callback is triggered when the player presses the key that is used to toggle the
        window which shows the unit orders.If the playfield layer which shows the info is visible it
        is hidden and vice versa.
        """

        # find the layer and toggle the visibility
        scenario.playfield.toggleVisibility(scenario.playfield.getLayer("orders_view"))

    def toggleInfoView(self):
        """
        This callback is triggered when the player presses the key that is used to toggle the
        window which shows the unit info. If the playfield layer which shows the info is visible it
        is hidden and vice versa.
        """

        # find the layer and toggle the visibility
        scenario.playfield.toggleVisibility(scenario.playfield.getLayer("info_view"))

    def toggleMinimap(self):
        """
        This callback is triggered when the player presses the key that is used to toggle the
        window which shows the minimap. If the playfield layer which shows the minimap is visible it 
        is hidden and vice versa.
 """

        # find the layer and toggle the visibility
        scenario.playfield.toggleVisibility(scenario.playfield.getLayer("minimap"))

    def toggleAudioControls(self):
        """
        his callback is triggered when the player presses the key that is used to toggle the
        window which shows the audio controls. If the window layer which shows the controls is
        visible it is hidden and vice versa.
        """

        # find the layer and toggle the visibility
        scenario.playfield.toggleVisibility(scenario.playfield.getLayer("audio"))

    def toggleMusic(self):
        """
        This callback is triggered when the player presses the key that is used to toggle the
        music on/off. If music is playing it will be paused and vice versa. If no music is
        available this method does nothing.
        """

        # are we playing music?
        if not scenario.audio.isPaused():
            # pause music
            scenario.audio.pauseMusic()

            # add message so that the player knows what happened
            scenario.messages.add("Music paused")

        else:
            # unpause it
            scenario.audio.unpauseMusic()

            # add message so that the player knows what happened
            scenario.messages.add("Music resumed")

    def showFeaturesDialog(self):
        """
        Shows the dialog where the player can select which features should be shown and which
        should be hidden. This makes it easy for the player to customize the playing
        environment. This callback will activate the internal state 'ToggleFeatures'.
        """

        # this is kind of a hack to avoid circular import
        # TODO: fix this using some proper mechanism
        from . import toggle_features

        # just activate a new state
        return toggle_features.ToggleFeatures(self)

    def showArmyStatus(self):
        """
        Shows the dialog where the player can get an overview of the army status. It shows all
        organizations and all losses. This callback will activate the internal state 'ArmyStatus'.
        """

        # this is kind of a hack to avoid circular import
        # TODO: fix this using some proper mechanism
        from . import army_status

        # just activate a new state
        return army_status.ArmyStatus(self)

    def setResolution(self):
        """
        Asks the player for a resolution and tries to set it.
        """
        from . import set_resolution
        # just activate a new state
        return set_resolution.SetResolution(self)

    def saveScreenshot(self):
        """
        Saves the current screen as a screenshot. The name of the screenshot will be asked from
        the player.
        """
        # get the file_name
        file_name = self.askInput(["Enter name of BMP screenshot"], "snapshot.bmp")

        # did we get anything at all? If the input was cancelled then we get a None name
        if file_name is None or file_name == '':
            # no name given, abort this silliness
            scenario.messages.add("Save screenshot ignored")
            return None

        # now do paint the playfield. note that this is really quite ugly, but it should be done in
        # order to get rid of the dialog before the screenshot is saved.
        scenario.playfield.paint()

        # and update the display to reflect all changes
        scenario.sdl.update()

        # do it
        scenario.sdl.saveScreenshot(file_name)

    def checkTerrain(self):
        """
        Callback triggered when the user presses the key 'C' for checking terrain at a given map
        position. Activates the state 'CheckTerrain'.
        """

        # TODO: fix this using some proper mechanism
        from . import check_terrain

        # just activate a new state
        return check_terrain.CheckTerrain(self)

    def saveGame(self):
        """
        Callback triggered when the user presses the 'Alt + s' keys. Asks the player weather
        he/she wants to save the game. If the question is accepted another dialog is shown where the
        user should enter a name for the game. If the input name is empty the saving is cancelled.
        """

        # aks for confirmation
        if not self.askQuestion(['Do you want to save the game?']):
            # saving ignored
            scenario.messages.add("Save ignored")
            return None

        # ok, get an input file_name
        name = self.askInput(["Enter name of save file"], "test")

        # did we get anything at all? If the input was cancelled then we get a None name
        if name is None or name == '':
            # no name given, abort this silliness
            scenario.messages.add("No file_name, save ignored")
            return None

        # clean up the name to avoid spaces and slashes
        name = name.replace(' ', '_')
        name = name.replace('/', ' ')

        # get the dir where we should save
        name = properties.path_saved_games + '/%s.xml.gz' % name

        # try to write
        if not ScenarioWriter().write(name):
            # oops, failed...
            scenario.messages.add("Failed to save game!", messages.ERROR)
        else:
            # save was ok
            scenario.messages.add("Game saved ok")

        # no new state needed
        return None

    def toggleDebugGfx(self):
        """
        Toggles graphics debugging on/off.
        """
        scenario.playfield.debug_gfx = 1 - scenario.playfield.debug_gfx
        scenario.playfield.getLayer("terrain").invalidateTerrain()
        scenario.playfield.needRepaint()
        scenario.playfield.paint()
        scenario.sdl.update()

    def toggleDebugLOS(self):
        """
        Toggles debugging of the internal LOS map on/off. This will show/hide the floating layer
        with the LOS image.
        """
        # precautions
        if not properties.debug:
            # not debugging, go away, we don't have such a layer then
            return

        # find the layer and toggle the visibility
        scenario.playfield.toggleVisibility(scenario.playfield.getLayer("los_debug"))

    def quit(self):
        """
        Callback triggered when the user presses the 'Alt + q' keys. Asks the player weather
        he/she really wants to quit. if the player agrees to quit then an immediate update is sent
        to the other player, and the main event loop is ended.
        """

        # ask the player first
        if self.askQuestion(['Do you really want to quit?']):
            # the answer to our quit question was accepted, create a new 'quit' action
            cmd = quit_act.QuitAct()

            # send off a command over the net
            scenario.connection.send(cmd.toString())

            # and we're no longer player
            scenario.playing = constants.GAME_ENDED

        # no new state needed
        return None

    def ceaseFire(self):
        """
        Callback triggered when the user presses the 'Alt + c' keys.  Asks the player weather
        he/she really wants to cease fire. If the question is accepted then an immediate update is
        sent to the other player, asking weather he/she/it will accept the cease fire. This method
        thus does not do anything more then ask the question and send away an immediate update.
        """

        # ask the player first
        if self.askQuestion(['Do you really want to offer a cease fire?']):
            # the answer to our cease fire question was accepted, create a new 'cease fire' action
            cmd = cease_fire_act.CeaseFireAct(scenario.local_player_id)

            # send it to the server, the server will inform us later if anything happened
            scenario.connection.send(cmd.toString())

            # add the message we have to the messages
            scenario.messages.add("Cease fire offer sent")

        # not accepted
        return None

    def surrender(self):
        """
        Callback triggered when the user presses the 'Alt + u' keys. Asks the player weather
        he/she really wants to surrender. If the player still wants to surrender an immediate update
        is sent to the other player. The same update is added to the local queue and handled after
        this callback is done, thus ending the game.
        """

        # ask the player first
        if self.askQuestion(['Do you really want to surrender?']):
            # the answer to our surrender question was accepted, create a new 'surrender' immediate command 
            cmd = surrender_act.SurrenderAct(scenario.local_player_id)

            # send it to the server, the server will inform us later if anything happened
            scenario.connection.send(cmd.toString())

        # no new state needed
        return None

    def help(self):
        """
        Callback triggered when the user presses the 'F1' key. This method will bring up a help
        dialog that displays the currently available keys.
        """

        from . import help

        # do we have any help texts?
        if self.helptext is None or self.helptext == []:
            # no help available
            print("State.help: no help")
            return None

        # create and return a new state showing our labels
        return help.Help(self.helptext, self)

    def helpBrowser(self):
        """
        Callback triggered when the user presses the 'F1' key. This method will bring up a help
        browser dialog that displays a browsable help text.
        """

        # this is kind of a hack to avoid circular import.
        # TODO: fix this using some proper mechanism
        from . import help_browser

        # Avoid multiple help browsers
        # This should not be needed anymore as we don't allow the help keys to be pressed anymore
        # if isinstance(self, help_browser.HelpBrowser):
        #    return None

        # create and return a new state for browsing the help
        return help_browser.HelpBrowser(self)

    def chat(self):
        """
        Callback triggered when the player presses the '0' key to send a chat message. Shows a
        small window where a message may be typed in.
        """

        from . import chat

        # create and return a new state showing our labels
        return chat.Chat(self)

    def toggleFullscreen(self):
        """
        Toggles fullscreen display on and off. If the game is in fullscreen mode then windowed
        mode is restored and vice versa.
        """

        # do the toggle
        if not pygame.display.toggle_fullscreen():
            # oops, failed
            scenario.messages.add('failed to toggle fullscreen mode')

    def showMessage(self, labels):
        """
        This method is a helper method for showing simple message to the player in a centered
        dialog. The dialog has an 'Ok' button for closing it. It will enter the state 'Message'. The
        parameter 'labels' is a list of lines that make up the question.

        WARNING: This method will totally grab all input and event handling of the entire
        application, no other events are handled while the dialog is shown. The method has no
        spacial return value.
        """

        from . import message

        # create and run the question, returning the flag indicating the answer
        return message.Message(labels).run()

    def askQuestion(self, label):
        """
        This method is a helper method for asking a question from the user. It will enter the
        state 'Question' where the passed question text will be presented to the user in a window
        along with 'Ok' and 'Cancel' buttons. The parameter 'question' is a list of lines that make
        up the question.

        WARNING: This method will totally grab all input and event handling of the entire
        application, no other events are handled while the dialog is shown. The return value from
        this method is 1 to indicate an accepted dialog and 0 for a rejected one.
        """

        from . import question

        # create and run the question, returning the flag indicating the answer
        return question.Question(label).run()

    def askInput(self, label, default=""):
        """
        This method is a helper method for asking the user to input a string. It will activate a
        state 'Input' where the passed question label will be presented to the user in a window
        along with 'Ok' and 'Cancel' buttons and a default text. The parameter 'question' is a list
        of lines that make up the question.

        WARNING: This method will totally grab all input and event handling of the entire
        application, no other events are handled while the dialog is shown. The return value from
        this method is a string to indicate an accepted dialog and None for a rejected one.
        """

        from . import input

        # create and run the question, returning the flag indicating the answer
        return input.Input(label, default).run()

    def setSelectedUnit(self, unit, clearfirst=1):
        """
        This method sets 'unit' as a selected unit. It modifies the global list of selected units
        in the following way:

        * add the unit to it if the list is empty
        * append the unit if the list is not empty but contains units of the same owner and
          'clearfirst' is false.
        * clears the list and add the unit if the list is not empty and contains units of another
          owner OR clearfirst is true.
        """

        # is the list empty?
        if not scenario.selected:
            # empty, just add it
            scenario.selected.append(unit)

        # not empty, is the first unit owned by the same owner and we're not instructed to first
        # clear the list?
        elif scenario.selected[0].getOwner() == unit.getOwner() and not clearfirst:
            # This check is needed
            if not unit in scenario.selected:
                # same owner, just append
                scenario.selected.append(unit)

        else:
            # another owner, clear list first and add the unit
            scenario.selected = [unit]

    def getSelectedUnit(self):
        """
        Returns the currently selected unit.
        """
        # get the first selected unit, if he have any
        if len(scenario.selected) > 0:
            return scenario.selected[0]

        # no selected units
        return None

    def getSelectedUnits(self):
        """
        Returns all currently selected units as a list.
        """
        return scenario.selected

    def removeSelectedUnit(self, unit):
        """
        Removes 'unit' from the selected units if it exists there.
        """
        # is it selected?
        if unit in scenario.selected:
            # yep, remove
            scenario.selected.remove(unit)

    def isUnitSelected(self, unit):
        """
        Returns 1 if 'unit' is already selected and 0 if it's not.
        """
        # is it selected?
        if unit in scenario.selected:
            # yep
            return 1

        # not selected
        return 0

    def clearSelectedUnits(self):
        """
        Clears all selected units. This means that no unit is selected anymore. Note
        that users of this should emit units_changed / unit_selected signals.
        """
        # Check if we actually need to do something. This saves us a repaint
        # sometimes
        if not scenario.selected:
            return 0

        # just do it
        scenario.selected = []

        return 1

    def fixSelected(self):
        """
        Common routine to get the next state after playing with selecting units.
        """

        from . import own_unit
        from . import enemy_unit
        from . import idle

        # we have a new selected unit
        newunit = self.getSelectedUnit()

        # do we still have selected units?
        if newunit is None:
            # no selected units anymore
            newstate = idle.Idle()
            newunit = None
        else:
            # is this unit an own unit or enemy unit?
            if newunit.getOwner() == scenario.local_player_id:
                # own player, create and return a new state which manages that unit
                newstate = own_unit.OwnUnit()

            else:
                # enemy unit
                newstate = enemy_unit.EnemyUnit()

                # we have a new selected unit
        scenario.dispatcher.emit('unit_selected', newunit)

        # return new state
        return newstate

    def activateUnit(self, x, y, localx, localy):
        """
        Checks for a unit at the given position or within a short distance from the position and
        actives it. The clicked unit can be a friendly or an enemy unit. if no unit is close enough
        to the clicked position then this method does nothing.

        The parameters localx, localy are the local coordiates, ie. relative to the top left corner


 """

        from . import choose_units

        # get the units
        units = scenario.info.units

        # by default we clear already selected units
        clear = 1

        # check weather we should clear the unit selection first. If shift or control is pressed then
        # we should add to the selection, otherwise it must be replaced
        mods = pygame.key.get_mods()

        # stay with this same state by default and no selected unit
        newstate = None
        newunit = None

        print("State.activateUnit:", x, y, localx, localy)

        # Print hex height
        (hexx, hexy) = scenario.map.pointToHex2((x, y))
        from civil.state import select
        if not scenario.map.isInside(hexx, hexy):
            return select.Select((localx, localy))

        height = scenario.map.getHex(hexx, hexy).getHeight()
        print("Map x %d, y %d, height %d" % (hexx, hexy, height))

        # A choice of candidates when clicking
        choice_candidates = []

        # any mods pressed
        if mods & KMOD_RSHIFT or mods & KMOD_LSHIFT or mods & KMOD_LCTRL or mods & KMOD_RCTRL:
            # one of the modifiers was pressed, so we don't clear
            clear = 0

        # loop over all units
        for unit in list(units.values()):
            # unless the unit is visible it can't be selected
            if not unit.isVisible():
                # not visible, can't do this
                continue

            # get the unit's position
            (unitx, unity) = unit.getPosition()

            # calculate the distance from the given point to the
            distance = abs(x - unitx) * abs(x - unitx) + abs(y - unity) * abs(y - unity)

            # is the distance within picking range?
            if distance < 100:
                choice_candidates.append(unit)

        # Now, go trough the list of units in choice_candidates
        if len(choice_candidates) > 1:
            newstate = choose_units.ChooseUnits(self, choice_candidates, self.getSelectedUnits(), clear)
            return newstate

        # Only clicked one unit
        if len(choice_candidates) == 1:
            unit = choice_candidates[0]
            # is this unit already selected and we're pressing a modifier? if so we should
            # basically toggle the unit selectivity. if it's selected it should be unselected
            # and vice versa
            if self.isUnitSelected(unit) and not clear:
                # yes, it was selected, remove it
                self.removeSelectedUnit(unit)

            else:
                # Is unit already selected, and it is the only unit?
                if self.isUnitSelected(unit) and len(self.getSelectedUnits()) == 1:
                    # Do nothing, saves us a repaint
                    return None

                # not selected, set it as a selected unit
                self.setSelectedUnit(unit, clear)

            # General
            newstate = self.fixSelected()

            # return the new state
            return newstate

        # we got this far, no unit was clicked, so assume we're trying to start a drag selection
        from civil.state import select
        return select.Select((localx, localy))

    def enableTimer(self, ms):
        """
        Enables timer events. Calling this method will make the method timer() get called every
        'ms' milliseconds. Call disableTimer() to disable the timer.
        """
        # just call the method, make no checks
        scenario.dispatcher.registerTimerCallback(ms, self.handleTimerEvent, self)

    def disableTimer(self):
        """
        Disables timer events.
        """
        # just call the method, make no checks
        scenario.dispatcher.deregisterTimerCallback(self)
