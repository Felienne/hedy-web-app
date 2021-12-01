import hedy
import textwrap
from test_level_01 import HedyTester

class TestsLevel11(HedyTester):
  level = 11

  def test_if_with_indent(self):
    code = textwrap.dedent("""\
    naam is Hedy
    if naam is Hedy
        print 'koekoek'""")
    expected = textwrap.dedent("""\
    naam = 'Hedy'
    if str(naam) == str('Hedy'):
      print(f'koekoek')""")
    result = hedy.transpile(code, self.level)

    self.assertEqual(expected, result.code)
    self.assertEqual(False, result.has_turtle)

  def test_if_else(self):
    code = textwrap.dedent("""\
    antwoord is ask 'Hoeveel is 10 plus 10?'
    if antwoord is 20
        print 'Goedzo!'
        print 'Het antwoord was inderdaad ' antwoord
    else
        print 'Foutje'
        print 'Het antwoord moest zijn ' antwoord""")

    expected = textwrap.dedent("""\
    antwoord = input(f'Hoeveel is 10 plus 10?')
    if str(antwoord) == str('20'):
      print(f'Goedzo!')
      print(f'Het antwoord was inderdaad {antwoord}')
    else:
      print(f'Foutje')
      print(f'Het antwoord moest zijn {antwoord}')""")

    result = hedy.transpile(code, self.level)

    self.assertEqual(expected, result.code)
    self.assertEqual(False, result.has_turtle)



  def test_for_loop(self):
    code = textwrap.dedent("""\
    a is 2
    b is 3
    for a in range 2 to 4
      a is a + 2
      b is b + 2""")
    expected = textwrap.dedent("""\
    a = '2'
    b = '3'
    step = 1 if int(2) < int(4) else -1
    for a in range(int(2), int(4) + step, step):
      a = int(a) + int(2)
      b = int(b) + int(2)""")

    result = hedy.transpile(code, self.level)

    self.assertEqual(expected, result.code)
    self.assertEqual(False, result.has_turtle)

  def test_if__else(self):
    code = textwrap.dedent("""\
    a is 5
    if a is 1
      x is 2
    else
      x is 222""")
    expected = textwrap.dedent("""\
    a = '5'
    if str(a) == str('1'):
      x = '2'
    else:
      x = '222'""")

    result = hedy.transpile(code, self.level)

    self.assertEqual(expected, result.code)
    self.assertEqual(False, result.has_turtle)

  def test_for_loop_with_print(self):
    code = textwrap.dedent("""\
    for i in range 1 to 10
      print i
    print 'wie niet weg is is gezien'""")
    expected = textwrap.dedent("""\
    step = 1 if int(1) < int(10) else -1
    for i in range(int(1), int(10) + step, step):
      print(f'{i}')
    print(f'wie niet weg is is gezien')""")

    result = hedy.transpile(code, self.level)

    self.assertEqual(expected, result.code)
    self.assertEqual(False, result.has_turtle)

  def test_for_loop_with_assignment(self):
    code = textwrap.dedent("""\
      for i in range 1 to 10
        a is i + 1""")
    expected = textwrap.dedent("""\
      step = 1 if int(1) < int(10) else -1
      for i in range(int(1), int(10) + step, step):
        a = int(i) + int(1)""")

    result = hedy.transpile(code, self.level)

    self.assertEqual(expected, result.code)
    self.assertEqual(False, result.has_turtle)

  def test_reverse_range(self):
    code = textwrap.dedent("""\
    for i in range 10 to 1
      print i
    print 'wie niet weg is is gezien'""")
    expected = textwrap.dedent("""\
    step = 1 if int(10) < int(1) else -1
    for i in range(int(10), int(1) + step, step):
      print(f'{i}')
    print(f'wie niet weg is is gezien')""")

    result = hedy.transpile(code, self.level)

    self.assertEqual(expected, result.code)
    self.assertEqual(False, result.has_turtle)


  def test_if_under_else_in_for(self):
    code = textwrap.dedent("""\
    for i in range 0 to 10
      antwoord is ask 'Wat is 5*5'
      if antwoord is 24
        print 'Dat is fout!'
      else
        print 'Dat is goed!'
      if antwoord is 25
        i is 10""")

    expected = textwrap.dedent("""\
    step = 1 if int(0) < int(10) else -1
    for i in range(int(0), int(10) + step, step):
      antwoord = input(f'Wat is 5*5')
      if str(antwoord) == str('24'):
        print(f'Dat is fout!')
      else:
        print(f'Dat is goed!')
      if str(antwoord) == str('25'):
        i = '10'""")

    result = hedy.transpile(code, self.level)

    self.assertEqual(expected, result.code)
    self.assertEqual(False, result.has_turtle)

    #fails, issue 363

  def test_for_ifbug(self):
    code = textwrap.dedent("""\
    for i in range 0 to 10
      antwoord is ask 'Wat is 5*5'
      if antwoord is 24
        print 'fout'
    print 'klaar met for loop'""")

    expected = textwrap.dedent("""\
      step = 1 if int(0) < int(10) else -1
      for i in range(int(0), int(10) + step, step):
        antwoord = input(f'Wat is 5*5')
        if str(antwoord) == str('24'):
          print(f'fout')
      print(f'klaar met for loop')""")

    result = hedy.transpile(code, self.level)

    self.assertEqual(expected, result.code)
    self.assertEqual(False, result.has_turtle)

  def test_for_loopbug599(self):
    code = textwrap.dedent("""\
    for i in range 0 to 10
      if i is 2
        print '2'""")

    expected = textwrap.dedent("""\
      step = 1 if int(0) < int(10) else -1
      for i in range(int(0), int(10) + step, step):
        if str(i) == str('2'):
          print(f'2')""")

    result = hedy.transpile(code, self.level)

    self.assertEqual(expected, result.code)
    self.assertEqual(False, result.has_turtle)

  def test_unindented_second_loop_1209(self):
    code = textwrap.dedent("""\
    for x in range 1 to 10
     for y in range 1 to 10
     print 'x*y'""")

    with self.assertRaises(hedy.exceptions.NoIndentationException) as context:
      result = hedy.transpile(code, self.level)

  def test_dedented_second_loop_1209(self):
    code = textwrap.dedent("""\
    for x in range 1 to 10
     for y in range 1 to 10
    print 'x*y'""")

    with self.assertRaises(hedy.exceptions.NoIndentationException) as context:
      result = hedy.transpile(code, self.level)

  def test_zigzag_indented_loop_1209(self):
    code = textwrap.dedent("""\
    for x in range 1 to 10
      for y in range 1 to 10
         print 'this number is'
        print x*y""")

    with self.assertRaises(hedy.exceptions.IndentationException) as context:
      result = hedy.transpile(code, self.level)



