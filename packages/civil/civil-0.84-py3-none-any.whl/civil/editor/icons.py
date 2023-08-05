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

import collections


class Icons(collections.UserDict):
    """
    This class defines a dictionary of the icons. The icons are indexed with their unique id. Apart
    from that this class also contains one icon that is designated the 'selected' icon. This is the
    icon that should be used for painting with.

    This class also maintains a list of those icons that are not valid. Some id:s may not have a real
    usable icon, so those id:s can be marked as invalid using markAsInvalid() and then queried using
    isInvalid().
    """

    def __init__(self):
        """
        Initializes the instance.
        """
        collections.UserDict.__init__(self)

        # no selected one yet
        self.selected = -1

        # a map of icons that are not valid, ie probably empty
        self.invalid = {}

        for id in range(574, 592):
            self.markAsInvalid(id)

    def getSelected(self):
        """
        Returns the currently selected icon, or -1 if no icon is selected.
        """
        return self.selected

    def setSelected(self, selected=-1):
        """
        Sets a new selected icon. Leave the default value to clear the selected icon.
        """
        self.selected = selected

    def hasSelected(self):
        """
        Returns 1 if an icon is currently selected and 0 if not.
        """
        if self.selected == -1:
            # nothing selected
            return 0

        return 1

    def markAsInvalid(self, id):
        """
        Marks the icon with the given id as not a valid icon.
        """
        self.invalid[id] = 1

    def isInvalid(self, id):
        """
        Checks weather the icon with the given id is invalid. Returns 1 if it is invalid and 0 if it
        is ok.
        """
        return id in self.invalid
