import pretty_output

from collections import OrderedDict

from kooki.jars import search_file, search_recipe, search_jar
from kooki.extension import load_extensions, caller

output = []

def output_search_start():
    global output
    output = []


def output_search(path, fullpath):
    if fullpath:
        output.append({'name': path, 'status': '[found]', 'path': fullpath})
    else:
        output.append({'name': path, 'status': ('[missing]', 'red'), 'path': ''})


def output_search_finish():
    pretty_output.infos(output, [('name', 'blue'), ('status', 'green'), ('path', 'cyan')])


def process_document(document_origin):
    document = document_origin.copy()
    recipe = document.recipe
    jars = document.jars

    # jars
    full_path_jars = []
    for jar in document.jars:
        jar_full_path = search_jar(jar)
        full_path_jars.append(jar_full_path)
    document.jars = full_path_jars

    # extensions
    pretty_output.title_3('extensions')
    output_search_start()
    extensions = load_extensions(document.jars, document.recipe)
    new_extensions = {}
    for extension_name, extension_path in extensions.items():
        new_extensions[extension_name] = caller(extension_path)
        output_search(extension_name, extension_path)
    output_search_finish()

    # template
    pretty_output.title_3('template')
    output_search_start()
    file_full_path = search_file(jars, recipe, document.template)
    output_search(document.template, file_full_path)
    if file_full_path:
        with open(file_full_path,'r') as f:
            file_read = f.read()
        document.template = file_read
        output_search_finish()
    else:
        output_search_finish()
        raise Exception('Bad template')

    # metadata
    pretty_output.title_3('metadata')
    metadata_full_path = {}
    output_search_start()
    for metadata in document.metadata:
        file_full_path = search_file(jars, recipe, metadata)
        with open(file_full_path,'r') as f:
            file_read = f.read()
        metadata_full_path[file_full_path] = file_read
        output_search(metadata, file_full_path)
    document.metadata = metadata_full_path
    output_search_finish()

    # content
    pretty_output.title_3('content')
    content_full_path = OrderedDict()
    output_search_start()
    for content in document.content:
        file_full_path = search_file(jars, recipe, content)
        with open(file_full_path,'r') as f:
            file_read = f.read()
        content_full_path[file_full_path] = file_read
        output_search(content, file_full_path)
    document.content = content_full_path
    output_search_finish()

    # recipe
    pretty_output.title_3('recipe')
    file_full_path = search_recipe(recipe)
    if file_full_path:
        with open(file_full_path,'r') as f:
            recipe_read = f.read()
            variables = {}

            exec(recipe_read, variables)
            if 'recipe' in variables:
                recipe = variables['recipe']
                recipe(document, new_extensions)
            else:
                raise(Exception('bad recipe: missing recipe function'))
    else:
        raise(Exception('bad recipe: missing file'))
