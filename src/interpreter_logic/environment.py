class Environment:
    def __init__(self, enclosing=None):
        self.enclosing = enclosing
        self.variables = dict()

    def define(self, name, value=None):
        if name in self.variables:
            raise SyntaxError(f'Redeclaration of variable {name}')

        self.variables[name] = value

    def get(self, name):
        if name in self.variables:
            return self.variables[name]
        else:
            # Jesteśmy w najwyższym bloku (globalnym)
            if self.enclosing is None:
                raise RuntimeError(f'Undefined variable: {name}')
            else:
                return self.enclosing.get(name)

    def assign(self, name, value, index=None):
        if name in self.variables.keys():
            if index is not None:
                try:
                    if index < 0 or index >= len(self.variables[name]):
                        raise IndexError('List index out of range')

                    self.variables[name][index] = value
                except TypeError as e:
                    print(e)
                    raise TypeError("Can't use subscript on a nonlist object")
            else:
                self.variables[name] = value
        else:
            # Jesteśmy w najwyższym bloku (globalnym)
            if self.enclosing is None:
                raise RuntimeError(f'Undefined variable: {name}')
            else:
                self.enclosing.assign(name, value, index)

