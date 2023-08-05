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

from civil.serialization.simple_dom_parser import SimpleDOMParser


class Block:
    """
    This class...
    """

    def __init__(self, file_name):
        """
        Initializes the instance.
        """

        # no icons yet
        self.icons = []

        # create a new parser
        domparser = SimpleDOMParser()

        # parse the data
        try:
            root = domparser.parseFile(file_name)

        except:
            # serious error
            raise RuntimeError("Block: error parsing %s" % file_name)

        # get name
        self.name = root.getChild('name').getData()

        self.max_x = 0
        self.max_y = 0

        # loop over all icons
        for node in root.getChild('icons').getChildren():
            # get the x, y and icon id
            x = int(node.getAttribute('x'))
            y = int(node.getAttribute('y'))
            id = int(node.getAttribute('id'))

            # store all data in a new item
            self.icons.append((x, y, id))

            # is this block enlarged now?
            if x > self.max_x:
                # new max x
                self.max_x = x

            if y > self.max_y:
                # new may y
                self.max_y = y

    def getName(self):
        """
        Returns the name of the block. This name can be used to identify the block in lists etc and
        is supposed to be human readable.
        """
        return self.name

    def getIcons(self):
        """
        Returns a list of all icons the block contains. The items in the list are tuples (x,y,id)
        where 'x' and 'y' are the hex coordinates and 'id' the id of the icon for that position.
        """
        return self.icons

    def getSize(self):
        """
        Returns the size of the block in hexes.
        """
        return self.max_x + 1, self.max_y + 1

