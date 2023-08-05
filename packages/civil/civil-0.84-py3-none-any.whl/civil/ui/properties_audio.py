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
This file contains a big dictionary that maps logical names (strings) to the sample that should be
played when that logical name is requested. The files should be normal wav files that are located
somewhere under the $path_sound/sound directory.
"""

from civil.properties import path_sound

# all samples
samplenames = {'button-clicked': path_sound + 'button-clicked.wav',
               'checkbox-toggled': path_sound + 'checkbox-toggled.wav',
               'firing_artillery': path_sound + 'firing_artillery.wav',
               'firing_infantry': path_sound + 'firing_infantry.wav',
               'explosion': path_sound + 'explosion.wav',
               'fanfare': path_sound + 'fanfare.wav'
               }
