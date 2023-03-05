"""
PI_ReloadPlugins.py

Port of Sandy Barbour's ReloadPlugin C++ plugin.

Matt Nicholson
04 MAR 2023
"""
from XPPython3 import xp


class PythonInterface:

    def __init__(self):
        self.Name = "ReloadPlugins v1.0"
        self.Sig = "reloadplugins.xppython3"
        self.Desc = "A plugin to reload installed X-Plane plugins."

    def XPluginStart(self):
        item = xp.appendMenuItem(xp.findPluginsMenu(), 'ReloadPlugins', None, 1)
        id = xp.createMenu('ReloadPlugins', xp.findPluginsMenu(), item,
                           self.ReloadPluginsMenuHandler, None)

        xp.appendMenuItem(id, 'Reload', 'Reload plugins', 1)

        return self.Name, self.Sig, self.Desc

    def XPluginStop(self):
        pass

    def XPluginEnable(self):
        return 1

    def XPluginDisable(self):
        pass

    def XPluginReceiveMessage(self, inFromWho, inMessage, inParam):
        pass

    def ReloadPluginsMenuHandler(self, mRef, iRef):
        if iRef == 'Reload plugins':
            xp.reloadPlugins()
