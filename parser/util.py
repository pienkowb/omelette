class UMLObject(object):
    '''
    Class representing UML diagram object.
    '''
    
    visibilities_order = ["+","#","-"]
    

    def __init__(self):
        self.__methods = []
        self.__attributes = []
        self.__properties = {}
        
    def __setitem__(self, key, value):
        self.__properties[key] = value
        
    def __getitem__(self, key):
        return self.__properties[key]

    def add_method(self, method):
        self.__methods.append(method)

    def add_attribute(self, property):
        self.__attributes.append(property)
        
    def methods(self):
        self.__visibility_sort(self.__methods)
        return self.__methods
        
    def attributes(self):
        self.__visibility_sort(self.__attributes)
        return self.__attributes
    
    def __visibility_sort(self, list):
        
        get_name = lambda x: x[1:]
        get_visibility = lambda x: x[0]
        
        #taking advantage of sort() stability
        list.sort(key=get_name)
        list.sort(key=get_visibility, cmp=self.__cmp_visibilities)
            
    def __cmp_visibilities(self, x, y):
        return  UMLObject.visibilities_order.index(x) - \
                UMLObject.visibilities_order.index(y)