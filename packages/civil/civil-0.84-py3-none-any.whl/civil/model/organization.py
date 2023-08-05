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

from civil.constants import REBEL, UNION


class Organization:
    """
    This class works as a base class for all organizations in the game. It provides common
    functionality needed on all organizational levels. This class should be inherited by actual real
    organizations, such as regiments and companies.

    The data contained in this class is mainly the unique id, a descriptive name and the leader that
    leads the organization.
    """

    def __init__(self, id, name, owner):
        """
        Initializes the instance. Sets the passed data.
        """
        self.id = id
        self.name = name

        # precautions
        if not owner in (REBEL, UNION):
            # oops, an invalid value
            raise ValueError("invalid owner: " + str(owner))

        # owner ok, store it
        self.owner = owner

        # no parent yet
        self.parent = None

        # use a base command delay
        # TODO: set this value to something meaningful!
        self.commanddelay = 5

    def getId(self):
        """
        Returns the unique id of this organization.
        """
        return self.id

    def getOwner(self):
        """
        Returns the unique owner of this organization.
        """
        return self.owner

    def getName(self):
        """
        Returns the name of this organization.
        """
        return self.name

    def setName(self, name):
        """
        Sets a new name for the organization. If the name is None then an empty name is set instead
        to avoid problems.
        """

        # is the name valid
        if name is None:
            # set an empty name
            self.name = ""
        else:
            self.name = name

    def getCommandDelay(self):
        """
        Returns the command delay for the unit. This value is given in turns. In the future this
        value can be used to simulate the full command delay from the top commanding unit all the
        way down to the separate companies.
        """
        return self.commanddelay

    def setParentOrganization(self, organization):
        """
        Sets the 'organization' as the parent organization for this organization. The parent is
        the larger organization this instance is part of. For a company the parent can be a
        regiment.
        """
        self.parent = organization

    def getParentOrganization(self):
        """
        Returns the parent organization for this organization.  If this method returns None then
        the organization has no parent, i.e. it is so high in the hierarchy that we don't simulate
        it.
        """
        return self.parent

    def __str__(self):
        """
        Debugging aid.
        """
        return "%d: %s" % (self.id, self.name)


class CompoundOrganization(Organization):
    """
    This class is an intermediate class that compund organizations should derive from. It provides
    some extra features and members that only compound organizations need. A compound organization
    here is an organization that consists of other organizations, such as regiments and companies.

    Mainly this class adds a headquarter company where the commander of the organization is
    located. A regiment for instance can have 10 companies, and the commander is placed in one of
    these. 

 """

    def __init__(self, id, name, owner):
        """
        Creates the instance of the class.
        """
        # call superclass constructor
        Organization.__init__(self, id, name, owner)

        # no headquarter yet
        self.headquarter = None

    def getHeadquarter(self):
        """
        Returns the headquarter company of the compound organization. This should be a company,
        but can basically be whatever was set with setHeadquarter(). If it has not been set then
        None is returned.
        """
        return self.headquarter

    def setHeadquarter(self, headquarter):
        """
        Sets a new headquarter for the compound organization. This should be a company otherwise
        TypeError is raised.
        """

        from civil.model.unit import Unit

        # is it a company
        if not isinstance(headquarter, Unit):
            # oops, this was not good
            raise RuntimeError("type '%s' is not a Company" % type(headquarter))

        # all ok, store it
        self.headquarter = headquarter


class Battalion(CompoundOrganization):
    """
    This class
    """

    def __init__(self, id, name, owner):
        """
        Creates the instance of the class.
        """
        # call superclass constructor
        Organization.__init__(self, id, name, owner)

        # initialize the list of companies
        self.companies = []

    def getCompanies(self):
        """
        Returns the companies currently assigned to this battalion.
        """
        return self.companies

    def toXML(self, indent, level):
        """
        Returns a string containing the battalion serialized as XML. The first line is using the
        indent string 'level' times. Internal data is indented 'level+1' steps.
        """

        # build up the xml
        xml = indent * level + '<battalion id="%d" name="%s">\n' % (self.id, self.name)

        # write the headquarter
        xml += self.headquarter.toXML(indent, level + 1)

        # append all companies
        for company in self.companies:
            # append it
            xml += '\n'
            xml += company.toXML(indent, level + 1)

        xml += indent * level + '</battalion>\n'

        return xml


