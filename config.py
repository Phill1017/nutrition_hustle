import configparser

_config = configparser.ConfigParser()
_config.read("nutrition.ini")

CONFIG = {
    "server": dict(_config["server"]),
    "database": dict(_config["database"]),
    "frontend": dict(_config["frontend"]),
    "api": dict(_config["api"])
}
