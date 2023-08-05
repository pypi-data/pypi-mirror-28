import em
from kooki.tools import DictAsMember, get_front_matter
from kooki.common import update_metadata


def apply_template(data, metadata):
    interpreter = em.Interpreter()
    interpreter.setPrefix('@')
    result = None

    if isinstance(data, list):
        result = []
        for content in data:
            result.append(interpreter.expand(content, metadata))

    elif isinstance(data, dict):
        result = {}
        for file_path, file_content in data.items():
            front_matter, content = get_front_matter(file_content)
            metadata = update_metadata(front_matter, metadata)
            result[file_path] = interpreter.expand(content, metadata)

    elif isinstance(data, str):
        result = ''
        result = interpreter.expand(data, metadata)

    return result
