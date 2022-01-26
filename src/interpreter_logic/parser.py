from interpreter_logic import ast_expression_nodes as expr_node
from interpreter_logic import ast_statement_nodes as stmt_node
from ply import yacc
from interpreter_logic.tokenizer import tokens
from logging_config import log

start = 'program'


def p_program(p):
    '''program : declarations'''
    p[0] = stmt_node.AstProgram(p[1])


def p_statement(p):
    '''statement : expression ';'
                 | if_statement
                 | while_statement
                 | for_statement
                 | block
                 | return_statement'''
    if not isinstance(p[1], list):
        p[0] = stmt_node.AstStatement(p[1])
    else:
        # Obiekt jest tworzony tutaj żeby móc wykorzystać regułę 'block'
        # również dal deklaracji funkcji
        p[0] = stmt_node.AstBlock(p[1])


def p_return(p):
    '''return_statement : RETURN expression ';'
                        | RETURN ';' '''
    if len(p) == 4:
        p[0] = stmt_node.AstReturn(p[1], p[2])
    else:
        p[0] = stmt_node.AstReturn(p[1], None)


def p_for_statement(p):
    '''for_statement : FOR variable_declaration expression ';' expression DO statement
                     | FOR statement expression ';' expression DO statement
                     | FOR variable_declaration ';' expression DO statement
                     | FOR statement ';' expression DO statement
                     | FOR variable_declaration ';' DO statement
                     | FOR statement expression ';' DO statement
                     | FOR ';' expression ';' expression DO statement
                     | FOR ';' expression ';' DO statement
                     | FOR ';' ';' expression DO statement
                     | FOR ';' ';' DO statement'''
    if p[2] == ';':
        initializer = None
    else:
        initializer = p[2]

    if p[3] == ';':
        condition = expr_node.AstLiteral(True)
    else:
        condition = p[3]

    if p[len(p) - 3] == ';':
        increment = None
    else:
        increment = p[len(p) - 3]

    body = p[len(p) - 1]
    if increment is not None:
        body = stmt_node.AstBlock([body, increment])

    body = stmt_node.AstWhile(condition, body)

    if initializer is not None:
        body = stmt_node.AstBlock([initializer, body])

    p[0] = body


def p_while_statement(p):
    '''while_statement : WHILE expression DO statement'''
    p[0] = stmt_node.AstWhile(p[2], p[4])


def p_if_statement(p):
    '''if_statement : IF expression THEN statement
                    | IF expression THEN statement ELSE statement'''
    if len(p) == 5:
        # Brak else
        p[0] = stmt_node.AstIf(p[2], p[4], None)
    else:
        # else występuje
        p[0] = stmt_node.AstIf(p[2], p[4], p[6])


# Bloki kodu ograniczone nawiasami wąsatymi
def p_block(p):
    '''block : '{' declarations '}' '''
    p[0] = p[2]


def p_declarations(p):
    '''declarations : declarations declaration
                    | declaration'''
    if len(p) == 3:
        if not isinstance(p[2], list):
            p[1].append(p[2])
            p[0] = p[1]
        else:
            p[0] = p[1] + p[2]
    else:
        p[0] = [p[1]]


def p_declaration(p):
    '''declaration : variable_declaration
                   | function_declaration
                   | statement'''
    p[0] = p[1]


def p_function_declaration(p):
    '''function_declaration : FUN function'''
    p[0] = p[2]


def p_function(p):
    '''function : ID '(' parameters_list ')' block
                | ID '(' ')' block'''
    if len(p) == 6:
        p[0] = stmt_node.AstFunctionDeclaration(p[1], p[3], p[5])
    else:
        p[0] = stmt_node.AstFunctionDeclaration(p[1], [], p[4])


def p_parameters_list(p):
    '''parameters_list : parameters_list ',' ID
                       | ID'''
    if len(p) == 4:
        if not isinstance(p[2], list):
            p[1].append(p[3])
            p[0] = p[1]
        else:
            p[0] = p[1] + p[2]
    else:
        p[0] = [p[1]]


def p_variable_declaration(p):
    '''variable_declaration : VAR ID '=' expression ';'
                            | VAR ID ';' '''
    if len(p) == 6:
        p[0] = stmt_node.AstStmtVariable(p[2], p[4])
    else:
        p[0] = stmt_node.AstStmtVariable(p[2], None)


# Number and logic expressions
def p_expression(p):
    '''expression : assignment'''
    p[0] = p[1]


