from karamel.command import Command

__command__ = 'freeze'
__description__ = 'Freeze version of Kooki and Jars'


class FreezeCommand(Command):

    def __init__(self):
        super(FreezeCommand, self).__init__(__command__, __description__)
        self.add_argument('-f', '--config-file', default='kooki.yaml')

    def callback(self, args):
        pass
