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

from civil.server.mode.changing_to_column import ChangingToColumn
from civil.server.mode.changing_to_formation import ChangingToFormation
from civil.server.mode.column import Column
from civil.server.mode.column_move import ColumnMove
from civil.server.mode.column_move_fast import ColumnMoveFast
from civil.server.mode.column_skirmish import ColumnSkirmish
from civil.server.mode.dismounted import Dismounted
from civil.server.mode.dismounted_move import DismountedMove
from civil.server.mode.dismounted_skirmish import DismountedSkirmish
from civil.server.mode.dismounting import Dismounting
from civil.server.mode.disorganized_column import DisorganizedColumn
from civil.server.mode.disorganized_formation import DisorganizedFormation
from civil.server.mode.disorganized_limbered import DisorganizedLimbered
from civil.server.mode.disorganized_mounted import DisorganizedMounted
from civil.server.mode.disorganized_unlimbered import DisorganizedUnlimbered
from civil.server.mode.disorganized_unmounted import DisorganizedUnmounted
from civil.server.mode.formation import Formation
from civil.server.mode.formation_assault import FormationAssault
from civil.server.mode.formation_move import FormationMove
from civil.server.mode.formation_skirmish import FormationSkirmish
from civil.server.mode.limbered import Limbered
from civil.server.mode.limbered_move import LimberedMove
from civil.server.mode.limbering import Limbering
from civil.server.mode.meleeing_column import MeleeingColumn
from civil.server.mode.meleeing_formation import MeleeingFormation
from civil.server.mode.meleeing_limbered import MeleeingLimbered
from civil.server.mode.meleeing_mounted import MeleeingMounted
from civil.server.mode.meleeing_unlimbered import MeleeingUnlimbered
from civil.server.mode.meleeing_unmounted import MeleeingUnmounted
from civil.server.mode.mounted import Mounted
from civil.server.mode.mounted_assault import MountedAssault
from civil.server.mode.mounted_move import MountedMove
from civil.server.mode.mounted_move_fast import MountedMoveFast
from civil.server.mode.mounted_skirmish import MountedSkirmish
from civil.server.mode.mounting import Mounting
from civil.server.mode.retreating_column import RetreatingColumn
from civil.server.mode.retreating_formation import RetreatingFormation
from civil.server.mode.retreating_limbered import RetreatingLimbered
from civil.server.mode.retreating_mounted import RetreatingMounted
from civil.server.mode.retreating_unlimbered import RetreatingUnlimbered
from civil.server.mode.retreating_unmounted import RetreatingUnmounted
from civil.server.mode.routed_artillery import RoutedArtillery
from civil.server.mode.routed_cavalry import RoutedCavalry
from civil.server.mode.routed_move_artillery import RoutedMoveArtillery
from civil.server.mode.routed_move_cavalry import RoutedMoveCavalry
from civil.server.mode.routed_move_infantry import RoutedMoveInfantry
from civil.server.mode.unlimbered import Unlimbered
from civil.server.mode.unlimbered_skirmish import UnlimberedSkirmish
from civil.server.mode.unlimbering import Unlimbering

# a map of all modes
modes = {
    'column': Column,
    'columnmove': ColumnMove,
    'columnmovefast': ColumnMoveFast,
    'columnskirmish': ColumnSkirmish,
    'changingtocolumn': ChangingToColumn,
    'dismounted': Dismounted,
    'dismountedmove': DismountedMove,
    'dismountedskirmish': DismountedSkirmish,
    'dismounting': Dismounting,
    'disorganizedcolumn': DisorganizedColumn,
    'disorganizedformation': DisorganizedFormation,
    'disorganizedlimbered': DisorganizedLimbered,
    'disorganizedunlimbered': DisorganizedUnlimbered,
    'disorganizedmounted': DisorganizedMounted,
    'disorganizedunmounted': DisorganizedUnmounted,
    'formation': Formation,
    'formationmove': FormationMove,
    'formationskirmish': FormationSkirmish,
    'formationassault': FormationAssault,
    'changingtoformation': ChangingToFormation,
    'limbered': Limbered,
    'limbering': Limbering,
    'limberedmove': LimberedMove,
    'meleeingcolumn': MeleeingColumn,
    'meleeingformation': MeleeingFormation,
    'meleeinglimbered': MeleeingLimbered,
    'meleeingunlimbered': MeleeingUnlimbered,
    'meleeingmounted': MeleeingMounted,
    'meleeingunmounted': MeleeingUnmounted,
    'mounted': Mounted,
    'mountedmove': MountedMove,
    'mountedmovefast': MountedMoveFast,
    'mountedskirmish': MountedSkirmish,
    'mountedassault': MountedAssault,
    'mounting': Mounting,
    'retreating_column': RetreatingColumn,
    'retreating_formation': RetreatingFormation,
    'retreating_limbered': RetreatingLimbered,
    'retreating_unlimbered': RetreatingUnlimbered,
    'retreating_mounted': RetreatingMounted,
    'retreating_unmounted': RetreatingUnmounted,
    'routedartillery': RoutedArtillery,
    'routedcavalry': RoutedCavalry,
    'routedmoveinfantry': RoutedMoveInfantry,
    'routedmovecavalry': RoutedMoveCavalry,
    'routedmoveartillery': RoutedMoveArtillery,
    'unlimbered': Unlimbered,
    'unlimberedskirmish': UnlimberedSkirmish,
    'unlimbering': Unlimbering
}


def createMode(mode):
    """
    This function works as a factory for creating instances of Mode subclases based on the passed
    string. The string should be the name of the wanted mode, just as the method 'getName()' on the
    mode would return. A new Mode subclass is returned.
    """

    # just create a new mode based on the name
    try:
        return modes[mode]()
    except:
        # no such mode?
        raise ValueError("mode '%s' is unknown to the factory" % mode)
