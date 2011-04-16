class Validator(object):

    def validate(self, uml_object):
        required = uml_object.required.keys()
        is_valid = True

        for name in uml_object.properties:
            if name in uml_object.required:
                required.remove(name)
            elif name in uml_object.allowed:
                pass
            else:
                is_valid = False

        return is_valid and len(required) == 0
