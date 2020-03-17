import unittest
import hedy
import json
import sys
import io
from contextlib import contextmanager

#this code let's us capture std out to also execute the generated Python
# and check its output
@contextmanager
def captured_output():
    new_out, new_err = io.StringIO(), io.StringIO()
    old_out, old_err = sys.stdout, sys.stderr
    try:
        sys.stdout, sys.stderr = new_out, new_err
        yield sys.stdout, sys.stderr
    finally:
        sys.stdout, sys.stderr = old_out, old_err

def run_code(code):
    with captured_output() as (out, err):
        exec(code)
    return out.getvalue().strip()

class TestsLevel1(unittest.TestCase):

    def test_transpile_other(self):
        with self.assertRaises(Exception) as context:
            result = hedy.transpile("abc felienne 123", 1)

        self.assertEqual(str(context.exception), 'Invalid')

    def test_transpile_print(self):
        result = hedy.transpile("print Hallo welkom bij Hedy!", 1)
        self.assertEqual(result, "print('Hallo welkom bij Hedy!')")
        self.assertEqual(run_code(result), 'Hallo welkom bij Hedy!')

    def test_transpile_ask(self):
        result = hedy.transpile("ask wat is je lievelingskleur?", 1)
        self.assertEqual(result, "answer = input('wat is je lievelingskleur?')")

    def test_transpile_print_multiple_lines(self):
        result = hedy.transpile("print Hallo welkom bij Hedy\nprint Mooi hoor", 1)
        self.assertEqual(result, "print('Hallo welkom bij Hedy')\nprint('Mooi hoor')")

    def test_transpile_three_lines(self):
        input = """print Hallo
ask Wat is je lievelingskleur
echo je lievelingskleur is"""
        result = hedy.transpile(input, 1)
        self.assertEqual(result, "print('Hallo')\nanswer = input('Wat is je lievelingskleur')\nprint('je lievelingskleur is' + answer)")

    def test_transpile_echo(self):
        result = hedy.transpile("echo Jouw lievelingskleur is dus...", 1)
        self.assertEqual(result, "print('Jouw lievelingskleur is dus...' + answer)")

    def test_transpile_unicode(self):
        result = hedy.transpile("print Héllo", 1)
        self.assertEqual(result, "print('Héllo')")

