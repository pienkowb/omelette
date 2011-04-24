
class Logger:
    def __init__(self):
        self.has_errors = False

    def log_error(self, line_number, error):
        self.has_errors = True
        print str(line_number) + " " + error + "\n"

    def clear(self):
        self.has_errors = False

instance = Logger()
