class MakaronException(Exception):
    pass


no_config_file_found_message = \
'''
No '.makaron.yml' file found.
Create one by executing 'makaron --generate-config'.
'''

class NoConfigFileFound(MakaronException):
    def __init__(self):
        message = no_config_file_found_message
        super(NoConfigFileFound, self).__init__(message)


yaml_error_config_file_parsing_message = \
'''Yaml error during config file parsing.
Please check the format of your config file.'''

class YamlErrorConfigFileParsing(MakaronException):
    def __init__(self, exc):
        message = yaml_error_config_file_parsing_message
        super(YamlErrorConfigFileParsing, self).__init__(message)


yaml_error_config_file_bad_type_message = \
'''The Yaml parsed should be a dict and it is a {}.
Please check the format of your config file.'''

class YamlErrorConfigFileBadType(MakaronException):
    def __init__(self, type_found):
        message = yaml_error_config_file_bad_type_message.format(type_found)
        super(YamlErrorConfigFileBadType, self).__init__(message)


config_bad_format_message = \
'''The config provided should be a dict and it is a {}.
Please check the format of your config.'''

class ConfigBadFormat(MakaronException):
    def __init__(self, type_found):
        message = config_bad_format_message.format(type_found)
        super(ConfigBadFormat, self).__init__(message)


rule_bad_format_message = \
'''The rule for finding version should be a string or a list of string.
Please check the format of your config.'''

class RuleBadFormat(MakaronException):
    def __init__(self):
        message = rule_bad_format_message
        super(RuleBadFormat, self).__init__(message)


versions_found_are_different_message = \
'''Versions found are different.
{}'''

class VersionsFoundAreDifferent(MakaronException):
    def __init__(self, versions):
        versions_formatted = ''
        for version in versions:
            versions_formatted += '- {}: {}\n'.format(version.file_name, version.version.get())
        message = versions_found_are_different_message.format(versions_formatted)
        super(VersionsFoundAreDifferent, self).__init__(message)


bad_version_format = \
'''The version provided is not compatible with makaron version format.
provided: {}
makaron format: [uint].[uint].[uint]'''

class BadVersionFormat(MakaronException):
    def __init__(self, version):
        message = bad_version_format.format(version)
        super(BadVersionFormat, self).__init__(message)


bad_version_component_format = \
'''The {} component of the version provided is not correct.
It should be an unsigned int.
provided: {}'''

class BadVersionComponentFormat(MakaronException):
    def __init__(self, component_type, value):
        message = bad_version_component_format.format(component_type, value)
        super(BadVersionComponentFormat, self).__init__(message)


bad_version_component_format = \
'''The rule ({}) you have provide for the file {} does not indicate the position of the version.
The string [version] should be written somewhere in the rule.'''

class MissingVersionInRule(MakaronException):
    def __init__(self, file_name, regex):
        message = bad_version_component_format.format(regex, file_name)
        super(MissingVersionInRule, self).__init__(message)


cannot_find_any_version = \
'''Cannot find any version in file {} with the pattern "{}".
Please check the pattern you have provided in your config.'''

class CannotFindAnyVersion(MakaronException):
    def __init__(self, file_name, regex):
        message = cannot_find_any_version.format(file_name, regex)
        super(CannotFindAnyVersion, self).__init__(message)
