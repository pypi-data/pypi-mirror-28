
from ppci.common import CompilerError
from ppci.lang.common import Token, SourceLocation
from ppci.lang.tools.recursivedescent import RecursiveDescentParser
import unittest


def gen_tokens(tokens):
    """ Helper function which creates a token iterator """
    col = 1
    for typ, val in tokens:
        loc = SourceLocation('test.c', 1, col, 1)
        yield Token(typ, val, loc)
        col += 1


class RecursiveDescentParserTestCase(unittest.TestCase):
    """ Test recursive descent parser """
    def setUp(self):
        self.parser = RecursiveDescentParser()

    def test_consume(self):
        """ Test consumption of a token type """
        tokens = [('ID', 'foo'), ('ID', 'bar')]
        self.parser.init_lexer(gen_tokens(tokens))
        self.assertFalse(self.parser.at_end)
        self.parser.consume('ID')
        self.assertFalse(self.parser.at_end)

    def test_failing_consume(self):
        """ Test consumption of more than one typ """
        tokens = [('ID', 'foo'), ('ID', 'bar')]
        self.parser.init_lexer(gen_tokens(tokens))
        token = self.parser.consume(['ID', 'NUMBER'])
        self.assertEqual('ID', token.typ)
        self.assertEqual('foo', token.val)
        self.assertFalse(self.parser.at_end)
        with self.assertRaises(CompilerError) as ctx:
            self.parser.consume(['-', '+'])
        self.assertEqual('Expected "-" or "+", got "ID"', ctx.exception.msg)
        with self.assertRaises(CompilerError) as ctx:
            self.parser.consume(['-', '+', '*'])
        self.assertEqual(
            'Expected "-", "+" or "*", got "ID"', ctx.exception.msg)
        token = self.parser.consume(['ID', 'NUMBER'])
        self.assertEqual('ID', token.typ)
        self.assertEqual('bar', token.val)
        self.assertTrue(self.parser.at_end)

    def test_look_ahead(self):
        """ Test consumption look ahead function """
        tokens = [('NUM', '100'), ('ID', 'bar'), (':', ':')]
        self.parser.init_lexer(gen_tokens(tokens))
        self.assertEqual('bar', self.parser.look_ahead(1).val)
        self.parser.consume('NUM')
        self.assertEqual('ID', self.parser.peak)
        self.assertEqual(':', self.parser.look_ahead(1).val)
        self.assertEqual(None, self.parser.look_ahead(2))


if __name__ == '__main__':
    unittest.main()
