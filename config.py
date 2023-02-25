import configparser
import os


class Config:
        # fill the initial configuration file inside the verify method
    @staticmethod
    def verify():
        if not path.exists("config.ini"):
            config = ConfigParser()
            config["CONSTANTS"] = {
                "version": "1.0.0",
                "env": "TEST"
            }
            with open("config.ini", "w") as file:
                config.write(file)


    @staticmethod
    def read(section, key):
        Configurator.verify()
        config = ConfigParser()
        config.read("config.ini")
        return config[section][key]

    @staticmethod
    def read_list(section, key, delimiter):
        Configurator.verify()
        config = ConfigParser()
        config.read("config.ini")
        data = config[section][key].split(delimiter)
        return list(map(str.strip, data))

    @staticmethod
    def update(section, key, value):
        Configurator.verify()
        config = ConfigParser()
        config.read("config.ini")
        config.set(section, key, value)
        with open("config.ini", "w") as file:
            config.write(file)
   
    @staticmethod
    def write_config(section, params):
        try:
            config = configparser.ConfigParser()
            config.add_section(section)
            for r in range(len(params)):
                config.set(section, params[r][0], params[r][1])
            with open("Config.ini", "w") as configfile:
                config.write(configfile)
        except:
            print("Unexpected Error occurred while writing config")
            return -1

    @staticmethod
    def config_exists():
        return True if os.path.exists("Config.ini") else False
