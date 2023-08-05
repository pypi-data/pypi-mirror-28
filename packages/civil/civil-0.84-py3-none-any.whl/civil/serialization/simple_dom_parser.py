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
import xml.parsers.expat


class DOMError(Exception):
    """
    Class that defines an exception that this class may throw.
    """
    pass


class Node:
    """
    This class defines a node in a DOM-tree (Document Object Model). It has a name, which is the
    name of the tag, any number of attributes, some textual data and any number of children. All
    these separate parts can be easily accessed.
    """

    def __init__(self, name, attrs=None, data=""):
        """
        Creates a new node with the given name and attributes. By default it has no data and no


 """
        if attrs is None:
            attrs = {}
        self.children = []
        self.data = data
        self.attrs = attrs
        self.name = name

    def getName(self):
        """
        Returns the name of the node.
        """
        return self.name

    def getAttributes(self):
        """
        Returns the attributes of the node. The returned type is a map with the attribute name as
        the key.
        """
        return self.attrs

    def getAttribute(self, name):
        """
        Returns the value of the given attribute of the node. The returned type is a string with
        the value for the given attribute. Raises KeyError if no such attribute was found.
        """
        return self.attrs[name]

    def hasAttribute(self, name):
        """
        Checks weather the node has the attribute 'name'. Returns 1 if it exists and 0 if not.
        """
        return name in self.attrs

    def getData(self):
        """
        Returns a string which is the data of the node. Data is found between the opening and
        closing tag.
        """
        return self.data

    def getChildren(self):
        """
        Returns all children of this node as a list. The list can be altered if needed.
        """
        return self.children

    def getChild(self, name):
        """
        Returns the first child with the given name. If no child is found then None is returned.
        """
        # loop over the children
        for child in self.children:
            # is this the wanted node?
            if child.getName() == name:
                return child

        # no such child found
        return None


class SimpleDOMParser:
    """
    This class is a simple parser that builds a DOM-tree (Document Object Model) from a passed
    file name of a XML file. The tree is created from a number of Node instances, and does not
    tightly follow the normal W3C conventions for DOM trees. The purpose of this parser is to be
    very fast and produce a tree that is very simple to iterate over.

    The main method is the method parse(). It takes a file name and parses the XML file and returns a
    valid tree.

    If errors occur there are a number of methods that help solve the problem.
    """

    def __init__(self):
        # create a new parser
        self.parser = xml.parsers.expat.ParserCreate()

        # start with an empty stack and no root
        self.stack = []
        self.root = None

        # set our handlers
        self.parser.StartElementHandler = self.startElement
        self.parser.EndElementHandler = self.endElement
        self.parser.CharacterDataHandler = self.dataHandler

    def parseFile(self, file):
        """
        Parses the passed open file. Creates a DOM-tree (Document Object Model) built up from Node
        instances. If an error occurs (such as invalid XML) None is returned.
        """

        # use our own parser to do it
        #        try:
        with open(file, 'rb') as f:
            self.parser.ParseFile(f)

        # is all ok?
        if self.getErrorCode() != 0:
            # nope
            print(self.getErrorString(), self.getErrorLine())
            return None

        return self.root

        #    except pyexpat.error:
        # oops, an exception occurred
        #       return None

    def parseString(self, string):
        """
        Parses the passed string. Creates a DOM-tree (Document Object Model) built up from Node
        instances. If an error occurs (such as invalid XML) None is returned.
        """
        # use our own parser to do it
        #        try:
        self.parser.Parse(string)

        # is all ok?
        if self.getErrorCode() != 0:
            # nope
            return None

        return self.root

        #    except pyexpat.error:
        # oops, an exception occurred
        #       return None

    def getErrorCode(self):
        """
        Returns the expat error code. This is 0 if all is ok.
        """
        return self.parser.ErrorCode

    def getErrorLine(self):
        """
        Returns the line where the error was observed.
        """
        return self.parser.ErrorLineNumber

    def getErrorByte(self):
        """
        Returns the byte offset where the error was observed.
        """
        return self.parser.ErrorByteIndex

    def getErrorString(self):
        """
        Returns the error string matching the current error.
        """
        return xml.parsers.expat.ErrorString(self.getErrorCode())

    def startElement(self, name, attrs):
        """
        Handles start tags.
        """

        # create a new node
        node = Node(name, attrs)

        # do we have a root?
        if self.root is None:
            self.root = node

        # get current top-level node
        if len(self.stack) > 0:
            current = self.stack[len(self.stack) - 1]

            # add to children of the node
            current.children.append(node)

        # add it to the stack
        self.stack.append(node)

    def endElement(self, name):
        """
        Handles end tags.
        """

        # do we have a tag or not?
        if len(self.stack) > 0:
            # yep, pop it out
            start = self.stack.pop()

            # is it the same
            if start.name != name:
                # oops, end tag does not match open start tag
                raise DOMError("End tag " + name + "' does not match tag '" + start.name + "'")

        else:
            # oops, no tag to end, this is an error
            raise DOMError("No start tag for end tag: " + name)

    def dataHandler(self, data):
        """
        Handles data for the current tag.
        """
        # get current top-level node
        if len(self.stack) > 0:
            current = self.stack[len(self.stack) - 1]

            # append data
            current.data += data

        else:
            raise DOMError("No open tag for data: '" + data + "'")


# testing
if __name__ == '__main__':

    # did we get enough parameters
    if len(sys.argv) != 2:
        print("usage: " + sys.argv[0] + " file.xml")
        sys.exit(1)

    print("Reading file: " + sys.argv[1])
    file = open(sys.argv[1])

    # create a parser
    parser = SimpleDOMParser()

    root = parser.parse(file)

    if root is None:
        print("Error parsing: " + str(parser.getErrorCode()) + ": " + str(parser.getErrorString()))

    else:
        for child in root.children:
            print(child, child.name)
