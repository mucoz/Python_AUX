import configparser
import os


class Config:
    """
        Functions return -1 if error occurs
        The name of the config file is "Config.ini"
        =============================================
        if Config.start_config() == -1:
        print("You need to fill the config file!")
        sys.exit()

        aa = Config.read_config("CONSTANTS", "aa")
        if aa !=-1 : print(aa)

        user = Config.read_config("CONSTANTS", "username")
        if user !=-1 : print(user)
        ==============================================
    """
    @staticmethod
    def start_config():
        config = Config.read_config("CONSTANTS", "version")
        if config == -1:
            Config.write_config("CONSTANTS", [["version", "1.0.0"],
                                              ["username", os.environ.get("USERNAME")]])
            config = Config.read_config("CONSTANTS", "version")
            return -1

    @staticmethod
    def read_config(section,key):
        file_name = "Config.ini"
        config = configparser.ConfigParser()
        if os.path.exists(file_name):
            config.read(file_name)
            try:
                config = config[section]
            except:
                print("No section found : " + section)
                return -1
            try:
                return config[key]
            except:
                print("No key found : " + key)
                return -1
        else:
            return -1

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
    def edit_config(section, key, value):
        try:
            config = configparser.ConfigParser()
            config.read("Config.ini")
            config[section][key] = value
            with open("Config.ini", "w") as configfile:
                config.write(configfile)
        except:
            print("Unexpected Error occurred while editing config")
            return -1

    @staticmethod
    def append_config(section, params):
        try:
            config = configparser.ConfigParser()
            config.add_section(section)
            for r in range(len(params)):
                config.set(section, params[r][0], params[r][1])
            with open("Config.ini", "a") as configfile:
                config.write(configfile)
        except:
            print("Unexpected Error occurred while appending config")
            return -1

    @staticmethod
    def config_exists():
        return True if os.path.exists("Config.ini") else False
