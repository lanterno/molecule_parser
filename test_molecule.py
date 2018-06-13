import unittest

from molecule import onize_formula, update_equation_with_multiplier, flaten_formula, parse_molecule

class MoleculeParserTestCases(unittest.TestCase):

    def test_onizing_formulas(self):
        self.assertEqual(onize_formula('H'), 'H1')
        self.assertEqual(onize_formula('H2O'), 'H2O1')
        self.assertEqual(onize_formula('Mg(OH)2'), 'Mg1(O1H1)2')
        self.assertEqual(onize_formula('K4[ON(SO3)2]2'), 'K4[O1N1(S1O3)2]2')

    def test_updating_formula_with_multipler(self):
        self.assertEqual(update_equation_with_multiplier('H1', '2'), 'H2')
        self.assertEqual(update_equation_with_multiplier('K4[O1N1(SO3)2]2', '2'), 'K8[O2N2(SO6)4]4')

    def test_flatting_formula(self):
        self.assertEqual(flaten_formula('H2O'), 'H2O')
        self.assertEqual(flaten_formula('[H1]2O'), 'H2O')
        self.assertEqual(flaten_formula('M1g1(O1H1)2'), 'M1g1O2H2')
        self.assertEqual(flaten_formula('K4[O1N1(S1O3)2]2'), 'K4O2N2S4O12')

    def test_full_parsing(self):
        parsed_mole = parse_molecule('H2O')
        self.assertEqual(len(parsed_mole.keys()), 2)
        self.assertEqual(parsed_mole['H'], 2)
        self.assertEqual(parsed_mole['O'], 1)

        parsed_mole = parse_molecule('Mg(OH)2')
        self.assertEqual(len(parsed_mole.keys()), 3)
        self.assertEqual(parsed_mole['H'], 2)
        self.assertEqual(parsed_mole['O'], 2)
        self.assertEqual(parsed_mole['Mg'], 1)

        parsed_mole = parse_molecule('K4[ON(SO3)2]2')
        self.assertEqual(len(parsed_mole.keys()), 4)
        self.assertEqual(parsed_mole['K'], 4)
        self.assertEqual(parsed_mole['O'], 14)
        self.assertEqual(parsed_mole['N'], 2)
        self.assertEqual(parsed_mole['S'], 4)


if __name__ == '__main__':
    unittest.main()
