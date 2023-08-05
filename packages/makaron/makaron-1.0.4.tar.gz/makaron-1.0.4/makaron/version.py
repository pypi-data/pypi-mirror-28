import re
from .exception import MakaronException, BadVersionFormat, BadVersionComponentFormat, VersionsFoundAreDifferent

full_version_regex_format = r'[0-9]+\.[0-9]+\.[0-9]+'


def check_version_are_identical(versions):
    different = False

    first_version = versions[0].version.get()
    for located in versions[1:]:
        if located.version.get() != first_version:
            different = True
            break

    if different:
        raise VersionsFoundAreDifferent(versions)


class Version():
    def __init__(self, string_version='0.0.0'):
        self.set_from_string(string_version)

    def __str__(self):
        return self.get()

    def copy(self, version):
        self.major = version.major
        self.minor = version.minor
        self.patch = version.patch

    def set_from_string(self, version):
        pattern = re.compile(full_version_regex_format)
        if not pattern.match(version):
            raise BadVersionFormat(version)

        version_spiltted = version.split('.')
        self.major = int(version_spiltted[0])
        self.minor = int(version_spiltted[1])
        self.patch = int(version_spiltted[2])

    def set_major(self, major):
        if not isinstance(major, int):
            raise BadVersionComponentFormat('major', major)
        if major < 0:
            raise BadVersionComponentFormat('major', major)
        self.major = major

    def set_minor(self, minor):
        if not isinstance(minor, int):
            raise BadVersionComponentFormat('minor', minor)
        if minor < 0:
            raise BadVersionComponentFormat('minor', minor)
        self.minor = minor

    def set_patch(self, patch):
        if not isinstance(patch, int):
            raise BadVersionComponentFormat('patch', patch)
        if patch < 0:
            raise BadVersionComponentFormat('patch', patch)
        self.patch = patch

    def increase_major(self):
        self.major += 1
        self.minor = 0
        self.patch = 0

    def increase_minor(self):
        self.minor += 1
        self.patch = 0

    def increase_patch(self):
        self.patch += 1

    def get(self):
        return '{}.{}.{}'.format(self.major, self.minor, self.patch)


class LocatedVersion():
    def __init__(self, version, file_name):
        self.version = Version(version)
        self.file_name = file_name
