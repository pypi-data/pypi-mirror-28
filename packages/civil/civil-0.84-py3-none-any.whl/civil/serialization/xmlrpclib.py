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

# TODO this does not like Python 3 very much, find replacement

#
# XML-RPC CLIENT LIBRARY
# $Id: xmlrpclib.py,v 1.1 2001/10/15 15:30:37 chakie Exp $
# an XML-RPC client interface for Python.
# the marshalling and response parser code can also be used to
# implement XML-RPC servers.
# Notes:
# this version uses the sgmlop XML parser, if installed.  this is
# typically 10-15x faster than using Python's standard XML parser.
# you can get the sgmlop distribution from:
#    http://www.pythonware.com/products/xml/sgmlop.htm
# this version is designed to work with Python 1.5.2 or newer.
# unicode encoding support requires at least Python 1.6.
# experimental HTTPS requires Python 2.0 built with SSL sockets.
# History:
# 1999-01-14 fl  Created
# 1999-01-15 fl  Changed dateTime to use localtime
# 1999-01-16 fl  Added Binary/base64 element, default to RPC2 service
# 1999-01-19 fl  Fixed array data element (from Skip Montanaro)
# 1999-01-21 fl  Fixed dateTime constructor, etc.
# 1999-02-02 fl  Added fault handling, handle empty sequences, etc.
# 1999-02-10 fl  Fixed problem with empty responses (from Skip Montanaro)
# 1999-06-20 fl  Speed improvements, pluggable parsers/transports (0.9.8)
# 2000-11-28 fl  Changed boolean to check the truth value of its argument
# 2001-02-24 fl  Added encoding/Unicode/SafeTransport patches
# 2001-02-26 fl  Added compare support to wrappers (0.9.9)
# Copyright (c) 1999-2001 by Secret Labs AB.
# Copyright (c) 1999-2001 by Fredrik Lundh.
# fredrik@pythonware.com
# http://www.pythonware.com
# --------------------------------------------------------------------
# The XML-RPC client interface is
# Copyright (c) 1999-2001 by Secret Labs AB
# Copyright (c) 1999-2001 by Fredrik Lundh
# By obtaining, using, and/or copying this software and/or its
# associated documentation, you agree that you have read, understood,
# and will comply with the following terms and conditions:
# Permission to use, copy, modify, and distribute this software and
# its associated documentation for any purpose and without fee is
# hereby granted, provided that the above copyright notice appears in
# all copies, and that both that copyright notice and this permission
# notice appear in supporting documentation, and that the name of
# Secret Labs AB or the author not be used in advertising or publicity
# pertaining to distribution of the software without specific, written
# prior permission.
# SECRET LABS AB AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH REGARD
# TO THIS SOFTWARE, INCLUDING ALL IMPLIED WARRANTIES OF MERCHANT-
# ABILITY AND FITNESS.  IN NO EVENT SHALL SECRET LABS AB OR THE AUTHOR
# BE LIABLE FOR ANY SPECIAL, INDIRECT OR CONSEQUENTIAL DAMAGES OR ANY
# DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS,
# WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS
# ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR PERFORMANCE
# OF THIS SOFTWARE.
# --------------------------------------------------------------------

# things to fix before 1.0 final:

# TODO: unicode marshalling -DONE
# TODO: ascii-compatible encoding support -DONE
# TODO: safe transport -DONE (but mostly untested)
# TODO: sgmlop memory leak -DONE
# TODO: sgmlop xml parsing -DONE
# TODO: support unicode method names -DONE
# TODO: update selftest -DONE
# TODO: add docstrings -DONE
# TODO: clean up parser encoding (trust the parser) -DONE
# TODO: fix host tuple handling in the server constructor
# TODO: let transport verify schemes
# TODO: update documentation
# TODO: authentication plugins
# TODO: memo problem (see HP's mail)

import operator
import re
import string
import time
import urllib.request, urllib.parse, urllib.error
import xmllib
from cgi import escape
from types import *

try:
    import sgmlop

    if not hasattr(sgmlop, "XMLParser"):
        raise ImportError
except ImportError:
    sgmlop = None  # accelerator not available

try:
    str
except NameError:
    str = None  # unicode support not available


