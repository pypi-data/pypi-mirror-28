from .version import check_version_are_identical, full_version_regex_format, LocatedVersion
from .tools import *
from .exception import MissingVersionInRule, CannotFindAnyVersion

def extract_version_from_rules(rules):
    version_collected = []
    for rule in rules:
        versions = rule.collect()
        version_collected += versions
    check_version_are_identical(versions)
    return version_collected[0].version


def apply_version_to_rules(rules, new_version):
    for rule in rules:
        rule.apply(new_version)


class Rule:

    def __init__(self, file_name, version_pattern):
        if exist(r'\[version\]', version_pattern):
            version_regex = version_pattern.replace('[version]', full_version_regex_format)
        else:
            raise MissingVersionInRule(file_name, version_pattern)

        self.version_pattern = version_pattern
        self.version_regex = version_regex
        self.file_name = file_name

    def collect(self):
        content = read_file(self.file_name)
        string_versions = search_all(self.version_regex, full_version_regex_format, content)
        versions = [LocatedVersion(string_version, self.file_name) for string_version in string_versions]

        if len(versions) == 0:
            raise CannotFindAnyVersion(self.file_name, self.version_pattern)

        return versions

    def apply(self, new_version):
        content = read_file(self.file_name)
        string_new_version = new_version.get()
        content = search_all_and_replace(self.version_regex, full_version_regex_format, content, string_new_version)
        write_file(self.file_name, content)
