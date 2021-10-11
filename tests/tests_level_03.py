import hedy
import textwrap
from tests_level_01 import HedyTester

class TestsLevel3(HedyTester):
  level = 3

  def test_transpile_other(self):
    with self.assertRaises(hedy.InvalidCommandException) as context:
      result = hedy.transpile("abc felienne 123", self.level)
    self.assertEqual('Invalid', context.exception.error_code)

  def test_transpile_print_level_2(self):
    with self.assertRaises(hedy.UnquotedTextException) as context:
      result = hedy.transpile("print felienne 123", self.level)

    self.assertEqual('Unquoted Text', context.exception.error_code)  # hier moet nog we een andere foutmelding komen!


  def test_print(self):

    code = textwrap.dedent("""\
    print 'hallo wereld!'""")

    result = hedy.transpile(code, self.level)

    expected = textwrap.dedent("""\
    print(f'hallo wereld!')""")

    self.assertEqual(expected, result.code)
    self.assertEqual(False, result.has_turtle)


  def test_transpile_turtle_basic(self):
    result = hedy.transpile("forward 50\nturn\nforward 100", self.level)
    expected = textwrap.dedent("""\
    t.forward(50)
    time.sleep(0.1)
    t.right(90)
    t.forward(100)
    time.sleep(0.1)""")
    self.assertEqual(expected, result.code)
    self.assertEqual(True, result.has_turtle)

  def test_transpile_turtle_with_ask(self):
    code = textwrap.dedent("""\
    afstand is ask 'hoe ver dan?'
    forward afstand""")
    result = hedy.transpile(code, self.level)
    expected = textwrap.dedent("""\
    afstand = input('hoe ver dan?')
    t.forward(afstand)
    time.sleep(0.1)""")
    self.assertEqual(expected, result.code)
    self.assertEqual(True, result.has_turtle)

  def test_print_with_comma(self):
    code = textwrap.dedent("""\
    naam is Hedy
    print 'ik heet ,'""")

    result = hedy.transpile(code, self.level)

    expected = textwrap.dedent("""\
    naam = 'Hedy'
    print(f'ik heet ,')""")

    self.assertEqual(expected, result.code)
    self.assertEqual(False, result.has_turtle)

  def test_name_with_underscore(self):
    code = textwrap.dedent("""\
    voor_naam is Hedy
    print 'ik heet '""")

    result = hedy.transpile(code, self.level)

    expected = textwrap.dedent("""\
    voor_naam = 'Hedy'
    print(f'ik heet ')""")

    self.assertEqual(expected, result.code)
    self.assertEqual(False, result.has_turtle)

  def test_name_that_is_keyword(self):
    hashed_var = hedy.hash_var("for")

    code = textwrap.dedent("""\
    for is Hedy
    print 'ik heet ' for """)

    result = hedy.transpile(code, self.level)

    expected = textwrap.dedent("""\
    vd55669822f1a8cf72ec1911e462a54eb = 'Hedy'
    print(f'ik heet {vd55669822f1a8cf72ec1911e462a54eb}')""")

    self.assertEqual(expected, result.code)
    self.assertEqual(False, result.has_turtle)

  def test_print_Spanish(self):

    code = textwrap.dedent("""\
    print 'Cuál es tu color favorito?'""")

    result = hedy.transpile(code, self.level)

    expected = textwrap.dedent("""\
    print(f'Cuál es tu color favorito?')""")

    self.assertEqual(expected, result.code)
    self.assertEqual(False, result.has_turtle)

  def test_print_with_list_var(self):

    code = textwrap.dedent("""\
    dieren is Hond, Kat, Kangoeroe
    print dieren at 1""")

    result = hedy.transpile(code, self.level)

    expected = textwrap.dedent("""\
    dieren = ['Hond', 'Kat', 'Kangoeroe']
    print(f'{dieren[1]}')""")

    self.assertEqual(expected, result.code)
    self.assertEqual(False, result.has_turtle)

    self.assertEqual(self.run_code(result), "Kat")

  def test_print_with_list_var_random(self):

    code = textwrap.dedent("""\
    dieren is Hond, Kat, Kangoeroe
    print 'hallo ' dieren at random""")

    result = hedy.transpile(code, self.level)

    expected = textwrap.dedent("""\
    dieren = ['Hond', 'Kat', 'Kangoeroe']
    print(f'hallo {random.choice(dieren)}')""")

    self.assertEqual(expected, result.code)
    self.assertEqual(False, result.has_turtle)
    self.assertIn(self.run_code(result), ['hallo Hond', 'hallo Kat', 'hallo Kangoeroe'])

  def test_transpile_ask_Spanish(self):
    code = textwrap.dedent("""\
    color is ask 'Cuál es tu color favorito?'""")

    result = hedy.transpile(code, self.level)

    expected = textwrap.dedent("""\
    color = input('Cuál es tu color favorito?')""")

    self.assertEqual(expected, result.code)
    self.assertEqual(False, result.has_turtle)

  def test_print_2(self):

    code = textwrap.dedent("""\
    print 'ik heet henk'""")

    result = hedy.transpile(code, self.level)

    expected = textwrap.dedent("""\
    print(f'ik heet henk')""")

    self.assertEqual(expected, result.code)
    self.assertEqual(False, result.has_turtle)

  def test_print_with_var(self):

    code = textwrap.dedent("""\
    naam is Hedy
    print 'ik heet' naam""")

    result = hedy.transpile(code, self.level)

    expected = textwrap.dedent("""\
    naam = 'Hedy'
    print(f'ik heet{naam}')""")

    self.assertEqual(expected, result.code)
    self.assertEqual(False, result.has_turtle)

  def test_transpile_ask_with_print(self):

    code = textwrap.dedent("""
    kleur is ask 'wat is je lievelingskleur?'
    print 'jouw lievelingskleur is dus' kleur '!'""")

    result = hedy.transpile(code, self.level)

    expected = textwrap.dedent("""\
    kleur = input('wat is je lievelingskleur?')
    print(f'jouw lievelingskleur is dus{kleur}!')""")

    self.assertEqual(expected, result.code)
    self.assertEqual(False, result.has_turtle)

  def test_transpile_ask_with_var(self):

    code = textwrap.dedent("""
    ding is kleur
    kleur is ask 'Wat is je lievelings' ding
    print 'Jouw favoriet is dus ' kleur""")

    result = hedy.transpile(code, self.level)

    expected = textwrap.dedent("""\
    ding = 'kleur'
    kleur = input('Wat is je lievelings'+ding)
    print(f'Jouw favoriet is dus {kleur}')""")

    self.assertEqual(expected, result.code)
    self.assertEqual(False, result.has_turtle)

  def test_transpile_ask_no_quotes(self):
    code = textwrap.dedent("""
    ding is kleur
    kleur is ask Wat is je lievelingskleur'
    print 'Jouw favoriet is dus ' kleur""")

    with self.assertRaises(hedy.UnquotedTextException) as context:
      result = hedy.transpile(code, self.level)

    self.assertEqual('Unquoted Text', context.exception.error_code)  # hier moet nog we een andere foutmelding komen!

  def test_use_slashes_at_end_of_print_allowed(self):
    code = "print 'Welcome to \\'"
    result = hedy.transpile(code, self.level)

    expected = textwrap.dedent("""\
    print(f'Welcome to \\\\')""")

    self.assertEqual(expected, result.code)
    self.assertEqual(False, result.has_turtle)

    expected_output = self.run_code(result)
    self.assertEqual("Welcome to \\", expected_output)

  def test_transpile_missing_opening_quote(self):
    code = textwrap.dedent("""\
      print hallo wereld'""")

    with self.assertRaises(hedy.UnquotedTextException) as context:
      result = hedy.transpile(code, self.level)

    self.assertEqual('Unquoted Text', context.exception.error_code)


  def test_transpile_missing_all_quotes(self):
    code = textwrap.dedent("""\
      print hallo wereld""")

    self.multi_level_tester(
      code=code,
      max_level=4,
      expected=hedy.UndefinedVarException,
      test_name=self.test_name()
    )

  def test_var_undefined_error_message(self):

    code = textwrap.dedent("""\
      naam is Hedy
      print 'ik heet ' name""")

    with self.assertRaises(hedy.UndefinedVarException) as context:
      result = hedy.transpile(code, self.level)

    self.assertEqual('Var Undefined', context.exception.error_code)
    self.assertEqual('name', context.exception.arguments['name'])


  def test_transpile_issue_375(self):
    code = textwrap.dedent("""
      is Foobar
      print welcome""")

    with self.assertRaises(hedy.ParseException) as context:
      result = hedy.transpile(code, self.level)

    self.assertEqual('Parse', context.exception.error_code)

  def test_two_spaces_after_print(self):

    max_level = 4
    code = "print        'hallo!'"

    expected = textwrap.dedent("""\
    print(f'hallo!')""")

    is_not_turtle = (lambda x: not x.has_turtle)

    self.multi_level_tester(
      code=code,
      max_level=max_level,
      expected=expected,
      test_name=self.test_name(),
      extra_check_function=is_not_turtle
    )




  def test_bengali_assign(self):
    hashed_var = hedy.hash_var("নাম")

    code = textwrap.dedent("""\
    নাম is হেডি""")

    result = hedy.transpile(code, self.level)

    expected = textwrap.dedent(f"""\
    {hashed_var} = 'হেডি'""")

    self.assertEqual(expected, result.code)
    self.assertEqual(False, result.has_turtle)

  def test_bengali_assign_and_use(self):
    hashed_var = hedy.hash_var("নাম")
    self.assertEqual('veb9b5c786e8cde0910df4197f630ee75', hashed_var)

    code = textwrap.dedent("""\
    নাম is হেডি
    print 'আমার নাম is ' নাম """)

    result = hedy.transpile(code, self.level)

    expected = textwrap.dedent("""\
    veb9b5c786e8cde0910df4197f630ee75 = 'হেডি'
    print(f'আমার নাম is {veb9b5c786e8cde0910df4197f630ee75}')""")

    self.assertEqual(expected, result.code)

  def test_chinese_assign_and_use(self):
    hashed_var = hedy.hash_var("你好世界")
    self.assertEqual('v65396ee4aad0b4f17aacd1c6112ee364', hashed_var)

    code = textwrap.dedent("""\
    你好世界 is 你好世界
    print 你好世界""")

    result = hedy.transpile(code, self.level)

    expected = textwrap.dedent("""\
    v65396ee4aad0b4f17aacd1c6112ee364 = '你好世界'
    print(f'{v65396ee4aad0b4f17aacd1c6112ee364}')""")

    self.assertEqual(expected, result.code)















