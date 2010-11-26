class _CodeObject(object):
    def __init__(self, position, header):
        self.position = position
        self.lines = [header]
        self.modified = True

    def __cmp__(self, other):
        return cmp(self.position, other.position)


def _before(position):
    return lambda o: o.position <= position

def _after(position):
    return lambda o: o.position >= position


def _is_header(line):
    return line.strip() and all([char not in line for char in ":+~#-"])


class Code(object):
    def __init__(self):
        self.__objects = [_CodeObject(-1, "")]

    def objects(self, condition=None):
        return filter(condition, self.__objects)

    def insert_line(self, number, line):
        for object in self.objects(_after(number)):
            object.position += 1

        previous = self.objects(_before(number))[-1]
        position = number - previous.position

        if _is_header(line):
            object = _CodeObject(number, line)

            object.lines.extend(previous.lines[position:])
            del previous.lines[position:]

            self.__objects.append(object)
            self.__objects.sort()
        else:
            previous.lines.insert(position, line)

    def remove_line(self, number):
        object = self.objects(_before(number))[-1]
        del object.lines[number - object.position]

        if object.position == number:
            previous = self.objects(_before(number))[-2]
            previous.lines.extend(object.lines)

            self.__objects.remove(object)

        for object in self.objects(_after(number)):
            object.position -= 1
