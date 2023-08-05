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

import os
import os.path
import zipfile

from civil import properties
from civil.model import scenario
from civil.constants import UNION, REBEL


class ScenarioWriter:
    """
    This class works as writer for scenarios. It will take the currently loaded scenario and write
    it to a file. It will only write to a file, not an URL. The format is the same XML that the
    class ScenarioParser can parse, so all data in the scenario is written.

    Use this class like this:

    if not ScenarioWriter ().write ( file_name ):
        # failed to write the file
        ...
    else:
        # file written ok
        ...


    This writer writes all data recursively.

    """

    def __init__(self):
        """
        Creates the instance of the class. Does no writing yet.
        """

        # nothing to do
        self.indent = '  '

    def write(self, file_name):
        """
        Writes the current scenario to a file. The file will be truncated and overwritten. If
        all is ok then 1 is returned, otherwise 0. Exceptions may be thrown on write errors. This
        method will write out three files in the same directory as the scenario is saved:

        * scenario.xml
        * info.xml
        * los.pickle

        These files are finally zipped into a file and deleted.
        """

        # get the dir we save into
        directory = os.path.dirname(file_name)

        # now create the two file names for the info and main data
        mainfile_name = os.path.join(directory, 'scenario.xml')
        infofile_name = os.path.join(directory, 'info.xml')
        losfile_name = os.path.join(directory, 'los.pickle')

        # save the LOS map 
        scenario.map.saveLosMap(losfile_name)

        try:
            file = open(mainfile_name, 'w')
        except IOError:
            # could not open the file
            print("could not open file '%s' for writing." % mainfile_name)
            return 0

        # write header
        if not self.writeHeader(file):
            print("failed to write header, aborting write")
            return 0

        # write out the scenario info
        if not self.writeScenarioInfo(file):
            print("failed to write scenario info, aborting write")
            return 0

        # write out weapons
        if not self.writeWeapons(file):
            print("failed to write weapons, aborting write")
            return 0

        # write out all units
        if not self.writeUnits(file):
            print("failed to write units, aborting write")
            return 0

        # write out all locations
        if not self.writeLocations(file):
            print("failed to write locations, aborting write")
            return 0

        # write out all objectives
        if not self.writeObjectives(file):
            print("failed to write objectives, aborting write")
            return 0

        # write out the map
        if not self.writeMap(file):
            print("failed to write map, aborting write")
            return 0

        # write closing footer
        if not self.writeFooter(file):
            print("failed to write closing footer, aborting write")
            return 0

        file.close()

        # and the info file
        info = open(infofile_name, 'w')

        # write out the header
        info.write('<?xml version="1.0"?>\n')

        # and the main info
        self.writeScenarioInfo(info)

        # close too
        info.close()

        # store the old directory and cd to where the files are saved. this must be done so that we
        # can add the files without a full path
        oldpwd = os.getcwd()
        os.chdir(directory)

        # all parts written out, now open a zip file where they are all written
        zip = zipfile.ZipFile(file_name, "w", zipfile.ZIP_DEFLATED)

        # write the parts we have
        zip.write(os.path.basename(mainfile_name))
        zip.write(os.path.basename(infofile_name))
        zip.write(os.path.basename(losfile_name))

        # close to avoid stuff getting lost
        zip.close()

        # remove the temporary files
        os.remove(mainfile_name)
        os.remove(infofile_name)
        os.remove(losfile_name)

        # cd back to where we started
        os.chdir(oldpwd)

        # all is ok
        return 1

    def writeHeader(self, file):
        """
        Writes out the needed XML header and (possible) DOCTYPE specification. Returns 1 if all
        is ok and 0 on error.
        """
        try:
            # write out the header
            file.write('<?xml version="1.0"?>\n<scenario version="%s">\n' % properties.version)
            # file.write ( '<?xml version="1.0"?>\n<scenario version="0.80">\n' )
        except:
            # failed to write
            return 0

        # all is ok
        return 1

    def writeFooter(self, file):
        """
        Writes out the needed XML footer, i.e. closing tag. Returns 1 if all is ok and 0 on
        error.
        """
        try:
            # write out the header
            file.write('</scenario>\n')
        except:
            # failed to write
            return 0

        # all is ok
        return 1

    def writeScenarioInfo(self, file):
        """
        Writes out the scenario info for the current scenario to 'file'. Returns 1 if all is ok
        and 0 on error.
        """
        # do we have a scenario info at all?
        if not scenario.info:
            # no info, we should not be here
            print("writeScenarioInfo: no scenario info")
            return 0

        # use existing method to do the trick
        try:
            file.write(scenario.info.toXML())
        except:
            # failed to write
            return 0

        # all is ok
        return 1

    def writeWeapons(self, file):
        """
        Writes out all available weapons in the scenario. Only those weapons that were in the
        possible original scenario that were actually *used* are written out. Weapons that are not
        used by any unit are not written. Returns 1 if all is ok and 0 on error.
        """

        try:
            # write start tag
            file.write(self.indent * 1 + '<weapons>\n')

            # a list of the weapon id:s we've already stored
            written = []

            # loop over all units we have
            list_of_all_units = list(scenario.info.units.values())
            list_of_all_units.extend(list(scenario.info.destroyed_units.values()))

            for unit in list_of_all_units:
                # get its weapon
                weapon = unit.getWeapon()
                id = weapon.getId()

                # have we already written out that weapon?
                if not id in written:
                    # not yet written, write out
                    file.write(self.indent * 2 + weapon.toXML() + '\n')

                    # add to the list
                    written.append(id)

            # write stop tag
            file.write(self.indent * 1 + '</weapons>\n')

        except:
            # failed to write
            raise

        # all is ok
        return 1

    def writeUnits(self, file):
        """
        Writes out the full hierarchy of units to 'file'. The hierarchy means all brigades,
        regiments, battalions and companies. The units are written to separate hierarchies for
        union and rebel units. Returns 1 if all is ok and 0 on error.
        """

        try:
            # write start tag
            file.write(self.indent + '<units>\n')

            # write out rebel brigades
            file.write(self.indent * 2 + '<rebel>\n')

            # perform the write
            self.writeBrigades(file, REBEL)

            file.write(self.indent * 2 + '</rebel>\n')

            # write out union brigades
            file.write(self.indent * 2 + '<union>\n')

            # perform the write
            self.writeBrigades(file, UNION)

            file.write(self.indent * 2 + '</union>\n')

            # write stop tag
            file.write(self.indent + '</units>\n')

        except:
            # failed to write
            raise

        # all is ok
        return 1

    def writeBrigades(self, file, player):
        """
        Writes out all brigades to 'file' for 'player'. Recursively writes all regiments
        too. Returns 1 if all is ok and 0 on error.
        """
        # get the brigades for the player
        brigades = scenario.info.brigades[player]

        try:
            # loop over all brigades we have for the player
            for brigade in list(brigades.values()):
                # write out
                file.write('\n' + brigade.toXML(self.indent, 4) + '\n')

        except:
            # failed to write
            raise

        # all is ok
        return 1

    def writeLocations(self, file):
        """
        Writes out all the special map locations that have been defined. Returns 1 if all is ok
        and 0 on error.
        """

        try:
            # write start tag
            file.write(self.indent + '<locations>\n')

            # loop over all locations we have
            for location in scenario.info.locations:
                # write out
                file.write(self.indent * 2 + location.toXML() + '\n')

            # write stop tag
            file.write(self.indent + '</locations>\n')

        except:
            # failed to write
            return 0

        # all is ok
        return 1

    def writeObjectives(self, file):
        """
        Writes out all define objectives. Returns 1 if all is ok and 0 on error.
        """

        try:
            # write start tag
            file.write(self.indent + '<objectives>\n')

            # loop over all objectives we have
            for objective in scenario.info.objectives:
                # write out
                file.write(self.indent * 2 + objective.toXML() + '\n')

            # write stop tag
            file.write(self.indent + '</objectives>\n')

        except:
            # failed to write
            raise

        # all is ok
        return 1

    def writeMap(self, file):
        """
        Writes out the map of the scenario. All hexes within are also written. Returns 1 if all
        is ok and 0 on error.
        """

        # get the map
        map = scenario.map

        # get size of map
        size_x, size_y = map.getSize()

        try:
            # write start tag
            file.write(self.indent + '<map size_x="%d" size_y="%d">\n' % (size_x, size_y))
            file.write(self.indent * 2 + '<hexes>\n')

            # now loop over the entire hex matrix and write out the hexes
            for x in range(size_x):
                for y in range(size_y):
                    # write out the hex
                    file.write(self.indent * 4 + map.getHex(x, y).toXML(x, y) + '\n')

            # write stop tags
            file.write(self.indent * 2 + '</hexes>\n')
            file.write(self.indent + '</map>\n')

        except:
            # failed to write
            return 0

        # all is ok
        return 1
