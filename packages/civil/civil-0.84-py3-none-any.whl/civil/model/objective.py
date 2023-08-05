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

from civil import constants
from civil.model.location import Location


class Objective(Location):
    """
    This class contains all needed information about a specific objective on the map. An objective
    is a location that is significant in some way to both the parties, and thus should be captures
    and held during the battle.

    An objective contains data about the position on the map of the objective, an optional name
    (such as Johnsons's Bridge), a longer textual description of why this objective is important,
    the number of victory points awarded to the owner at the end of the battle as well as the
    current owner.

    The positions of objectives are direct pixel values, not hex values. This means that objectives
    may be painted over several objectives.
    
    Some objectives start by being owned by a player, other are neutral and later conquered.

    NOTE: We are a subclass of Location.
    """

    def __init__(self, id, position=None):
        """
        Initializes the instance. Sets the passed id and position
        """
        self.id = id

        # reset all other members
        name = "objective %d" % id
        self.description = ""
        self.owner = constants.UNKNOWN
        self.points = 0

        # do we have a position?
        if position is None:
            position = (-1, -1)

        Location.__init__(self, position[0], position[1], name)

    def getId(self):
        """
        Returns the id of this objective.
        """
        return self.id

    def getDescription(self):
        """
        Returns the description of this objective.
        """
        return self.description

    def setDescription(self, description):
        """
        Sets a new description for the objective.
        """
        self.description = description

    def getOwner(self):
        """
        Returns the owner of this objective.
        """
        return self.owner

    def setOwner(self, owner):
        """
        Sets a new owner for the objective.
        """
        self.owner = owner

    def getPoints(self):
        """
        Returns the points of this objective.
        """
        return self.points

    def setPoints(self, points):
        """
        Sets a new points value for the objective.
        """
        self.points = points

    def toXML(self):
        """
        Returns a string containing the objective serialized as XML. The lines are not indented in
        any way, and contain no newline
        """
        # get a string for the owner
        owner = ('rebel', 'union', 'unknown')[self.owner]

        # build up the xml
        xml = '<objective id="%d" x="%d" y="%d" ' % (self.id, self.position[0], self.position[1])
        xml += 'name="%s" ' % self.name
        xml += 'points="%d" owner="%s">%s</objective>' % (self.points, owner, self.description)

        return xml


# testing
if __name__ == '__main__':
    Objective()
