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

from civil import properties
from civil.map.hex_template import HexTemplate


class Hex:
    """
    This class defines a single hex in the map. A hex is the smallest possible location a unit can
    be positioned on. Each hex contains an icon id, the absolute heights of each of the six
    triangles in the hex and a reference to a template hex. The templates are shared among all
    hexes, and thus are present only once. They are used to query static data about a hex, such as
    terrain, color data, road/river info etc. As this data does not change there is no need to
    duplicate it unnecessarily

    Also provides functionality for returning a RGB color representing the hex.

    If a new hex is added the file 'terrains.txt' *must* be changed too.
    """

    # a dict of templates for all the terrain hexes
    templates = None

    def __init__(self, iconid, height=0):
        """
        Initializes the hex and stores passed data.
        """

        # do we already have the hex data loaded?
        if Hex.templates is None:
            # not yet loaded, so go do it
            self.__loadHexTemplates()

        # store the template that this hex uses as base
        self.template = Hex.templates[iconid]

        # set the height too
        self.height = height

    def getTerrains(self):
        """
        Returns the terrains for each triangle in the hex. The terrains are returned as a list of
        instances of Terrain.
        """
        return self.template.terrains

    def getTerrain(self, triangle):
        """
        Returns the terrain for th given triangle in the hex.
        """
        return self.template.terrains[triangle]

    def getColor(self):
        """
        Returns a tuple (red,green,blue) that represents the general color of the icon. This color
        can be used in for instance the minimap. If the icon does not have a color allocated then it
        returns a black color and prints a warning.
        """
        return self.template.color

    def getHeight(self):
        """
        Returns the absolute height of the hex.
        """
        return self.height

    def setHeight(self, height):
        """
        Set a new height for the hex.
        """
        self.height = height

    def getRoads(self):
        """
        Returns the roads of the triangles in the hex. If the hex has roads then the corresponding
        values in the returned list are 1, otherwise 0.
        """
        return self.template.roads

    def getRivers(self):
        """
        Returns the rivers of the triangles in the hex. If the hex has roads then the corresponding
        values in the returned list are 1, otherwise 0.
        """
        return self.template.rivers

    def getIconId(self):
        """
        Returns the id of the icon for this hex.
        """
        return self.template.id

    def toXML(self, x, y):
        """
        Returns a string containing the hex serialized as XML. The lines are not indented in
        any way, and contain no newline. As the hex does no longer know its position in the map (the
        hexes may be shared) the position is passed as parameters.
        """

        # build up the xml and return it
        return '<hex x="%d" y="%d" terrain="%d" height="%d"/>' % (x, y, self.template.id, self.height)

    def __loadHexTemplates(self):
        """
        Loads the static terrain data from a file and stores it all in an internal shared
        dictionary. Each hex will have a line that describes the terrain, height and roads/rivers
        for each triangle of the hex.
        """

        print("loading hex templates")

        # init the dictionary
        Hex.templates = {}

        count = 1

        # open the file for reading and read all lines
        for line in open(properties.hex_data_file).readlines():
            # clean it up
            line = line.strip()

            # is this a comment or an empty line?
            if len(line) == 0 or line[0] == "#":
                # and empty line, next please
                continue

            # take a trailing comment into account
            index = line.find("#")
            if index != -1:
                line = line[:index]

            # split it up into parts based on spaces
            parts = line.split()

            # we should have three parts
            if len(parts) != 4:
                # illegal data
                raise RuntimeError(
                    "terrain data file %s is illegal, line %d (%s)" % (properties.hex_data_file, count, line))
            # get the id and split up the terrain types, road/river into and height
            id = int(parts[0])
            terrains = parts[1]
            heights = parts[2]
            color = parts[3].split(',')

            # create a new template
            template = HexTemplate(id, terrains, heights, color)

            # cache it in the shared dict
            Hex.templates[id] = template

            count += 1
