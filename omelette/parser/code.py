class _CodeObject:
    def __init__(self, position, header):
        self.position = position
        self.lines = [header]
        self.modified = True

    def __cmp__(self, other):
        return cmp(self.position, other.position)


def _is_header(line):
    return line.strip() and all([line.find(c) == -1 for c in "~#:-+"])


class Code:
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
        pass

    def remove_line(self, number):
        pass
