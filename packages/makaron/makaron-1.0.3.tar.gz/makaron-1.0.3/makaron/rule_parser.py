from .config import read_config_file
from .rule import Rule
from .exception import ConfigBadFormat, RuleBadFormat

def parse_version_rules(config):

    if not isinstance(config, dict):
        raise ConfigBadFormat(type(config))

    rules = []
    for file_name, info in config.items():
        parse_version_rule(rules, file_name, info)
    return rules


def parse_version_rule(rules, file_name, info):

    if isinstance(info, str):
        rule = Rule(file_name, info)
        rules.append(rule)

    elif isinstance(info, list):
        for info_item in info:
            if isinstance(info_item, str):
                rule = Rule(file_name, info_item)
                rules.append(rule)
            else:
                raise RuleBadFormat()

    else:
        raise RuleBadFormat()
