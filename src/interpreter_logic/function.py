from interpreter_logic.environment import Environment


# Wyjątek używany do zwracania danych z funkcji
class ReturnException(Exception):
    def __init__(self, value):
        super().__init__()
        self.value = value


class Function:
    def __init__(self, declaration):
        self.declaration = declaration
        self.arity = len(declaration.params)

    def call(self, interpreter, arguments):
        function_environment = Environment(interpreter.globals)
        for param, argument in zip(self.declaration.params, arguments):
            function_environment.define(param, argument)

        try:
            interpreter.execute_block(self.declaration.body, function_environment)
        except ReturnException as function_return:
            return function_return.value
