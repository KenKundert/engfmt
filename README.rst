engfmt - Engineering Format
===========================

A light-weight package used to read and write numbers in engineering format. In 
engineering format a number generally includes the units if available and uses 
SI scale factors to indicate the magnitude of the number. For example:

   | 1ns
   | 1.4204GHz

A quantity is the pairing of a real number and units, though the units may be 
empty. This package is designed to convert quantities between the various ways 
in which they are represented.  Those ways are:

As a tuple:
    For example, 1ns would be represented as (1e-9, 's').
    Notice that the scale factor is not included in the units. This is always 
    true.

As a string:
    For example, 1ns would be represented as '1e-9 s' or as '0.000000001s'. This 
    form is often difficult to read for people and so *engfmt* treats it more as 
    a format meant for machines rather than people.

As text:
    For example, 1ns would be represented as '1ns'.  This form is often 
    difficult to read for machines and so *engfmt* treats it more as a human 
    readable format.

Here the distinction between string and text is unusual and needs to be 
clarified. Of course both are strings, but in using the term string, a computer 
science term, I am suggesting a textual representation that is meant to be 
consumed by a computer. Conversely, the term text suggests a form that is meant 
to be consumed by people.

The *Quantity* class is provided for converting between these various forms. It 
takes one or two arguments. The first is taken to be the value, and the second, 
if given, is taken to be the units.  The value may be given as a float or as 
a string. The string may be in floating point notation, in scientific notation, 
or in engineering format and may include the units. By engineering notation, it 
is meant that the number can use the SI scale factors. For example, any of the 
following ways can be used to specify 1ns:

.. code-block:: python

    >>> from engfmt import Quantity
    >>> period = Quantity(1e-9, 's')
    >>> print(period)
    1ns

    >>> period = Quantity('0.000000001 s')
    >>> print(period)
    1ns

    >>> period = Quantity('1e-9s')
    >>> print(period)
    1ns

    >>> period = Quantity('1ns')
    >>> print(period)
    1ns

In all cases, the giving the units is optional.

From a quantity object, you can generate any representation:

.. code-block:: python

    >>> h_line = Quantity('1420.405751786 MHz')

    >>> h_line.to_tuple()
    (1420405751.786, 'Hz')

    >>> h_line.to_text()
    '1.4204GHz'

    >>> h_line.to_str()
    '1420.405751786e6Hz'

You can also access the value without the units::

    >>> h_line.to_float()
    1420405751.786

    >>> h_line.to_text_strip()
    '1.4204G'

    >>> h_line.to_str_strip()
    '1420.405751786e6'

Or you can access just the units::

    >>> h_line.units
    'Hz'


Shortcut Functions
------------------

Generally one uses the shortcut functions to convert numbers to and from 
engineering format. All of these functions take the value and units in the same 
ways that they are specified to Quantity.  In particular, the value may be 
a string or a real number.  If it is a string it may be given in traditional 
format or in engineering format, and it may include the units.  For example:

.. code-block:: python

   >>> from engfmt import to_tuple
   >>> to_tuple('1.4204GHz')
   (1420400000.0, 'Hz')

   >>> from engfmt import to_text
   >>> to_text(1420400000.0, 'Hz')
   '1.4204GHz'

   >>> from engfmt import to_str
   >>> to_str(1420400000.0, 'Hz')
   '1.4204e+09Hz'

   >>> from engfmt import to_float
   >>> to_float('1.4204GHz')
   1420400000.0

   >>> from engfmt import to_str_strip
   >>> to_str_strip('1.4204GHz')
   '1.4204e9'

   >>> from engfmt import to_text_strip
   >>> to_text_strip('1.4204e9Hz')
   '1.4204G'

   >>> from engfmt import strip
   >>> strip('1.4204GHz')
   '1.4204G'
   >>> strip('1.4204e9Hz')
   '1.4204e9'

Notice that the output of base functions always include the units and the output 
of *_strip* functions do not.

