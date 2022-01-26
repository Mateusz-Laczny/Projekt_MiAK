
class Print:
    def __init__(self):
        self.arity = None

    def call(self, _interpreter, arguments):
        for argument in arguments:
            print(argument)
