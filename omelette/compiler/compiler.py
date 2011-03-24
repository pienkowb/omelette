from omelette.compiler.parser import Parser
from omelette.compiler.resolver import DependencyResolver

class Compiler(object):
    def __init__(self, libraries=[]):
        self.__uml_objects = {}

        self.__parser = Parser()
        self.__resolver = DependencyResolver(self.__uml_objects)

        for library in libraries:
            self.compile(library)

    def compile(self, code):
        code_objects = code.objects(lambda o: o.modified)
        uml_objects = self.__parser.parse(code_objects)

        for code_object in code_objects:
            code_object.modified = False

        self.__uml_objects.update(uml_objects)
        self.__resolver.resolve()

        return uml_objects
