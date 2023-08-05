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


class Sequence:
    """
    This class is a simple class mainly used to contain a numeric sequence of numbers and provide
    means to get the next number from that sequence. It is designed to work as a id generator for
    commands within the server engine.

    The main methods are next() which returns the next available id and increses it, and get() which
    returns the current id without increasing.
    """

    def __init__(self, value=0):
        """
        Initializes the instance. Sets default sequence value.
        """
        # store the value
        self.value = 0

    def __next__(self):
        """
        Returns the next available value from the sequence. Increases the sequence by 1.
        """
        # increase value
        self.value += 1

        return self.value

    def get(self):
        """
        Returns the current value without altering it in any way.
        """
        return self.value

    def toString(self):
        """
        Returns a string representation of the sequence value.
        """
        return str(self.value)

    def __str__(self):
        """
        Returns a string representation of the sequence value.
        """
        return str(self.value)
