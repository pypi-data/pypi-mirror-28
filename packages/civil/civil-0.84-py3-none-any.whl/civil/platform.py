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
import sys

from civil import properties

try:
    import paths
except:
    # no such file, probably a windows/osx machine?
    print("paths not found")


def setup():
    """
    Sets up platform specific directories in 'properties'. Sets up all needed directories as well
    as a static name for the platform. That name can then later be used if there is a need to do
    something that is specific to some platform.
    """

    # get the platform name as a lowercase string
    osname = sys.platform.lower()

    # what are we running?
    if osname.find('linux') != -1:
        # a linux was found, set dirs
        properties.path_home = os.environ['HOME'] + '/.civil/'
        properties.path_saved_games = properties.path_home + 'saved_games'
        properties.path_custom_scenarios = properties.path_home + 'scenarios'

        # set platform name
        properties.platform_name = 'linux'

        # set path to ai
        #properties.path_ai_client = paths.prefix + '/civil-ai'

    elif osname.find('bsd') != -1:
        # a bsd was found, set dirs
        properties.path_home = os.environ['HOME'] + '/.civil/'
        properties.path_saved_games = properties.path_home + 'saved_games'
        properties.path_custom_scenarios = properties.path_home + 'scenarios'

        # set platform name
        properties.platform_name = 'bsd'

        # set path to ai
        properties.path_ai_client = paths.prefix + '/civil-ai'

    elif osname.find('darwin') != -1:
        # osx was found, set dirs
        properties.path_home = os.environ['HOME'] + '/.civil/'
        properties.path_saved_games = properties.path_home + 'saved_games'
        properties.path_custom_scenarios = properties.path_home + 'scenarios'

        # set platform name
        properties.platform_name = 'darwin'

        # set path to ai
        properties.path_ai_client = paths.prefix + '/civil-ai'

    elif osname.find('win') != -1:
        # some kind of windows was found, set dirs
        properties.path_home = 'XXXXXXXXXXX' + '/'
        properties.path_saved_games = properties.path_home + 'saved_games'
        properties.path_custom_scenarios = properties.path_home + 'scenarios'

        # set a common platform name
        properties.platform_name = 'windows'

    else:
        # some other platform. just bail out so that we can fix it later and add the platform as a
        # 'supported platform'
        raise RuntimeError("'%s' is an unknown platform. Please report to the Civil developers!")