def _decode(data, encoding, is8bit=re.compile("[\x80-\xff]").search):
    # decode non-ascii string (if possible)
    if str and is8bit(data):
        data = str(data, encoding)
    return data


__version__ = "0.9.9"


# --------------------------------------------------------------------
# Exceptions

class Error:
    # base class for client errors
    pass


class ProtocolError(Error):
    """

    """
    # indicates an HTTP protocol error
    def __init__(self, url, errcode, errmsg, headers):
        self.url = url
        self.errcode = errcode
        self.errmsg = errmsg
        self.headers = headers

    def __repr__(self):
        return (
                "<ProtocolError for %s: %s %s>" %
                (self.url, self.errcode, self.errmsg)
        )


class ResponseError(Error, Exception):
    # indicates a broken response package
    pass


class Fault(Error):
    """

    """
    # indicates a XML-RPC fault package
    def __init__(self, faultCode, faultString, **extra):
        self.faultCode = faultCode
        self.faultString = faultString

    def __repr__(self):
        return (
                "<Fault %s: %s>" %
                (self.faultCode, repr(self.faultString))
        )


# --------------------------------------------------------------------
# Special values

# boolean wrapper
# use True or False to generate a "boolean" XML-RPC value

class Boolean:
    """

    """
    def __init__(self, value=0):
        self.value = operator.truth(value)

    def encode(self, out):
        """

        Args:
            out: 
        """
        out.write("<value><boolean>%d</boolean></value>\n" % self.value)

    def __cmp__(self, other):
        if isInstanceType(other, Boolean):
            other = other.value
        return cmp(self.value, other)

    def __repr__(self):
        if self.value:
            return "<Boolean True at %x>" % id(self)
        else:
            return "<Boolean False at %x>" % id(self)

    def __int__(self):
        return self.value

    def __bool__(self):
        return self.value


True, False = Boolean(1), Boolean()


def boolean(value, truefalse=(False, True)):
    """

    Args:
        value: 
        truefalse: 

    Returns:

    """
    # convert any Python value to XML-RPC boolean
    return truefalse[operator.truth(value)]


# dateTime wrapper
# wrap your iso8601 string or time tuple or localtime integer value
# in this class to generate a "dateTime.iso8601" XML-RPC value

class DateTime:
    """

    """
    def __init__(self, value=0):
        t = type(value)
        if not isInstanceType(t, string):
            if not isInstanceType(t, tuple):
                if value == 0:
                    value = time.time()
                value = time.localtime(value)
            value = time.strftime("%Y%m%dT%H:%M:%S", value)
        self.value = value

    def __cmp__(self, other):
        if isInstanceType(other, DateTime):
            other = other.value
        return cmp(self.value, other)

    def __repr__(self):
        return "<DateTime %s at %x>" % (self.value, id(self))

    def decode(self, data):
        """

        Args:
            data: 
        """
        self.value = string.strip(data)

    def encode(self, out):
        """

        Args:
            out: 
        """
        out.write("<value><dateTime.iso8601>")
        out.write(self.value)
        out.write("</dateTime.iso8601></value>\n")


# binary data wrapper

class Binary:
    """

    """
    def __init__(self, data=None):
        self.data = data

    def __cmp__(self, other):
        if isInstanceType(other, Binary):
            other = other.data
        return cmp(self.data, other)

    def decode(self, data):
        """

        Args:
            data: 
        """
        import base64
        self.data = base64.decodestring(data)

    def encode(self, out):
        """

        Args:
            out: 
        """
        import base64, io
        out.write("<value><base64>\n")
        base64.encode(io.StringIO(self.data), out)
        out.write("</base64></value>\n")


WRAPPERS = DateTime, Binary, Boolean

# --------------------------------------------------------------------
# XML parsers

