from omelette.compiler.parser import Parser
from omelette.compiler.resolver import DependencyResolver

class Compiler(object):

    def __init__(self, libraries=[]):
        self.__uml_objects = {}
        self.__lib_uml_objects = {}

        self.__parser = Parser()
        self.__resolver = DependencyResolver(self.__uml_objects)

        for library in libraries:
            self.compile(library, True)
            
    def compile(self, code, is_lib = False):
        code_objects = code.objects(lambda o: o.modified)
        uml_objects = self.__parser.parse(code_objects)

        for code_object in code_objects:
            code_object.modified = False

        self.__uml_objects.update(uml_objects)
        self.__resolver.resolve()
        
        if(is_lib == False):
            for name, uml_object in uml_objects.items():
                if uml_object.is_prototype:
                    del uml_objects[name]
        else:            
            self.__lib_uml_objects.update(uml_objects)

        return uml_objects
    
    def clear(self, libs = False):
        self.__uml_objects.clear()
        if(libs == True):
            self.__lib_uml_objects()
        else:
            self.__uml_objects.update(self.__lib_uml_objects)