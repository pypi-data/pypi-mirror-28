import yaml, pretty_output

from karamel.command import Command

from kooki.version import __version__
from kooki.tools import read_file

__command__ = 'check'
__description__ = 'Check version of kooki freeze'

class CheckCommand(Command):

    def __init__(self):
        super(CheckCommand, self).__init__(__command__, __description__)
        self.add_argument('--no-color', help='The output has no color.', action='store_true')
        self.add_argument('--no-output', help='There is no output.', action='store_true')

    def callback(self, args):
        pretty_output.set_output_policy(not args.no_output)
        pretty_output.set_color_policy(not args.no_color)
        pretty_output.set_debug_policy(args.debug)
        pretty_output.command(self.command)

        freeze_file = read_file('.kooki_freeze')
        freeze_data = yaml.safe_load(freeze_file)
        check_kooki_freeze(__version__, freeze_data)


def check_kooki_freeze(version, freeze_data):

    # check kooki version
    Output.start_step('kooki')
    if freeze_data['kooki'] != version:
        Output._print_colored('version needed ', 'blue', end='')
        Output._print_colored(freeze_data['kooki'], 'cyan', end='')
        Output._print_colored(', version installed ', 'blue', end='')
        Output._print_colored(version, 'cyan', end='')
        Output._print_colored(' [bad kooki version]', 'red')
    else:
        Output._print_colored('version ', 'blue', end='')
        Output._print_colored(version, 'cyan', end='')
        Output._print_colored(' [good kooki version]', 'green')

    jars = get_jars()

    Output.start_step('jars')
    for jar in freeze_data['repositories']:
        version_freezed = freeze_data['repositories'][jar]['version']
        Output._print_colored(jar, 'blue')
        Output._print_colored('  freezed: ', 'yellow', end='')
        Output._print_colored(version_freezed, 'cyan')
        Output._print_colored('  installed: ', 'yellow', end='')
        if jar in jars:
            version_installed = jars[jar]['version']
            if version_freezed == version_installed:
                Output._print_colored(version_installed, 'green')
            else:
                Output._print_colored(version_installed, 'red', end='')
                Output._print_colored(' [bad version installed]', 'red')
        else:
            Output._print_colored('[jar not installed]', 'red')
