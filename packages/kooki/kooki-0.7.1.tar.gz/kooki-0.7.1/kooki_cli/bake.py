import pretty_output, argparse, traceback

from karamel.command import Command

from kooki.jars import search_file, search_recipe, search_jar
from kooki.config import read_config_file
from kooki.rule_parser import parse_document_rules
from kooki.extension import load_extensions, caller
from kooki.exception import KookiException

from collections import OrderedDict

__command__ = 'bake'
__description__ = 'Bake a kooki'

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


class BakeCommand(Command):

    def __init__(self):
        super(BakeCommand, self).__init__(__command__, __description__)
        self.add_argument('documents', nargs='*')
        self.add_argument('--config-file', default='kooki.yaml')
        self.add_argument('-h', '--help', action='help', default=argparse.SUPPRESS, help='Show this help message and exit.')
        self.add_argument('-d', '--debug', help='Show information to help debug the bake processing', action='store_true')
        self.add_argument('--no-color', help='The output has no color.', action='store_true')
        self.add_argument('--no-output', help='There is no output.', action='store_true')

    def callback(self, args):
        try:
            pretty_output.set_output_policy(not args.no_output)
            pretty_output.set_color_policy(not args.no_color)
            pretty_output.set_debug_policy(args.debug)
            pretty_output.command('bake')

            self.real_call(args)

        except KookiException as e:
            pretty_output.error_step('Errors')
            pretty_output.error(e)

        except Exception as e:
            pretty_output.error_step('Errors')
            pretty_output.error(traceback.format_exc()[:-1])

        finally:
            pretty_output.command()

    def real_call(self, args):
        config = read_config_file(args.config_file)
        document_rules = parse_document_rules(config)

        if args.documents == []:
            documents = document_rules
        else:
            documents = {}
            for document_name in args.documents:
                if document_name in document_rules:
                    documents[document_name] = document_rules[document_name]
                else:
                    raise Exception('Bad document')

        for name, document in documents.items():
            recipe = document.recipe
            jars = document.jars

            pretty_output.start_document(name)

            # jars
            pretty_output.start_step('jars')
            output_search_start()
            full_path_jars = []
            for jar in document.jars:
                jar_full_path = search_jar(jar)
                output_search(jar, jar_full_path)
                full_path_jars.append(jar_full_path)
            document.jars = full_path_jars
            output_search_finish()

            # extensions
            pretty_output.start_step('extensions')
            output_search_start()
            extensions = load_extensions(document.jars, document.recipe)
            new_extensions = {}
            for extension_name, extension_path in extensions.items():
                new_extensions[extension_name] = caller(extension_path)
                output_search(extension_name, extension_path)
            output_search_finish()

            # template
            pretty_output.start_step('template')
            output_search_start()
            file_full_path = search_file(jars, recipe, document.template)
            output_search(document.template, file_full_path)
            if file_full_path:
                with open(file_full_path,'r') as f:
                    file_read = f.read()
                document.template = file_read
            output_search_finish()

            # metadata
            pretty_output.start_step('metadata')
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
            pretty_output.start_step('content')
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
            pretty_output.start_step('recipe')
            output_search_start()
            file_full_path = search_recipe(recipe)
            output_search(document.recipe, file_full_path)
            output_search_finish()

            if file_full_path:
                with open(file_full_path,'r') as f:
                    recipe_read = f.read()
                    variables = {}
                    exec(recipe_read, variables)
                    if 'recipe' in variables:
                        recipe = variables['recipe']
                    recipe(document, new_extensions)
            else:
                raise(Exception('bad recipe'))