if sgmlop:

    class FastParser:
        """

        """
        # sgmlop based XML parser.  this is typically 15x faster
        # than SlowParser...

        def __init__(self, target):

            # setup callbacks
            self.finish_starttag = target.start
            self.finish_endtag = target.end
            self.handle_data = target.data
            self.handle_xml = target.xml

            # activate parser
            self.parser = sgmlop.XMLParser()
            self.parser.register(self)
            self.feed = self.parser.feed
            self.entity = {
                "amp": "&", "gt": ">", "lt": "<",
                "apos": "'", "quot": '"'
            }

        def close(self):
            """

            """
            try:
                self.parser.close()
            finally:
                self.parser = self.feed = None  # nuke circular reference

        def handle_proc(self, tag, attr):
            """

            Args:
                tag: 
                attr: 
            """
            m = re.search("encoding\s*=\s*['\"]([^\"']+)[\"']", attr)
            if m:
                self.handle_xml(m.group(1), 1)

        def handle_entityref(self, entity):
            """

            Args:
                entity: 
            """
            # <string> entity
            try:
                self.handle_data(self.entity[entity])
            except KeyError:
                self.handle_data("&%s;" % entity)

else:

    FastParser = None


class SlowParser(xmllib.XMLParser):
    """

    """
    # slow but safe standard parser, based on the XML parser in
    # Python's standard library

    def __init__(self, target):
        self.handle_xml = target.xml
        self.unknown_starttag = target.start
        self.handle_data = target.data
        self.unknown_endtag = target.end
        xmllib.XMLParser.__init__(self)


# --------------------------------------------------------------------
# XML-RPC marshalling and unmarshalling code

class Marshaller:
    """
    Generate an XML-RPC params chunk from a Python data structure
    """

    # USAGE: create a marshaller InstanceType for each set of parameters,
    # and use "dumps" to convert your data (represented as a tuple) to
    # a XML-RPC params chunk.  to write a fault response, pass a Fault
    # InstanceType instead.  you may prefer to use the "dumps" convenience
    # function for this purpose (see below).

    # by the way, if you don't understand what's going on in here,
    # that's perfectly ok.

    def __init__(self, encoding=None):
        self.memo = {}
        self.data = None
        self.encoding = encoding

    dispatch = {}

    def dumps(self, values):
        """

        Args:
            values: 

        Returns:

        """
        self.__out = []
        self.write = write = self.__out.append
        if isInstanceType(values, Fault):
            # fault InstanceType
            write("<fault>\n")
            self.__dump(vars(values))
            write("</fault>\n")
        else:
            # parameter block
            write("<params>\n")
            for v in values:
                write("<param>\n")
                self.__dump(v)
                write("</param>\n")
            write("</params>\n")
        result = "".join(self.__out)
        del self.__out, self.write  # don't need this any more
        return result

    def __dump(self, value):
        try:
            f = self.dispatch[type(value)]
        except KeyError:
            raise TypeError("cannot marshal %s objects" % type(value))
        else:
            f(self, value)

    def dump_int(self, value):
        """

        Args:
            value: 
        """
        self.write("<value><int>%s</int></value>\n" % value)

    dispatch[int] = dump_int

    def dump_double(self, value):
        """

        Args:
            value: 
        """
        self.write("<value><double>%s</double></value>\n" % value)

    dispatch[float] = dump_double

    def dump_string(self, value):
        """

        Args:
            value: 
        """
        self.write("<value><string>%s</string></value>\n" % escape(value))

    dispatch[string] = dump_string

    if str:
        def dump_unicode(self, value):
            """

            Args:
                value: 
            """
            value = value.encode(self.encoding)
            self.write("<value><string>%s</string></value>\n" % escape(value))

        dispatch[string] = dump_unicode

    def container(self, value):
        """

        Args:
            value: 
        """
        if value:
            i = id(value)
            if i in self.memo:
                raise TypeError("cannot marshal recursive data structures")
            self.memo[i] = None

    def dump_array(self, value):
        """

        Args:
            value: 
        """
        self.container(value)
        write = self.write
        write("<value><array><data>\n")
        for v in value:
            self.__dump(v)
        write("</data></array></value>\n")

    dispatch[tuple] = dump_array
    dispatch[list] = dump_array

    def dump_struct(self, value):
        """

        Args:
            value: 
        """
        self.container(value)
        write = self.write
        write("<value><struct>\n")
        for k, v in list(value.items()):
            write("<member>\n")
            if type(k) is not string:
                raise TypeError("dictionary key must be string")
            write("<name>%s</name>\n" % escape(k))
            self.__dump(v)
            write("</member>\n")
        write("</struct></value>\n")

    dispatch[dict] = dump_struct

    def dump_InstanceType(self, value):
        """

        Args:
            value: 
        """
        # check for special wrappers
        if value.__class__ in WRAPPERS:
            value.encode(self)
        else:
            # store InstanceType attributes as a struct (really?)
            self.dump_struct(value.__dict__)

    dispatch[InstanceType] = dump_InstanceType