The output of the *to_text_strip* and *to_text* is always rounded to the 
desired precision, which can be specified as an argument to these functions.
This differs from the *to_str_strip* and *to_str* functions. They attempt to 
retain the original format of the number if it is specified as a string. In this 
way it retains its original precision. The underlying assumption behind this 
difference is that engineering notation is generally used when communicating 
with people, whereas floating point notation is used when communicating with 
machines. People benefit from having a limited number of digits in the numbers, 
whereas machines benefit from have full precision numbers.


Preferences
-----------

You can adjust some of the behavior of these functions on a global basis using 
*set_preferences*:

.. code-block:: python

   >>> from engfmt import set_preferences
   >>> set_preferences(hprec=2, spacer=' ')
   >>> to_text('1.4204GHz')
   '1.42 GHz'
   >>> to_text('1.4204GHz', prec=4)
   '1.4204 GHz'

Specifying *hprec* to be 4 gives 5 digits of precision (you get one more digit 
than the number you specify for precision). Thus, the valid range for *prec* is 
from 0 to around 12 to 14 for double precision numbers.

Passing *None* as a value in *set_preferences* returns that preference to its 
default value:

.. code-block:: python

   >>> set_preferences(hprec=None, spacer=None)
   >>> to_text('1.4204GHz')
   '1.4204GHz'


Quantity Class
--------------

Though rarely used directly, the Quantity class forms the foundation of the 
engfmt package. It is more flexible than the shortcut functions:

.. code-block:: python

   >>> from engfmt import Quantity
   >>> h_line = Quantity('1420.405751786 MHz')

   >>> str(h_line)
   '1.4204GHz'

   >>> float(h_line)
   1420405751.786

   >>> h_line.to_tuple()
   (1420405751.786, 'Hz')

   >>> h_line.to_text(7)
   '1.4204058GHz'

   >>> h_line.to_str()
   '1420.405751786e6Hz'

   >>> h_line.to_float()
   1420405751.786

   >>> h_line.to_text_strip(4)
   '1.4204G'

   >>> h_line.to_str_strip()
   '1420.405751786e6'

   >>> h_line.strip()
   '1420.405751786M'

   >>> h_line.units
   'Hz'

   >>> h_line.add_name('Fhy')
   >>> h_line.name
   'Fhy'

   >>> h_line.add_desc('frequency of hydrogen line')
   >>> h_line.desc
   'frequency of hydrogen line'

   >>> h_line.is_infinite()
   False

   >>> h_line.is_nan()
   False


Physical Constants
------------------

The Quantity class also supports a small number of physical constants (you can 
modify the source code if you would like to add more).

Plank's constant:

.. code-block:: python

   >>> plank = Quantity('h')
   >>> print(plank)
   662.61e-36J-s

Boltzmann's constant:

.. code-block:: python

   >>> boltz = Quantity('k')
   >>> print(boltz)
   13.806e-24J/K

Elementary charge:

.. code-block:: python

   >>> q = Quantity('q')
   >>> print(q)
   160.22e-21C

Speed of light:

.. code-block:: python

   >>> c = Quantity('c')
   >>> print(c)
   299.79Mm/s

Zero degrees Celsius in Kelvin:

.. code-block:: python

   >>> zeroC = Quantity('C0')
   >>> print(zeroC)
   273.15K

*engfmt* uses *k* rather than *K* to represent kilo so that you can distinguish 
between kilo and Kelvin.

Permittivity of free space:

.. code-block:: python

   >>> eps0 = Quantity('eps0')
   >>> print(eps0)
   8.8542pF/m

Permeability of free space:

.. code-block:: python

   >>> mu0 = Quantity('mu0')
   >>> print(mu0)
   1.2566uH/m

Characteristic impedance of free space:

.. code-block:: python

   >>> Z0 = Quantity('Z0')
   >>> print(Z0)
   376.73Ohms


String Formatting
-----------------

