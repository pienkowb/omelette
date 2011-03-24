class DependencyResolver(object):
    
    def __init__(self, uml_objects):
        self.__uml_objects = uml_objects

    def resolve(self):
        for uml_object in self.__uml_objects.values():
            self.__resolve_object(uml_object)

    def __resolve_object(self, uml_object):
        if uml_object.type != None: return

        if uml_object.parent == None:
            uml_object.type = uml_object.name
        else:
            parent = self.__uml_objects[uml_object.parent]
            self.__resolve_object(parent)

            uml_object.type = parent.type

            properties = parent.properties.copy()
            properties.update(uml_object.properties)
            uml_object.properties = properties
