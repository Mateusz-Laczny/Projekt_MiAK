import globals

from interpreter_logic.environment import Environment
from interpreter_logic.function import Function, ReturnException
from interpreter_logic.parser import parse
from logging_config import log

TYPE_NAMES = {
    int: 'int',
    float: 'float',
    bool: 'bool',
    str: 'string',
    list: 'list',
    None: 'none'
}

MAX_ARGUMENTS_NUM = 255


class Interpreter:
    TYPES_ADDITION = [int, float, bool, str]
    TYPES_SUBTRACTION = [int, float, bool]
    TYPES_UNARY_MINUS = TYPES_SUBTRACTION
    TYPES_MULTIPLICATION = TYPES_SUBTRACTION
    TYPES_DIVISION = TYPES_SUBTRACTION
    TYPES_COMPARISON = TYPES_SUBTRACTION
    TYPES_NOT = TYPES_SUBTRACTION

    def __init__(self):
        self.globals = Environment()
        self.globals.define('print', globals.Print())
        self.environment = self.globals

    def interpret(self, interpreter_input, debug=False):
        parsed_input = parse(interpreter_input, debug)
        self.execute(parsed_input)

    def evaluate(self, expression):
        return expression.accept(self)

    def execute(self, statement):
        statement.accept(self)

    def execute_block(self, statements, new_environment):
        previous_environment = self.environment
        # Zmiana środowiska jest w bloku try, tak aby środowisko
        # było zawsze ustawione na poprawny obiekt
        try:
            self.environment = new_environment
            for statement in statements:
                self.execute(statement)
        finally:
            self.environment = previous_environment

    def are_equal(self, fist_value, second_value):
        if type(fist_value) is not type(second_value):
            return False
        else:
            # Druga wartość ma ten sam typ
            values_type = type(fist_value)
            if values_type is int or values_type is float or values_type is str or values_type is bool:
                # Dla str - długość musi się zgadzać,
                # tak jak odpowiadające sobie elementy na tych samych indeksach
                return fist_value == second_value
            elif values_type == list:
                if len(fist_value) != len(second_value):
                    return False
                else:
                    for elem1, elem2 in enumerate(zip(fist_value, second_value)):
                        if not self.are_equal(elem1, elem2):
                            return False
                    return True

    def visit_literal(self, expression):
        return expression.value

    def visit_list(self, list_expression):
        return [self.evaluate(elem) for elem in list_expression.values]

    def visit_grouping(self, expression):
        return self.evaluate(expression.inside_expression)

    def visit_unary(self, expression):
        value = self.evaluate(expression.right)
        value_type = type(value)
        operator = expression.operator

        if operator == '-':
            if value_type not in self.TYPES_UNARY_MINUS:
                raise TypeError(f"Unsupported operator '{operator}' for type '{TYPE_NAMES[value_type]}'")
            return -value
        elif operator == 'not':
            if value_type not in self.TYPES_NOT:
                raise TypeError(f"Unsupported operator '{operator}' for type '{TYPE_NAMES[value_type]}'")
            return not bool(value)

    def visit_binary(self, expression):
        left_side_value = self.evaluate(expression.left)
        right_side_value = self.evaluate(expression.right)
        left_side_type = type(left_side_value)
        right_side_type = type(right_side_value)
        operator = expression.operator

        if operator == '-':
            # TODO - MODULO, INTEGER DIVISION
            if left_side_type not in self.TYPES_SUBTRACTION or right_side_type not in self.TYPES_SUBTRACTION:
                raise TypeError(f"Unsupported operator '{operator}' for types '{TYPE_NAMES[left_side_type]}' and "
                                f"'{TYPE_NAMES[right_side_type]}'")
            return left_side_value - right_side_value
        elif operator == '+':
            if left_side_type not in self.TYPES_ADDITION or right_side_type not in self.TYPES_ADDITION:
                raise TypeError(f"Unsupported operator '{operator}' for types '{TYPE_NAMES[left_side_type]}' and "
                                f"'{TYPE_NAMES[right_side_type]}'")
            return left_side_value + right_side_value
        elif operator == '*':
            if left_side_type not in self.TYPES_MULTIPLICATION or right_side_type not in self.TYPES_MULTIPLICATION:
                raise TypeError(f"Unsupported operator '{operator}' for types '{TYPE_NAMES[left_side_type]}' and "
                                f"'{TYPE_NAMES[right_side_type]}'")
            return left_side_value * right_side_value
        elif operator == '/':
            if left_side_type not in self.TYPES_DIVISION or right_side_type not in self.TYPES_DIVISION:
                raise TypeError(f"Unsupported operator '{operator}' for types '{TYPE_NAMES[left_side_type]}' and "
                                f"'{TYPE_NAMES[right_side_type]}'")
            return left_side_value / right_side_value

        if operator == 'is':
            return self.are_equal(left_side_value, right_side_value)
        elif operator == 'is not':
            return not self.are_equal(left_side_value, right_side_value)

        if left_side_type not in self.TYPES_COMPARISON or right_side_type not in self.TYPES_COMPARISON:
            raise TypeError(f"Unsupported operator '{operator}' for types '{TYPE_NAMES[left_side_type]}' and "
                            f"'{TYPE_NAMES[right_side_type]}'")

        if operator == '>':
            return left_side_value > right_side_value
        elif operator == '>=':
            return left_side_value >= right_side_value
        elif operator == '<':
            return left_side_value < right_side_value
        elif operator == '<=':
            return left_side_value <= right_side_value

    def visit_logic(self, expression):
        left_value = self.evaluate(expression.left)
        if expression.operator == 'and':
            if not left_value:
                return left_value
        elif expression.operator == 'or':
            if left_value:
                return left_value

        return self.evaluate(expression.right)

    def visit_program(self, program):
        for statement in program.statements:
            self.execute(statement)

    def visit_statement(self, statement):
        self.evaluate(statement.expression)

    def visit_stmt_variable(self, statement):
        if statement.initializer is None:
            self.environment.define(statement.name)
        else:
            value = self.evaluate(statement.initializer)
            self.environment.define(statement.name, value)

    def visit_expr_variable(self, variable):
        return self.environment.get(variable.name)

    def visit_assignment(self, expression):
        value = self.evaluate(expression.value)
        self.environment.assign(expression.name, value)
        return value

    def visit_list_assignment(self, expression):
        value = self.evaluate(expression.value)
        index = self.evaluate(expression.index)
        self.environment.assign(expression.name, value, index)
        return value

    def visit_block(self, block):
        self.execute_block(block.statements, Environment(self.environment))

    def visit_if(self, if_statement):
        if self.evaluate(if_statement.condition):
            self.execute(if_statement.then_branch)
        else:
            if if_statement.else_branch is not None:
                self.execute(if_statement.else_branch)

    def visit_while(self, while_statement):
        while self.evaluate(while_statement.condition):
            self.execute(while_statement.body)

    def visit_function_declaration(self, declaration):
        function_object = Function(declaration)
        self.environment.define(declaration.name, function_object)

    def visit_call(self, call_expression):
        function_object = self.environment.get(call_expression.name)
        arguments = [self.evaluate(argument) for argument in call_expression.arguments]
        try:
            # Arity = None - funkcja przyjmuje zmienną liczbę argumentów
            if function_object.arity is not None and len(arguments) != function_object.arity:
                log.error('Error: Function arity mismatch')
                raise RuntimeError(f'Call with {len(arguments)} arguments to a function "{call_expression.name}" '
                                   f'with arity {function_object.arity}')

            return function_object.call(self, arguments)
        except NotImplementedError:
            log.error('Error: Called object not callable')
            raise RuntimeError('Object is not callable')

    def visit_subscript(self, subscript_expression):
        try:
            index = self.evaluate(subscript_expression.index)
            index = int(index)
            list_values = self.environment.get(subscript_expression.name)
            if index < 0 or index >= len(list_values):
                log.error('Error: Index error while interpreting subscript')
                raise IndexError(f"List index out of range")
            return list_values[index]
        except TypeError:
            log.error('Error: Type error while interpreting subscript')
            raise TypeError('Non - list objects are not subscritable')
        except RuntimeError as e:
            log.error(f'Error: Runtime error while interpreting subscript - {e}')
            raise e

    def visit_return(self, return_statement):
        if return_statement.value is not None:
            return_value = self.evaluate(return_statement.value)
        else:
            return_value = None

        raise ReturnException(return_value)

