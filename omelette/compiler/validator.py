class Validator(object):

    def __init__(self, uml_object):
        self.uml_object = uml_object
        self.required_left = uml_object.required.keys()

    def validate_type(self, name, types):
        value, type = self.uml_object.properties[name]

        if not isinstance(types[name], list):
            return type == types[name]
        else:
            return type == "CONSTANT" and value in types[name]

    def validate_property(self, name):
        required = self.uml_object.required
        allowed = self.uml_object.allowed

        if name in required:
            self.required_left.remove(name)
            return self.validate_type(name, required)
        elif name in allowed:
            return self.validate_type(name, allowed)
        else:
            return False

    def validate(self):
        are_valid = map(self.validate_property, self.uml_object.properties)
        return all(are_valid) and len(self.required_left) == 0
