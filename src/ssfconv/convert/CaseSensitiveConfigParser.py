import configparser

# 为了使其区分大小写，重载 ConfigParser
class CaseSensitiveConfigParser(configparser.ConfigParser):
    def optionxform(self, optionstr):
        return optionstr