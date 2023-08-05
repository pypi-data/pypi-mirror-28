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

import select


class ConnectionClosed(IOError):
    """
     """
    pass


class Connection:
    """
    This class is the sole connection to the remote player in the whole game. This is the socket
    connected to the remote player and all traffic goes through this. This class has convenient
    methods for sending and receiving packets of data, as well as checking weather there is data
    available.
    """

    def __init__(self, socket):
        """
        Initializes the instance.
        """

        # store the passed socket
        self.socket = socket

        # we're connected ok
        self.connection_ok = 1

        # start with an empty buffer
        self.buffer = ""

        # accounting information
        self.totalsent = 0
        self.totalread = 0

        # a queue of data added internally
        self.queue = []

    def addToQueue(self, line):
        """
        Adds 'line' to the internal queue. This line will be retrieved the next time a
        'readLine()' is called, unless there already is something enqueued.
        """
        self.queue.append(line)

    def close(self):
        """
        Closes the connection.
        """
        try:
            self.socket.close()
        except:
            # ignore errors
            pass

    def isValid(self):
        """
        Returns 1 if the socket is still valid, i.e. connected ok. 0 if not.
        """
        if self.fileno() == -1:
            # not valid
            return 0

        # all ok
        return 1

    def fileno(self):
        """
        Returns a integer referring to the internal socket. This is needed for the select() call
        in readLine() and is not meant for external use.
        """
        return self.socket.fileno()

    def file(self, mode):
        """
        Returns the socket as a file. This is suitable for operations that expect normal file
        methods. The returned file can be closed when finished.
        """
        return self.socket.makefile(mode)

    def send(self, data):
        """
        Sends 'data' over the socket. Returns 1 if all is ok and 0 on error.
        """
        # are we even connected?
        if not self.connection_ok:
            # socket is closed
            return 0

        # send it over the socket
        data = data.encode()
        self.socket.send(data)

        # increment the number of bytes sent
        self.totalsent += len(data)

        # all is ok
        return 1

    def read(self, size):
        """
        Reads 'data' from the socket. Returns data, or 0 on error.
        """
        # are we even connected?
        if not self.connection_ok:
            # socket is closed
            return 0

        # get a file
        file = self.socket.makefile()

        # read data from the socket
        data = file.read(size)

        # increment the number of bytes read
        self.totalread += len(data)

        file.close()

        # all is ok
        return data

    def findLine(self):
        """
        Tries to find a line from the internal buffer. A line is something that is terminated by
        a newline. Modifies the buffer to point after the newline and returns the line.
        """
        # yep, try to find a newline
        index = self.buffer.find('\n')

        # did we find an empty line?
        if index == 0:
            line = ''

            # how long is the buffer?
            if len(self.buffer) == 1:
                self.buffer = ''
            else:
                # get everything
                self.buffer = self.buffer[1:]

            # increase number of read bytes
            self.totalread += len(line)

            return line

        # did we find anything?
        elif index != -1:
            # yep, extract a line and shrink the buffer
            line = self.buffer[: index]
            self.buffer = self.buffer[index + 1:]

            # increase number of read bytes
            self.totalread += len(line)

            return line

        # nothing here
        return None

    def readLine(self, timeout=0):
        """
        Reads one line of data until a '\n' is read. If there is no data that can be read
        immediately the behaviour depends on the value of 'timeout'. If it is 0 then the method will
        return None immediately. If it has some other value the method will block 'timeout' seconds
        for some data to arrive. If data is available (both cases) the read line is returned.

        If a line of data is available on the internal queue it is returned instead.
        """

        # is the connection ok?
        if not self.connection_ok:
            # socket is closed
            raise IOError("Connection.readLine: network connection not ok")

        # do we have a line already in the queue?
        if len(self.queue) > 0:
            # yep, get it
            line = self.queue[0]

            # remove it
            self.queue = self.queue[1:]

            return line

        # do we already have something here?
        if len(self.buffer) > 0:
            # yep, try to find a newline
            line = self.findLine()

            # did we find a whole ready line?
            if line is not None:
                return line

        # perform the select. We're only interested in incoming events. Check for weather we should
        # have a timeout or not
        if timeout < 0:
            # do not use a timeout, block forever
            incoming, out, exceptional = select.select([self], [], [])

        else:
            # use supplied timeout
            incoming, out, exceptional = select.select([self], [], [], timeout)

        # did we get anything?
        if len(incoming) == 0:
            # nothing to read
            return None

        # read a maximum of 1024 bytes
        try:
            self.buffer += self.socket.recv(65536).decode()
        except:
            print("Connection.readLine: error reading from the socket, closing connection")
            try:
                self.socket.close()
            except:
                pass

            # th connection is not ok anymore
            self.connection_ok = 0
            raise ConnectionClosed()

        # did we read anything or is it closed?
        if len(self.buffer) == 0:
            print("Connection.readLine: connection closed by remote party")
            self.socket.close()

            # th connection is not ok anymore
            self.connection_ok = 0
            raise ConnectionClosed()
            # return None

        # yep, try to find a newline
        line = self.findLine()

        # did we find a whole ready line?
        if line:
            return line

        # nothing read
        return None

    def getTotalSent(self):
        """
        Returns the total number of bytes that have been sent over the connection.
        """
        return self.totalsent

    def getTotalRead(self):
        """
        Returns the total number of bytes that have been read over the connection.
        """
        return self.totalread
