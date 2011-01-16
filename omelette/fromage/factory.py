import inspect

def _import(name):
    module = __import__(name)
    components = name.split(".")

    for component in components[1:]:
        module = getattr(module, component)

    return module


class DrawableFactory:
    @staticmethod
    def create(diagram, uml_object):
        module = _import("omelette.fromage.modules." + diagram)

        name = "Drawable" + uml_object.type.capitalize()
        drawable = getattr(module, name, None)

        if inspect.isclass(drawable):
            return drawable(uml_object)
