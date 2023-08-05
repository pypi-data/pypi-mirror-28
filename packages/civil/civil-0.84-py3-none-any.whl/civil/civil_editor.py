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

import sys
import traceback

from PyQt5 import QtWidgets

from civil.editor import globals as editor_globals
from civil import properties
from civil.serialization.simple_dom_parser import SimpleDOMParser
from civil.editor.mainwindow import MainWindow
from civil.editor.editor_weapon import EditorWeapon


def readWeapons():
    """
    Reads in all weapons from an XML file and stores them in the global data.
    """

    # create a parser
    parser = SimpleDOMParser()

    # parse the data
    try:
        # read it
        # TODO hardcoded?
        root = parser.parseFile('civil/editor/data/weapons.xml')

        # is the root ok?
        if root.getName() != 'weapons':
            # oops, invalid weapon data file
            print("invalid data in editor/data/weapons.xml, expected 'weapons' root tag")
            sys.exit(1)

        # loop over all children this node has
        for node in root.getChildren():
            # what do we have here?
            if node.getName() == 'defaults':
                # read the attributes indicating the default weapon id:s for the various units
                editor_globals.defaultweapons['infantry'] = int(node.getAttribute('infantry'))
                editor_globals.defaultweapons['cavalry'] = int(node.getAttribute('cavalry'))
                editor_globals.defaultweapons['artillery'] = int(node.getAttribute('artillery'))
                editor_globals.defaultweapons['headquarter'] = int(node.getAttribute('headquarter'))

            elif node.getName() == 'weapon':
                # get the necessary attributes
                id = int(node.getAttribute('id'))
                name = node.getAttribute('name')
                type = node.getAttribute('type')
                range = int(node.getAttribute('range'))
                damage = int(node.getAttribute('damage'))
                accuracy = int(node.getAttribute('accuracy'))

                # availability data
                startyear = int(node.getAttribute('startyear'))
                startmonth = int(node.getAttribute('startmonth'))
                endyear = int(node.getAttribute('endyear'))
                endmonth = int(node.getAttribute('endmonth'))

                # create a new weapon
                weapon = EditorWeapon(id, name, type, range, damage, accuracy,
                                      (startyear, startmonth), (endyear, endmonth))

                # add the new objective to the global hash
                editor_globals.weapons[id] = weapon

            else:
                # oops, invalid tag here
                print("Invalid data in : editor/data/weapons.xml, expected weapons of defaults")
                sys.exit(1)

    except KeyError:
        # oops, something went wrong
        print("error parsing editor/data/weapons.xml: ")
        traceback.print_exc(file=sys.stdout)
        sys.exit(1)


def readRanks():
    """
    Reads in all available commander ranks from an XML file and stores them in the global data.'
    """

    # create a parser
    parser = SimpleDOMParser()

    # parse the data
    try:
        # read it
        # TODO hardcoded?
        root = parser.parseFile('civil/editor/data/ranks.xml')

        # is the root ok?
        if root.getName() != 'ranks':
            # oops, invalid weapon data file
            print("invalid data in editor/data/ranks.xml, expected 'ranks' root tag")
            sys.exit(1)

        # loop over all children this node has
        for node in root.getChildren():
            # what do we have here?
            if node.getName() == 'default':
                # the default rank
                editor_globals.defaultrank = node.getData()

            elif node.getName() == 'rank':
                # a rank, get the rank name
                rank = node.getData()

                # add the new rank to the global data
                editor_globals.ranks.append(rank)

    except KeyError:
        # oops, something went wrong
        print("error parsing editor/data/ranks.xml: ")
        traceback.print_exc(file=sys.stdout)
        sys.exit(1)


def readXML():
    """
    Reads in all XML data.
    """

    # read weapons
    readWeapons()

    # read ranks
    readRanks()


def main():
    """
    Main function of the game. Initializes everything and executes the main window of the entire
    application.
    """

    # Needed by scenario_parser.parseMap
    properties.is_civil_editor = 1

    # parse in all XML data
    readXML()

    # create the application
    application = QtWidgets.QApplication(sys.argv)

    # create the main window
    mainwindow = MainWindow()
    application.setMainWidget(mainwindow)

    # show it
    mainwindow.show()

    # execute the application
    application.exec_loop()


# run, civil, run
if __name__ == '__main__':
    main()
