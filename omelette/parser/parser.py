from omelette.parser.translator import Translator
from omelette.parser.resolver import DependencyResolver

class Parser(object):
    def __init__(self):
        self.translator = Translator()

    def parse(self, code):
        uml_objects = self.translator.parse([code])

        uml_objects = dict([(o.name, o) for o in uml_objects])
        DependencyResolver(uml_objects).resolve()

        return uml_objects
