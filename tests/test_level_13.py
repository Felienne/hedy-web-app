
import hedy
import textwrap
from test_level_01 import HedyTester

class TestsLevel13(HedyTester):
  level = 13

  def test_and(self):
    code = textwrap.dedent("""\
      naam is ask 'hoe heet jij?'
      leeftijd is ask 'hoe oud ben jij?'
      if naam is 'Felienne' and leeftijd is 37
          print 'hallo jij!'""")
    expected = textwrap.dedent("""\
      naam = input(f'hoe heet jij?')
      try:
        naam = int(naam)
      except ValueError:
        try:
          naam = float(naam)
        except ValueError:
          pass
      leeftijd = input(f'hoe oud ben jij?')
      try:
        leeftijd = int(leeftijd)
      except ValueError:
        try:
          leeftijd = float(leeftijd)
        except ValueError:
          pass
      if str(naam) == str('Felienne') and str(leeftijd) == str('37'):
        print(f'hallo jij!')""")

    self.multi_level_tester(
      max_level=16,
      code=code,
      expected=expected
    )

  def test_or(self):
    code = textwrap.dedent("""\
      if 5 is 5 or 4 is 4
          print 'hallo'""")
    expected = textwrap.dedent("""\
      if str('5') == str('5') or str('4') == str('4'):
        print(f'hallo')""")

    self.multi_level_tester(
      code=code,
      max_level=16,
      expected=expected,
      expected_commands=['if', 'or', 'print']
    )