class Unmarshaller:
    """

    """
    # unmarshal an XML-RPC response, based on incoming XML event
    # messages (start, data, end).  call close to get the resulting
    # data structure

    # note that this reader is fairly tolerant, and gladly accepts
    # bogus XML-RPC data without complaining (but not bogus XML).

    # and again, if you don't understand what's going on in here,
    # that's perfectly ok.

    def __init__(self):
        self._type = None
        self._stack = []
        self._marks = []
        self._data = []
        self._methodname = None
        self._encoding = "utf-8"
        self.append = self._stack.append

    def close(self):
        """

        Returns:

        """
        # return response tuple and target method
        if self._type is None or self._marks:
            raise ResponseError()
        if self._type == "fault":
            raise Fault(*(), **self._stack[0])
        return tuple(self._stack)

    def getmethodname(self):
        """

        Returns:

        """
        return self._methodname

    #
    # event handlers

    def xml(self, encoding, standalone):
        """

        Args:
            encoding: 
            standalone: 
        """
        self._encoding = encoding or "utf-8"
        # FIXME: assert standalone == 1 ???

    def start(self, tag, attrs):
        """

        Args:
            tag: 
            attrs: 
        """
        # prepare to handle this element
        if tag in ("array", "struct"):
            self._marks.append(len(self._stack))
        self._data = []
        self._value = (tag == "value")

    def data(self, text):
        """

        Args:
            text: 
        """
        self._data.append(text)

    dispatch = {}

    def end(self, tag):
        """

        Args:
            tag: 

        Returns:

        """
        # call the appropriate end tag handler
        try:
            f = self.dispatch[tag]
        except KeyError:
            pass  # unknown tag ?
        else:
            return f(self)

    #
    # element decoders

    def end_boolean(self, join=string.join):
        """

        Args:
            join: 
        """
        value = join(self._data, "")
        if value == "0":
            self.append(False)
        elif value == "1":
            self.append(True)
        else:
            raise TypeError("bad boolean value")
        self._value = 0

    dispatch["boolean"] = end_boolean

    def end_int(self, join=string.join):
        """

        Args:
            join: 
        """
        self.append(int(join(self._data, "")))
        self._value = 0

    dispatch["i4"] = end_int
    dispatch["int"] = end_int

    def end_double(self, join=string.join):
        """

        Args:
            join: 
        """
        self.append(float(join(self._data, "")))
        self._value = 0

    dispatch["double"] = end_double

    def end_string(self, join=string.join):
        """

        Args:
            join: 
        """
        data = join(self._data, "")
        if self._encoding:
            data = _decode(data, self._encoding)
        self.append(data)
        self._value = 0

    dispatch["string"] = end_string
    dispatch["name"] = end_string  # struct keys are always strings

    def end_array(self):
        """

        """
        mark = self._marks[-1]
        del self._marks[-1]
        # map arrays to Python lists
        self._stack[mark:] = [self._stack[mark:]]
        self._value = 0

    dispatch["array"] = end_array

    def end_struct(self):
        """

        """
        mark = self._marks[-1]
        del self._marks[-1]
        # map structs to Python dictionaries
        dict = {}
        items = self._stack[mark:]
        for i in range(0, len(items), 2):
            dict[items[i]] = items[i + 1]
        self._stack[mark:] = [dict]
        self._value = 0

    dispatch["struct"] = end_struct

    def end_base64(self, join=string.join):
        """

        Args:
            join: 
        """
        value = Binary()
        value.decode(join(self._data, ""))
        self.append(value)
        self._value = 0

    dispatch["base64"] = end_base64

    def end_dateTime(self, join=string.join):
        """

        Args:
            join: 
        """
        value = DateTime()
        value.decode(join(self._data, ""))
        self.append(value)

    dispatch["dateTime.iso8601"] = end_dateTime

    def end_value(self):
        """

        """
        # if we stumble upon an value element with no internal
        # elements, treat it as a string element
        if self._value:
            self.end_string()

    dispatch["value"] = end_value

    def end_params(self):
        """

        """
        self._type = "params"

    dispatch["params"] = end_params

    def end_fault(self):
        """

        """
        self._type = "fault"

    dispatch["fault"] = end_fault

    def end_methodName(self, join=string.join):
        """

        Args:
            join: 
        """
        data = join(self._data, "")
        if self._encoding:
            data = _decode(data, self._encoding)
        self._methodname = data

    dispatch["methodName"] = end_methodName


