"""
Molecule Parser
"""

OPENNING_BRACKETS = ['[', '(']
CLOSING_BRACKETS = [']', ')']
BRACKETS = {'(': ')', '[': ']'}

def onize_formula(formula=""):
    """
    Chemical formulas don't show ones like H2O1, it ignores numbers when it's equal to one.
    For consistency, we're adding those ones here.
    input: str
    output: str
    This function is idempotent
    """
    formula_with_ones = []
    for element in formula:
        if element.isdigit():
            formula_with_ones.append(element)
        elif element.islower():  # means that it's part of the previous element name
            formula_with_ones.append(element)
        else:
            if formula_with_ones and not formula_with_ones[-1].isdigit() and formula_with_ones[-1] not in ['(', '[']:
                formula_with_ones.append('1')
            formula_with_ones.append(element)

    if not formula_with_ones[-1].isdigit():
        formula_with_ones.append('1')
    return ''.join(formula_with_ones)


def update_equation_with_multiplier(formula, multiplier):
    """
    Updates the whole equation with a multipler
    >> Assumes the formula is already onized
    example: (H2O, 2) -> H4O2
    input: str, str
    output: str
    """
    multiplier = int(multiplier)
    _formula = []
    for element in formula:
        if element.isdigit():
            element = str(int(element) * multiplier)
        _formula.append(element)
    return ''.join(_formula)


def flaten_formula(formula=""):
    """
    Recursive function to remove all brackets from out inward.
    """
    bracketless_formula = ""
    while formula:
        element, formula = formula[0], formula[1:]
        if element in BRACKETS:
            closing_bracket = BRACKETS[element]
            inner_formula, formula = formula.rsplit(closing_bracket)
            multipler, formula = formula[0], formula[1:]
            flattened_formula = flaten_formula(inner_formula)
            inner_formula = update_equation_with_multiplier(flattened_formula, multipler)
            bracketless_formula += inner_formula
        else:
            bracketless_formula += element
    return bracketless_formula

def parse_molecule(formula):
    """
    For a given chemical formula represented by a string,
    Count the number of atoms of each element contained in the molecule and return a dict.
    Examples: H2, H2O, Mg(OH)2, K4[ON(SO3)2]2
    """
    dist = {}
    formula_with_ones = onize_formula(formula)
    flat_formula = list(flaten_formula(formula_with_ones))

    while flat_formula:
        char = flat_formula.pop(0)
        if flat_formula and flat_formula[0].islower():  # handling two-letter elements
            char += flat_formula.pop(0)
        number = flat_formula.pop(0)
        if flat_formula and flat_formula[0].isdigit():  # handling numbers more than 9
            number += flat_formula.pop(0)
        dist[char] = dist.get(char, 0) + int(number)

    return dist
