# encoding: utf-8
#
# Physical Quantities
#
# Utilities for working with physical quantities (numbers with units).
#
# This module inputs and outputs in several different forms:
#    quantities (numbers with units):
#        (1e6, 'Hz') -- quantity
#        '1MHz'      -- engineering format
#        '1e6Hz'     -- string
#    numbers (numbers without units):
#        1e6         -- num
#        '1M'        -- unitless engineering format
#        '1e6'       -- unitless string
#

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
__version__ = '1.0.2'
import re

# Parameters {{{1
CURRENCY_SYMBOLS = '$'
DEFAULT_HUMAN_PRECISION = 4
DEFAULT_MACHINE_PRECISION = 8
DEFAULT_SPACER = ''
DEFAULT_UNITY_SCALE_FACTOR = ''
DEFAULT_OUTPUT_SCALE_FACTORS = 'TGMkmunpfa'
DEFAULT_IGNORE_SCALE_FACTORS = False
DEFAULT_ASSIGNMENT_FORMATTER = '{n} = {v}'
DEFAULT_ASSIGNMENT_RECOGNIZER = (
    r'\A\s*(?:(\w+)\s*=\s*)?(.*?)(?:\s*--\s*(.*?)\s*)?\Z'
)

import math
CONSTANTS = {
    'h': (6.62606957e-34, 'J-s'),      # Plank's constant
    'k': (1.3806488e-23, 'J/K'),       # Boltzmann's constant
    'q': (1.602176565e-19, 'C'),       # Elementary charge
    'c': (2.99792458e8, 'm/s'),        # Speed of light
    'C0': (273.15, 'K'),               # Zero degrees Celsius in Kelvin
    'eps0': (8.854187817e-12, 'F/m'),  # Permittivity of free space
    'mu0': (4e-7*math.pi, 'H/m'),      # Permeability of free space
    'Z0': (376.730313461, 'Ohms'),     # Characteristic impedance of free space
}


# Constants {{{1
MAPPINGS = {
    'Y': ('e24',  1e24 ),
    'Z': ('e21',  1e21 ),
    'E': ('e18',  1e18 ),
    'P': ('e15',  1e15 ),
    'T': ('e12',  1e12 ),
    'G': ('e9',   1e9  ),
    'M': ('e6',   1e6  ),
    'K': ('e3',   1e3  ),
    'k': ('e3',   1e3  ),
    '_': ('',     1    ),
    '' : ('',     1    ),
    'm': ('e-3',  1e-3 ),
    'u': ('e-6',  1e-6 ),
    'n': ('e-9',  1e-9 ),
    'p': ('e-12', 1e-12),
    'f': ('e-15', 1e-15),
    'a': ('e-18', 1e-18),
    'z': ('e-21', 1e-21),
    'y': ('e-24', 1e-24),
}

BIG_SCALE_FACTORS = 'kMGTPEZY'
    # These must be given in order, one for every three decades.
    # Use k rather than K, because K looks like a temperature when used alone.

SMALL_SCALE_FACTORS = 'munpfazy'
    # These must be given in order, one for every three decades.

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
smpl_units = named_regex('units', r'(?:[a-zA-Z_]*)')
    # may only contain alphabetic characters, ex: V, A, Ohms, etc.
currency = named_regex('currency', '[%s]' % CURRENCY_SYMBOLS)
nan = named_regex('nan', '(?i)inf|nan')
left_delimit = r'(?:\A|(?<=[^a-zA-Z0-9_.]))'
right_delimit = r'(?=[^-+0-9_]|\Z)'

embedded_engineering_notation = re.compile(
    '{left_delimit}{mantissa}{scale_factor}{smpl_units}{right_delimit}'.format(
        **locals()
    )
)

embedded_floating_point_notation = re.compile(
    '{left_delimit}{mantissa}{exponent}?{smpl_units}{right_delimit}'.format(
        **locals()
    )
)

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

all_number_converters = [
    (re.compile('\A\s*{}\s*\Z'.format(pattern)), get_mant, get_sf, get_units)
    for pattern, get_mant, get_sf, get_units in [
        number_with_exponent, number_with_scale_factor, simple_number,
        currency_with_exponent, currency_with_scale_factor, simple_currency,
        nan_with_units, currency_nan, simple_nan,
    ]
]

sf_free_number_converters = [
    (re.compile('\A\s*{}\s*\Z'.format(pattern)), get_mant, get_sf, get_units)
    for pattern, get_mant, get_sf, get_units in [
        number_with_exponent, simple_number,
        currency_with_exponent, simple_currency,
        nan_with_units, currency_nan, simple_nan,
    ]
]

