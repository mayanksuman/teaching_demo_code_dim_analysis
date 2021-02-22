""" A class representing a nondimensional number """

from collections import namedtuple
from fractions import Fraction

from typing import List, Dict

_BaseQuantity = namedtuple("BaseQuantity", ['Quantity', 'Dimension'])

_SI_base_units = {_BaseQuantity('Length', 'L'): 'm',
                  _BaseQuantity('Mass', 'M'): 'kg',
                  _BaseQuantity('Time', 'T'): 's',
                  _BaseQuantity('Temperature', '\\theta'): 'K',
                  _BaseQuantity('Electric Current', 'I'): 'A',
                  _BaseQuantity('Amount of Substance', 'N'): 'mol',
                  _BaseQuantity('Luminous Intensity', 'J'): 'cd',
                 }
_SI_derived_units = {'N': {'kg': 1, 'm': 1, 's': -2},
                     'Pa': {'kg': 1, 'm': -1, 's': -2},
                     'J': {'kg': 1, 'm': 2, 's': -2},
                     'W': {'kg': 1, 'm': 2, 's': -3},
                     'C': {'A': 1, 's': 1},
                     'V': {'kg': 1, 'm': 2, 's': -3, 'A': -1},
                     '\\ohm': {'kg': 1, 'm': 2, 's': -3, 'A': -2},
                     'S': {'kg': -1, 'm': -2, 's': 3, 'A': 2},
                     'F': {'kg': -1, 'm': -2, 's': 4, 'A': 2},
                     'T': {'kg': 1, 's': -2, 'A': -1},
                     'Wb': {'kg': 1, 'm': 2, 's': -2, 'A': -1},
                     'H': {'kg': 1, 'm': 2, 's': -2, 'A': -2},
                     }


class Parameter(object):
    """
    A lightweight class representing a parameter.
    """

    def __init__(self, symbol: str, units: Dict[str, int]) -> None:
        self.units = self._parse_unit(units)
        self.symbol = symbol

    @property
    def dimension(self, base_quantities=_SI_base_units):
        base_dim_units = {k.Dimension: v for k, v in base_quantities.items()}
        dim = {}
        for k, v in self.units.items():
            for kb, vb in base_dim_units.items():
                if vb == k:
                    dim[kb] = v
        return dim

    def _parse_unit(self, units: Dict[str, int],
                    unit_system=_SI_base_units,
                    derived_units=_SI_derived_units):
        base_units = set(unit_system.values())
        units = self._fix_derived_units(units, derived_units)
        units = self._remove_unused_units(units)
        units_provided = set(units.keys())
        unknown_units = units_provided - base_units
        if unknown_units:
            raise ValueError(f'Unknown Units: {unknown_units}')
        return units

    def _fix_derived_units(self, units: Dict[str, int],
                           derived_units=_SI_derived_units):
        used_derived_units = set(units.keys()).intersection(
            set(derived_units.keys()))
        for u in used_derived_units:
            for k, v in derived_units[u].items():
                if k in units.keys():
                    units[k] += v*units[u]
                else:
                    units[k] = v*units[u]
            units[u] = 0
        return units

    def _remove_unused_units(self, units: Dict[str, int]):
        return {k: v for k, v in units.items() if v != 0}

    def __mul__(self, other):
        common_units = set(self.units.keys()).intersection(
            set(other.units.keys()))
        units = {u: self.units[u] + other.units[u] for u in common_units}
        units.update({k: v for k, v in self.units.items()
                      if k not in common_units})
        units.update({k: v for k, v in other.units.items()
                      if k not in common_units})
        return Parameter(f"{self.symbol} * {other.symbol}", units)

    def __truediv__(self, other):
        other2 = Parameter(other.symbol, {k: -v for k, v in other.units.items()})
        ret = self.__mul__(other2)
        ret.symbol = f"{self.symbol} / {other.symbol}"
        return ret

    def __add__(self, other):
        if self.units != others.units:
            raise ValueError('Inconsistent units.')
        return Parameter(f"{self.symbol} + {other.symbol}", self.units)

    def __diff__(self, other):
        ret = self.__add__(other)
        ret.symbol = f"{self.symbol} - {other.symbol}"
        return ret

    def __str__(self):
        return f"{self.symbol.__repr__()}"

    def __repr__(self):
        _units = "".join(f"{k}" + (" " if v == 1 else "^{" + f"{v}" + "}")
                         for k, v in self.units.items())
        return f"$${self.symbol}\\ \\ (unit: {_units})$$"
    
    def copy(self):
        return Parameter(self.symbol, self.units)