# --------------------------------------------------------------------
# convenience functions

def getparser():
    """
    getparser() -> parser, unmarshaller

    Create an InstanceType of the fastest available parser, and attach
    it to an unmarshalling object.  Return both objects.
    """
    target = Unmarshaller()
    if FastParser:
        return FastParser(target), target
    return SlowParser(target), target


def dumps(params, methodname=None, methodresponse=None, encoding=None):
    """
    data [,options] -> marshalled data

    Convert a tuple or a fault object to an XML-RPC request (or
    response, if the methodsresponse option is used).

    In addition to the data object, the following options can be
    given as keyword arguments:

        methodname: the method name for a methodCall packet
        methodresponse: true to create a methodResponse packet
        encoding: the packet encoding (default is UTF-8)

    All 8-bit strings in the data structure are assumed to use the
    packet encoding.  Unicode strings are automatically converted,
    as necessary.
    """

    assert type(params) == tuple or isInstanceType(params, Fault), \
        "argument must be tuple or Fault InstanceType"

    if not encoding:
        encoding = "utf-8"

    m = Marshaller(encoding)
    data = m.dumps(params)

    if encoding != "utf-8":
        xmlheader = "<?xml version='1.0' encoding=%s?>\n" % repr(encoding)
    else:
        xmlheader = "<?xml version='1.0'?>\n"  # utf-8 is default

    # standard XML-RPC wrappings
    if methodname:
        # a method call
        if not isInstanceType(methodname, string):
            methodname = methodname.encode(encoding)
        data = (
            xmlheader,
            "<methodCall>\n"
            "<methodName>", methodname, "</methodName>\n",
            data,
            "</methodCall>\n"
        )
    elif methodresponse or isInstanceType(params, Fault):
        # a method response
        data = (
            xmlheader,
            "<methodResponse>\n",
            data,
            "</methodResponse>\n"
        )
    else:
        return data  # return as is
    return "".join(data)


def loads(data):
    """
    data -> unmarshalled data, method name

    Convert an XML-RPC packet to unmarshalled data plus a method
    name (None if not present).

    If the XML-RPC packet represents a fault condition, this function
    raises a Fault exception.
    """
    p, u = getparser()
    p.feed(data)
    p.close()
    return u.close(), u.getmethodname()


# --------------------------------------------------------------------
# request dispatcher

class _Method:
    # some magic to bind an XML-RPC method to an RPC server.
    # supports "nested" methods (e.g. examples.getStateName)
    def __init__(self, send, name):
        self.__send = send
        self.__name = name

    def __getattr__(self, name):
        return _Method(self.__send, "%s.%s" % (self.__name, name))

    def __call__(self, *args):
        return self.__send(self.__name, args)