def p_assignment(p):
    '''assignment : l_value_expression '=' assignment
                  | binary_logic_operator'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        if isinstance(p[1], expr_node.AstExprVariable):
            p[0] = expr_node.AstAssignment(p[1].name, p[3])
        elif isinstance(p[1], expr_node.AstSubscript):
            p[0] = expr_node.AstListAssignment(p[1].name, p[1].index, p[3])


def p_l_value_expression(p):
    '''l_value_expression : equality'''
    if not (isinstance(p[1], expr_node.AstExprVariable) or isinstance(p[1], expr_node.AstSubscript)):
        raise SyntaxError(f'Incorrect l_value: {p[1]}')

    p[0] = p[1]


def p_binary_logic_operator(p):
    '''binary_logic_operator : and_operator
                             | or_operator
                             | equality'''
    p[0] = p[1]


def p_and_operator(p):
    '''and_operator : and_operator AND equality
                    | equality'''
    if len(p) == 2:
        # Wyrażenie o wyższym priorytecie, nie operator logiczny
        p[0] = p[1]
    else:
        p[0] = expr_node.AstLogic(p[1], p[2], p[3])


def p_or_operator(p):
    '''or_operator : or_operator OR equality
                    | equality'''
    if len(p) == 2:
        # Wyrażenie o wyższym priorytecie, nie operator logiczny
        p[0] = p[1]
    else:
        p[0] = expr_node.AstLogic(p[1], p[2], p[3])


# is and is not
def p_equality(p):
    '''equality : expression IS comparison
                | expression IS NOT comparison
                | comparison'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        if p[2] == 'is' and p[3] == 'not':
            p[0] = expr_node.AstBinary(p[1], f'{p[2]} {p[3]}', p[4])
        else:
            p[0] = expr_node.AstBinary(p[1], p[2], p[3])


# >, >=, <, <=
def p_comparison(p):
    '''comparison : comparison COMPARISON term
                  | term'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = expr_node.AstBinary(p[1], p[2], p[3])


# +, -
def p_term(p):
    '''term : term '-' factor
            | term '+' factor
            | factor'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = expr_node.AstBinary(p[1], p[2], p[3])


# /, *
def p_factor(p):
    '''factor : factor '/' unary
              | factor '*' unary
              | unary'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = expr_node.AstBinary(p[1], p[2], p[3])


# not, -
def p_unary(p):
    '''unary : NOT unary
             | '-' unary
             | call_or_subscript'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = expr_node.AstUnary(p[1], p[2])


def p_call_or_subscript(p):
    '''call_or_subscript : function_call
                         | ID '[' expression ']'
                         | primary'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = expr_node.AstSubscript(p[1], p[3])


def p_function_call(p):
    '''function_call : ID '(' arguments ')' '''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = expr_node.AstCall(p[1], p[3])


def p_arguments(p):
    '''arguments : arguments ',' expression
                 | expression'''
    if len(p) == 4:
        if not isinstance(p[3], list):
            p[1].append(p[3])
            p[0] = p[1]
        else:
            p[0] = p[1] + p[3]
    else:
        p[0] = [p[1]]


# literals and parenthesized expressions
def p_primary(p):
    '''primary : number_literal
               | boolean_literal
               | STRING
               | NONE
               | '(' expression ')'
               | ID
               | list_literal'''
    if p.slice[1].type == 'ID':
        p[0] = expr_node.AstExprVariable(p[1])
    else:
        if len(p) == 4:
            p[0] = expr_node.AstGrouping(p[2])
        else:
            if isinstance(p[1], expr_node.AstList):
                p[0] = p[1]
            else:
                p[0] = expr_node.AstLiteral(p[1])


def p_list_literal(p):
    '''list_literal : '[' arguments ']'
                    | '[' ']' '''
    if len(p) == 4:
        p[0] = expr_node.AstList(p[2])
    else:
        p[0] = expr_node.AstList([])


def p_number_literal(p):
    '''number_literal : INT
                      | FLOAT'''
    p[0] = p[1]


def p_boolean_literal(p):
    '''boolean_literal : TRUE
                      | FALSE'''
    p[0] = p[1]


def p_error(p):
    if p is None:
        print('Error: Unexpected EOF')
    else:
        while True:
            token = parser.token()
            if token is None:
                break
            elif token.type == ';':
                parser.token()
                break
        parser.restart()


parser = yacc.yacc()


def parse(starting_symbol, debug):
    return parser.parse(starting_symbol, debug=debug)
