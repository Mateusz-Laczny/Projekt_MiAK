import sys

from tokenizer import tokenize
from parser import parse
from interpreter_logic.interpreter import Interpreter, ReturnException

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Path to file not given")
    else:
        debug = False
        if len(sys.argv) == 3:
            if sys.argv[2] != '-d':
                print(f"Incorrect flag {sys.argv[2]}")
                sys.exit(1)
            else:
                debug = True
        filepath = sys.argv[1]
        interpreter = Interpreter()

        try:
            with open(filepath, mode='r', encoding='utf8') as file:
                input_file = file.read()
            interpreter.interpret(input_file, debug)
        except ReturnException:
            print('Error: Return statement outside of function')
        except Exception as e:
            print(e)
