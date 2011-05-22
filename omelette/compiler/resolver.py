from omelette.compiler import logging
import collections

class DependencyResolver(object):

    def __init__(self, uml_objects):
        self.__uml_objects = uml_objects

    def __find_circular_refs(self):
        """
        This method performs topological sorting in order to check
        if there are any circular references in given array of umlobjects
        i.e. if one object is descendant and ancestor of another object

        Method returns set of objects involved in such relations (empty set
        if no circular references were found).
        """

        ref_count = collections.defaultdict(int)

        for uml_object in self.__uml_objects.values():
            # Add all objects, even when they aren't referenced, we need them
            # to properly calculate number of incoming refs in other objects.
            if not uml_object.name in ref_count:
                ref_count[uml_object.name] = 0

            if not uml_object.parent is None:
                if uml_object.parent in self.__uml_objects:
                    ref_count[uml_object.parent] += 1

        while True:
            leaves = filter(lambda n: ref_count[n] == 0, ref_count.keys())

            if not leaves:
                # No leaves left, either we reduced all of the nodes, or there
                # are circular references
                break
            else:
                # Delete all leaves, and update reference count of their parents
                for object in map(lambda key: self.__uml_objects[key], leaves):
                    if not object.parent is None:
                        if object.parent in ref_count:
                            ref_count[object.parent] -= 1
                    del ref_count[object.name]

        return ref_count.keys()

    def resolve(self):
        circular_refs = self.__find_circular_refs()

        if circular_refs:
            message = "circular references: " + ", ".join(circular_refs)
            uml_object = self.__uml_objects[circular_refs[0]]
            logging.getLogger("compiler").error(message, object=uml_object)
            return

        for uml_object in self.__uml_objects.values():
            self.__resolve_object(uml_object)

    def __resolve_object(self, uml_object):
        if uml_object.type != None: return

        if uml_object.parent == None:
            uml_object.type = uml_object.name
        else:
            if uml_object.parent in self.__uml_objects:
                parent = self.__uml_objects[uml_object.parent]
            else:
                logger = logging.getLogger("compiler")
                message = "non-existing object referenced: " + uml_object.parent
                logger.error(message, object=uml_object)
                return

            self.__resolve_object(parent)
            uml_object.type = parent.type

            properties = parent.properties.copy()
            properties.update(uml_object.properties)
            uml_object.properties = properties

            required = parent.required.copy()
            required.update(uml_object.required)
            uml_object.required = required

            allowed = parent.allowed.copy()
            allowed.update(uml_object.allowed)
            uml_object.allowed = allowed
