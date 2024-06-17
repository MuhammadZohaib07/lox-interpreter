README

Directory Structure:
The project is organized as follows:


project_root/
├── src/
│ ├── ast_printer.py
│ ├── environment.py
│ ├── Expr.py
│ ├── lox.py
│ ├── lox_callable.py
│ ├── lox_class.py
│ ├── lox_function.py
│ ├── lox_instance.py
│ ├── lox_interpreter.py
│ ├── lox_parser.py
│ ├── lox_resolver.py
│ ├── lox_return.py
│ ├── lox_token.py
│ ├── scanner.py
│ ├── Stmt.py
│ └── token_type.py
├── tests/
│ ├── classes.lox
│ ├── ForLoop.lox
│ ├── stage1.lox
│ ├── stage2.lox
│ ├── stage3.lox
│ ├── stage4.lox
│ ├── stage5.lox
│ ├── superclass.lox
│ └── variables.lox
├── tool/
│ └── generate_ast.py
├── BUILD.txt
└── README.txt



Running the Interpreter:
To run the interpreter and interact with the various stages, follow these steps:
1. Ensure you have Python 3.12 installed on your machine.
2. Optionally, create and activate a virtual environment.
3. Navigate to the `src` directory and run the interpreter:


cd src
python lox.py


4. Follow the on-screen menu to select a stage and execute Lox code.

Project Stages:
The project is separated into distinct stages, each adding more advanced features:
1. **Stage 1**
2. **Stage 2**
3. **Stage 3**
4. **Stage 4**
5. **Stage 5**
6. **Classes**
7. **Superclass**
8. **For Loop**
9. **Variables**


Test Files:
Test files are located in the `tests` directory and correspond to the stages mentioned above. These files contain example Lox code to test the functionality of each stage.

Additional Information:
- The `generate_ast.py` script in the `tool` directory is used to generate AST classes. Running this script is part of the AST generation process but is not necessary for running the interpreter.
