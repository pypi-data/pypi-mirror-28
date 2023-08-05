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


class Leader:
    """
    This class defines a leader for a unit in the game. The leader is the commanding officer and
    reflects to a large extent how the controlled unit behaves. A good leader can influence a bad
    unit to good performance while a bad leader can lead a unit to disaster.

    Main attributes of a leader is the experience which directly influences combat success. Also
    important is the aggressiveness which controls how aggressively the leader will drive its unit
    in battle. An aggressive leader has better chances of doing great victories. The rally skill
    influences how well a leader can keep the unit 'in line' when the going gets tough, and how fast
    a retreating/routing unit can be reorganized.

    The skill 'motivation' affects how good the leader is in keeping the ranks together when the
    going gets tough. A higher skill simulates the leader's ability to motivate the troops the do
    something, such as not retreat when under pressure.
    """

    def __init__(self, name, rank, aggressiveness, experience, rallyskill, motivation):
        """
        Creates an instance of the class. Uses the passed data or default values.
        """
        # set the passed name and rank
        self.name = name
        self.rank = rank

        # set the other attributes
        self.aggressiveness = aggressiveness
        self.experience = experience
        self.rallyskill = rallyskill
        self.motivation = motivation

    def getName(self):
        """
        Returns the name of the leader. This is a cleartext name suitable for displaying to the
        players.
        """
        return self.name

    def setName(self, name):
        """
        Stores a new name for the leader.
        """
        self.name = name

    def getRank(self):
        """
        Returns the rank of the leader. This is a cleartext rank and no class.
        """
        return self.rank

    def setRank(self, rank):
        """
        Stores a new rank for the leader.
        """
        self.rank = rank

    def getExperience(self):
        """
        Returns the experience of the leader.
        """
        return self.experience

    def setExperience(self, experience):
        """
        Sets a new experience value for the leader.
        """
        self.experience = experience

    def getAggressiveness(self):
        """
        Returns the aggressiveness of the leader.
        """
        return self.aggressiveness

    def setAggressiveness(self, aggressiveness):
        """
        Sets a new aggressiveness value for the leader.
        """
        self.aggressiveness = aggressiveness

    def getRallySkill(self):
        """
        Returns the rallyskill of the leader.
        """
        return self.rallyskill

    def setRallySkill(self, rallyskill):
        """
        Sets a new rallyskill value for the leader.
        """
        self.rallyskill = rallyskill

    def getMotivation(self):
        """
        Returns the motivation of the leader.
        """
        return self.motivation

    def setMotivation(self, motivation):
        """
        Sets a new motivation value for the leader.
        """
        self.motivation = motivation

    def modifyBaseDelay(self, delay):
        """
        This method modifies the passed delay according to the leader's abilities. The passed
        delay is a 'base' time in turns before the unit can start executing an order. This method
        will add to that delay if needed. A good leader will increase it less and a bad leader will
        increase it a lot. The returned value is a floating point value.

        TODO: handle experience/command control here, hardcoded value.
        """

        # do we have command control?
        delay *= 1.0

        # use the experience as a base modifier
        return delay + delay * (1 - (self.experience.getValue() / 100))

    def toXML(self, indent, level):
        """
        Returns a string containing the leader serialized as XML. The first line is using the
        indent string 'level' times. Internal data is indented 'level+1' steps.
        """

        # build up the xml
        xml = indent * level + '<commander name="%s">\n' % self.name
        xml += indent * (level + 1) + '<rank>%s</rank>\n' % self.rank
        xml += indent * (level + 1) + '<experience value="%d"/>\n' % self.experience.getValue()
        xml += indent * (level + 1) + '<aggressiveness value="%d"/>\n' % self.aggressiveness.getValue()
        xml += indent * (level + 1) + '<rally value="%d"/>\n' % self.rallyskill.getValue()
        xml += indent * (level + 1) + '<motivation value="%d"/>\n' % self.motivation.getValue()
        xml += indent * level + '</commander>\n'

        return xml
