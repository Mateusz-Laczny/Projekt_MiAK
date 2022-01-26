from ply import lex

# Słowa kluczowe
reserved = {
    'fun': 'FUN',
    'var': 'VAR',
    'for': 'FOR',
    'while': 'WHILE',
    'do': 'DO',
    'if': 'IF',
    'then': 'THEN',
    'else': 'ELSE',
    'and': 'AND',
    'or': 'OR',
    'is': 'IS',
    'not': 'NOT',
    'return': 'RETURN',
    'true': 'TRUE',
    'false': 'FALSE',
    'none': 'NONE',
}

literals = ['+', '-', '*', '/', '{', '}', ',', ';', '(', ')', '[', ']', '=']

tokens = [
             'ID',
             'INT',
             'FLOAT',
             'STRING',
             'COMPARISON',
         ] + list(reserved.values())

t_COMPARISON = r'>= | <= | > | <'
# Linie zaczynające się od # oraz białe zanki są ignorowane
t_ignore_COMMENT = r'\#(.)*'
t_ignore_WHITESPACE = r'\s'


def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'ID')  # Check for reserved words
    if t.type == 'TRUE':
        t.value = True
    elif t.type == 'FALSE':
        t.value = False
    elif t.type == 'NONE':
        t.value = None
    return t


def t_FLOAT(t):
    r'\d\.(\d+)'
    t.value = float(t.value)
    return t


def t_INT(t):
    r'\d+'
    t.value = int(t.value)
    return t


def t_STRING(t):
    r'".*?"'
    t.value = t.value.strip('"')
    return t


def t_error(t):
    raise TypeError(f"Unknown text '{t.value}'")


lexer = lex.lex()


def tokenize(input_text):
    lex.input(input_text)
    tokens_list = []
    for token in iter(lex.token, None):
        tokens_list.append(token)
    return tokens_list
