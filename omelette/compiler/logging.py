_loggers = {}

def getLogger(name):
    if not name in _loggers:
        _loggers[name] = Logger()
    return _loggers[name]

class Logger:

    def __init__(self):
        self.events = []

    def info(self, msg, object=None):
        e = Event(msg, "INFO", object)
        self.events.append(e)

    def warning(self, msg, object=None):
        e = Event(msg, "WARNING", object)
        self.events.append(e)

    def error(self, msg, object=None):
        e = Event(msg, "ERROR", object)
        self.events.append(e)

    def critical(self, msg, object=None):
        e = Event(msg, "CRITICAL", object)
        self.events.append(e)

    def flush(self):
        self.events = []

    def is_empty(self):
        return len(self.events) == 0

class Event:
    def __init__(self, msg, level, object):
        self.msg = msg
        self.level = level
        if not object is None:
            self.object = object.name
            if not object.code_object is None:
                self.line_number = object.code_object.position
        else:
            self.line_number = -1


    def __str__(self):
        value = self.level
        if not self.line_number is None:
            value += ":" + str(self.line_number)
        elif not self.object is None:
            value += " " + self.object.name
        value += ": " + self.msg 
        return value

