import re

def read_file(file_name):
    try:
        stream = open(file_name, 'r')
        content = stream.read()
        stream.close()
        return content
    except IOError as e:
        raise RuntimeError('No such file: \'{0}\''.format(file_name))


def write_file(file_name, content):
    stream = open(file_name, 'w')
    stream.write(content)
    stream.close()
    return content


def exist(regex, content):
    return len(re.findall(regex, content)) > 0


def search(regex, content):
    return re.findall(regex, content)


def search_one(regex, content):
    result = re.findall(regex, content)
    if len(result) == 0:
        raise RuntimeError('Found no occurence of the following regex {} in {}'.format(regex, content))
    if len(result) > 1:
        raise RuntimeError('Found more then one occurence of the following regex {} in {}'.format(regex, content))
    return result[0]


def search_all(first_regex, second_regex, content):
    parts = search(first_regex, content)
    found = []
    for part in parts:
        found.append(search_one(second_regex, part))
    return found


def search_all_and_replace(first_regex, second_regex, content, replace_string):
    parts = search(first_regex, content)
    for part in parts:
        string_found = search_one(second_regex, part)
        new_part = part.replace(string_found, replace_string)
        content = content.replace(part, new_part)
    return content
