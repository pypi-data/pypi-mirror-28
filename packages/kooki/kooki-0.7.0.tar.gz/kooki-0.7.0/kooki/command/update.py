from karamel.command import Command

__command__ = 'update'
__description__ = 'Update a kooki project'


class UpdateCommand(Command):

    def __init__(self):
        super(UpdateCommand, self).__init__(__command__, __description__)
        self.add_argument('-f', '--config-file', default='kooki.yaml')

    def callback(self, args):
        pass
