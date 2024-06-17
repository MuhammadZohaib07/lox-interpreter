import Expr
import scanner
import lox_token


class AstPrinter:
    # Entry point for testing the AST printer
    def main(self):
        # Create an example expression:
        # (* (- 123) (group 45.67))
        expression = Expr.Binary(
            Expr.Unary(
                lox_token.LoxToken(scanner.TokenType.MINUS, "-", None, 1),
                Expr.Literal(123)),
            lox_token.LoxToken(scanner.TokenType.STAR, "*", None, 1),
            Expr.Grouping(Expr.Literal(45.67)))
        # Print the AST of the example expression
        print(AstPrinter().print_expr(expression))

    def print_expr(self, expr: Expr):
        # Print the expression by accepting the AST printer visitor
        return expr.accept(self)

    def visit_binary_expr(self, expr: Expr):
        # Visit a binary expression and parenthesize it
        return self.parenthesize(expr.operator.lexeme, expr.left, expr.right)

    def visit_grouping_expr(self, expr: Expr):
        # Visit a grouping expression and parenthesize it
        return self.parenthesize("", expr.expr)

    def visit_literal_expr(self, expr: Expr):
        # Visit a literal expression and return its value as a string
        return str(expr.value)

    def visit_unary_expr(self, expr: Expr):
        # Visit a unary expression and parenthesize it
        return self.parenthesize(expr.operator.lexeme, expr.right)

    def parenthesize(self, name, *exprs):
        # Helper method to parenthesize expressions
        out = "(" + name

        for expr in exprs:
            out += " "
            out += expr.accept(self)

        out += ")"
        return out