Quantities can be passed into the string *format* function:

.. code-block:: python

   >>> print('{}'.format(h_line))
   1.4204GHz

You can specify the precision as part of the format specification

.. code-block:: python

   >>> print('{:.6}'.format(h_line))
   1.420406GHz

The 'q' type specifier can be used to explicitly indicate both the number and 
units are desired:

.. code-block:: python

   >>> print('{:.6q}'.format(h_line))
   1.420406GHz

Alternately, 'r' can be used to indicate just the number is desired:

.. code-block:: python

   >>> print('{:r}'.format(h_line))
   1.4204G

Use 'u' to indicate that only the units are desired:

.. code-block:: python

   >>> print('{:u}'.format(h_line))
   Hz

You can also use the string and floating point format type specifiers:

.. code-block:: python

   >>> print('{:f}'.format(h_line))
   1420405751.786000

   >>> print('{:e}'.format(h_line))
   1.420406e+09

   >>> print('{:g}'.format(h_line))
   1.42041e+09

   >>> print('{:s}'.format(h_line))
   1.4204GHz

It is also possible to add a name and perhaps a description to the quantity, and 
access those with special format codes as well:

.. code-block:: python

   >>> h_line.add_name('Fhy')
   >>> h_line.add_desc('frequency of hydrogen line')
   >>> print('{:n}'.format(h_line))
   Fhy

   >>> print('{:d}'.format(h_line))
   frequency of hydrogen line

   >>> print('{:Q}'.format(h_line))
   Fhy = 1.4204GHz

   >>> print('{:R}'.format(h_line))
   Fhy = 1.4204G

   >>> print('{0:Q} ({0:d})'.format(h_line))
   Fhy = 1.4204GHz (frequency of hydrogen line)


Exceptions
----------

A ValueError is raised if engfmt is passed a string it cannot convert into 
a number:

.. code-block:: python

   >>> try:
   ...     value, units = to_tuple('xxx')
   ... except ValueError as err:
   ...     print(err)
   xxx: not a valid number.


Text Processing
---------------

Two functions are available for converting quantities embedded within text to 
and from engineering notation:

.. code-block:: python

   >>> from engfmt import all_to_eng_fmt, all_from_eng_fmt
   >>> all_to_eng_fmt('The frequency of the hydrogen line is 1420405751.786Hz.')
   'The frequency of the hydrogen line is 1.4204GHz.'

   >>> all_from_eng_fmt('The frequency of the hydrogen line is 1.4204GHz.')
   'The frequency of the hydrogen line is 1.4204e9Hz.'


Add to Namespace
----------------

It is possible to put a collection of quantities in a text string and then use 
the *add_to_namespace* function to parse the quantities and add them to the 
Python namespace. For example:

.. code-block:: python

   >>> from engfmt import add_to_namespace

   >>> design_parameters = '''
   ...     Fref = 156 MHz  -- Reference frequency
   ...     Kdet = 88.3 uA  -- Gain of phase detector (Imax)
   ...     Kvco = 9.07 GHz/V  -- Gain of VCO
   ... '''
   >>> add_to_namespace(design_parameters)

   >>> print(Fref, Kdet, Kvco, sep='\n')
   156MHz
   88.3uA
   9.07GHz/V

Any number of quantities may be given, with each quantity given on its own line.  
The identifier given to the left '=' is the name of the variable in the local 
namespace that is used to hold the quantity. The text after the '--' is used as 
a description of the quantity.


Installation
------------

Use 'pip install engfmt' to install. Requires Python2.7 or Python3.3 or better.

.. image:: https://travis-ci.org/KenKundert/engfmt.svg?branch=master
    :target: https://travis-ci.org/KenKundert/engfmt

.. image:: https://coveralls.io/repos/github/KenKundert/engfmt/badge.svg?branch=master
    :target: https://coveralls.io/github/KenKundert/engfmt?branch=master


Testing
-------

Run 'py.test' to run the tests.
