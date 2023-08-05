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

import datetime
import sys
import traceback

from civil import properties
from civil.model import scenario
from civil.constants import UNION, REBEL, UNKNOWN
from civil.model.location import Location
from civil.map.hex import Hex
from civil.model.organization import Brigade, Battalion, Regiment
from civil.serialization.simple_dom_parser import SimpleDOMParser
from civil.model.unit import InfantryCompany, CavalryCompany, ArtilleryBattery, Headquarter
from civil.model.leader import Leader
from civil.model.modifier import Morale, Fatigue, Experience, Aggressiveness, RallySkill, Motivation
from civil.model.objective import Objective
from civil.model.scenario_info import ScenarioInfo
from civil.model.weapon import Weapon


class ScenarioParser:
    """
    This class works as a compact parser for the scenario files used within Civil. This class has as
    its only purpose to read a given url/file_name and parse all scenario data from it. All data is
    stored in members in the global file 'scenario'. 

    The parsing works by first reading the entire file into a simple DOM tree and then doing the
    actual parsing. This is a simpler approach as we when the actual parsing is done have the full
    data available.

    Use this class like this:

    if not ScenarioParser ().parseFile ( file ):
        # failed to parse the file
        ...
    else:
        # file parsed ok
        ...

    Separate methods exist for most of the big groups of data in the scenario file.
    """

    def __init__(self):
        """
        Creates the instance of the class. Does no parsing yet.
        """

        # no root yet
        self.root = None

        # helper members for the unit hierarchy
        self.currentBrigade = None
        self.currentRegiment = None
        self.currentBattalion = None

        # helper hash for all weapons
        self.weapons = {}

    def parseString(self, data):
        """
        Parses the passed string 'data' and creates the data into the scenario. An internal DOM
        tree is built up from the XML data and it is then parsed. Returns 1 on success and 0 on
        error.
        """

        # create a new parser
        domparser = SimpleDOMParser()

        # parse the data
        try:
            self.root = domparser.parseString(data)

        except:
            # serious error
            print("Error parsing passed string, aborting parse")
            raise

        # did we get anything?
        if self.root is None:
            # nope, failed to retrieve it
            print("Failed to parse XML from string")
            del self.root
            return 0

        # now parse the data
        status = self.parseRoot()

        # delete the root and return the data
        del self.root
        return status

    def parseFile(self, file_name):
        """
        Parses the passed 'file_name' and creates the data into the scenario. An internal DOM tree is
        built up from the XML data and it is then parsed. Returns 1 on success and 0 on error.
        """

        # create a new parser
        domparser = SimpleDOMParser()

        try:
            # parse the data
            # self.root = domparser.parseFile ( open ( url ) )
            self.root = domparser.parseFile(file_name)
            # self.root = domparser.parseFile ( gzip.GzipFile  ( url, 'rb' ) )

        except:
            # serious error
            print("Error reading: " + file_name + ", aborting parse")
            raise

        # did we get anything?
        if self.root is None:
            # nope, failed to retrieve it
            print("Failed to retrive or parse XML from: " + file_name)
            del self.root
            return 0

        # now parse the data
        status = self.parseRoot()

        # delete the root and return the data
        del self.root
        return status

    def parseRoot(self):
        """
        Parses a passed DOM-tree and builds up a number of instances of ScenarioInfo. They are
        appended to the internal list of scenario-info:s.
        """
        # the top-level root should be 'scenario'
        if self.root.getName() != 'scenario':
            # oops, illegal file
            print("DOM tree is illegal, top-level tag is: " + self.root.getName() + ", ")
            print("the node should be 'scenario'")
            return

        # Default
        version = "0.80"
        try:
            version = self.root.getAttribute("version")
        except:
            print("Don't know which version format, assuming 0.80")
            pass

        #
        # Here we should decide which scenario_parser to really
        # use, based on the variable "version"
        #
        # Currently supported versions:
        # 0.80, tagged 2002-08-30
        #
        # 0.82, tagged 2003-xx-yy, adds the <valid/> and <invalid/> tags

        # set the valid children for this level
        valid = {'scenarioinfo': self.parseScenarioInfo,
                 'weapons': self.parseWeapons,
                 'units': self.parseUnits,
                 'locations': self.parseLocations,
                 'objectives': self.parseObjectives,
                 'map': self.parseMap}

        # loop over all top-level children
        for node in self.root.getChildren():
            try:
                # execute the proper handler for the node
                valid[node.getName()](node)

            except KeyError:
                # no such node
                print("Illegal tag in root tag: '%s'." % node.getName())
                raise

        # fix the targets of the units
        if not self.fixUnitTargets():
            return 0

        return 1

    def parseScenarioInfo(self, node):
        """


 """
        try:
            # get the simple data
            name = node.getChild('name').getData()
            location = node.getChild('location').getData()
            theatre = node.getChild('theatre').getData()

            # do we have an id?
            if node.hasAttribute('id'):
                # yep, get it
                id = int(node.getAttribute('id'))
            else:
                id = None

            # do we have a local player id? if we have that then it must be parsed too
            idnode = node.getChild('localplayer')
            if idnode is not None:
                # yes, we have one so get the attribute and store it
                scenario.local_player_id = int(idnode.getAttribute('id'))

            # no description yet
            description = []

            # and the description
            for paratag in node.getChild('description').getChildren():
                # get the text
                para = paratag.getData()

                # append the text to the description
                description.append(para)

            # get the rebel and union missions
            rebel = []
            union = []

            # get the missions
            mission = node.getChild('missions')

            # rebel missions
            for paratag in mission.getChild('rebel').getChildren():
                # get the text and append to the description
                rebel.append(paratag.getData().strip())

            # union missions
            for paratag in mission.getChild('union').getChildren():
                # get the text and append to the description
                union.append(paratag.getData().strip())

            # create a new scenario info if we don't already have one 
            if scenario.info is None:
                scenario.info = ScenarioInfo(id)

            # get the starting date and split it up
            start_datenode = node.getChild('startdate')
            start_year = int(start_datenode.getAttribute('year'))
            start_month = int(start_datenode.getAttribute('month'))
            start_day = int(start_datenode.getAttribute('day'))
            start_hour = int(start_datenode.getAttribute('hour'))
            start_minute = int(start_datenode.getAttribute('minute'))
            start_second = 0

            # get the current date and split it up
            current_datenode = node.getChild('currentdate')
            current_year = int(current_datenode.getAttribute('year'))
            current_month = int(current_datenode.getAttribute('month'))
            current_day = int(current_datenode.getAttribute('day'))
            current_hour = int(current_datenode.getAttribute('hour'))
            current_minute = int(current_datenode.getAttribute('minute'))
            current_second = 0

            # get the ending date and split it up
            end_datenode = node.getChild('enddate')
            end_year = int(end_datenode.getAttribute('year'))
            end_month = int(end_datenode.getAttribute('month'))
            end_day = int(end_datenode.getAttribute('day'))
            end_hour = int(end_datenode.getAttribute('hour'))
            end_minute = int(end_datenode.getAttribute('minute'))
            end_second = 0

            # set all parsed data
            scenario.info.setName(name)
            scenario.info.setLocation(location)
            scenario.info.setTheatre(theatre)
            scenario.info.setDescription(description)
            scenario.info.setStartDate(datetime.datetime(start_year, start_month, start_day,
                                                         start_hour, start_minute, start_second))
            scenario.info.setCurrentDate(datetime.datetime(current_year, current_month, current_day,
                                                           current_hour, current_minute, current_second))
            scenario.info.setEndDate(datetime.datetime(end_year, end_month, end_day,
                                                       end_hour, end_minute, end_second))
            scenario.info.setMission(REBEL, rebel)
            scenario.info.setMission(UNION, union)

            # now we need to see if the scenario is valid at all
            # TODO: version checks?
            if node.getChild('valid') is None:
                # no such node, so the scenario is invalid
                scenario.info.setValid(0)
            else:
                # it's valid all right
                scenario.info.setValid(1)

        except KeyError:
            # oops, invalid data
            traceback.print_exc(file=sys.stdout)
            print("Invalid data in <scenarioinfo> node of scenario.")
            return 0

        # all is ok
        return 1

    def parseUnits(self, node):
        """
        This method parses all units of the game. This method parses the tag <units> and the
        children <union> and <rebel> of that tag.
        """

        # get the mandatory children
        rebel = node.getChild('rebel')
        union = node.getChild('union')

        # loop over all union brigades
        for node in union.getChildren():
            # parse the brigade
            if not self.parseBrigade(node, UNION):
                # failed to parse it
                return 0

        # loop over all rebel brigades
        for node in rebel.getChildren():
            # parse the brigade
            if not self.parseBrigade(node, REBEL):
                # failed to parse it
                return 0

        # all is ok
        return 1

    def parseBrigade(self, node, owner):
        """


 """
        # precautions
        if node.getName() != 'brigade':
            # oops, invalid tag here
            print("Invalid data: '" + node.getName() + "', expected brigade")
            return 0

        # get the necessary attributes
        id = int(node.getAttribute('id'))
        name = node.getAttribute('name')

        # create a new brigade
        brigade = Brigade(id, name, owner)

        # parse and set the headquarter
        hq = self.parseHeadquarter(node.getChild('headquarter'), owner)
        brigade.setHeadquarter(hq)

        # make the hq a hq for this brigade
        hq.setHeadquarterFor(brigade)

        # set the parent organization
        # TODO: higher organizations?
        brigade.setParentOrganization(None)
        hq.setParentOrganization(None)

        # add the brigade to the scenario data
        scenario.info.brigades[brigade.getOwner()][brigade.getId()] = brigade

        # this brigade is the new current brigade
        self.currentBrigade = brigade

        # loop over all the regiments
        for regiment in node.getChildren():
            # is this node a commander?
            if regiment.getName() == 'headquarter':
                # yep, don't parse it
                continue

            # parse the regiment
            if not self.parseRegiment(regiment, owner):
                # failed to parse it
                return 0

        # print "Parsed brigade id ", id

        # all is ok
        return 1

    def parseRegiment(self, node, owner):
        """


 """
        # precautions
        if node.getName() != 'regiment':
            # oops, invalid tag here
            print("Invalid data: '" + node.getName() + ", expected regiment")
            return 0

        # get the necessary attributes
        id = int(node.getAttribute('id'))
        name = node.getAttribute('name')

        # create a new regiment
        regiment = Regiment(id, name, owner)

        # parse and set the headquarter
        hq = self.parseHeadquarter(node.getChild('headquarter'), owner)
        regiment.setHeadquarter(hq)

        # make the hq a hq for this brigade
        hq.setHeadquarterFor(regiment)

        # set the parent organization 
        regiment.setParentOrganization(self.currentBrigade)
        hq.setParentOrganization(self.currentBrigade)

        # add this regiment to the regiments for the current brigade
        self.currentBrigade.getRegiments().append(regiment)

        # this  is the new current 
        self.currentRegiment = regiment
        self.currentBattalion = None

        # loop over all the sub-nodes. These may be battalions or companies
        for organization in node.getChildren():
            # is this node a leader?
            if organization.getName() == 'headquarter':
                # yep, don't parse it
                continue

            # what do we have here?
            elif organization.getName() == 'battallion':
                # parse the battalion
                if not self.parseBattalion(organization, owner):
                    # error parsing
                    return 0

            elif organization.getName() == 'company':
                # parse the battalion
                if not self.parseCompany(organization, owner):
                    # error parsing
                    return 0

            else:
                # invalid tag
                print("Invalid data: '" + organization.getName() + ", expected battalion, company")
                return 0

        # print "Parsed regiment id ", id

        # all is ok
        return 1

    def parseBattalion(self, node, owner):
        """


 """
        # precautions are unnecessary here, as it was checked above

        try:
            # get the necessary attributes
            id = int(node.getAttribute('id'))
            name = node.getAttribute('name')

            # create a new brigade
            battalion = Battalion(id, name, owner)

            # parse and set the headquarter
            hq = self.parseHeadquarter(node.getChild('headquarter'), owner)
            battalion.setHeadquarter(hq)

            # make the hq a hq for this brigade
            hq.setHeadquarterFor(battalion)

            # set the parent organization 
            battalion.setParentOrganization(self.currentRegiment)
            hq.setParentOrganization(self.currentRegiment)

            # add this regiment to the regiments for the current brigade
            self.currentRegiment.getBattalions().append(battalion)

            # this  is the new current 
            self.currentBattalion = battalion

            # loop over all the companies
            for company in node.getChildren():
                # is this node a leader?
                if company.getName() == 'headquarter':
                    # yep, don't parse it
                    continue

                # parse the company
                if not self.parseCompany(company, owner):
                    # failed to parse it
                    return 0

        except KeyError:
            # oops, invalid data
            traceback.print_exc(file=sys.stdout)
            print("Invalid data in <battalion> node of scenario.")
            return 0

        # print "Parsed battalion id ", id

        # all is ok
        return 1

    def parseCompany(self, node, owner):
        """


 """
        # precautions
        if node.getName() != 'company':
            # oops, invalid tag here
            print("Invalid data: '" + node.getName() + ", expected company")
            return 0

        try:
            # get the necessary attributes
            id = int(node.getAttribute('id'))
            name = node.getAttribute('name')
            type = node.getAttribute('type')
            company = None

            # what type did we get?
            if type == 'infantry':
                # create a new infantry unit
                company = InfantryCompany(id, name, owner)

            elif type == 'cavalry':
                # create a new cavalry unit
                company = CavalryCompany(id, name, owner)

            elif type == 'artillery':
                # create a new artillery unit
                company = ArtilleryBattery(id, name, owner)

            else:
                print("Unknown company type: " + type)
                return 0

            # parse the commander from the <commander> tag
            company.setCommander(self.parseCommander(node.getChild('commander')))

            # add the unit to the current battalion or regiment
            if self.currentBattalion is not None:
                # currently filling in a battalion
                self.currentBattalion.getCompanies().append(company)

                # set the parent organization 
                company.setParentOrganization(self.currentBattalion)

            elif self.currentRegiment is not None:
                # currently filling in a regiment
                self.currentRegiment.getCompanies().append(company)

                # set the parent organization 
                company.setParentOrganization(self.currentRegiment)

            # get all other data
            company.setMen(int(node.getChild('men').getAttribute('ok')))
            company.setKilled(int(node.getChild('men').getAttribute('killed')))
            company.setFacing(int(node.getChild('facing').getAttribute('value')))
            company.setMorale(Morale(int(node.getChild('morale').getAttribute('value'))))
            company.setExperience(Experience(int(node.getChild('experience').getAttribute('value'))))
            company.setFatigue(Fatigue(int(node.getChild('facing').getAttribute('value'))))

            # get the position
            pos = node.getChild('pos')
            company.setPosition((int(pos.getAttribute('x')), int(pos.getAttribute('y'))))

            # do we have a arrival turn if we have that then it must be parsed too
            arrivesnode = node.getChild('arrives')
            if arrivesnode is not None:
                # yes, so get the attribute describing when the unit arrives and split it up
                year = int(arrivesnode.getAttribute('year'))
                month = int(arrivesnode.getAttribute('month'))
                day = int(arrivesnode.getAttribute('day'))
                hour = int(arrivesnode.getAttribute('hour'))
                minute = int(arrivesnode.getAttribute('minute'))
                second = 0

                # create a date object from the data
                date = datetime.datetime(year, month, day, hour, minute, second)

                # store the unit as a reinforcement along with the date
                scenario.info.reinforcements[company.getId()] = (company, date)

                # make unit hidden at first
                company.setVisible(0)
            else:
                # the unit is immediately available, but does it have any men at all? it might
                # already be destroyed
                if company.getMen() == 0:
                    # no men, so this is a destroyed unit
                    scenario.info.destroyed_units[company.getId()] = company
                    company.setDestroyed()
                else:
                    # unit is ok
                    scenario.info.units[company.getId()] = company

            # do we have a target id? if we have that then it must be parsed too
            targetnode = node.getChild('target')
            if targetnode is not None:
                # yes, we have one so get the attribute and store it. Note that this is basically
                # wrong! We store a numeric id in the member, where a full unit was expected. This
                # will later in the parser be fixed by looping all units and setting the correct
                # id:s. it can't be done now, as all units may not yet be parsed
                company.target = int(targetnode.getAttribute('id'))

            # get and set the the weapon
            try:
                # get the weapon
                weapon = int(node.getChild('weapon').getAttribute('id'))
                okcount = int(node.getChild('weapon').getAttribute('ok'))
                destroyedcount = int(node.getChild('weapon').getAttribute('destroyed'))

                # get the matching weapon. The weapon is an id that refers to previously parsed
                # weapons stored locally
                company.setWeapon(self.weapons[weapon])
                company.setWeaponCounts(okcount, destroyedcount)

            except KeyError:
                # we have a custom catch here, as this is one of the few places where we refer to
                # old information
                traceback.print_exc(file=sys.stdout)
                print("Invalid weapon id in <company> node of scenario.")
                return 0

        except KeyError:
            # oops, invalid data
            traceback.print_exc(file=sys.stdout)
            print("Invalid data in <company> node of scenario.")
            return 0

        # print "Parsed company id ", id

        # all is ok
        return 1

    def parseHeadquarter(self, node, owner):
        """
         """
        # precautions
        if node.getName() != 'headquarter':
            # oops, invalid tag here
            print("Invalid data: '" + node.getName() + ", expected headquarter")
            return None

        try:
            # get the necessary attributes
            id = int(node.getAttribute('id'))
            name = node.getAttribute('name')

            # create a hq
            hq = Headquarter(id, name, owner)

            # parse the commander from the <commander> tag
            hq.setCommander(self.parseCommander(node.getChild('commander')))

            # get all other data
            hq.setMen(int(node.getChild('men').getAttribute('ok')))
            hq.setKilled(int(node.getChild('men').getAttribute('killed')))
            hq.setFacing(int(node.getChild('facing').getAttribute('value')))
            hq.setMorale(Morale(int(node.getChild('morale').getAttribute('value'))))
            hq.setExperience(Experience(int(node.getChild('experience').getAttribute('value'))))
            hq.setFatigue(Fatigue(int(node.getChild('fatigue').getAttribute('value'))))

            # does it have any men at all?
            if hq.getMen() == 0:
                # no men, so this is a destroyed unit
                scenario.info.destroyed_units[hq.getId()] = hq
                hq.setDestroyed()
            else:
                # unit is ok
                scenario.info.units[hq.getId()] = hq

            # get the position
            pos = node.getChild('pos')
            hq.setPosition((int(pos.getAttribute('x')), int(pos.getAttribute('y'))))

            # get and set the the weapon
            weapon = int(node.getChild('weapon').getAttribute('id'))
            okcount = int(node.getChild('weapon').getAttribute('ok'))
            destroyedcount = int(node.getChild('weapon').getAttribute('destroyed'))

            # get the matching weapon. The weapon is an id that refers to previously parsed
            # weapons stored locally
            hq.setWeapon(self.weapons[weapon])
            hq.setWeaponCounts(okcount, destroyedcount)

        except KeyError:
            # oops, invalid data
            traceback.print_exc(file=sys.stdout)
            print("Invalid data in <headquarter> node of scenario.")
            return None

        # print "Parsed headquarter",hq

        # all is ok
        return hq

    def parseCommander(self, node):
        """
        This method parses out data of a <commander> tag. A new instance of the class Leader is
        created and returned if all is ok. If not then None is returned. This method differs a bit
        from the return-value semantics of the other methods.
        """
        # precautions are unnecessary here, as it was checked above

        try:
            # get the necessary attributes
            name = node.getAttribute('name')
            # rank  = "Captain"
            rank = node.getChild('rank').getData()
            agg = Aggressiveness(int(node.getChild('aggressiveness').getAttribute('value')))
            exp = Experience(int(node.getChild('experience').getAttribute('value')))
            rally = RallySkill(int(node.getChild('rally').getAttribute('value')))
            mot = Motivation(int(node.getChild('motivation').getAttribute('value')))

            # print "Parsed commander name", name

            # create a new leader and return it
            return Leader(name, rank, agg, exp, rally, mot)

        except KeyError:
            # oops, invalid data
            traceback.print_exc(file=sys.stdout)
            print("Invalid data in <commander> node of scenario.")
            return None

    def parseObjectives(self, node):
        """


 """
        # loop over all children this node has
        for tmpnode in node.getChildren():

            # precautions
            if tmpnode.getName() != 'objective':
                # oops, invalid tag here
                print("Invalid data: '" + tmpnode.getName() + "', expected objective")
                return 0

            try:
                # get the necessary attributes
                id = int(tmpnode.getAttribute('id'))
                points = int(tmpnode.getAttribute('points'))
                x = int(tmpnode.getAttribute('x'))
                y = int(tmpnode.getAttribute('y'))
                owner = tmpnode.getAttribute('owner')
                name = tmpnode.getAttribute('name')
                desc = tmpnode.getData()

                # create a new objective
                objective = Objective(id, (x, y))

                # assign the other data
                objective.setName(name)
                objective.setDescription(desc)
                objective.setPoints(points)

                # set the owner
                owners = {"union": UNION, "rebel": REBEL, "unknown": UNKNOWN}
                objective.setOwner(owners.get(owner, UNKNOWN))

                # add the new objective to the scenario data
                scenario.info.objectives.append(objective)

            except KeyError:
                # oops, invalid data
                traceback.print_exc(file=sys.stdout)
                print("Invalid data in <objectives> node of scenario.")
                raise

        # all is ok
        return 1

    def parseWeapons(self, node):
        """
        This method parses the tag <weapons> and all the subtags <weapon> that should be in
        it. The weapons arw initialized and placed in an internal list, where they can be retrieved
        when needed for units.
        """
        # loop over all children this node has
        for tmpnode in node.getChildren():
            # precautions
            if tmpnode.getName() != 'weapon':
                # oops, invalid tag here
                print("Invalid data: '" + tmpnode.getName() + "', expected weapon")
                return 0

            try:
                # get the necessary attributes
                id = int(tmpnode.getAttribute('id'))
                name = tmpnode.getAttribute('name')
                type = tmpnode.getAttribute('type')
                range = int(tmpnode.getAttribute('range'))
                damage = int(tmpnode.getAttribute('damage'))
                accuracy = int(tmpnode.getAttribute('accuracy'))

                # create a new weapon
                weapon = Weapon(id, name, type, range, damage, accuracy)

                # add the new objective to the internal hash
                self.weapons[id] = weapon

            except KeyError:
                # oops, invalid data
                traceback.print_exc(file=sys.stdout)
                print("Invalid data in <weapon> node of scenario.")
                return 0

        # all is ok
        return 1

    def parseLocations(self, node):
        """
        This method parses all data in the tag <location>, i.e. all specially named locations on
        the map. Creates instances of Location and stores in the global scenario data.
        """
        # loop over all children this node has
        for tmpnode in node.getChildren():
            # precautions
            if tmpnode.getName() != 'location':
                # oops, invalid tag here
                print("Invalid data: '" + tmpnode.getName() + "', expected location")
                return 0

            try:
                # get the necessary attributes
                x = int(tmpnode.getAttribute('x'))
                y = int(tmpnode.getAttribute('y'))
                name = tmpnode.getData()

                # create a new location
                location = Location(x, y, name)

                # add the new location to the scenario data
                scenario.info.locations.append(location)

            except KeyError:
                # oops, invalid data
                traceback.print_exc(file=sys.stdout)
                print("Invalid data in <locations> node of scenario.")
                return 0

        # all is ok
        return 1

    def parseMap(self, node):
        """


 """
        # precautions
        if node.getName() != 'map':
            # oops, invalid tag here
            print("Invalid data: '" + node.getName() + "', expected map")
            return 0

        try:
            # get the necessary attributes
            size_x = int(node.getAttribute('xsize'))
            size_y = int(node.getAttribute('ysize'))

            # create a new map
            if properties.is_civil_editor:
                from civil.editor.editor_map import EditorMap
                map = EditorMap(size_x, size_y)
            else:
                from civil.map.map_displayable import MapDisplayable
                map = MapDisplayable(size_x, size_y)

            # store the map too
            scenario.map = map

            # loop over all children this node has
            for tmpnode in node.getChild('hexes').getChildren():
                # precautions
                if tmpnode.getName() != 'hex':
                    # oops, invalid tag here
                    print("Invalid data: '" + tmpnode.getName() + "', expected hex")
                    return 0

                # get the necessary attributes
                terrain = int(tmpnode.getAttribute('terrain'))
                x = int(tmpnode.getAttribute('x'))
                y = int(tmpnode.getAttribute('y'))

                # Compatibility cruft if no height given
                try:
                    height = int(tmpnode.getAttribute('height'))
                except:
                    height = 0

                # create a new hex
                hex = Hex(terrain, height)

                # store the hex
                map.getHexes()[y][x] = hex

            # do we have any extra features?
            features = node.getChild('features')
            if features is None:
                # no such data, so we're done here
                return 1

            # loop over all the features we got
            for featurenode in features.getChildren():
                # get all data from it
                type = featurenode.getAttribute('type')
                id = int(featurenode.getAttribute('id'))
                x = int(featurenode.getAttribute('x'))
                y = int(featurenode.getAttribute('y'))

                # and add the new feature to the map
                map.addFeature(type, id, x, y)

        except KeyError:
            # oops, invalid data
            traceback.print_exc(file=sys.stdout)
            print("Invalid data in <hex> node of scenario.")
            return 0

        # all is ok
        return 1

    def fixUnitTargets(self):
        """
        Loops over all units and sets the proper targets for them. While parsing the units the
        targets we set (for those that had them) to be the id:s of the targets, not the full
        units. Now all units are parsed, and we can assign the full units instead of the
        id:s. Returns 1 if all is ok and 0 on error.
        """

        try:
            # loop over all units we have
            for unit in scenario.info.units.values():
                # get the target
                targetid = unit.getTarget()

                # is it an id?
                if targetid is None:
                    # no, next please
                    continue

                # get the target matching the id and assign it
                unit.setTarget(scenario.info.units[targetid])

        except KeyError:
            # oops, no such unit
            traceback.print_exc(file=sys.stdout)
            print("could not find unit %d, invalid target for unit %d" % (targetid, unit.getId()))
            return 0


# testing
if __name__ == '__main__':
    ScenarioParser().parseFile('../scenarios/scenario10.xml')
    print("ok")
