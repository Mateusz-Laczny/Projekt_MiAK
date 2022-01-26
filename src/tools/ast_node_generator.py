import sys


def generate_ast_classes_file(filename, generated_file):
    with open(filename, 'r') as file:
        with open(f'D:/Studia/MIAK/atena/src/interpreter_logic/{generated_file}.py', 'w') as output:
            for line in file:
                line = line.strip('\n')
                line = line.replace(' ', '')
                name, definition = line.split(':')
                name_with_underscores = name
                name = name.split('_')
                for i, part in enumerate(name):
                    name[i] = part.capitalize()
                name = ''.join(name)
                output.write(f'class Ast{name}:\n')
                fields_list = definition.split(',')
                parameters = ''
                for i, field in enumerate(fields_list):
                    if i == len(fields_list) - 1:
                        parameters += field
                    else:
                        parameters += field + ', '
                output.write(f'    def __init__(self, {parameters}):\n')
                for field in fields_list:
                    output.write(f'        self.{field} = {field}\n')

                output.write('\n')

                output.write('    def accept(self, visitor):\n')
                output.write(f'        return visitor.visit_{name_with_underscores.lower()}(self)\n')

                output.write('\n')

                output.write('    def __str__(self):\n')
                str_representation = "f'"
                for field in fields_list:
                    str_representation += '{self.' + field + '} '
                str_representation = str_representation.strip()
                str_representation += "'"
                output.write(f'        return {str_representation}\n')
                output.write('\n\n')


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Wrong number of arguments")
    else:
        generate_ast_classes_file(sys.argv[1], sys.argv[2])
