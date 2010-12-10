from omelette.parser.code import Code
from omelette.parser.resolver import DependencyResolver

class Parser:
    def __init__(self):
        self.__code = Code()
        self.__uml_objects = {}
        self.__resolver = DependencyResolver(self.__uml_objects)

    def insert(self, number, line):
        self.__code.insert_line(number, line)

    def update(self, number, line):
        self.remove(number)
        self.insert(number, line)

    def remove(self, number):
        self.__code.remove_line(number)

    def parse(self):
        code_objects = self.__code.objects(lambda o: o.modified)
        uml_objects = {}

        # translation

        self.__uml_objects.update(uml_objects)
        self.__resolver.resolve()

        return uml_objects