class Transport:
    """
    Handles an HTTP transaction to an XML-RPC server
    """

    # client identifier (may be overridden)
    user_agent = "xmlrpclib.py/%s (by www.pythonware.com)" % __version__

    def request(self, host, handler, request_body, verbose=0):
        """

        Args:
            host: 
            handler: 
            request_body: 
            verbose: 

        Returns:

        """
        # issue XML-RPC request

        h = self.make_connection(host)
        if verbose:
            h.set_debuglevel(1)

        self.send_request(h, handler, request_body)
        self.send_host(h, host)
        self.send_user_agent(h)
        self.send_content(h, request_body)

        errcode, errmsg, headers = h.getreply()

        if errcode != 200:
            raise ProtocolError(
                host + handler,
                errcode, errmsg,
                headers
            )

        self.verbose = verbose

        return self.parse_response(h.getfile())

    def make_connection(self, host):
        """

        Args:
            host: 

        Returns:

        """
        # create a HTTP connection object from a host descriptor
        import http.client
        return http.client.HTTP(host)

    def send_request(self, connection, handler, request_body):
        """

        Args:
            connection: 
            handler: 
            request_body: 
        """
        connection.putrequest("POST", handler)

    def send_host(self, connection, host):
        """

        Args:
            connection: 
            host: 
        """
        connection.putheader("Host", host)

    def send_user_agent(self, connection):
        """

        Args:
            connection: 
        """
        connection.putheader("User-Agent", self.user_agent)

    def send_content(self, connection, request_body):
        """

        Args:
            connection: 
            request_body: 
        """
        connection.putheader("Content-Type", "text/xml")
        connection.putheader("Content-Length", str(len(request_body)))
        connection.endheaders()
        if request_body:
            connection.send(request_body)

    def parse_response(self, f):
        """

        Args:
            f: 

        Returns:

        """
        # read response from input file, and parse it

        p, u = getparser()

        while 1:
            response = f.read(1024)
            if not response:
                break
            if self.verbose:
                print("body:", repr(response))
            p.feed(response)

        f.close()
        p.close()

        return u.close()


class SafeTransport(Transport):
    """
    Handles an HTTPS transaction to an XML-RPC server
    """

    def make_connection(self, host):
        """

        Args:
            host: 

        Returns:

        """
        # create a HTTPS connection object from a host descriptor
        # host may be a string, or a (host, x509-dict) tuple
        import http.client
        if isInstanceType(host, tuple):
            host, x509 = host
        else:
            x509 = {}
        try:
            HTTPS = http.client.HTTPS
        except AttributeError:
            raise NotImplementedError("your version of httplib doesn't support HTTPS")
        else:
            return HTTPS(*(host, None), **x509)

    def send_host(self, connection, host):
        """

        Args:
            connection: 
            host: 
        """
        if isInstanceType(host, tuple):
            host, x509 = host
        connection.putheader("Host", host)


class Server:
    """
    uri [,options] -> a logical connection to an XML-RPC server

    uri is the connection point on the server, given as
    scheme://host/target.

    The standard implementation always supports the "http" scheme.  If
    SSL socket support is available (Python 2.0), it also supports
    "https".

    If the target part and the slash preceding it are both omitted,
    "/RPC2" is assumed.

    The following options can be given as keyword arguments:

        transport: a transport factory
        encoding: the request encoding (default is UTF-8)

    All 8-bit strings passed to the server proxy are assumed to use
    the given encoding.
    """

    def __init__(self, uri, transport=None, encoding=None, verbose=0):
        # establish a "logical" server connection

        # get the url
        type, uri = urllib.parse.splittype(uri)
        if type not in ("http", "https"):
            raise IOError("unsupported XML-RPC protocol")
        self.__host, self.__handler = urllib.parse.splithost(uri)
        if not self.__handler:
            self.__handler = "/RPC2"

        if transport is None:
            if type == "https":
                transport = SafeTransport()
            else:
                transport = Transport()
        self.__transport = transport

        self.__encoding = encoding
        self.__verbose = verbose

    def __request(self, methodname, params):
        # call a method on the remote server

        request = dumps(params, methodname, encoding=self.__encoding)

        response = self.__transport.request(
            self.__host,
            self.__handler,
            request,
            verbose=self.__verbose
        )

        if len(response) == 1:
            response = response[0]

        return response

    def __repr__(self):
        return (
                "<Server proxy for %s%s>" %
                (self.__host, self.__handler)
        )

    __str__ = __repr__

    def __getattr__(self, name):
        # magic method dispatcher
        return _Method(self.__request, name)

        # note: to call a remote object with an non-standard name, use
        # result getattr(server, "strange-python-name")(args)


# --------------------------------------------------------------------
# test code

if __name__ == "__main__":

    # simple test program (from the XML-RPC specification)

    # server = Server("http://localhost:8000") # local server
    server = Server("http://betty.userland.com")

    print(server)

    try:
        print(server.examples.getStateName(41))
    except Error as v:
        print("ERROR", v)
