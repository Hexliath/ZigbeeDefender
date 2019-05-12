import configparser
import os

class Config:
    file = "config.ini"
    def __init__(self,file=None):
        try:
            if file is not None:
                self.file = file
            fh = open(self.file, 'r')
            fh.close()
        except FileNotFoundError:
            print("File did not exits. It will be created")
            self.create()

    def get(self, section, variable):
        config = configparser.RawConfigParser()
        config.read(self.file)
        value = config.get(section, variable)
        if(section == "sensors"):
            value = [int(x) for x in value.split(",")]
        return value

    def reset(self):
        os.remove(self.file)
        self.create()

    def create(self):
        config = configparser.RawConfigParser()
        config.add_section('mariadb')
        config.set('mariadb', 'port', '3306')
        config.set('mariadb', 'host', 'localhost')
        config.set('mariadb', 'db', 'zigbee_defender')
        config.set('mariadb', 'user', 'root')
        config.set('mariadb', 'password', 'changeme')

        config.add_section('server')
        config.set('server', 'password', 'changeme')
        config.set('server', 'port', '4001')

        config.add_section('model')
        config.set('model', 'mode', 'TRAIN')
        config.set('model', 'version', '0x00')

        config.add_section('sensors')
        config.set('sensors', 'luminosity', '0,1000')
        config.set('sensors', 'presence', '0,1')
        config.set('sensors', 'temperature', '10,40')

        with open(self.file, 'w') as configfile:
            config.write(configfile)

    def getSectionKeys(self,section):
        config = configparser.ConfigParser()
        config.read(self.file)
        return [option for option in config[section]]


