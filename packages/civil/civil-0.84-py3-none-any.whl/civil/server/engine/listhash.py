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


class ListHash(collections.UserDict):
    """
    This class defines a hash which contains lists as the elements. It builds up a 2D
    structure. The meaning is to have each key in the hash be the id of a turn, and the value for
    each key a list of commands.

    All normal dictionary actions can be performed on this class, but the method add() should be
    used to perform the addition of elements.
    """

    def add(self, id, value):
        """
        Adds 'value' to the end of the list which is found under the key 'key'. If no such key
        exists in the hash then it is created.
        """
        # do we have such a key?
        if id not in self.data:
            # nope, add it
            self.data[id] = []

        # get the list
        list = self.data[id]

        # append the element
        list.append(value)


if __name__ == '__main__':
    l = ListHash()

    for i in range(10):
        for j in range(3):
            l.add(10 - i, j)

    keys = list(l.keys())
    keys.sort()

    for key in keys:
        print(key, l[key])
