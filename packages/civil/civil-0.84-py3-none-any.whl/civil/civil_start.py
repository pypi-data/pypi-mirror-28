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

import getopt
import os
import os.path
import traceback

from pygame.locals import *

from civil.ui import event_loop
from civil import platform
from civil.ui.animation_manager import AnimationManager
from civil.ui.audio_manager import AudioManager
from civil import constants
from civil.ui.dialog import *
from civil.ui.main_dialog import MainDialog
from civil.ui.setup_client import SetupClient
from civil.ui.setup_network import SetupNetwork
from civil.ui.setup_opponent import SetupOpponent
from civil.ui.start_game import StartGame
from civil.ui.messages import Messages
from civil.ui.dispatcher import Dispatcher
# debugging layers
from civil.playfield.ai_debug_layer import AIDebugLayer
from civil.playfield.army_status_layer import ArmyStatusLayer
from civil.playfield.audio_layer import AudioLayer
from civil.playfield.chat_layer import ChatLayer
from civil.playfield.choose_units_layer import ChooseUnitsLayer
from civil.playfield.combat_policy_layer import CombatPolicyLayer
from civil.playfield.commanders_layer import CommandersLayer
from civil.playfield.help_browser_layer import HelpBrowserLayer
from civil.playfield.help_layer import HelpLayer
from civil.playfield.input_layer import InputLayer
from civil.playfield.location_layer import LocationLayer
from civil.playfield.los_debug_layer import LosDebugLayer
from civil.playfield.menu_layer import MenuLayer
from civil.playfield.message_layer import MessageLayer
from civil.playfield.messages_layer import MessagesLayer
from civil.playfield.minimap_layer import MinimapLayer
from civil.playfield.objective_layer import ObjectiveLayer
from civil.playfield.playfield import Playfield
from civil.playfield.question_layer import QuestionLayer
from civil.playfield.selection_layer import SelectionLayer
from civil.playfield.set_resolution_layer import SetResolutionLayer
from civil.playfield.terrain_layer import TerrainLayer
from civil.playfield.toggle_features_layer import ToggleFeaturesLayer
from civil.playfield.unit_info_view_layer import UnitInfoViewLayer
from civil.playfield.unit_layer import UnitLayer
from civil.playfield.unit_los_layer import UnitLosLayer
from civil.playfield.unit_orders_layer import UnitOrdersLayer
from civil.playfield.unit_orders_view_layer import UnitOrdersViewLayer
from civil.playfield.weapon_info_layer import WeaponInfoLayer
from civil.playfield.weapon_range_layer import WeaponRangeLayer
from civil.ui.sdl import SDL


def quit():
    """
    Quits Civil in a civilized manner. Sets the flag informing the poller thread that we are
    going away, quits Pygame and then exits.
    """

    # quit pygame
    pygame.quit()

    # make sure the flag is set too so that the ClientPollerThread can catch it an exit
    scenario.playing = constants.GAME_ENDED

    # finally exit
    sys.exit(0)


def versionToInt(version):
    """
    Returns an integer that matches the passed version string. The string should be in the format
    x.y.z or just x.y. The returned integer can be used to compare versions.
    """
    value = 0

    # the coefficients for each digit
    coefficients = (10000, 100, 1)

    # split the version and convert them to integers
    parts = list(map(int, version.split('.')))

    # loop over all parts
    for index in range(len(parts)):
        # add the value for this specific parts
        value += coefficients[index] * parts[index]

    return value


def is_ok_val(val_string):
    """
    Returns 1 if the passed argument is a value that can be interpreted as a 'true' value.
    """
    return val_string.lower() in ('1', 'yes', 'y')


def parseCommandline(args):
    """
    Parses the commandline options and make sure they are valid. Exits the application on error
    and prints an error message.
    """

    optval, other_args = getopt.getopt(sys.argv[1:],
                                       # Short options
                                       "fruq",
                                       # Long options
                                       ["full", "fullscreen",
                                        "rebel",
                                        "union",
                                        "sound=",
                                        "bad-pygame="])

    for (opt, val) in optval:
        if opt in ('-f', '--full', '--fullscreen'):
            # run in fullscreen mode
            properties.window_hwflags = properties.window_hwflags | FULLSCREEN
            properties.window_safeflags = properties.window_safeflags | FULLSCREEN

        # should we run quickstart as rebel with hardcoded values?
        elif opt in ['-r', '--rebel']:
            # yep, setup hardcoded data
            scenario.commandline_quickstart = 'r'

        # should we run quickstart as union with hardcoded values?
        elif opt in ['-u', '--union']:
            # yep, setup hardcoded data
            scenario.commandline_quickstart = 'u'

        elif opt in ['--sound']:
            if is_ok_val(val):
                scenario.commandline_sound = 1
            else:
                scenario.commandline_sound = 0


def createDirectory(path):
    """
    Helper function for creating a directory if it does not already exist. Throws an exception on
    error.
    """

    # does the path already exist?
    if os.path.exists(path):
        # it does exist, but is it a file?
        if os.path.isfile(path):
            # damnation, it's a file!
            raise RuntimeError("exists", path)

        # it's a directory, all is don for now
        return

    # no such thing, make it
    os.mkdir(path)

    print("  >>> creating directory: %s" % path)


