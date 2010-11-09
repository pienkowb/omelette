class CodeObject:
    def __init__(self, position, lines=[]):
        self.__position = position
        self.__lines = lines
        self.__modified = True

    def __cmp__(self, other):
        return cmp(self.__position, other.__position)


class Code:
    def __init__(self):
        self.__objects = []

    def insert_line(self, number, line):
        pass

    def update_line(self, number, line):
        pass

    def remove_line(self, number):
        pass
