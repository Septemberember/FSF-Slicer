"""javalang parser with lossless unary operators on casts and parentheses.

Adapted expression parsing from javalang 0.13.0 (MIT; see licenses/javalang.txt).
"""
import javalang
from javalang import tree
from javalang.parser import JavaSyntaxError
from javalang.tokenizer import Operator


class JavaParser(javalang.parser.Parser):
    def parse_expression_3(self):
        prefixes = []
        while self.tokens.look().value in Operator.PREFIX:
            prefixes.append(self.tokens.next().value)
        if self.would_accept('('):
            try:
                with self.tokens:
                    expression = self.parse_lambda_expression()
                    if expression:
                        if prefixes: self.illegal('Unary operator on a lambda')
                        return expression
            except JavaSyntaxError:
                pass
            try:
                with self.tokens:
                    self.accept('(')
                    target = self.parse_type()
                    self.accept(')')
                    expression = self.parse_expression_3()
                    cast = tree.Cast(type=target, expression=expression)
                    cast.prefix_operators = prefixes
                    cast.postfix_operators = []
                    cast.selectors = []
                    return cast
            except JavaSyntaxError:
                pass
        primary = self.parse_primary()
        primary.prefix_operators = prefixes + (getattr(primary, 'prefix_operators', None) or [])
        primary.selectors = list(getattr(primary, 'selectors', None) or [])
        primary.postfix_operators = list(getattr(primary, 'postfix_operators', None) or [])
        while self.tokens.look().value in {'[', '.'}:
            token = self.tokens.look()
            selector = self.parse_selector()
            selector._position = token.position
            primary.selectors.append(selector)
        while self.tokens.look().value in Operator.POSTFIX:
            primary.postfix_operators.append(self.tokens.next().value)
        return primary


def parse_compilation_unit(source):
    return JavaParser(javalang.tokenizer.tokenize(source)).parse()
