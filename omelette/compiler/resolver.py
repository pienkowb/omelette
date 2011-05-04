from omelette.compiler import logging
import collections

class DependencyResolver(object):

    def __init__(self, uml_objects):
        self.__uml_objects = uml_objects

    def __find_circular_refs(self, objects):
        """
        this method performs topological sorting in order to check
        if there are any circular references in given array of umlobjects
        i.e. if one object is descendant and ancestor of another object

        Method returns set of objects involved in such relations (empty set
        if no circular references were found).
        """

        ref_count=collections.defaultdict(int)

        for uml_object in objects.values():
            if not uml_object.name in ref_count:
                ref_count[uml_object.name]=0
            if not uml_object.parent is None:
                ref_count[uml_object.parent]+=1

        while(1):
            leafs = filter(lambda n: ref_count[n] == 0, ref_count.keys())
            
            if len(leafs) < 1:
            # no leafs left, either we reduced all of the nodes, or there are
            # circular references
                break
            else:
            # delete all leafs, and update reference count of their parents
                for o in map(lambda key: objects[key], leafs):
                    if not o.parent is None:
                        ref_count[o.parent]-=1
                    del ref_count[o.name]

        return frozenset(ref_count.keys())

    def resolve(self):
        circular_refs = self.__find_circular_refs(self.__uml_objects)
        if circular_refs > frozenset([]):
            logging.getLogger('compiler').error("circular reference",
                    object_name=" ".join(circular_refs))
            return

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

