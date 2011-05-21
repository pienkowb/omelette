from omelette.compiler.code import Library
from omelette.compiler.parser import Parser
from omelette.compiler.resolver import DependencyResolver

class Compiler(object):

    def __init__(self, libraries=[]):
        self.__library_uml_objects = {}
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

        if isinstance(code, Library):
            self.__library_uml_objects.update(uml_objects)

        self.__uml_objects.update(uml_objects)
        self.__resolver.resolve()

        for name, uml_object in uml_objects.items():
            if uml_object.is_prototype:
                del uml_objects[name]

        return uml_objects

    def clear(self):
        self.__uml_objects.clear()
        self.__uml_objects.update(self.__library_uml_objects)
