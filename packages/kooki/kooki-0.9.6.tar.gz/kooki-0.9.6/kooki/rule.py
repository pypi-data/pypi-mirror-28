from kooki.exception import KookiException

invalid_field_message = \
'''Invalid config file
The '{1}' field of '{0}' is not in a valid format.
It should be a {2} and it is a {3}.'''


class Rule:

    reserved = ['name', 'template', 'recipe', 'jars', 'metadata', 'content']

    def __init__(self, document_name='', config={}):
        self.document_name = document_name
        self.name = ''
        self.template = ''
        self.recipe = ''
        self.jars = []
        self.metadata = []
        self.content = []
        self.set_config(config)

    def set_config(self, config):
        for key, value in config.items():
            if key == 'name':
                if not isinstance(value, str):
                    raise KookiException(invalid_field_message.format(self.document_name, key, str, type(value)))
                self.name = value
            elif key == 'template':
                if not isinstance(value, str):
                    raise KookiException(invalid_field_message.format(self.document_name, key, str, type(value)))
                self.template = value
            elif key == 'recipe':
                if not isinstance(value, str):
                    raise KookiException(invalid_field_message.format(self.document_name, key, str, type(value)))
                self.recipe = value
            elif key == 'jars':
                if not isinstance(value, list):
                    raise KookiException(invalid_field_message.format(self.document_name, key, list, type(value)))
                self.jars += value
            elif key == 'metadata':
                if not isinstance(value, list):
                    raise KookiException(invalid_field_message.format(self.document_name, key, list, type(value)))
                self.metadata += value
            elif key == 'content':
                if not isinstance(value, list):
                    raise KookiException(invalid_field_message.format(self.document_name, key, list, type(value)))
                self.content += value

    def copy(self):
        rule = Rule()
        rule.name = self.name
        rule.template = self.template
        rule.recipe = self.recipe
        rule.jars = list(self.jars)
        rule.metadata = list(self.metadata)
        rule.content = list(self.content)
        return rule
