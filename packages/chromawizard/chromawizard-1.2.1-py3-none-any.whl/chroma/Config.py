import json
import logging
from PyQt5 import QtCore

_t = QtCore.QCoreApplication.translate

log = None
p_fallback = None
fallback = None

class Data:
    def __init__(self, data:dict):
        self.__dict__.update(data)

    def __getattr__(self, name):
        if p_fallback:
            if log:
                log.warning(_t("Config", "Attribute '{}' is not in config file. Use fallback version {}. This could happen after a version upgrade.".format(name, p_fallback)))

            return fallback.get(name)
        else:
            raise AttributeError


class Config:
    def __init__(self, path:str, config:dict):
        self.path = path
        self.config = Data(config)

    def __iter__(self):
        for key in self.config.__dict__:
            yield key

    def update(self):
        with open(self.path, 'w') as outfile:
            json.dump(self.config.__dict__, outfile, sort_keys=True, indent=2)

    def save(self, path):
        with open(path, 'w') as outfile:
            json.dump(self.config.__dict__, outfile, sort_keys=True, indent=2)

    def get_fields(self):
        return tuple(self.config.__dict__.keys())

    def get_dict(self):
        return self.config.__dict__

    @classmethod
    def read_create_config(cls, path:str, path_fallback: str=None, logger: logging.Logger=None):
        global p_fallback
        global fallback
        global log

        p_fallback = path_fallback
        log = logger

        try:
            with open(path, "r") as infile:
                json_data = json.loads(infile.read())

            return Config(path, json_data)
        except:
            try:
                if p_fallback:
                    with open(p_fallback, "r") as infile:
                        fallback = json.loads(infile.read())

                with open(path, "w") as infile:
                    infile.write("{}")
                    return Config(path, {})
            except:
                raise


if __name__ == "__main__":
    d = Data({'a':5})
    print(d.a)

    # Read or create empty config file
    conf = Config.read_create_config("test.json")

    # Add field test to config
    conf.config.test = "Hello World!"
    conf.config.myArray=["Hallo", 2, {'n':10}]

    # Update config json (write changes to file)
    conf.update()

    # Show fields in config
    print(conf.get_fields())

    # Show fields in config
    print(conf.get_dict())

    for item in conf:
        print(item)
