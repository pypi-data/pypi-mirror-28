import pretty_output, argparse, traceback

from karamel.command import Command

from kooki.config import read_config_file, get_kooki_recipe_manager, get_kooki_dir_recipes, get_kooki_jar_manager, get_kooki_dir_jars
from kooki.rule_parser import parse_document_rules
from kooki.exception import KookiException
from kooki.process import process_document

from karamel.packages import install_packages, freeze_packages

__command__ = 'bake'
__description__ = 'Bake a kooki'


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

            self.real_call(args)

        except KookiException as e:
            pretty_output.error_step('Errors')
            pretty_output.error(e)

        except Exception as e:
            pretty_output.error_step('Errors')
            pretty_output.error(traceback.format_exc()[:-1])

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
            pretty_output.title_1(name)
            self.execute_unfreeze(document)
            self.execute_bake(document)
            pretty_output.title_2()

    def on_package_downloading(self, package_name):
        print('Downloading \'{}\''.format(package_name))

    def on_package_installing(self, package_name):
        print('Installing \'{}\''.format(package_name))

    def on_package_install_success(self, package_name):
        print('Successfully installed \'{}\''.format(package_name))

    def on_package_already_installed(self, package_name, package_path):
        print('Package \'{}\' already installed in \'{}\''.format(package_name, package_path))

    def on_package_not_found(self, package_name):
        print('Package not found \'{}\''.format(package_name))
        raise KookiException('Error during configuration unfreezing')

    def on_package_bad_version_provided(self, package_name, version):
        print('Could not find the version \'{1}\' for package \'{0}\''.format(package_name, version))
        raise KookiException('Error during configuration unfreezing')

    def execute_unfreeze(self, document):
        pretty_output.title_2('unfreeze')

        pretty_output.title_3('jars')
        package_manager_url = get_kooki_jar_manager()
        package_install_dir = get_kooki_dir_jars()
        install_packages(package_manager_url,
                         package_install_dir,
                         document.jars,
                         self.on_package_downloading,
                         self.on_package_installing,
                         self.on_package_install_success,
                         self.on_package_already_installed,
                         self.on_package_not_found,
                         self.on_package_bad_version_provided)

        pretty_output.title_3('recipe')
        package_manager_url = get_kooki_recipe_manager()
        package_install_dir = get_kooki_dir_recipes()
        install_packages(package_manager_url,
                         package_install_dir,
                         [document.recipe],
                         self.on_package_downloading,
                         self.on_package_installing,
                         self.on_package_install_success,
                         self.on_package_already_installed,
                         self.on_package_not_found,
                         self.on_package_bad_version_provided)

    def execute_bake(self, document):
        pretty_output.title_2('bake')
        process_document(document)
