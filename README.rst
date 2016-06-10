engfmt - Engineering Format
===========================

A light-weight package used to read and write numbers in engineering format. In 
engineering format a number generally includes the units if available and uses 
SI scale factors to indicate the magnitude of the number. For example:

   | 1ns
   | 1.4204GHz

The pairing of a number and units is referred to as a quantity.


Shortcut Functions
------------------

Generally one uses the shortcut functions to convert numbers to and from 
engineering format. All of these functions take a value and units. The value may 
be a string or a real number. If it is a string it may be given in traditional 
format or in engineering format, and it may include the units. For example:

.. code-block:: python

   >>> from engfmt import to_quantity
   >>> to_quantity('1.4204GHz')
   (1420400000.0, 'Hz')

   >>> from engfmt import to_eng_quantity
   >>> to_eng_quantity(1420400000.0, 'Hz')
   '1.4204GHz'

   >>> from engfmt import to_flt_quantity
   >>> to_flt_quantity(1420400000.0, 'Hz')
   '1.4204e+09Hz'

   >>> from engfmt import to_number
   >>> to_number('1.4204GHz')
   1420400000.0

   >>> from engfmt import to_flt_number
   >>> to_flt_number('1.4204GHz')
   '1.4204e9'

   >>> from engfmt import to_eng_number
   >>> to_eng_number('1.4204e9Hz')
   '1.4204G'

   >>> from engfmt import strip_units
   >>> strip_units('1.4204GHz')
   '1.4204G'
   >>> strip_units('1.4204e9Hz')
   '1.4204e9'

Notice that the output of *quanity* functions always include the units and the 
output of *number* functions do not.

The output of the *to_eng_number* and *to_eng_quantity* is always rounded to the 
desired precision, which can be specified as an argument to these functions.
This differs from the *to_flt_number* and *to_flt_quantity* functions. They 
attempt to retain the original format of the number if it is specified as 
a string. In this way it retains its original precision. The underlying 
assumption behind this difference is that engineering notation is generally used 
when communicating with people, whereas floating point notation is used when 
communicating with machines. People benefit from having a limited number of 
digits in the numbers, whereas machines benefit from have full precision 
numbers.


Preferences
-----------

You can adjust some of the behavior of these functions on a global basis using 
*set_preferences*:

.. code-block:: python

   >>> from engfmt import set_preferences
   >>> set_preferences(prec=2, spacer=' ')
   >>> to_eng_quantity('1.4204GHz')
   '1.42 GHz'
   >>> to_eng_quantity('1.4204GHz', prec=4)
   '1.4204 GHz'

Specifying *prec* to be 4 gives 5 digits of precision (you get one more digit 
than the number you specify for precision). Thus, the valid range for *prec* is 
from 0 to around 12 to 14 for double precision numbers.

Passing *None* as a value in *set_preferences* returns that preference to its 
default value:

.. code-block:: python

   >>> set_preferences(prec=None, spacer=None)
   >>> to_eng_quantity('1.4204GHz')
   '1.4204GHz'


Quantity Class
--------------

Though rarely used, the engfmt package defines the Quantity class, which is 
a bit more flexible than the shortcut functions:

.. code-block:: python

   >>> from engfmt import Quantity
   >>> h_line = Quantity('1420.405751786 MHz')

   >>> str(h_line)
   '1.4204GHz'

   >>> float(h_line)
   1420405751.786

   >>> h_line.to_quantity()
   (1420405751.786, 'Hz')

   >>> h_line.to_eng_quantity(4)
   '1.4204GHz'

   >>> h_line.to_flt_quantity()
   '1420.405751786e6Hz'

   >>> h_line.to_number()
   1420405751.786

   >>> h_line.to_eng_number(4)
   '1.4204G'

   >>> h_line.to_flt_number()
   '1420.405751786e6'

   >>> h_line.strip_units()
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
special format codes are available for printing those as well:

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
   ...     value, units = to_quantity('xxx')
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
namespace that is used to hold the quantity. The text after the '--' is ignored 
and is generally used as a description of the quantity.


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
