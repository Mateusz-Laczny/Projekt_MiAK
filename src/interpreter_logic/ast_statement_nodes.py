class AstProgram:
    def __init__(self, statements):
        self.statements = statements

    def accept(self, visitor):
        return visitor.visit_program(self)

    def __str__(self):
        return f'{self.statements}'


class AstStatements:
    def __init__(self, statements):
        self.statements = statements

    def accept(self, visitor):
        return visitor.visit_statements(self)

    def __str__(self):
        return f'{self.statements}'


class AstStatement:
    def __init__(self, expression):
        self.expression = expression

    def accept(self, visitor):
        return visitor.visit_statement(self)

    def __str__(self):
        return f'{self.expression}'


class AstStmtVariable:
    def __init__(self, name, initializer):
        self.name = name
        self.initializer = initializer

    def accept(self, visitor):
        return visitor.visit_stmt_variable(self)

    def __str__(self):
        return f'{self.name} {self.initializer}'


class AstBlock:
    def __init__(self, statements):
        self.statements = statements

    def accept(self, visitor):
        return visitor.visit_block(self)

    def __str__(self):
        return f'{self.statements}'


class AstIf:
    def __init__(self, condition, then_branch, else_branch):
        self.condition = condition
        self.then_branch = then_branch
        self.else_branch = else_branch

    def accept(self, visitor):
        return visitor.visit_if(self)

    def __str__(self):
        return f'{self.condition} {self.then_branch} {self.else_branch}'


class AstWhile:
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

    def accept(self, visitor):
        return visitor.visit_while(self)

    def __str__(self):
        return f'{self.condition} {self.body}'


class AstFor:
    def __init__(self, initializer, end, increment, body):
        self.initializer = initializer
        self.end = end
        self.increment = increment
        self.body = body

    def accept(self, visitor):
        return visitor.visit_for(self)

    def __str__(self):
        return f'{self.initializer} {self.end} {self.increment} {self.body}'


class AstFunctionDeclaration:
    def __init__(self, name, params, body):
        self.name = name
        self.params = params
        self.body = body

    def accept(self, visitor):
        return visitor.visit_function_declaration(self)

    def __str__(self):
        return f'{self.name} {self.params} {self.body}'


class AstReturn:
    def __init__(self, keyword, value):
        self.keyword = keyword
        self.value = value

    def accept(self, visitor):
        return visitor.visit_return(self)

    def __str__(self):
        return f'{self.keyword} {self.value}'


