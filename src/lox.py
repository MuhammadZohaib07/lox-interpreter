import sys
import os
from scanner import Scanner
from lox_parser import Parser
from lox_interpreter import Interpreter
from token_type import TokenType
from lox_resolver import Resolver


class Lox:
    def __init__(self):
        # Initialize the Lox interpreter with command line arguments and an interpreter instance
        self.args = sys.argv
        self.interpreter = Interpreter()

    def main(self):
        # Main method to start the interactive prompt for the Lox interpreter
        current_dir = os.getcwd()
        print(current_dir)

        # List of available stages for testing
        stages = ["stage1", "stage2", "stage3", "stage4", "stage5", "classes", "superclass", "loops", "variables"]

        while True:
            # Display the available stages and prompt the user for input
            print("\nAvailable stages:")
            for i, stage in enumerate(stages, 1):
                print(f"{i}. {stage}")
            print("q. Quit")

            stage = input("\nEnter the stage number you want to see (e.g., 1, 2, 3, 4, 5, 6, 7, 8, 9) or 'q'/'quit' to exit: ").strip()
            if stage.lower() in ['quit', 'q']:
                # Exit the program if the user inputs 'q' or 'quit'
                print("Exiting the program.")
                break

            if stage.isdigit() and 1 <= int(stage) <= len(stages):
                # Generate the file name based on the selected stage
                file_name = f"../tests/{stages[int(stage) - 1]}.lox"
            else:
                # Handle invalid input
                print("Invalid input. Please enter a valid stage number or 'q'/'quit' to exit.")
                continue

            if not os.path.exists(file_name):
                # Check if the file exists and continue if it does not
                print(f"File {file_name} does not exist.")
                continue

            # Run the selected stage file
            self.run_file(file_name)

    def run_file(self, path):
        # Method to run the Lox code from a file
        with open(path, 'r') as f:
            self.run(f.read())

    def run_prompt(self):
        # Interactive prompt for running Lox code line by line
        while True:
            prompt = input("py-lox> ")
            self.run(prompt)

    def run(self, source):
        # Core method to run the Lox code
        scanner = Scanner(source)  # Tokenize the source code
        tokens = scanner.scan_tokens()  # Get the list of tokens
        parser = Parser(tokens)  # Create a parser with the tokens
        statements = parser.parse()  # Parse the tokens into statements
        resolver = Resolver(self.interpreter)  # Create a resolver for variable resolution
        resolver.resolve_stmts(statements)  # Resolve variable scopes
        self.interpreter.interpret(statements)  # Interpret and execute the statements

    def parse_error(self, token, message):
        # Handle parse errors
        if token.type == TokenType.EOF:
            self.report(token.line, "at end", message)
        else:
            self.report(token.line, " at '" + token.lexeme + "'", message)

    def error(self, line, message):
        # Report a general error with line number
        self.report(line, "", message)

    def runtime_error(self, error):
        # Handle runtime errors by raising the error
        raise error

    def report(self, line, where, message):
        # General method to format and raise errors
        raise RuntimeError("[line " + str(line) + "] Error" + where + ": " + message)


if __name__ == "__main__":
    # Entry point of the program
    s = Lox()
    s.main()
