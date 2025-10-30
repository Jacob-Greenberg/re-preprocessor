"""
plugin_discovery.py

Searches installed packages for plugins
"""
from importlib.metadata import entry_points, EntryPoints, EntryPoint
from importlib import import_module


class PluginDiscovery:
    def __init__(self, plugin_groups: list[str] = ["repr-plugin", "repr-extractor", "repr-identifier"]):
        """
        :plugin_groups: a list of strings for entry-point groups which should be considered plugins
                        `repr-extractor` and `repr-identifier` are required
        """
        self.plugin_groups = plugin_groups
        self.extractors = {}
        self.identifiers = {}
        self.plugins = self.discover_plugins()

    def discover_plugins(self):
        """
        Discovers installed plugins via entry points, returns a dictionary of plugins
        Does not import plugins, just provides a list
        """

        plugins = {}
        """
        plugins = {
            "<name>":{
                "group": <group>,
                "class": <some_class>
                ...
            }
        }
        """
        for group in self.plugin_groups:
            for ep in entry_points(group=group):
                if group == 'repr-extractor':
                        self.extractors[ep.name] = {
                        "group":     group,
                        "module":    ep.module,
                        "attribute": ep.attr
                    }
                elif group == 'repr-identifier':
                        self.identifiers[ep.name] = {
                        "group":     group,
                        "module":    ep.module,
                        "attribute": ep.attr
                    }

                plugins[ep.name] = {
                    "group":     group,
                    "module":    ep.module,
                    "attribute": ep.attr
                }
        return plugins
    
    def list_extractors(self):
        """
        Returns a list of available extractors
        """
        extractors = []
            
        for key, value in self.plugins.items():
            if value['group'] == 'repr-extractor':
                extractors.append(key)
        
        return extractors

    def list_identifiers(self):
        """
        Returns a list of available identifiers
        """
        identifiers = []
            
        for key, value in self.plugins.items():
            if value['group'] == 'repr-identifier':
                identifiers.append(key)
        
        return identifiers

if __name__ == "__main__":

    pd = PluginDiscovery()
    print(pd.list_extractors())
    print(pd.list_identifiers())
    print(pd.plugins)