class Regiment(CompoundOrganization):
    """
    This class defines a regiment. A regiment is a collection of <10 companies or two battalions,
    each <8 companies. 

 """

    def __init__(self, id, name, owner):
        """
        Creates the instance of the class.
        """
        # call superclass constructor
        Organization.__init__(self, id, name, owner)

        # initialize the list of companies
        self.companies = []
        self.battalions = []

    def getCompanies(self):
        """
        Returns the companies currently assigned to this regmient.
        """
        return self.companies

    def getBattalions(self):
        """
        Returns the battalions currently assigned to this battalion.
        """
        return self.battalions

    def toXML(self, indent, level):
        """
        Returns a string containing the regiment serialized as XML. The first line is using the
        indent string 'level' times. Internal data is indented 'level+1' steps.
        """

        # build up the xml
        xml = indent * level + '<regiment id="%d" name="%s">\n' % (self.id, self.name)

        # write the headquarter
        xml += self.headquarter.toXML(indent, level + 1)

        # append all battalions
        for battalion in self.battalions:
            # append it
            xml += '\n'
            xml += battalion.toXML(indent, level + 1)

        # append all companies
        for company in self.companies:
            # append it
            xml += '\n'
            xml += company.toXML(indent, level + 1)

        xml += indent * level + '</regiment>\n'

        # print xml
        return xml


class Brigade(CompoundOrganization):
    """
    This class
    """

    def __init__(self, id, name, owner):
        """
        Creates the instance of the class.
        """
        # call superclass constructor
        Organization.__init__(self, id, name, owner)

        # initialize the list of regiments
        self.regiments = []

    def getCompanies(self):
        """
        Returns all the companies currently assigned to this brigade.
        """
        companies = []

        # loop over all regiments and add its companies
        for regiment in self.regiments:
            # append the companies of the regiment
            companies = companies + regiment.getCompanies()

        return companies

    def getRegiments(self):
        """
        Returns the regiments currently assigned to this battalion.
        """
        return self.regiments

    def toXML(self, indent, level):
        """
        Returns a string containing the brigade serialized as XML. The first line is using the
        indent string 'level' times. Internal data is indented 'level+1' steps.
        """

        # print self.id, self.name, self.headquarter.getId()

        # build up the xml
        xml = indent * level + '<brigade id="%d" name="%s">\n' % (self.id, self.name)

        # write the headquarter
        xml += self.headquarter.toXML(indent, level + 1)

        # append all regiments
        for regiment in self.regiments:
            # append it
            xml += '\n'
            xml += regiment.toXML(indent, level + 1)

        xml += indent * level + '</brigade>\n'
        return xml


class Division(CompoundOrganization):
    """
    This class
    """

    def __init__(self, id, name, owner):
        """
        Creates the instance of the class.
        """
        # call superclass constructor
        Organization.__init__(self, id, name, owner)

        # initialize the list of brigades
        self.brigades = []

    def getCompanies(self):
        """
        Returns all the companies currently assigned to this division.
        """
        companies = []

        # loop over all brigades and add its companies
        for brigade in self.brigades:
            # append the companies of the brigade
            companies = companies + brigade.getCompanies()

        return companies

    def getBrigades(self):
        """
        Returns the brigades currently assigned to this battalion.
        """
        return self.brigades


def toString(id):
    """
    Creates and returns a string that matches the given id. The id is one of the integers REBEL
    and UNION defined in the beginning of this file. Raises ValueError on invalid value.
    """
    # do we have a union?
    if id == UNION:
        return "union"

    # do we have a rebel?
    if id == REBEL:
        return "rebel"

    # something else
    raise ValueError('invalid id: ' + str(id))