# Regular expression for recognizing and decomposing string .format method codes
format_spec = re.compile(r'\A([<>]?)(\d*)(?:\.(\d+))?([qruseEfFgGdnQR]?)\Z')

# Utilities {{{1
# is_str {{{2
from six import string_types
def is_str(obj):
    """Identifies strings in all their various guises."""
    return isinstance(obj, string_types)

def num_to_str(num):
    return "{0:.{1}g}".format(num, MachinePrecision+1)

# _combine {{{2
def _combine(mantissa, sf, units, spacer):
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

# Preferences {{{1
HumanPrecision = DEFAULT_HUMAN_PRECISION
MachinePrecision = DEFAULT_MACHINE_PRECISION
Spacer = DEFAULT_SPACER
UnityScaleFactor = DEFAULT_UNITY_SCALE_FACTOR
OutputScaleFactors = DEFAULT_OUTPUT_SCALE_FACTORS
IgnoreScaleFactors = DEFAULT_IGNORE_SCALE_FACTORS
AssignmentFormatter = DEFAULT_ASSIGNMENT_FORMATTER
AssignmentRecognizer = re.compile(DEFAULT_ASSIGNMENT_RECOGNIZER)

def set_preferences(
        hprec=False, mprec=False, spacer=False, unity=False, output=False,
        ignore_sf=0, assign_fmt=False, assign_rec=False
):
    """Set Global Preferences

    hprec (int): Human precision in digits where 0 corresponds to 1 digit. Must
        be nonnegative. This precision is used when generating engineering
        format.
    mprec (int): Machine precision in digits where 0 corresponds to 1 digit,
        must be nonnegative. This precision is used when not generating
        engineering format.
    spacer (str): May be '' or ' ', use the latter if you prefer a space between
        the number and the units. Generally using ' ' makes numbers easier to
        read, particularly with complex units, and using '' is easier to parse.
    unity (str): The output scale factor for unity, generally '' or '_'.
    output (str): Which scale factors to output, generally one would only use
        familiar scale factors.
    ignore_sf (bool): Whether scale factors should be ignored by default.
    assign_fmt (str): Format string for an assignment. Will be passed through
        string .format method. Format string takes three possible arguments
        named n, q, and d for the name, value and description.  The default is
        '{n} = {v}'
    assign_rec (str): Regular expression used to recognize an assignment. Used
        in add_to_namespace(). Default recognizes the form
            "Temp = 300_K -- Temperature".

    Any value not passed in are left alone. Pass in None to reset it to its
    default value.
    """
    global HumanPrecision, MachinePrecision
    global Spacer, UnityScaleFactor, OutputScaleFactors, IgnoreScaleFactors
    global AssignmentFormatter, AssignmentRecognizer
    if hprec is not False:
        HumanPrecision = hprec if hprec is not None else DEFAULT_HUMAN_PRECISION
    if mprec is not False:
        MachinePrecision = (
            mprec if mprec is not None else DEFAULT_MACHINE_PRECISION
        )
    if spacer is not False:
        Spacer = spacer if spacer is not None else DEFAULT_SPACER
    if unity is not False:
        UnityScaleFactor = (
            unity if unity is not None else DEFAULT_UNITY_SCALE_FACTOR
        )
    if output is not False:
        OutputScaleFactors = (
            output if output is not None else DEFAULT_OUTPUT_SCALE_FACTORS
        )
    if ignore_sf is not 0:
        IgnoreScaleFactors = (
            ignore_sf if ignore_sf is not None else DEFAULT_IGNORE_SCALE_FACTORS
        )
    if assign_fmt is not False:
        AssignmentFormatter = (
            assign_fmt if assign_fmt is not None else DEFAULT_ASSIGNMENT_FORMATTER
        )
    if assign_rec is not False:
        AssignmentRecognizer = re.compile(
            assign_rec if assign_rec is not None else DEFAULT_ASSIGNMENT_RECOGNIZER
        )

