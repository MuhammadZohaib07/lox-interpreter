TAB = '    '


class GenerateAst:
    def __init__(self):
        # Define the structure of expressions and statements
        self.expressions = {
            "Assign": ('name', 'value'),
            "Binary": ('left', 'operator', 'right'),
            "Call": ('callee', 'paren', 'arguments'),
            "Get": ('object', 'name'),
            "Grouping": ('expr'),
            "Literal": ('value'),
            "Logical": ('left', 'operator', 'right'),
            "Set": ('object', 'name', 'value'),
            "Super": ('keyword', 'method'),
            "This": ('keyword'),
            "Unary": ('operator', 'right'),
            "Variable": ('name')
        }
        self.statements = {
            "Block": ('stmts'),
            "Class": ('name', 'super_class', 'methods'),
            "Expression": ('expr'),
            "Function": ('name', 'params', 'body'),
            "If": ('condition', 'then_branch', 'else_branch'),
            "Print": ('expr'),
            "Return": ('keyword', 'value'),
            "Var": ('name', 'initializer'),
            "While": ('condition', 'body')
        }

    def main(self):
        # Generate the AST classes for expressions and statements
        self.define_ast("Expr", self.expressions)
        self.define_ast("Stmt", self.statements)

    def define_ast(self, baseName, types):
        # Create a new file for the AST base class and its subclasses
        path = "../src/" + baseName + ".py"
        file = open(path, "w")
        file.write('from abc import ABC, abstractmethod\n')
        self.define_visitor(file, baseName, types)
        file.write(f'class {baseName}:\n')
        file.write(f'{TAB}')
        file.write(f'@abstractmethod\n')
        file.write(f'{TAB}def __init__(self):\n')
        file.write(f'{TAB * 2}')
        file.write('pass\n')
        for className, fields in types.items():
            file.write('\n')
            self.define_type(file, baseName, className, fields)
        file.write('\n')

    def define_type(self, file, baseName, className, fields):
        # Define a subclass for each type of expression or statement
        file.write(f'class {className}({baseName}):\n')
        file.write(f'{TAB}')
        if type(fields) is not tuple:
            file.write(f'def __init__(self, {fields}):\n')
        else:
            file.write(f'def __init__(self, {", ".join(fields)}):\n')
        if type(fields) is not tuple:
            file.write(f'{TAB * 2}self.{fields} = {fields}\n')
        else:
            for field in fields:
                att = field.split(":")[0]
                file.write(f'{TAB * 2}self.{att} = {att}\n')
        file.write('\n')
        file.write(f'{TAB}def accept(self, visitor):\n')
        file.write(f'{TAB * 2}return visitor.visit_{className.lower()}_{baseName.lower()}(self)\n')

    def define_visitor(self, file, baseName, types):
        # Define the visitor interface for the AST base class
        visitor = f'{baseName}Visitor'
        file.write(f'\n')
        file.write(f'class {visitor}(ABC):\n')
        for type in types:
            file.write(f'{TAB}@abstractmethod\n')
            file.write(f'{TAB}def visit_{type.lower()}_{baseName.lower()}(self, expr):\n')
            file.write(f'{TAB * 2}pass \n')
        file.write(f'\n')


# Sanity check to generate the AST classes
g = GenerateAst()
g.main()
