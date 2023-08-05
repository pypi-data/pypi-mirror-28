import os, yaml

from .exception import YamlErrorConfigFileParsing, NoConfigFileFound, YamlErrorConfigFileBadType

config_file_name = '.makaron.yml'

config_file_content = \
'''# {}
# more info at https://makaron.gitlab.io

setup.py: "__version__ = '[version]'"

'''.format(config_file_name)


def generate_config_file():
    with open(config_file_name, 'w') as stream:
        stream.write(config_file_content)


def read_config_file():
    if os.path.isfile(config_file_name):
        with open(config_file_name, 'r') as stream:
            try:
                content = stream.read()
                config = yaml.safe_load(content)
                if not isinstance(config, dict):
                    raise YamlErrorConfigFileBadType(type(config))

                return config
            except yaml.YAMLError as exc:
                raise YamlErrorConfigFileParsing(exc)

    else:
        raise NoConfigFileFound()