# Quantity class {{{1
class Quantity:
    def __init__(self, value, units=None, ignore_sf=None):
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
        self.units = units
        ignore_sf = IgnoreScaleFactors if ignore_sf is None else ignore_sf

        if is_str(value):
            if ignore_sf:
                number_converters = sf_free_number_converters
            else:
                number_converters = all_number_converters
            # if we get a string, keep all the pieces so we can reconstruct it
            # exactly as it was given.
            for pattern, get_mant, get_sf, get_units in number_converters:
                match = pattern.match(value)
                if match:
                    self._value = None
                    self._mantissa = get_mant(match)
                    sf = get_sf(match)
                    self._scale_factor = sf if sf != '_' else ''
                    self.units = get_units(match)
                    if self.units:
                        if units:
                            assert units == self.units
                    else:
                        self.units = units
                    return
            try:
                self._value, self.units = CONSTANTS[value]
            except KeyError:
                raise ValueError('%s: not a valid number.' % value)

    def is_infinite(self):
        value = self._mantissa if self._value is None else str(self._value)
        return value.lower() in ['inf', '-inf', '+inf']

    def is_nan(self):
        value = self._mantissa if self._value is None else str(self._value)
        return value.lower() in ['nan', '-nan', '+nan']

    def add_name(self, name):
        "Add a name."
        self.name = name

    def add_desc(self, desc):
        "Add a description."
        self.desc = desc

    def strip(self):
        """Returns the value as a string in the originally given notation.

        The original string is returned with units removed. This allows you
        access to the value specified without any loss of precision if the value
        was specified as a string.
        """
        if self._value is None:
            return self._mantissa + self._scale_factor
        else:
            return num_to_str(self._value)

    def to_float(self):
        """Returns the value as a float."""
        if self._value is None:
            sf = self._scale_factor
            return float(self._mantissa + MAPPINGS.get(sf, [sf])[0])
        else:
            return self._value

    def to_unitless_str(self):
        """Renders the value as a string in floating point notation.

        The original string is returned with units removed and the scale factor
        converted to exponential form. This allows you access to the value
        specified without any loss of precision if the value was specified as a
        string.
        """
        if self._value is None:
            sf = self._scale_factor
            return self._mantissa + MAPPINGS.get(sf, [sf])[0]
        else:
            return num_to_str(self._value)

    def to_unitless_eng(self, prec=None):
        "Renders the value as a string in engineering notation."
        # this is a bit of a hack, temporarily remove the units
        units = self.units
        self.units = None
        eng_number = self.to_eng(prec)
        self.units = units
        return eng_number

    def to_tuple(self):
        "Returns a tuple that contains the value as a float and the units."
        return self.to_float(), self.units

    def to_str(self):
        "Renders the value and units as a string in floating point notation."
        number = self.to_unitless_str()
        units = self.units
        return _combine(number, '', units, Spacer)

    def to_eng(self, prec=None):
        "Renders the value and units as a string in engineering notation."

        # determine precision
        if prec is None:
            prec = HumanPrecision
        else:
            prec = int(prec)
        assert (prec >= 0)

        # check for infinities or NaN
        if self.is_infinite() or self.is_nan():
            return _combine(self.strip(), '', self.units, ' ')

        # convert into scientific notation with proper precision
        value = self.to_float()
        units = self.units
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

        # remove trailing zeros (except if mantissa does not contain a .)
        if mantissa.find('.') >= 0:
            mantissa = mantissa.rstrip("0")

        # remove trailing decimal point
        mantissa = mantissa.rstrip(".")

        return _combine(mantissa, sf, units, Spacer)

    def to_sci(self, prec=None):
        "Renders the value and units as a string in scientific notation."

        # determine precision
        if prec is None:
            prec = HumanPrecision
        else:
            prec = int(prec)
        assert (prec >= 0)

        # check for infinities or NaN
        if self.is_infinite() or self.is_nan():
            return _combine(self.strip(), '', self.units, ' ')

        # convert into scientific notation with proper precision
        value = self.to_float()
        units = self.units
        number = "%.*e" % (prec, value)
        mantissa, exp = number.split("e")
        exp = exp.replace('+', '')
        superscripts = str.maketrans('-0123456789', '⁻⁰¹²³⁴⁵⁶⁷⁸⁹')
        sf = '×10' + exp.translate(superscripts)
        return _combine(mantissa, sf, units, '')

    def __str__(self):
        return self.to_eng()

    def __format__(self, fmt):
        """Convert quantity to string for Python string format function.

        Supports the normal floating point and string format types as well
        'q', 'r' and 'u'.  All will output the number using the SI scale
        factors, but the 's' and 'q' types also include the units.

        The format is specified using AW.PT where:
        A is character and gives the alignment: either '', '>', or '<'
        W is integer and gives the width
        P is integer and gives the precision
        T is char and gives the type: choose from q, r, s, e, f, g, u, n, d, ...
           q = quantity (1.4204GHz)
           r = real (1.4204G)
           s = string (1.4204GHz)
           e = exponential form (1.4204e9)
           f, F = float (1420400000.000000)
           g, G = float (1.4204e+09)
           u = units (Hz)
           n = name (f)
           d = description (hydrogen line)
           Q = name and quantity (f = 1.4204GHz)
           R = name and real (f = 1.4204G)
        """
        match = format_spec.match(fmt)
        if match:
            align, width, prec, ftype = match.groups()
            if ftype in 'qs':
                value = self.to_eng(prec)
                return '{0:{1}{2}s}'.format(value, align, width)
            elif ftype == 'r':
                value = self.to_unitless_eng(prec)
                return '{0:{1}{2}s}'.format(value, align, width)
            elif ftype == 'u':
                value = self.units
                return '{0:{1}{2}s}'.format(value, align, width)
            elif ftype == 'n':
                value = getattr(self, 'name', '')
                return '{0:{1}{2}s}'.format(value, align, width)
            elif ftype == 'd':
                value = getattr(self, 'desc', '')
                return '{0:{1}{2}s}'.format(value, align, width)
            elif ftype in 'Q':
                name = getattr(self, 'name', '')
                desc = getattr(self, 'desc', '')
                value = self.to_eng(prec)
                if name:
                    value = AssignmentFormatter.format(n=name, v=value, d=desc)
                return '{0:{1}{2}s}'.format(value, align, width)
            elif ftype in 'R':
                name = getattr(self, 'name', '')
                desc = getattr(self, 'desc', '')
                value = self.to_unitless_eng(prec)
                if name:
                    value = AssignmentFormatter.format(n=name, v=value, d=desc)
                return '{0:{1}{2}s}'.format(value, align, width)
            else:
                value = self.to_float()
                return '{0:{1}}'.format(value, fmt)
        else:
            return self.to_eng()

    def __float__(self):
        return self.to_float()


