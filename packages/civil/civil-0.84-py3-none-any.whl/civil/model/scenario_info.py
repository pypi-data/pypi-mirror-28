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

from civil.model import scenario
from civil.constants import REBEL, UNION


class ScenarioInfo:
    """
    This class contains all needed information about the current scenario. The scenario is the
    current battle, and the information contained is the name, a description, the historical date
    and the duration of the battle. The duration is given as a starting date/time and an ending
    date/time. 

    The description and the mission attribute is a list of strings, each string representing one
    paragraph. 

    This class basically reflects the tag <scenarioinfo> in the scenario files.
    
    Methods exist for accessing all the information.
    """

    def __init__(self, path=''):
        """
        Creates the instance of the class.
        """
        # init all members
        self.name = ""
        self.description = []
        self.start_date = None
        self.current_date = None
        self.end_date = None
        self.location = ""

        # the overall theatre. we hard-code this for now
        self.theatre = "us-civil"

        # all brigades in the game. THe brigades then in turn contain all other organization, such as
        # regiments, battalions and companies in a tree-like structure. The map has the id of the unit as a
        # key 
        self.brigades = {REBEL: {},
                         UNION: {}}

        # all companies and batteries of the game. These can be reached from the 'Brigades' instance as well,
        # but usually only the companies/batteries need to be accessed, so this structure is provided for
        # convenience. The map has the unit id as a key
        self.units = {}

        # a map with all destroyed units. This works in the same way as 'units' above does, with the
        # exception that only units which have been destroyed are here. So companies that are here are *not*
        # in 'units' and vice versa. the units are indexed by their id
        self.destroyed_units = {}

        # a hash that maps unit id:s to a tuple (unit,date) which is the actual unit and the date it arrives
        # as soon as the current time is past the date the unit should arrive
        self.reinforcements = {}

        # a list of all objectives on the map
        self.objectives = []

        # a list of all locations
        self.locations = []

        # store whatever path we got
        self.path = path

        # set the default missions
        self.missions = {REBEL: [],
                         UNION: []}

        # by default the scenario is assumed to be valid
        self.valid = 1

    def getPath(self):
        """
        Returns the unique path of the instance.
        """
        return self.path

    def getName(self):
        """
        Returns the name of this scenario.
        """
        return self.name

    def setName(self, name):
        """
        Sets a new name for the scenario.
        """
        self.name = name

    def isValid(self):
        """
        Returns 1 if the scenario is supposed to be valid.
        """
        return self.valid

    def setValid(self, valid):
        """
        Sets a new validity for the scenario. The value must be 1 or 0.
        """
        # precautions
        assert (valid in (0, 1))

        # all ok, store new flag
        self.valid = valid

    def getLocation(self):
        """
        Returns the location of this scenario.
        """
        return self.location

    def setLocation(self, location):
        """
         Sets a new location for the scenario.
         """
        self.location = location

    def getTheatre(self):
        """
        Returns the theatre of this scenario.
        """
        return self.theatre

    def setTheatre(self, theatre):
        """
         Sets a new theatre for the scenario.
         """
        self.theatre = theatre

    def getDescription(self):
        """
        Returns the description of this scenario. This returns a list which contains strings, one
        for each paragraph. The list is empty if there is no description.
        """
        return self.description

    def setDescription(self, description):
        """
        Sets a new description for the scenario. The parameter should be a list of strings.
        """
        self.description = description

    def getMission(self, player):
        """
        Returns the mission description for the given 'player'. The mission description is like
        the overall description a list with strings, each string a paragraph of text. It may be
        empty too.
        """
        # just brutally assume the passed player is ok
        return self.missions[player]

    def setMission(self, player, description):
        """
        Sets a new mission description for 'player'.  The mission description is like
        the overall description a list with strings, each string a paragraph of text. It may be
        empty, i.e. an empty list.
        """
        # precautions
        if not player in (REBEL, UNION):
            # ouch, fubar player
            raise ValueError("invalid player id given")

        # just set it
        self.missions[player] = description

    def getStartDate(self):
        """
        Returns the starting date of this scenario. This is a datetime instance or None if not yet set.
        """
        return self.start_date

    def getStartDateString(self):
        """
        Returns a pretty string with the starting date. The format is 'Aug 20th 1863, at 12:34'.
        """
        date = self.getStartDate()

        # get the month for the date
        monthstr = ('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec')[date.month - 1]

        # get the extension for the day
        ext = ('xx', 'st', 'nd', 'rd', 'th', 'th', 'th', 'th', 'th', 'th',
               'th', 'th', 'th', 'th', 'th', 'th', 'th', 'th', 'th', 'th',
               'th', 'st', 'nd', 'rd', 'th', 'th', 'th', 'th', 'th', 'th',
               'st')[date.day]

        # and create the date and return it
        return "%s %d%s %d, at %02d:%02d" % (monthstr, date.day, ext, date.year, date.hour, date.minute)

    def setStartDate(self, date):
        """
        Sets a new starting date for the scenario. This must be a datetime instance.
        """
        self.start_date = date

    def getCurrentDate(self):
        """
        Returns the current date of this scenario. This is a datetime instance and should always
        be valid or same as the starting date.
        """
        return self.current_date

    def getCurrentDateString(self):
        """
        Returns a pretty string with the current date. The format is 'Aug 20th 1863, at 12:34'.
        """
        date = self.getCurrentDate()

        # get the month for the date
        monthstr = ('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec')[date.month - 1]

        # get the extension for the day
        ext = ('xx', 'st', 'nd', 'rd', 'th', 'th', 'th', 'th', 'th', 'th',
               'th', 'th', 'th', 'th', 'th', 'th', 'th', 'th', 'th', 'th',
               'th', 'st', 'nd', 'rd', 'th', 'th', 'th', 'th', 'th', 'th',
               'st')[date.day]

        # and create the date and return it
        return "%s %d%s %d, at %02d:%02d" % (monthstr, date.day, ext, date.year, date.hour, date.minute)

    def setCurrentDate(self, date):
        """
        Sets a new current date for the scenario. This must be a datetime instance.
        """
        self.current_date = date

    def getEndDate(self):
        """
        Returns the ending date of this scenario. This is a datetime instance or None if not yet set.
        """
        return self.end_date

    def getEndDateString(self):
        """
        Returns a pretty string with the ending date. The format is 'Aug 20th 1863, at 12:34'.
        """
        date = self.getEndDate()

        # get the month for the date
        monthstr = ('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec')[date.month - 1]

        # get the extension for the day
        ext = ('xx', 'st', 'nd', 'rd', 'th', 'th', 'th', 'th', 'th', 'th',
               'th', 'th', 'th', 'th', 'th', 'th', 'th', 'th', 'th', 'th',
               'th', 'st', 'nd', 'rd', 'th', 'th', 'th', 'th', 'th', 'th',
               'st')[date.day]

        # and create the date and return it
        return "%s %d%s %d, at %02d:%02d" % (monthstr, date.day, ext, date.year, date.hour, date.minute)

    def setEndDate(self, date):
        """
        Sets a new ending date for the scenario. This must be a datetime instance.
        """
        self.end_date = date

    def hasEnded(self):
        """
        Checks the current date to see if it is equal to or past the ending date. This method can
        be used to check if the scenario has ended and is mainly needed by the server. Returns 1 to
        indicate an ended game and 0 if not.
        """
        # just do a brutal check
        if self.current_date < self.end_date:
            # not yet ended
            return 0
        else:
            return 1

    def toXML(self):
        """
        Returns a string containing the scenario info serialized as XML. The top-level tag is
        <scenarioinfo>.
        """

        # build up the xml. This is really quite nice, I'm impressed with Python's handling of strings!
        xml = '\t<scenarioinfo>\n'
        xml += '\t\t<name>%s</name>\n' % self.name
        xml += '\t\t<theatre>%s</theatre>\n' % self.theatre
        xml += '\t\t<location>%s</location>\n' % self.location

        # write the validity
        xml += '\t\t<%s/>\n' % ('invalid', 'valid')[self.valid]

        # do we have a local player? this one should be set if we're saving from within a game, but
        # should not be set in the editor
        if scenario.local_player_id is not None:
            # yes, we have one. add it
            xml += '\t\t<localplayer id="%d"/>\n' % scenario.local_player_id

        # write out the starting date
        year, month, day = self.start_date.year, self.start_date.month, self.start_date.day
        hour, minute, second = self.start_date.hour, self.start_date.minute, self.start_date.second
        xml += '\t\t<startdate year="%d" month="%d" day="%d" ' % (year, month, day)
        xml += 'hour="%d" minute="%d" second="%d"/>\n' % (hour, minute, second)

        # write out the current date
        year, month, day = self.current_date.year, self.current_date.month, self.current_date.day
        hour, minute, second = self.current_date.hour, self.current_date.minute, self.current_date.second
        xml += '\t\t<currentdate year="%d" month="%d" day="%d" ' % (year, month, day)
        xml += 'hour="%d" minute="%d" second="%d"/>\n' % (hour, minute, second)

        # write out the ending date
        year, month, day = self.end_date.year, self.end_date.month, self.end_date.day
        hour, minute, second = self.end_date.hour, self.end_date.minute, self.end_date.second
        xml += '\t\t<enddate year="%d" month="%d" day="%d" ' % (year, month, day)
        xml += 'hour="%d" minute="%d" second="%d"/>\n' % (hour, minute, second)
        xml += "\t\t<description>\n"

        # and the description. First, do we have one at all?
        if not self.description:
            # no description
            xml += "\t\t</description>\n"

        else:
            # loop over all the paragraphs
            for para in self.description:
                # add the para
                xml += "\t\t\t<para>%s</para>\n" % para

            # close the description
            xml += "\t\t</description>\n"

        # now the missions
        xml += "\t\t<missions>\n"

        # loop over them
        for label, player in (('rebel', REBEL), ('union', UNION)):
            # get the description
            text = self.getMission(player)

            # print the start
            xml += "\t\t\t<%s>\n" % label

            # loop over all the paragraphs
            for para in text:
                # add the para
                xml += "\t\t\t\t<para>%s</para>\n" % para

            # print the end
            xml += "\t\t\t</%s>\n" % label

        xml += "\t\t</missions>\n"
        xml += "\t</scenarioinfo>\n"

        return xml

