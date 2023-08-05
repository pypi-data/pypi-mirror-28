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
This application is a sample test application that works as a scenario repository server. It can
serve out scenarios using XML-RPC to clients on the 'net. The clients can get information such as
the number of available scenarios, a list of scenarios, scenario names and of course full
scenarios.

The server reads the scenarios from a directory which is given as a commandline parameter. The
directory must contain a 'scenarioindex.xml' file which contains condensed info about the
scenarios in the directory.
"""

import string

from civil.serialization import xmlrpcserver


class ScenarioServer(xmlrpcserver.RequestHandler):
    """
    Comments...
    """

    def __init__(self, manager):
        # store the scenario manager
        self.manager = manager

    def call(self, method, params):
        """

        Args:
            method: 
            params: 

        Returns:

        """
        print("Dispatching: ", method, params)
        try:
            server_method = getattr(self, method)
        except:
            raise AttributeError("Server does not contain XML-RPC procedure %s" % method)
        return server_method(method, params)

    def getScenarioList(self, method, params):
        """

        Args:
            method: 
            params: 

        Returns:

        """
        # build up the raw xml we're about to send
        xml = '<?xml version="1.0"?><scenarioindex>\n'

        # loop over all infos we got
        for info in self.manager.getScenarios():
            # add the xml for this info
            xml += info.toXML()

        # append the closing tag
        xml += '</scenarioindex>\n'
        return xml

    def getScenarioNames(self, method, params):
        """
        Returns a list of all the names of the scenarios.
        """

        names = []

        # loop over all infos we got
        for info in self.manager.getScenarios():
            # add the name
            names.append(info.getName())

        # return the list
        return names

    def getScenarioCount(self, method, params):
        """
        Returns the number of scenarios that are available.
        """

        # just return the count
        return len(self.manager.getScenarios())

    def getScenario(self, method, params):
        """
        Returns a scenario with the given 'id' or some kind of error on error.
        """

        # extract the id
        id = params[0]

        # loop over all infos we got
        for info in self.manager.getScenarios():
            # is this the wanted?
            if id == info.getId():
                # yep, here it is, read it in into a list
                file = info.getFile()
                print("sending %s" % file)

                # read in all lines
                scenario = open(file).readlines()

                # join the strings and send out
                return "".join(scenario)

        # we got this far, so no matching scenario found
        return 'invalid id'
