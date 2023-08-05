from luaparser import tests
from luaparser import Parser, Printer
from luaparser.astNodes import *
import textwrap


# https://www.lua.org/manual/5.3/manual.html#3.4

class TokensTestCase(tests.TestCase):
    def setUp(self):
        self.parser = Parser()

    def test_addition(self):
        tokens = self.parser.srcToTokens(textwrap.dedent("""
            if true then 
            elseif false then     
            end
            """))
        print(tokens)

