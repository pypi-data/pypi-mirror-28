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

from pygame.locals import *

from civil.state import state
from civil.model import scenario
from civil.server.action import chat_act
from civil.ui.messages import CHAT2


class Chat(state.State):
    """
    This class is a state that is used to show a simple help text on the screen. It will add a new
    layer to the playfield and use it to display a dialog with some help text. The user can click a
    button 'Ok' to return to the previous state pr press 'Escape'.

    TODO: fixme
    """

    # a list of allowed keys
    allowedkeys = [K_0, K_1, K_2, K_3, K_4, K_5, K_6, K_7, K_8, K_9,
                   K_AMPERSAND, K_ASTERISK, K_AT, K_BACKQUOTE, K_BACKSLASH,
                   K_CARET, K_COLON, K_COMMA, K_DOLLAR, K_EQUALS, K_EURO, K_EXCLAIM,
                   K_GREATER, K_HASH, K_LESS, K_MINUS, K_PERIOD, K_PLUS, K_POWER,
                   K_QUESTION, K_QUOTE, K_QUOTEDBL, K_SLASH, K_SPACE, K_UNDERSCORE,
                   K_a, K_b, K_c, K_d, K_e, K_f, K_g, K_h, K_i, K_j, K_k, K_l, K_m,
                   K_n, K_o, K_p, K_q, K_r, K_s, K_t, K_u, K_v, K_w, K_x, K_y, K_z,
                   K_RETURN, K_BACKSLASH, K_DELETE, K_BACKSPACE, K_ESCAPE]

    def __init__(self, caller):
        """
        Initializes the instance. Sets default values for all needed member. This state has no
        keymap as it handles all key events itself.
        """

        # call superclass constructor
        state.State.__init__(self)

        # set default cursor
        self.setDefaultCursor()

        # set defaults
        self.name = "chat_state"

        # store the calling state
        self.caller = caller

        # set default message
        self.message = ""

        # find the chat layer
        self.chatlayer = scenario.playfield.getLayer("chat")

        # and make it visible
        scenario.playfield.setVisible(self.chatlayer)

    def handleKeyDown(self, event):
        """
        Handles a key down event. Checks weather the key is a legal (printable) key and if it is
        then manipulates the internal message accordingly. Some keys will add characters and
        delete/backspace will remove characters. Return will send off the message to the server and


 """

        # get the key from the event
        key = event.key

        # print "Chat.handleKeyDown:",event

        # is this a legal key?
        if not key in Chat.allowedkeys:
            # no key we want to handle at all
            return None

        # do we have a return key?
        if key == K_RETURN:
            # yep, so send off the message if there is something to send
            if self.message != "":
                # add our own message first 
                scenario.messages.add(self.message, CHAT2)

                #  create a new 'chat' action
                cmd = chat_act.ChatAct(self.message)

                # send off a command
                scenario.connection.send(cmd.toString())

                # no message anymore
                self.message = ""

                # assign the message to the layer that displays it
                self.chatlayer.setMessage("")

            # close ourselves
            return self.close()

        # escape?
        elif key == K_ESCAPE:
            # no message anymore
            self.message = ""

            # assign the message to the layer that displays it
            self.chatlayer.setMessage("")

            # close ourselves without sending anything
            return self.close()

        # are we deleting a character?
        elif key == K_BACKSPACE or key == K_DELETE:
            # delete the rightmost character (if we have anything here)
            if self.message != "":
                # yep, strip off the left one
                self.message = self.message[:-1]

        else:
            # get the character and append to our string
            self.message += event.unicode

        # assign the message to the layer that displays it
        self.chatlayer.setMessage(self.message)

        # repaint the playfield
        scenario.playfield.needInternalRepaint(self.chatlayer)

        # no key we're interested in
        return None

    def handleLeftMousePressed(self, event):
        """
        Handles a click with the left mouse button. This method simply terminates this
        state, and as there is no Ok/Cancel buttons to click any click is a canceling click. Returns
        the 'caller' state, ie the one that was given in the constructor.
        """

        # use nice close() method
        return self.close()

    def close(self):
        """
        Closes the state, i.e. returns to the previous state. The playfield layer for the chat
        window will be hidden.
        """

        # find the layer and hide it
        scenario.playfield.setVisible(self.chatlayer, 0)

        # return the previous state
        return self.caller
