class _CodeObject(object):
    def __init__(self, position, header):
        self.position = position
        self.lines = [header]
        self.modified = True

    def __cmp__(self, other):
        return cmp(self.position, other.position)


def _is_header(line):
    return line.strip() and all([line.find(char) == -1 for char in "~#:-+"])


class Code(object):
    def __init__(self):
        self.__objects = []

    def objects(self):
        return sorted(self.__objects)

    def __objects_before(self, position):
        return [o for o in self.objects() if o.position < position]

    def __objects_after(self, position):
        return [o for o in self.objects() if o.position >= position]


    def insert_line(self, number, line):
        for object in self.__objects_after(number):
            object.position += 1

        if _is_header(line):
            self.__objects.append(_CodeObject(number, line))
        else:
            object = self.__objects_before(number)[-1] # last predecessor
            object.lines.insert(number - object.position, line)

    def update_line(self, number, line):
        object = self.__objects_before(number)[-1]
        object.lines[number - object.position] = line

    def remove_line(self, number):
        object = self.__objects_before(number)[-1]
        del object.lines[number - object.position]

        for object in self.__objects_after(number):
            object.position -= 1
