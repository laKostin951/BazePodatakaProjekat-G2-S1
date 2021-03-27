from config._config import _Config
from config._icon import _Icon
from cache.server.connections import Connections
from src.mysql.connection import make_pool_party

config = _Config()
icon = _Icon(config)
mysqlServerConnections = Connections()
cnxpool = make_pool_party(mysqlServerConnections[0])

WIDTH = 1920
HEIGHT = 1080

DEFAULT_DATA_FOLDER = config.get_default_data_path()