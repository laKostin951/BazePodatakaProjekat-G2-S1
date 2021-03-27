import json
import os


class _Config:
    def __init__(self):
        self.config = None
        self._config_path = f"assets{os.path.sep}config{os.path.sep}data{os.path.sep}config.json"
        self._load_config()

    def _load_config(self):
        try:
            config_file = open(self._config_path, 'r')
            self.config = json.load(config_file)
            config_file.close()

        except IOError:
            pass

    def get_icon_config(self):
        return self.config["icon"]

    def get_default_data_path(self):
        return os.getcwd() + os.path.sep + self.config["data"]["default_folder"]

