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

import glob
import os
import stat

from PyQt5 import QtWidgets, QtCore


class PluginView(QtWidgets.QListView):
    """
    This class is a simple view that is shown in the main tab bar. It contains a list of all the
    plugins that are available. It lets the user select a plugin and then start doing stuff in the
    map. It mainly relays events to the currently selected plugin.
    """

    def __init__(self, mainwindow):
        """
        Goes trough the plugins directory, searching for all plugins
        """
        QtWidgets.QListView.__init__(self, mainwindow)
        self.mainwindow = mainwindow

        # find all plugins 
        self.plugins = []
        self.__findPlugins()

        # we want single selection
        self.setSelectionMode(QtWidgets.QListView.Single)

    def __findPlugins(self):
        """
        Scans a hardcoded path and finds and initializes all plugins. The plugins are added to
        the listbox with all plugins.
        """

        # create a nice os independent path
        plugin_path = os.path.normpath('editor/plugins/*.py')

        # get all plugins
        for file in glob.glob(plugin_path):
            mode = os.stat(file)[0]
            if not stat.S_ISREG(mode):
                continue

            file = file[:-3]  # skip .py

            try:
                plugin = __import__(file, globals(), locals(), file)
                if "new" not in plugin.__dict__:
                    continue
                instance = plugin.new(self.mainwindow.iconview)
                if not instance:
                    continue
                item = QtCore.QString(instance.name)
                self.insertItem(item)
                self.plugins.append(instance)
                print("Added plugin %s..." % instance.name)
            except:
                print("PLUGIN FAILED", file)
                pass

    def getPlugin(self):
        """

        Returns:

        """
        # get the selected plugin index (if any)
        index = self.currentItem()

        # do we have a selected plugin?
        if index == -1:
            # nope, go away
            return None

        return self.plugins[index]

    def mapClickedLeft(self, x, y, hexx, hexy):
        """
        Callback triggered when the map has been clicked with the left mouse button. Relays the
        event to the currently selected plugin, if any.
        """

        plugin = self.getPlugin()
        if not plugin:
            return

        plugin.mapClickedLeft(x, y, hexx, hexy)

        print("PluginView.mapClickedLeft")

    def mapClickedMid(self, x, y, hexx, hexy):
        """
        Callback triggered when the map has been clicked with the middle mouse button. Relays the
        event to the currently selected plugin, if any.
        """

        plugin = self.getPlugin()
        if not plugin:
            return

        plugin.mapClickedMid(x, y, hexx, hexy)

        print("PluginView.mapClickedMid")

    def mapClickedRight(self, x, y, hexx, hexy):
        """
        Callback triggered when the map has been clicked with the right mouse button. Relays the
        event to the currently selected plugin, if any.
        """

        plugin = self.getPlugin()
        if not plugin:
            return

        plugin.mapClickedRight(x, y, hexx, hexy)

        print("PluginView.mapClickedRight")