class TestsLevel2(unittest.TestCase):

    # some commands should not change:
    def test_transpile_other(self):
        with self.assertRaises(Exception) as context:
            result = hedy.transpile("abc felienne 123", 2)
            x = result

        self.assertEqual(str(context.exception), 'Invalid')

    def test_transpile_print(self):
        result = hedy.transpile("print Hallo welkom bij Hedy!", 2)
        self.assertEqual(result, "import random\nprint('Hallo'+' '+'welkom'+' '+'bij'+' '+'Hedy'+'!')")

    def test_transpile_ask(self):
        result = hedy.transpile("kleur is ask wat is je lievelingskleur?", 2)
        self.assertEqual(result, "import random\nkleur = input('wat is je lievelingskleur'+'?')")
    
    def test_transpile_ask_unicode(self):
        result = hedy.transpile("é is ask é?", 2)
        self.assertEqual(result, "import random\né = input('é'+'?')")

    def test_transpile_ask_with_print(self):
        result = hedy.transpile("kleur is ask wat is je lievelingskleur?\nprint kleur!", 2)
        self.assertEqual(result, "import random\nkleur = input('wat is je lievelingskleur'+'?')\nprint(kleur+'!')")

    def test_transpile_print_multiple_lines(self):
        result = hedy.transpile("print Hallo welkom bij Hedy!\nprint Mooi hoor", 2)
        self.assertEqual(result, "import random\nprint('Hallo'+' '+'welkom'+' '+'bij'+' '+'Hedy'+'!')\nprint('Mooi'+' '+'hoor')")
        self.assertEqual(run_code(result), "Hallo welkom bij Hedy!\nMooi hoor")

    def test_transpile_assign(self):
        result = hedy.transpile("naam is Felienne", 2)
        self.assertEqual(result, "import random\nnaam = 'Felienne'")

    def test_transpile_assign_2_integer(self):
        result = hedy.transpile("naam is 14", 2)
        self.assertEqual(result, "import random\nnaam = '14'")

    def test_transpile_assign_and_print(self):
        result = hedy.transpile("naam is Felienne\nprint naam", 2)
        self.assertEqual(result, "import random\nnaam = 'Felienne'\nprint(naam)")

    def test_transpile_assign_and_print_more_words(self):
        result = hedy.transpile("naam is Felienne\nprint hallo naam", 2)
        self.assertEqual(result, "import random\nnaam = 'Felienne'\nprint('hallo'+' '+naam)")

    def test_transpile_assign_and_print_punctuation(self):
        result = hedy.transpile("naam is Hedy\nprint Hallo naam!", 2)
        self.assertEqual(result, "import random\nnaam = 'Hedy'\nprint('Hallo'+' '+naam+'!')")

    def test_transpile_assign_and_print_in_sentence(self):
        result = hedy.transpile("naam is Hedy\nprint naam is jouw voornaam", 2)
        self.assertEqual(result, "import random\nnaam = 'Hedy'\nprint(naam+' '+'is'+' '+'jouw'+' '+'voornaam')")

    def test_transpile_assign_and_print_something_else(self):
        result = hedy.transpile("naam is Felienne\nprint Hallo", 2)
        self.assertEqual(result, "import random\nnaam = 'Felienne'\nprint('Hallo')")

    def test_set_list_var(self):
        result = hedy.transpile("dieren is Hond, Kat, Kangoeroe", 2)
        self.assertEqual(result, "import random\ndieren = ['Hond', 'Kat', 'Kangoeroe']")

    def test_print_with_list_var(self):
        result = hedy.transpile("dieren is Hond, Kat, Kangoeroe\nprint dieren at 1", 2)
        self.assertEqual(result, "import random\ndieren = ['Hond', 'Kat', 'Kangoeroe']\nprint(dieren[1])")
        self.assertEqual(run_code(result), "Kat")


    def test_print_with_list_var_random(self):
        result = hedy.transpile("dieren is Hond, Kat, Kangoeroe\nprint dieren at random", 2)
        self.assertEqual(result, "import random\ndieren = ['Hond', 'Kat', 'Kangoeroe']\nprint(random.choice(dieren))")
        self.assertIn(run_code(result), ['Hond', 'Kat', 'Kangoeroe'])

class TestsLevel3(unittest.TestCase):
    def test_transpile_other(self):
        with self.assertRaises(Exception) as context:
            result = hedy.transpile("abc felienne 123", 3)

        self.assertEqual(str(context.exception), 'Invalid')

    def test_transpile_print_level_2(self):
        with self.assertRaises(Exception) as context:
            result = hedy.transpile("print felienne 123", 3)
            self.assertEqual(str(context), 'First word is not a command') #hier moet nog we een andere foutmelding komen!

    def test_print(self):
        result = hedy.transpile("print 'hallo wereld!'", 3)
        self.assertEqual(result, "import random\nprint('hallo wereld!')")

    def test_print_2(self):
        result = hedy.transpile("print 'ik heet henk'", 3)
        self.assertEqual(result, "import random\nprint('ik heet henk')")

    def test_print_with_var(self):
        result = hedy.transpile("naam is Hedy\nprint 'ik heet' naam", 3)
        self.assertEqual(result, "import random\nnaam = 'Hedy'\nprint('ik heet'+naam)")

class TestsLevel4(unittest.TestCase):
    def test_simple_calculation(self):
        result = hedy.transpile("nummer is 4 + 5", 4)
        self.assertEqual('import random\nnummer=4+5\n', result)

    def test_calculation_and_printing(self):
        result = hedy.transpile("nummer is 4 + 5\nprint nummer", 4)
        self.assertEqual('import random\nnummer=4+5\nprint(nummer)\n', result)
        self.assertEqual(run_code(result), "9")




if __name__ == '__main__':
    unittest.main()



    # python = transpile(tree)
    # print(python)
    #
    # exec(python)
