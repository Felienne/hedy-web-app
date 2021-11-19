import hedy
import textwrap
from test_level_01 import HedyTester

class TestsLevel18(HedyTester):
    level = 18

    def test_print_var_brackets(self):
        code = textwrap.dedent("""\
        naam is Hedy
        print('ik heet', naam)""")

        expected = textwrap.dedent("""\
        naam = 'Hedy'
        print(f'ik heet{naam}')""")

        self.multi_level_tester(
          code=code,
          expected=expected,
          extra_check_function=self.is_not_turtle(),
          test_name=self.name()
        )

    def test_smaller(self):
        code = textwrap.dedent("""\
        leeftijd is input('Hoe oud ben jij?')
        if leeftijd < 12:
            print('Dan ben je jonger dan ik!')""")
        expected = textwrap.dedent("""\
        leeftijd = input('Hoe oud ben jij?')
        if int(leeftijd) < int('12'):
          print(f'Dan ben je jonger dan ik!')""")

        self.multi_level_tester(
          max_level=20,
          code=code,
          expected=expected,
          extra_check_function=self.is_not_turtle(),
          test_name=self.name()
        )
    def test_bigger(self):
        code = textwrap.dedent("""\
        leeftijd is input('Hoe oud ben jij?')
        if leeftijd > 12:
            print('Dan ben je ouder dan ik!')""")
        expected = textwrap.dedent("""\
        leeftijd = input('Hoe oud ben jij?')
        if int(leeftijd) > int('12'):
          print(f'Dan ben je ouder dan ik!')""")

        self.multi_level_tester(
          max_level=20,
          code=code,
          expected=expected,
          extra_check_function=self.is_not_turtle(),
          test_name=self.name()
        )
    def test_big_and_small(self):
        code = textwrap.dedent("""\
        leeftijd is input('Hoe oud ben jij?')
        if leeftijd < 12:
            print('Dan ben je jonger dan ik!')
        elif leeftijd > 12:
            print('Dan ben je ouder dan ik!')""")
        expected = textwrap.dedent("""\
        leeftijd = input('Hoe oud ben jij?')
        if int(leeftijd) < int('12'):
          print(f'Dan ben je jonger dan ik!')
        elif int(leeftijd) > int('12'):
          print(f'Dan ben je ouder dan ik!')""")

        self.multi_level_tester(
          max_level=20,
          code=code,
          expected=expected,
          extra_check_function=self.is_not_turtle(),
          test_name=self.name()
        )

    def test_print_brackets(self):
      code = textwrap.dedent("""\
      leeftijd is input('Hoe oud ben jij?')
      print('Dus jij hebt zo veel verjaardagen gehad:')
      for i in range(0,leeftijd):
          print(i)""")
      expected = textwrap.dedent("""\
      leeftijd = input('Hoe oud ben jij?')
      print(f'Dus jij hebt zo veel verjaardagen gehad:')
      step = 1 if int(0) < int(leeftijd) else -1
      for i in range(int(0), int(leeftijd) + step, step):
        print(f'{i}')""")

      self.multi_level_tester(
        max_level=20,
        code=code,
        expected=expected,
        extra_check_function=self.is_not_turtle(),
        test_name=self.name()
      )

    def test_unsupported_float_with_dot(self):
      self.multi_level_tester(
        code="print(1.5 + 1)",
        exception=hedy.UnsupportedFloatException,
        test_name=self.name()
      )

    def test_unsupported_float_with_comma(self):
      self.multi_level_tester(
        code="print(1,5 + 1)",
        exception=hedy.UnsupportedFloatException,
        test_name=self.name()
      )

    def test_if_else(self):
      code = textwrap.dedent("""\
      antwoord is input('Hoeveel is 10 plus 10?')
      if antwoord is 20:
          print('Goedzo!')
          print('Het antwoord was inderdaad ' antwoord)
      else:
          print('Foutje')
          print('Het antwoord moest zijn ' antwoord)""")

      expected = textwrap.dedent("""\
      antwoord = input('Hoeveel is 10 plus 10?')
      if str(antwoord) == str('20'):
        print(f'Goedzo!')
        print(f'Het antwoord was inderdaad {antwoord}')
      else:
        print(f'Foutje')
        print(f'Het antwoord moest zijn {antwoord}')""")

      self.multi_level_tester(
        max_level=20,
        code=code,
        expected=expected,
        extra_check_function=self.is_not_turtle(),
        test_name=self.name()
      )

    def test_for_loop(self):
      code = textwrap.dedent("""\
      a is 2
      a is 3
      for a in range(2,4):
        a is a + 2
        b is b + 2""")
      expected = textwrap.dedent("""\
      a = '2'
      a = '3'
      step = 1 if int(2) < int(4) else -1
      for a in range(int(2), int(4) + step, step):
        a = int(a) + int(2)
        b = int(b) + int(2)""")

      self.multi_level_tester(
        max_level=20,
        code=code,
        expected=expected,
        extra_check_function=self.is_not_turtle(),
        test_name=self.name()
      )

    def test_allow_space_after_else_line(self):
      code = textwrap.dedent("""\
      a is 1
      if a is 1:
        print(a)
      else:   
        print('nee')""")

      expected = textwrap.dedent("""\
      a = '1'
      if str(a) == str('1'):
        print(f'{a}')
      else:
        print(f'nee')""")

      self.multi_level_tester(
        code=code,
        max_level=19,
        expected=expected,
        test_name=self.name()
      )

    def test_allow_space_before_colon(self):
      code = textwrap.dedent("""\
      a is 1
      if a is 1  :
        print(a)
      else:   
        print('nee')""")

      expected = textwrap.dedent("""\
      a = '1'
      if str(a) == str('1'):
        print(f'{a}')
      else:
        print(f'nee')""")

      self.multi_level_tester(
        code=code,
        max_level=19,
        expected=expected,
        test_name=self.name()
      )

    def test_forloop(self):
      code = textwrap.dedent("""\
      for i in range(1, 10):
        print(i)
      print('wie niet weg is is gezien')""")
      expected = textwrap.dedent("""\
      step = 1 if int(1) < int(10) else -1
      for i in range(int(1), int(10) + step, step):
        print(f'{i}')
      print(f'wie niet weg is is gezien')""")

      self.multi_level_tester(
        code=code,
        expected=expected,
        extra_check_function=self.is_not_turtle(),
        test_name=self.name()
      )

    def test_for_nesting(self):
      code = textwrap.dedent("""\
      for i in range(1, 3):
        for j in range(1,4):
          print('rondje: ' i ' tel: ' j)""")
      expected = textwrap.dedent("""\
      step = 1 if int(1) < int(3) else -1
      for i in range(int(1), int(3) + step, step):
        step = 1 if int(1) < int(4) else -1
        for j in range(int(1), int(4) + step, step):
          print(f'rondje: {i} tel: {j}')""")

      self.multi_level_tester(

        code=code,
        expected=expected,
        extra_check_function=self.is_not_turtle(),
        test_name=self.name()
      )

    def test_if_nesting(self):
      code = textwrap.dedent("""\
      kleur is blauw
      kleurtwee is geel
      if kleur is blauw:
        if kleurtwee is geel:
          print('Samen is dit groen!')""")
      expected = textwrap.dedent("""\
      kleur = 'blauw'
      kleurtwee = 'geel'
      if str(kleur) == str('blauw'):
        if str(kleurtwee) == str('geel'):
          print(f'Samen is dit groen!')""")

      self.multi_level_tester(
        max_level=20,
        code=code,
        expected=expected,
        extra_check_function=self.is_not_turtle(),
        test_name=self.name()
      )

    def test_if_under_else_in_for(self):
      code = textwrap.dedent("""\
      for i in range(0, 10):
        antwoord is input('Wat is 5*5')
        if antwoord is 24:
          print('Dat is fout!')
        else:
          print('Dat is goed!')
        if antwoord is 25:
          i is 10""")

      expected = textwrap.dedent("""\
      step = 1 if int(0) < int(10) else -1
      for i in range(int(0), int(10) + step, step):
        antwoord = input('Wat is 5*5')
        if str(antwoord) == str('24'):
          print(f'Dat is fout!')
        else:
          print(f'Dat is goed!')
        if str(antwoord) == str('25'):
          i = '10'""")

      self.multi_level_tester(
        max_level=20,
        code=code,
        expected=expected,
        extra_check_function=self.is_not_turtle(),
        test_name=self.name()
      )

    def test_input_disallows_lists(self):
      code = textwrap.dedent("""
      color is green, blue
      choice is input('Is your favorite color one of: ' color)""")

      with self.assertRaises(hedy.InvalidArgumentTypeException) as context:
        result = hedy.transpile(code, self.level)
      self.assertEqual('Invalid Argument Type', context.exception.error_code)

    def test_multiple_spaces_after_print(self):
      code = "print    ('hallo!')"

      expected = textwrap.dedent("""\
      print(f'hallo!')""")

      self.multi_level_tester(
        code=code,
        max_level=22,
        expected=expected,
        test_name=self.name(),
        extra_check_function=self.is_not_turtle()
      )

    def test_two_spaces_after_bracket(self):
      code = "print(   'hallo!')"

      expected = textwrap.dedent("""\
      print(f'hallo!')""")

      self.multi_level_tester(
        code=code,
        max_level=22,
        expected=expected,
        test_name=self.name(),
        extra_check_function=self.is_not_turtle()
      )

    def test_multiple_spaces_before_and_after_bracket(self):
      code = "print  (   'hallo!')"

      expected = textwrap.dedent("""\
      print(f'hallo!')""")

      self.multi_level_tester(
        code=code,
        max_level=22,
        expected=expected,
        test_name=self.name(),
        extra_check_function=self.is_not_turtle()
      )

    # negative tests
    def test_var_undefined_error_message(self):
      code = textwrap.dedent("""\
        naam is Hedy
        print('ik heet ' name)""")

      self.multi_level_tester(
        code=code,
        exception=hedy.UndefinedVarException,
        max_level=20,
        test_name=self.name()
      )

      # deze extra check functie kan nu niet mee omdat die altijd op result werkt
      # evt toch splitsen in 2 (pos en neg?)
      # self.assertEqual('name', context.exception.arguments['name'])