# Shortcut functions {{{1
def quant_to_tuple(value, units=None):
    return Quantity(value, units).to_tuple()

def quant_to_eng(value, units=None, prec=None):
    return Quantity(value, units).to_eng(prec)

def quant_to_str(value, units=None):
    return Quantity(value, units).to_str()

def quant_to_float(value, units=None):
    return Quantity(value, units).to_float()

def quant_to_unitless_eng(value, units=None, prec=None):
    return Quantity(value, units).to_unitless_eng(prec)

def quant_to_unitless_str(value, units=None):
    return Quantity(value, units).to_unitless_str()

def quant_strip(value):
    return Quantity(value).strip()

# Text processing functions {{{1
# All to engineering format {{{2
def all_to_eng_fmt(text):
    """Convert all quantities found in text to engineering format.

    It is assumed that any units are assumed to be simple, meaning that they
    contain only alphabetic characters (no numbers or symbols)."""
    out = []
    start = 0
    for match in embedded_floating_point_notation.finditer(text):
        end = match.start(0)
        number = match.group(0)
        try:
            number = quant_to_eng(number)
        except ValueError:  # pragma: no cover
            # something unexpected happened
            # but this is not essential, so ignore it
            pass
        out.append(text[start:end] + number)
        start = match.end(0)
    return ''.join(out) + text[start:]

# All from engineering format {{{2
def all_from_eng_fmt(text):
    """Convert all occurrences of quantities found in text to engineering format

    It is assumed that there is no space between the number and the scale factor
    and any units are assumed to be simple, meaning that they contain only
    alphabetic characters (no numbers or symbols)."""
    out = []
    start = 0
    for match in embedded_engineering_notation.finditer(text):
        end = match.start(0)
        number = match.group(0)
        try:
            number = quant_to_str(number)
        except ValueError:  # pragma: no cover
            # something unexpected happened
            # but this is not essential, so ignore it
            pass
        out.append(text[start:end] + number)
        start = match.end(0)
    return ''.join(out) + text[start:]

# Add to namespace {{{1
assignment = re.compile(
    r'\A\s*(?:(\w+)\s*=\s*)?(.*?)(?:\s*--\s*(.*?)\s*)?\Z'
)

def add_to_namespace(quantities):
    """ Add to Namespace

    Takes a string that contains quantity definitions and places those
    quantities in the calling namespace. The string may contain one definition
    per line, of the form:
        <name> = <value> -- <description>
    The description is discarded.
    """
    # Access the namespace of the calling frame
    import inspect
    frame = inspect.stack()[1][0]
    namespace = frame.f_globals

    for line in quantities.splitlines():
        match = assignment.match(line)
        if match:
            name, value, desc = match.groups()
            if not value:
                continue
            if not name:
                raise ValueError('{}: no variable name given.'.format(line))
            quantity = Quantity(value)
            quantity.add_name(name)
            quantity.add_desc(desc)
            namespace[name] = quantity
        else:  # pragma: no cover
            raise ValueError('{}: not a valid number.'.format(line))
