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

from civil.model.weapon import Weapon


class EditorWeapon(Weapon):
    """
    This class defines a weapon subclass used within the editor. It adds some data to weapons that
    is not needed within the normal game, thus the subclass. The extra data is a availability date
    range. This tells the editor at what date a given weapon can be used. Some weapons may not be
    available at a certain date (obsoleted or not yet invented), and thus should not be allowed
    inside the editor.
    """

    def __init__(self, id, name, type, range, damage, accuracy, start_avail, end_avail):
        """
        Initializes the  and allocates necessary data.
        """
        Weapon.__init__(self, id, name, type, range, damage, accuracy)

        # store custom data
        self.start_avail = start_avail
        self.end_avail = end_avail

    def getAvailabilityStart(self):
        """
        Returns a (year,month) tuple which is the first month and year the weapon is available.
        """
        return self.start_avail

    def getAvailabilityEnd(self):
        """
        Returns a (year,month) tuple which is the last month and year the weapon is available.
        """
        return self.end_avail

    def isAvailable(self, year, month):
        """
        Checks weather the weapon is available for the given month and year. Returns 1 if it is
        and 0 if not.
        """
        # convert the given data to months
        start = self.start_avail[0] * 12 + self.start_avail[1]
        end = self.end_avail[0] * 12 + self.end_avail[1]
        current = year * 12 + month

        # just do a little check
        if start <= current <= end:
            # yep, it's available
            return 1

        return 0
