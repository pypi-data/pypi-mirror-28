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

from civil.editor.plugins.creator import *


class HillCreator(Creator):
    """
    HillCreator creates the proper icons for a continuous road. It does
    NOT generate road, merely looks for and places suitable road icons.
    """

    def __init__(self, iconview):
        Creator.__init__(self, iconview, Creator.addkind__hill, "HillCreator", "Create continuous hill crestlines")

    def isEmpty(self, set, id):
        """

        Args:
            set: 
            id: 

        Returns:

        """
        for i in set[id]:
            if i != 0:
                return 0
        return 1


def new(iconview):
    """

    Args:
        iconview: 

    Returns:

    """
    return HillCreator(iconview)
