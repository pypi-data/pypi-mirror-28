class KookiException(Exception):
    pass

no_config_file_found_message = \
'''
No '{}' file found.
Create one by executing 'kooki new'.
'''

class NoConfigFileFound(KookiException):
    def __init__(self, config_file_name):
        message = no_config_file_found_message.format(config_file_name)
        super(NoConfigFileFound, self).__init__(message)


yaml_error_config_file_parsing_message = \
'''Yaml error during config file parsing.
Please check the format of your config file.'''

class YamlErrorConfigFileParsing(KookiException):
    def __init__(self, exc):
        message = yaml_error_config_file_parsing_message
        super(YamlErrorConfigFileParsing, self).__init__(message)


yaml_error_config_file_bad_type_message = \
'''The Yaml parsed should be a dict and it is a {}.
Please check the format of your config file.'''

class YamlErrorConfigFileBadType(KookiException):
    def __init__(self, type_found):
        message = yaml_error_config_file_bad_type_message.format(type_found)
        super(YamlErrorConfigFileBadType, self).__init__(message)
