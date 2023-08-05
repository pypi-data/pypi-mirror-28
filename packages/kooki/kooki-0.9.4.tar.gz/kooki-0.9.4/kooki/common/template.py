import em
from kooki.tools import get_front_matter
from collections import OrderedDict


def apply_template(data, metadata):
    interpreter = em.Interpreter()
    interpreter.setPrefix('@')
    result = None

    if isinstance(data, list):
        result = []
        for content in data:
            result.append(interpreter.expand(content, metadata))

    elif isinstance(data, OrderedDict):
        result = OrderedDict()
        for file_path, file_content in data.items():
            front_matter, content = get_front_matter(file_content)
            metadata.update(front_matter)
            result[file_path] = interpreter.expand(content, metadata)

    elif isinstance(data, dict):
        result = {}
        for file_path, file_content in data.items():
            front_matter, content = get_front_matter(file_content)
            metadata.update(front_matter)
            result[file_path] = interpreter.expand(content, metadata)

    elif isinstance(data, str):
        result = ''
        result = interpreter.expand(data, metadata)

    else:
        raise Exception('templating bad data type {}'.format(type(data)))

    return result
