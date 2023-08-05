
class Rule:

    reserved = ['name', 'template', 'recipe', 'jars', 'metadata', 'content']

    def __init__(self, config={}):
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
                self.name = value
            elif key == 'template':
                self.template = value
            elif key == 'recipe':
                self.recipe = value
            elif key == 'jars':
                self.jars += value
            elif key == 'metadata':
                self.metadata += value
            elif key == 'content':
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