def initDirectories():
    """
    Initializes the directories where local player-specific data is stored. On an error an error
    message is printed and the application exits.
    """

    print("creating personal directories for saved games and scenarios")

    # create all needed custom directories
    createDirectory(properties.path_home)
    createDirectory(properties.path_saved_games)
    createDirectory(properties.path_custom_scenarios)

    # all done
    print("personal directories created ok")


def initPlayfield():
    """
    Initializes the playfield. Creates all needed layers etc. Note that if the labels for the
    layers in this function are changed they must also be changed in all the classes in state/ that
    use these names to refer to layers. Otherwise we'll get errors.
    """
    # create the playfield
    scenario.playfield = Playfield()

    # TODO: move all this stuff to some Playfield method and make it far less hardcoded

    # add the needed layers
    scenario.playfield.addLayer(TerrainLayer(name="terrain"))
    scenario.playfield.addLayer(ObjectiveLayer(name="objectives"))
    scenario.playfield.addLayer(LocationLayer(name="locations"))

    # now figure out which player we are and which the remote player is
    if scenario.local_player_id == constants.UNION:
        own = constants.UNION
        enemy = constants.REBEL
    else:
        own = constants.REBEL
        enemy = constants.UNION

    scenario.playfield.addLayer(UnitOrdersLayer(name="unit_orders"))
    scenario.playfield.addLayer(UnitLosLayer(name="unit_los"), visible=0)

    # scenario.playfield.addLayer ( UnitTargetsLayer    ( name="unit_targets" ),      visible=1 )
    scenario.playfield.addLayer(CommandersLayer(name="unit_commanders"))
    scenario.playfield.addLayer(WeaponRangeLayer(name="weapon_ranges"))

    # now create layers with our units and the enemy units
    scenario.playfield.addLayer(UnitLayer(name="own_units", player=own))
    scenario.playfield.addLayer(UnitLayer(name="enemy_units", player=enemy))

    # other info layers
    scenario.playfield.addLayer(WeaponInfoLayer(name="weapon_info"), visible=0)
    scenario.playfield.addLayer(MessagesLayer(name="messages"))
    scenario.playfield.addLayer(CombatPolicyLayer(name="combat_policy"), visible=0)

    # add the selection layer
    scenario.playfield.addLayer(SelectionLayer(name="selection"), visible=0)

    # are we debugging?
    if properties.debug:
        # debug layers, NOT visible by default!
        scenario.playfield.addLayer(AIDebugLayer(name="ai_debug"), visible=0)
        scenario.playfield.addLayer(LosDebugLayer(name="los_debug"), visible=0)

    # floating windows: minimap, action, audio, unit info and orders windows
    scenario.playfield.addLayer(MinimapLayer(name="minimap"))
    scenario.playfield.addLayer(UnitOrdersViewLayer(name="orders_view"))
    scenario.playfield.addLayer(UnitInfoViewLayer(name="info_view"))
    scenario.playfield.addLayer(AudioLayer(name="audio"))

    # Don't show audio layer if no audio available
    if not scenario.audio.hasAudio():
        scenario.playfield.setVisible(scenario.playfield.getLayer("audio"), 0)

    # a few top-level thingies
    scenario.playfield.addLayer(HelpLayer(name="help"), visible=0)
    scenario.playfield.addLayer(HelpBrowserLayer(name="help_browser"), visible=0)
    scenario.playfield.addLayer(MenuLayer(name="menu"), visible=0)
    scenario.playfield.addLayer(ChatLayer(name="chat"), visible=0)
    scenario.playfield.addLayer(QuestionLayer(name="question"), visible=0)
    scenario.playfield.addLayer(MessageLayer(name="message"), visible=0)
    scenario.playfield.addLayer(SetResolutionLayer(name="set_resolution"), visible=0)
    scenario.playfield.addLayer(ToggleFeaturesLayer(name="toggle_features"), visible=0)
    scenario.playfield.addLayer(ChooseUnitsLayer(name="choose_units"), visible=0)
    scenario.playfield.addLayer(ArmyStatusLayer(name="army_status"), visible=0)
    scenario.playfield.addLayer(InputLayer(name="input"), visible=0)


def initData():
    """
    Initializes misc data that does not fit under any other function.
    """

    # initialize the animation manager
    scenario.animation_manager = AnimationManager()

    # initialize the messages from the other player and the engine too
    scenario.messages = Messages()


