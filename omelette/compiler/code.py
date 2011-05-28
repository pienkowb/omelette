import os.path
from pyparsing import StringEnd, ParseException
from omelette.compiler.lexer import Lexer

class _CodeObject(object):
    """Class containing the code of a single object."""

    def __init__(self, position, header):
        self.position = position
        self.lines = [header]
        self.modified = True

    def insert_line(self, number, line):
        self.lines.insert(number - self.position, line)
        self.modified = True

    def update_line(self, number, line):
        self.lines[number - self.position] = line
        self.modified = True

    def remove_line(self, number):
        del self.lines[number - self.position]
        self.modified = True

    def transfer_lines(self, other, number):
        position = number - self.position

        if position in range(len(self.lines)):
            other.lines.extend(self.lines[position:])
            del self.lines[position:]

            self.modified = other.modified = True

    def is_empty(self):
        return all(map(lambda line: not line.strip(), self.lines))

    def __cmp__(self, other):
        return cmp(self.position, other.position)

    def __str__(self):
        return  "\n".join(self.lines)


def _before(position):
    return lambda o: o.position <= position

def _after(position):
    return lambda o: o.position >= position


class Code(object):
    """Class representing the code divided into objects."""

    def __init__(self, code=""):
        self.__objects = [_CodeObject(-1, "")]
        self.__lexer = Lexer()

        lines = code.split("\n") if code else []

        for number, line in enumerate(lines):
            self.insert_line(number, line)

    def objects(self, condition=None):
        return filter(condition, self.__objects)

    def __is_header(self, line):
        try:
            header = self.__lexer["header"] + StringEnd()
            header.parseString(line)
            return True
        except ParseException:
            return False

    def __shift(self, position, offset):
        for object in self.objects(_after(position)):
            object.position += offset

    def insert_line(self, number, line):
        self.__shift(number, 1)

        if self.__is_header(line):
            object = _CodeObject(number, line)

            previous = self.objects(_before(number))[-1]
            previous.transfer_lines(object, number)

            self.__objects.append(object)
            self.__objects.sort()
        else:
            object = self.objects(_before(number))[-1]
            object.insert_line(number, line)

    def update_line(self, number, line):
        object = self.objects(_before(number))[-1]
        updated_line = object.lines[number - object.position]

        if self.__is_header(line) == self.__is_header(updated_line):
            object.update_line(number, line)
        else:
            self.remove_line(number)
            self.insert_line(number, line)

    def remove_line(self, number):
        object = self.objects(_before(number))[-1]
        object.remove_line(number)

        if object.position == number:
            previous = self.objects(_before(number))[-2]
            object.transfer_lines(previous, number)

            self.__objects.remove(object)

        self.__shift(number, -1)


class Library(Code):
    """Class reading the code from the specified file."""

    def __init__(self, path):
        with open(path) as library:
            Code.__init__(self, library.read())

    @staticmethod
    def load_libraries():
        script_path = os.path.dirname(os.path.realpath(__file__))
        lib_path = os.path.normcase("../../lib")
        lib_directory = os.path.join(script_path, lib_path)

        libraries = []

        for name in os.listdir(lib_directory):
            path = os.path.join(lib_directory, name)
            basename, extension = os.path.splitext(path)
            if extension != '.uml' : continue
            if not os.path.isdir(path):
                libraries.append(Library(path))

        return libraries
