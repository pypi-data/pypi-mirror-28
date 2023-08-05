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

import pickle
import datetime
import glob
import os
import os.path
import zipfile

from civil import constants
from civil.model import scenario
from civil.serialization.scenario_parser import ScenarioParser
from civil.serialization.simple_dom_parser import SimpleDOMParser
from civil.model.scenario_info import ScenarioInfo


class ScenarioManager:
    """
    This class works as a central manager for all scenario handling in Civil. This class knows how
    to load full scenarios and can also load index files and info files for all found scenarios.
    """

    def __init__(self):
        """
        Initializes the instance.
        """
        # init all members
        self.scenarios = []

    def loadScenario(self, path):
        """
        Loads the scenario with the given path. Opens the scenario archive file and reads the
        scenario and LOS data. The scenario and LOS data is stored internally. If the LOS map does
        not exist it is created. Returns 1 if all is ok and 0 on error.
        """

        # does the file exist?
        if not os.path.exists(path):
            # no such file?
            print("ScenarioManager.loadScenario: invalid scenario:", path)
            return 0

        print("ScenarioManager.loadScenario: loading scenario:", path)

        # open the file as a zip file
        archive = zipfile.ZipFile(path)

        # get the main scenario file from the archive
        buffer = archive.read('scenario.xml')

        # the los map *may* not be there. check if it is
        if 'los.pickle' in archive.namelist():
            # yes, we have it there, read it
            los_data = archive.read('los.pickle')
        else:
            # no los map
            los_data = None

        # and close it
        archive.close()

        print("ScenarioManager.loadScenario: scenario loaded ok")

        # parse the read data and thus build up all scenario data
        ScenarioParser().parseString(buffer)

        # did we get a los map? if not then the scenario was saved without a LOS map
        if los_data is None:
            # no los map, create it
            print("ScenarioManager.loadScenario: creating the LOS map...")
            scenario.map.createLosMap()

        else:
            # we have data, unpickle the LOS map from the given data
            print("ScenarioManager.loadScenario: loading the LOS map...")
            los_map = pickle.loads(los_data)

            # and assign it to the map
            scenario.map.setLosMap(los_map)

        # we're done here
        return 1

    def loadAllScenarioInfos(self, dir):
        """
        Attempts to load all info files for scenarios that are found in 'dir'. Loads scenario
        infos from the files and returns a list of infos.
        """

        # no scenario infos yet
        self.scenarios = []

        # loop over all files in the directory that are civil scenarios
        for file in glob.glob(dir + "/*.civil"):
            print("parsing scenario: %s..." % file)

            # load and parse it
            if not self.__loadScenarioInfo(file):
                # we failed to read it, so abort all reading
                return []

        # we got this far, so all must be ok
        return self.scenarios

    def __loadScenarioInfo(self, path):
        """
        This method reads scenario info from the passed scenario file. The file is opened as a
        zip file and the 'info.xml' part is extracted and parsed. The final info data is stored
        internally and associated with the file name. Returns 1 if all is ok and 0 on error.
        """

        try:
            # open the file as a zip file
            archive = zipfile.ZipFile(path)

            # get the info file from the archive
            buffer = archive.read('info.xml')
        except:
            # not a scenario?
            print("ScenarioManager.loadScenarioInfo: invalid archive:", path)
            return 0

        # create a parser
        parser = SimpleDOMParser()

        # parse the read data
        root = parser.parseString(buffer)

        # did we get anything?
        if root is None:
            # nope, failed to retrieve it
            print("ScenarioManager.loadScenarioInfo: parse error for:", path)
            archive.close()
            return 0

        # now parse the data
        info = self.__parseScenarioInfo(root, path)

        # close the archive too
        archive.close()

        # return whatever we got
        return info

    def __parseScenarioInfo(self, root, file_name):
        """
        Parses the <scenarioinfo> tag, extracts and stores all the info in a ScenarioInfo
        object. The passed 'root' is expected to be the <scenarioinfo> node. Returns the info object
        if all is ok and None on error.
        """

        # is it a proper info node?
        if root.getName() != 'scenarioinfo':
            # oops, illegal file
            print("DOM tree is illegal, top-level tag is: " + root.getName() + ", ")
            print("the node should be 'scenarioinfo'")
            return None

        try:
            # get the simple data
            name = root.getChild('name').getData()
            location = root.getChild('location').getData()

            # get the file if we have it
            file = root.getChild('file')

            # get the starting date and split it up
            datenode = root.getChild('startdate')
            start_year = int(datenode.getAttribute('year'))
            start_month = int(datenode.getAttribute('month'))
            start_day = int(datenode.getAttribute('day'))
            start_hour = int(datenode.getAttribute('hour'))
            start_minute = int(datenode.getAttribute('minute'))
            start_second = 0

            # get the current date and split it up
            datenode = root.getChild('currentdate')
            current_year = int(datenode.getAttribute('year'))
            current_month = int(datenode.getAttribute('month'))
            current_day = int(datenode.getAttribute('day'))
            current_hour = int(datenode.getAttribute('hour'))
            current_minute = int(datenode.getAttribute('minute'))
            current_second = 0

            # get the ending date and split it up
            datenode = root.getChild('enddate')
            end_year = int(datenode.getAttribute('year'))
            end_month = int(datenode.getAttribute('month'))
            end_day = int(datenode.getAttribute('day'))
            end_hour = int(datenode.getAttribute('hour'))
            end_minute = int(datenode.getAttribute('minute'))
            end_second = 0

            # no description yet
            description = []

            # and the description
            for paratag in root.getChild('description').getChildren():
                # get the text
                para = paratag.getData()

                # append the text to the description
                description.append(para)

            # get the rebel and union missions
            rebel = []
            union = []

            # get the missions
            mission = root.getChild('missions')

            # rebel missions
            for paratag in mission.getChild('rebel').getChildren():
                # get the text and append to the description
                rebel.append(paratag.getData())

            # union missions
            for paratag in mission.getChild('union').getChildren():
                # get the text and append to the description
                union.append(paratag.getData())

            # create a new scenario info and set all parsed data
            info = ScenarioInfo(file_name)
            info.setName(name)
            info.setLocation(location)
            info.setDescription(description)
            info.setMission(constants.REBEL, rebel)
            info.setMission(constants.UNION, union)

            # set the dates too
            info.setStartDate(datetime.datetime(start_year, start_month, start_day,
                                                start_hour, start_minute, start_second))
            info.setCurrentDate(datetime.datetime(current_year, current_month, current_day,
                                                  current_hour, current_minute, current_second))
            info.setEndDate(datetime.datetime(end_year, end_month, end_day,
                                              end_hour, end_minute, end_second))

            # now we need to see if the scenario is valid at all
            if root.getChild('valid') is None:
                # no such node, so the scenario is invalid
                info.setValid(0)
            else:
                # it's valid all right
                info.setValid(1)

            # add to our internal list
            self.scenarios.append(info)

            # all ok
            return info

        except KeyError:
            # oops, invalid data
            print("Invalid scenario info.")
            return None