def setup():
    """
    Sets up all parameters for the game in an interactive way. The player is presented a few
    dialogs where he/she can choose some basic info as well as the opponent.If running as a client
    the player needs not do anything more than wait for the other player (the server) to pick
    parameters and send the scenario. If running as server the player gets to select the scenario
    and the sides. The server then sends the scenario data to the waiting client. When the dialogs
    return with an ACCEPTED state the game is ready to continue to the normal event loop.
    """

    # client not yet setup
    client_setup = 0
    opponent_setup = 0

    # create a new client setup dialog and run it. we do the loop until the player is satisfied
    while 1:

        if not client_setup:
            if SetupClient().run() == ACCEPTED:
                # now it is 
                client_setup = 1
            else:
                # player wants to quit, so do it
                quit()

        # is the opponent already setup?
        if not opponent_setup:
            # no, so go do it
            if SetupOpponent().run() == ACCEPTED:
                # now it is, so the opponent is done and client is done
                opponent_setup = 1
                client_setup = 1
            else:
                # player clicked "back", so run the client dialog again
                client_setup = 0
                continue

            # we got this far, the previous dialog was "ok", so setup the network too
            if SetupNetwork().run() == ACCEPTED:
                # player clicked "ok", all done now
                break
            else:
                # player clicked "back", rerun the opponent setup
                opponent_setup = 0
                continue

    # we got this far, so the game is now set up properly and we are connected to whoever is our
    # opponent and/or server

    # are we starting the server? only the server player should see the main dialog
    if scenario.start_server:
        # run the main dialog
        if MainDialog().run() != ACCEPTED:
            # not ok, so just quit
            quit()

    else:
        # show a dialog while waiting for the server player to pick scenario data
        if StartGame().run() != ACCEPTED:
            # not ok, so just go away
            quit()

            # we got this far, seems like all systems are go


def initAudio():
    """
    Initializes sound. Creates the single class that all audio operations will use.
    """

    # create it, let the class sort out the details
    scenario.audio = AudioManager()

    if not scenario.commandline_sound:
        scenario.audio.disableAudio()
        return

    # load our intro sample
    scenario.audio.loadMusic(properties.music_intro)

    # play it too
    scenario.audio.playMusic()


def checkRequirements():
    """
    This function tries to do some sanity checks about the used system. If the system doesn't
    fulfill the requirements, and the requirement is vital, then this method should return 0. If all
    is ok to proceed then it should return 1.
    """

    # is this the broken pygame?
    if versionToInt('1.5') <= versionToInt(pygame.version.ver) <= versionToInt('1.5.2'):
        # oops, we can't just handle this version of pygame, it'll just crash and burn at any random
        # point 
        print()
        print("Pygame is version %s, and that version has a few bugs that we can't " % pygame.version.ver)
        print("work around. Please upgrade to a version >= 1.5.1")
        print()
        print("Sorry for the inconvenience.")
        print()
        return 0

    else:
        print("pygame version is %s, works ok" % pygame.version.ver)

    # no problems
    return 1


def setupIcon():
    """
    Sets up the desktop icon to be used for Civil.
    """
    # load the civil icon
    try:
        # load it
        icon = pygame.image.load(properties.civil_icon)

        # and assign colorkey info. no, it seems to look hideous
        # icon.set_colorkey ( (255,255,255) )

        # use the icon
        pygame.display.set_icon(icon)

    except:
        # oops, failed to load it?
        print("failed to load the Civil icon, continuing without it...")


def initAll():
    """
    Initializes all data when the application is started for the first time. Creates internal
    datastructures and loads the scenario.
    """

    # setup platform specific data first. should set variables in properties that are specific to this 
    # platform that we are currently using.
    platform.setup()

    # parse commandline options
    parseCommandline(sys.argv[1:])

    # create local directories
    initDirectories()

    # initialize pygame
    pygame.init()

    # setup a nice window manager icon
    setupIcon()

    # check if all kinds of requirements are met
    if not checkRequirements():
        # not ok
        quit()

    # set keyboard repeat speed
    pygame.key.set_repeat(200, 20)

    # create the event dispatcher
    scenario.dispatcher = Dispatcher()

    # and allow our events
    pygame.event.set_allowed(pygame.USEREVENT)
    pygame.event.set_allowed(pygame.USEREVENT + 1)

    # initialize SDL
    scenario.sdl = SDL()

    # init sound
    initAudio()

    # setup parameters
    setup()

    # fade out music
    scenario.audio.fadeoutMusic(2000)

    # init all misc data
    initData()

    # create the playfield
    initPlayfield()


def main():
    """
    Main function of the game. Initializes everything and the runs the main event loop.
    """
    # initialize everything
    initAll()

    # show an initial message in the panel
    scenario.messages.add("Good luck, commander %s" % scenario.local_player_name, constants.NORMAL)
    scenario.messages.add("Press F1 for help", constants.HELP)
    scenario.messages.add("Press F2 to see the keyboard shortcuts", constants.HELP)
    scenario.messages.add("The right mouse button shows a menu", constants.HELP)

    # now we're playing!
    scenario.playing = constants.PLAYING

    # load another pieces of music
    scenario.audio.loadMusic(properties.music_main)

    # play it too
    scenario.audio.playMusic()

    # start the main event loop
    event_loop.event_loop()


def start():
    """
    Starting point for the application, simply runs main() and checks for errors and finally
    quits the application.
    """

    # run civil
    main()

    quit()


# starting point if run directly on the commandline
if __name__ == '__main__':
    start()
