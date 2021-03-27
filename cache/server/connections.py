import json
import os


class Connections:
    def __init__(self):
        self.connections = None
        self._connections_path = f"cache{os.path.sep}server{os.path.sep}data{os.path.sep}connections.json"
        self._load_connections()

    def __getitem__(self, item):
        return self.connections[item]

    def _load_connections(self):
        try:
            connections_file = open(self._connections_path, 'r')
            self.connections = json.load(connections_file)
            connections_file.close()

        except IOError:
            pass