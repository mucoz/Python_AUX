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








Innovation:

I will dedicate 10% of my time each week to researching and exploring new technologies that could enhance our products and services.
I will propose at least three innovative ideas for new features or products that could generate revenue for the company in the next quarter.
I will collaborate with colleagues in different departments to identify areas where we can implement innovative solutions to improve efficiency and reduce costs.
Collaboration:

I will actively seek out opportunities to collaborate with other developers, designers, and stakeholders on projects, rather than working in silos.
I will encourage a culture of knowledge-sharing and collaboration by organizing regular team meetings and knowledge-sharing sessions.
I will prioritize open communication and feedback with my colleagues, and work towards building strong working relationships across the organization.
Digitalization:

I will identify at least three manual processes within our team that could be automated or digitized using existing tools or platforms.
I will stay up-to-date with the latest trends and best practices in digitalization and automation, and share my findings with my colleagues.
I will work towards reducing the use of paper and physical documentation within our team, and encourage others to do the same.
Simplification:

I will review and streamline at least two existing processes within our team to reduce complexity and increase efficiency.
I will work with stakeholders to identify areas where we can simplify our products or services without sacrificing functionality or user experience.
I will prioritize clear and concise communication with colleagues and stakeholders, and avoid unnecessary jargon or complexity in my work.

