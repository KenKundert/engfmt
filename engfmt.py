# Physical Quantities
#
# Utilities for working with physical quantities (numbers with units).

# License {{{1
# Copyright (C) 2016 Kenneth S. Kundert
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see [http://www.gnu.org/licenses/].

# Imports {{{1
import re

# Parameters {{{1
CURRENCY_SYMBOLS = '$'
DEFAULT_PRECISION = 4
DEFAULT_SPACER = ''
DEFAULT_UNITY_SCALE_FACTOR = ''
DEFAULT_OUTPUT_SCALE_FACTORS = 'TGMkmunpfa'

# Constants {{{1
MAPPINGS = {
    'Y' : ('e24',  1e24 ),
    'Z' : ('e21',  1e21 ),
    'E' : ('e18',  1e18 ),
    'P' : ('e15',  1e15 ),
    'T' : ('e12',  1e12 ),
    'G' : ('e9',   1e9  ),
    'M' : ('e6',   1e6  ),
    'K' : ('e3',   1e3  ),
    'k' : ('e3',   1e3  ),
    '_' : ('',     1    ),
    ''  : ('',     1    ),
    'm' : ('e-3',  1e-3 ),
    'u' : ('e-6',  1e-6 ),
    'n' : ('e-9',  1e-9 ),
    'p' : ('e-12', 1e-12),
    'f' : ('e-15', 1e-15),
    'a' : ('e-18', 1e-18),
    'z' : ('e-21', 1e-21),
    'y' : ('e-24', 1e-24),
}
BIG_SCALE_FACTORS = 'kMGTPEZY'
    # these must be given in order, one for every three decades
    # use k rather than K, because K looks like a temperature when used alone
SMALL_SCALE_FACTORS = 'munpfazy'
    # these must be given in order, one for every three decades

# Pattern Definitions {{{1
# Build regular expressions used to recognize quantities
def named_regex(name, regex):
    return '(?P<%s>%s)' % (name, regex)
sign = named_regex('sign', '[-+]?')
mantissa = named_regex('mant', r'[0-9]*\.?[0-9]+')
exponent = named_regex('exp', '[eE][-+]?[0-9]+')
scale_factor = named_regex('sf', '[%s]' % ''.join(MAPPINGS))
units = named_regex('units', r'(?:[a-zA-Z][-^/()\w]*)?')
    # examples: Ohms, V/A, J-s, m/s^2, H/(m-s)
    # leading char must be letter to avoid 1.0E-9s -> ('1.0e18', '-9s')
currency = named_regex('currency', '[%s]' % CURRENCY_SYMBOLS)
nan = named_regex('nan', '(?i)inf|nan')

number_with_scale_factor = (
    r'{sign}{mantissa}\s*{scale_factor}{units}'.format(**locals()),
    lambda match: match.group('sign') + match.group('mant'),
    lambda match: match.group('sf'),
    lambda match: match.group('units')
)

number_with_exponent = (
    r'{sign}{mantissa}{exponent}\s*{units}'.format(**locals()),
    lambda match: match.group('sign') + match.group('mant'),
    lambda match: match.group('exp').lower(),
    lambda match: match.group('units')
)

# this one must be processed after number_with_scale_factor
simple_number = (
    r'{sign}{mantissa}\s*{units}'.format(**locals()),
    lambda match: match.group('sign') + match.group('mant'),
    lambda match: '',
    lambda match: match.group('units')
)

currency_with_scale_factor = (
    r'{sign}{currency}{mantissa}\s*{scale_factor}'.format(**locals()),
    lambda match: match.group('sign') + match.group('mant'),
    lambda match: match.group('sf'),
    lambda match: match.group('currency')
)

currency_with_exponent = (
    r'{sign}{currency}{mantissa}{exponent}'.format(**locals()),
    lambda match: match.group('sign') + match.group('mant'),
    lambda match: match.group('exp').lower(),
    lambda match: match.group('currency')
)

simple_currency = (
    r'{sign}{currency}{mantissa}'.format(**locals()),
    lambda match: match.group('sign') + match.group('mant'),
    lambda match: '',
    lambda match: match.group('currency')
)

nan_with_units = (
    r'{sign}{nan}\s+{units}'.format(**locals()),
    lambda match: match.group('sign') + match.group('nan').lower(),
    lambda match: '',
    lambda match: match.group('units')
)

currency_nan = (
    r'{sign}{currency}{nan}'.format(**locals()),
    lambda match: match.group('sign') + match.group('nan').lower(),
    lambda match: '',
    lambda match: match.group('currency')
)

simple_nan = (
    r'{sign}{nan}'.format(**locals()),
    lambda match: match.group('sign') + match.group('nan').lower(),
    lambda match: '',
    lambda match: ''
)


number_converters = [
    (re.compile('\A\s*{}\s*\Z'.format(pattern)), get_mant, get_sf, get_units)
    for pattern, get_mant, get_sf, get_units  in [
        number_with_exponent, number_with_scale_factor, simple_number,
        currency_with_exponent, currency_with_scale_factor, simple_currency,
        nan_with_units, currency_nan, simple_nan,
    ]
]

# Utilities {{{1
from six import string_types
def is_str(obj):
    """Identifies strings in all their various guises."""
    return isinstance(obj, string_types)

# Preferences {{{1
Precision = DEFAULT_PRECISION
Spacer = DEFAULT_SPACER
UnityScaleFactor = DEFAULT_UNITY_SCALE_FACTOR
OutputScaleFactors = DEFAULT_OUTPUT_SCALE_FACTORS

def set_preferences(prec=False, spacer=False, unity=False, output=False):
    """Set Global Preferences
    prec (int): precision in digits where 0 corresponds to 1 digit, must be
        nonnegative.
    spacer 9str): may be '' or ' ', use the latter if you prefer a space between
        the number and the units.
    unity (str): the scale factor for unity, generally '' or '_'.
    output (str): which scale factors to output

    Any value not passed in are left alone. Pass in None to reset it to its
    default value.
    """
    global Precision, Spacer, UnityScaleFactor, OutputScaleFactors
    if prec is not False:
        Precision = prec if prec is not None else DEFAULT_PRECISION
    if spacer is not False:
        Spacer = spacer if spacer is not None else DEFAULT_SPACER
    if unity is not False:
        UnityScaleFactor = unity if unity is not None else DEFAULT_UNITY_SCALE_FACTOR
    if output is not False:
        OutputScaleFactors = output if output is not None else DEFAULT_OUTPUT_SCALE_FACTORS

# Quantity class {{{1
class Quantity:
    def __init__(self, value, units=None):
        """Physical Quantity
        A real quantity with units.

        value: may be a float or a string. If a string, it may be specified with
            SI scale factors and units. For example, the following are all valid:
                2.5ns, 1.7 MHz, 1e6ohms, 2.8_V, 1e12 F, 42, etc.
        units: the quantities units.
        """
        if units is None:
            units = ''
        self._value = value
        self._units = units
        if is_str(value):
            # if we get a string, keep all the pieces so we can reconstruct it
            # exactly as it was given.
            for pattern, get_mant, get_sf, get_units in number_converters:
                match = pattern.match(value)
                if match:
                    self._value = None
                    self._mantissa = get_mant(match)
                    self._scale_factor = get_sf(match)
                    self._units = get_units(match)
                    if self._units:
                        if units:
                            assert units == self._units
                    else:
                        self._units = units
                    return
            raise ValueError('%s: not a valid number.' % value)

    def value(self):
        """Returns the value as a float."""
        if self._value is None:
            sf = self._scale_factor
            return float(self._mantissa + MAPPINGS.get(sf, [sf])[0])
        else:
            return self._value

    def rawvalue(self):
        """Returns the value as a string.
        The original string is returned with units removed. This allows you
        access to the value specified without any loss of precision if the value
        was specified as a string.
        """
        if self._value is None:
            return self._mantissa + self._scale_factor
        else:
            return str(self._value)

    def svalue(self):
        """Returns the value as a string.
        The original string is returned with units removed and the scale factor
        converted to exponential form. This allows you access to the value
        specified without any loss of precision if the value was specified as a
        string.
        """
        if self._value is None:
            sf = self._scale_factor
            return self._mantissa + MAPPINGS.get(sf, [sf])[0]
        else:
            return str(self._value)

    def units(self):
        """Returns the units."""
        return self._units

    def quantity(self):
        """Returns a tuple that contains the value as a float and the units."""
        return self.value(), self.units()

    def is_infinite(self):
        value = self._mantissa if self._value is None else str(self._value)
        return value.lower() in ['inf', '-inf', '+inf']

    def is_nan(self):
        value = self._mantissa if self._value is None else str(self._value)
        return value.lower() in ['nan', '-nan', '+nan']

    def render(self, prec=None):
        """renders value and units"""

        # determine precision
        if prec is None:
            prec = Precision
        assert (prec >= 0)

        def combine(mantissa, sf, units, spacer):
            mantissa = mantissa.lstrip('+')
            if units:
                if units in CURRENCY_SYMBOLS:
                    # prefix the value with the units
                    if mantissa[0] == '-':
                        # if negative, the sign goes before the currency symbol
                        return '-' + units + mantissa[1:] + sf
                    else:
                        return units + mantissa + sf
                else:
                    if sf in MAPPINGS:
                        # has a scale factor
                        return mantissa + spacer + sf + units
                    else:
                        # has an exponent
                        return mantissa + sf + spacer + units
            else:
                return mantissa + sf

        # check for infinities or NaN
        if self.is_infinite() or self.is_nan():
            return combine(self.rawvalue(), '', self.units(), ' ')

        # convert into scientific notation with proper precision
        value = self.value()
        units = self.units()
        number = "%.*e" % (prec, value)
        mantissa, exp = number.split("e")
        exp = int(exp)

        # find scale factor
        index = exp // 3
        shift = exp % 3
        sf = "e%d" % (exp - shift)
        if index == 0:
            if units and units not in CURRENCY_SYMBOLS and not Spacer:
                sf = UnityScaleFactor
            else:
                sf = ''
        elif (index > 0):
            if index <= len(BIG_SCALE_FACTORS):
                if BIG_SCALE_FACTORS[index-1] in OutputScaleFactors:
                    sf = BIG_SCALE_FACTORS[index-1]
        else:
            index = -index
            if index <= len(SMALL_SCALE_FACTORS):
                if SMALL_SCALE_FACTORS[index-1] in OutputScaleFactors:
                    sf = SMALL_SCALE_FACTORS[index-1]

        # move decimal point as needed
        if shift == 0:
            num = float(mantissa)
        elif (shift == 1):
            num = 10*float(mantissa)
        else:
            num = 100*float(mantissa)
        mantissa = "%.*f" % (prec-shift, num)

        #remove trailing zeros (except if mantissa does not contain a .)
        if mantissa.find('.') >= 0:
            mantissa = mantissa.rstrip("0")

        #remove trailing decimal point
        mantissa = mantissa.rstrip(".")

        return combine(mantissa, sf, units, Spacer)

    def __str__(self):
        return self.render()

# Shortcut functions {{{1
def from_eng_fmt(value, units=None):
    return Quantity(value, units).quantity()

def to_eng_fmt(value, units=None, prec=None):
    return Quantity(value, units).render(prec)

def strip_units(value, units=None):
    return Quantity(value, units).rawvalue()

def to_number(value, units=None):
    return Quantity(value, units).value()

def to_number_as_str(value, units=None):
    return Quantity(value, units).svalue()
