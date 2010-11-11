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

    def __str__(self):
        return "\n".join(["\n".join(o.lines) for o in self.objects()])


    def objects(self):
        return sorted(self.__objects)

    def __object_before(self, position):
        objects = [o for o in self.objects() if o.position < position]
        return objects[-1] if objects else None

    def __objects_after(self, position):
        return [o for o in self.objects() if o.position >= position]


    def insert_line(self, number, line):
        for object in self.__objects_after(number):
            object.position += 1

        previous = self.__object_before(number) # last predecessor

        if _is_header(line):
            object = _CodeObject(number, line)
            self.__objects.append(object)

            if previous:
                object.lines.extend(previous.lines[number:])
                del previous.lines[number:]
        else:
            previous.lines.insert(number - previous.position, line)

    def update_line(self, number, line):
        object = self.__object_before(number)
        object.lines[number - object.position] = line

    def remove_line(self, number):
        object = self.__object_before(number)
        del object.lines[number - object.position]

        for object in self.__objects_after(number):
            object.position -= 1
