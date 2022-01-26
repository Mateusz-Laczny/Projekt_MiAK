class AstBinary:
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

    def accept(self, visitor):
        return visitor.visit_binary(self)

    def __str__(self):
        return f'{self.left} {self.operator} {self.right}'


class AstGrouping:
    def __init__(self, inside_expression):
        self.inside_expression = inside_expression

    def accept(self, visitor):
        return visitor.visit_grouping(self)

    def __str__(self):
        return f'{self.inside_expression}'


class AstLiteral:
    def __init__(self, value):
        self.value = value

    def accept(self, visitor):
        return visitor.visit_literal(self)

    def __str__(self):
        return f'{self.value}'


class AstUnary:
    def __init__(self, operator, right):
        self.operator = operator
        self.right = right

    def accept(self, visitor):
        return visitor.visit_unary(self)

    def __str__(self):
        return f'{self.operator} {self.right}'


class AstExprVariable:
    def __init__(self, name):
        self.name = name

    def accept(self, visitor):
        return visitor.visit_expr_variable(self)

    def __str__(self):
        return f'{self.name}'


class AstAssignment:
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def accept(self, visitor):
        return visitor.visit_assignment(self)

    def __str__(self):
        return f'{self.name} {self.value}'


class AstListAssignment:
    def __init__(self, name, index, value):
        self.name = name
        self.index = index
        self.value = value

    def accept(self, visitor):
        return visitor.visit_list_assignment(self)

    def __str__(self):
        return f'{self.name} {self.index} {self.value}'


class AstLogic:
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

    def accept(self, visitor):
        return visitor.visit_logic(self)

    def __str__(self):
        return f'{self.left} {self.operator} {self.right}'


class AstCall:
    def __init__(self, name, arguments):
        self.name = name
        self.arguments = arguments

    def accept(self, visitor):
        return visitor.visit_call(self)

    def __str__(self):
        return f'{self.name} {self.arguments}'


class AstSubscript:
    def __init__(self, name, index):
        self.name = name
        self.index = index

    def accept(self, visitor):
        return visitor.visit_subscript(self)

    def __str__(self):
        return f'{self.name} {self.index}'


class AstList:
    def __init__(self, values):
        self.values = values

    def accept(self, visitor):
        return visitor.visit_list(self)

    def __str__(self):
        return f'{self.values}'


