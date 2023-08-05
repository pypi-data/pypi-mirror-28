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


class Location:
    """
    This class defines a location on the map. A location can be any place that can be associated
    with a coordinate and a name, such as a bridge, field, town etc. The engine can use these
    locations to paint labels on the map for added atmosphere.

    Each location contains simply a x- and y-coordinate and a text. The coordinates are the pixel
    coordinates of the location, not hex coordinates.
    """

    def __init__(self, x, y, name=""):
        """
        Creates the instance of the class. Sets passed values for all members.
        """

        # store the data
        self.position = (x, y)

        # did we get a label?
        if name:
            self.name = name
        else:
            self.name = ""

    def getName(self):
        """
        Returns the name of the location. The name is never None, but may be ''.
        """
        return self.name

    def setName(self, name):
        """
        Sets a new name. If the name is None then '' is used.
        """
        if name:
            self.name = name
        else:
            self.name = ""

    def getPosition(self):
        """
        Returns a (x,y) tuple with the position of the location on the map. The coordinates are
        the pixel coordinates of the location, not hex coordinates.
        """
        return self.position

    def setPosition(self, position):
        """
        Sets a new position for the objective. The new position is a (x,y) tuple.
        """
        self.position = position

    def toXML(self):
        """
        Returns a string containing the location serialized as XML. The lines are not indented in
        any way, and contain no newline
        """
        # build up the xml
        xml = '<location x="%d" y="%d">%s</location>' % (self.position[0], self.position[1], self.name)

        return xml
