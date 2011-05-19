_loggers = {}

def getLogger(name):
    if not name in _loggers:
        _loggers[name] = Logger()
    return _loggers[name]

class Logger:

    def __init__(self):
        self.events = []

    def info(self, msg, line_number=None, object=None):
        e = Event(msg, "INFO", line_number, object)
        self.events.append(e)

    def warning(self, msg, line_number=None, object=None):
        e = Event(msg, "WARNING", line_number, object)
        self.events.append(e)

    def error(self, msg, line_number=None, object=None):
        e = Event(msg, "ERROR", line_number, object)
        self.events.append(e)

    def critical(self, msg, line_number=None, object=None):
        e = Event(msg, "CRITICAL", line_number, object)
        self.events.append(e)

    def flush(self):
        self.events = []

    def is_empty(self):
        return len(self.events) == 0

class Event:
    def __init__(self, msg, level, line_number, object):
        self.msg = msg
        self.level = level
        self.line_number = line_number
        self.object = object

    def __str__(self):
        value = self.level
        if not self.line_number is None:
            value += " " + str(self.line_number)
        elif not self.object is None:
            value += " " + self.object.name
        value += ": " + self.msg 
        return value

