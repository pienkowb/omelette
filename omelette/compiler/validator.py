from omelette.compiler import logging

class Validator(object):

    def __init__(self, uml_objects):
        self.__uml_objects = uml_objects

    def __log_error(self, message):
        logger = logging.getLogger("compiler")
        logger.error(message, object=self.__uml_object)

    def __validate_reference(self, reference):
        if reference not in self.__uml_objects.keys():
            self.__log_error("non-existing object referenced: " + reference)

    def __validate_type(self, name, types):
        value, type = self.__uml_object.properties[name]
        message = "invalid type of '%s' property, expected %s"

        if not isinstance(types[name], list):
            if type != types[name]:
                self.__log_error(message % (name, types[name]))
            elif type == "OBJECT":
                self.__validate_reference(value)
        else:
            if value not in types[name]:
                expected = "[" + ", ".join(types[name]) + "]"
                self.__log_error(message % (name, expected))

    def __validate_property(self, name):
        required = self.__uml_object.required
        allowed = self.__uml_object.allowed

        if name in required:
            self.__required_left.remove(name)
            self.__validate_type(name, required)
        elif name in allowed:
            self.__validate_type(name, allowed)
        else:
            self.__log_error("property '%s' not allowed" % name)

    def validate(self):
        for uml_object in self.__uml_objects.values():
            self.__uml_object = uml_object
            self.__required_left = uml_object.required.keys()

            for name in self.__uml_object.properties:
                self.__validate_property(name)

            for name in self.__required_left:
                self.__log_error("required property '%s' not defined" % name)