class NondimensionalNumber(object):
    """
    Class which represents a nondimensional number.
    You initialize it with the list of parameters used
    in a particular problem and the specific vector of
    Fraction types that represents the power of each parameter
    in the nondimensional number.
    """

    def __init__(
        self, parameters: List[Parameter], nondimensional_vector: List[Fraction]
    ) -> None:
        self.parameters = parameters
        self.vector = nondimensional_vector
        self.string_representation = self._parse_nondimensional_number()

    def _parse_nondimensional_number(self) -> str:
        """
        Takes the list of parameters and the nondimensional number
        vector, and parses it into a string that may be typeset
        with LaTeX
        """
        # Initialize two empty strings for the numerator and
        # denominator of the nondimensional number
        numerator_string = ""
        denominator_string = ""

        for p, n in zip(self.parameters, self.vector):
            # No need to typeset the parameters if they do not
            # appear in the nondimensional number
            if n == 0:
                continue

            # If the exponent on the parameter is one,
            # we do not need to write it.
            if n == 1 or n == -1:
                parsed_parameter = p.symbol
            # If the exponent is a whole number, we do
            # not need to represent it as a fraction.
            elif n.denominator == 1 or n.denominator == -1:
                parsed_parameter = p.symbol + "^{%i}" % (abs(n.numerator))
            # If power is 1/2 then put it inside squareroot
            elif abs(n) == 0.5:
                parsed_parameter = '\\sqrt{' + p.symbol + '}'
            # Otherwise, represent it as a fraction
            else:
                parsed_parameter = p.symbol + "^{%i/%i}" % (
                    abs(n.numerator), abs(n.denominator)
                )

            # Depending upon whether the exponent is positive or
            # negative, put it in the numerator or the denominator
            if n > 0:
                numerator_string = " ".join([numerator_string, parsed_parameter])
            elif n < 0:
                denominator_string = " ".join([denominator_string, parsed_parameter])

        # If the numerator is empty, make it a one
        if numerator_string == "":
            parsed_number = "\\frac{1}{" + denominator_string + "}"
        # If the denominator is empty, there is no need for a fraction
        elif denominator_string == "":
            parsed_number = numerator_string
        # Otherwise make it a fraction
        else:
            parsed_number = "\\frac{" + numerator_string + "}{" + denominator_string + "}"

        # And we are done! We return a LaTeX string
        return parsed_number

    # Let IPython know how this may be typeset with LaTeX

    def _repr_latex_(self) -> str:
        return "$$" + self.string_representation + "$$"

    # Return the string form of the nondimensional number

    def __str__(self) -> str:
        return self.string_representation


# This is a bit of a hack: Here I am subclassing
# the builtin Python list type and adding a
# function for print_latex(). This allows
# IPython to be able to render a list of
# nondimensional numbers as well as a single one.


class NondimensionalNumberList(list):
    # Make a comma delimited list of the
    # nondimensional numbers

    def __str__(self) -> str:
        string_representation = ""
        for n in range(len(self)):
            s = str(self.__getitem__(n))
            string_representation += s
            if n != len(self) - 1:
                string_representation += ", "
        return string_representation

    # Add symbols for typesetting with LaTeX

    def print_latex(self) -> str:
        return "$$" + self.__str__() + "$$"


# Register the print_latex function with IPython if we are using it
try:
    get_ipython().display_formatter.formatters["text/latex"].for_type(
        NondimensionalNumberList, NondimensionalNumberList.print_latex
    )
    get_ipython().display_formatter.formatters["text/latex"].for_type(
        Parameter, Parameter.__repr__
    )
except:
    pass
