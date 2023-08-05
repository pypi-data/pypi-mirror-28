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
See http://www.xml-rpc.com/
    http://www.pythonware.com/products/xmlrpc/

Based on "xmlrpcserver.py" by Fredrik Lundh (fredrik@pythonware.com)
"""

import string
import sys

from civil.serialization import xmlrpclib


class xmlrpc_handler:
    def match(self, request):
        """

        Args:
            request: 

        Returns:

        """
        # Note: /RPC2 is not required by the spec, so you may override this method.
        if request.uri[:5] == '/RPC2':
            return 1
        else:
            return 0

    def handle_request(self, request):
        """

        Args:
            request: 
        """
        [path, params, query, fragment] = request.split_uri()

        if request.command in ('post', 'put'):
            request.collector = collector(self, request)
        else:
            request.error(400)

    def continue_request(self, data, request):
        """

        Args:
            data: 
            request: 
        """
        params, method = xmlrpclib.loads(data)
        try:
            # generate response
            try:
                response = self.call(method, params)
                if type(response) != type(()):
                    response = (response,)
            except:
                # report exception back to server
                response = xmlrpclib.dumps(
                    xmlrpclib.Fault(1, "%s:%s" % (sys.exc_info()[0], sys.exc_info()[1]))
                )
            else:
                response = xmlrpclib.dumps(response, methodresponse=1)
        except:
            # internal error, report as HTTP server error
            request.error(500)
        else:
            # got a valid XML RPC response
            request['Content-Type'] = 'text/xml'
            request.push(response)
            request.done()

    def call(self, method, params):
        """

        Args:
            method: 
            params: 
        """
        # override this method to implement RPC methods
        raise RuntimeError("NotYetImplemented")


class collector:
    "gathers input for POST and PUT requests"

    def __init__(self, handler, request):

        self.handler = handler
        self.request = request
        self.data = ''

        # make sure there's a content-length header
        cl = request.get_header('content-length')

        if not cl:
            request.error(411)
        else:
            cl = string.atoi(cl)
            # using a 'numeric' terminator
            self.request.channel.set_terminator(cl)

    def collect_incoming_data(self, data):
        """

        Args:
            data: 
        """
        self.data = self.data + data

    def found_terminator(self):
        """

        """
        # set the terminator back to the default
        self.request.channel.set_terminator('\r\n\r\n')
        self.handler.continue_request(self.data, self.request)


if __name__ == '__main__':
    class rpc_demo(xmlrpc_handler):
        def call(self, method, params):
            """

            Args:
                method: 
                params: 

            Returns:

            """
            print('method="%s" params=%s' % (method, params))
            return "Sure, that works"


    import asyncore
    import http_server

    hs = http_server.http_server('', 8000)
    rpc = rpc_demo()
    hs.install_handler(rpc)

    asyncore.loop()
