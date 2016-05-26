engfmt - Engineering Format
===========================

A light-weight package used to read and write numbers in engineering format. In 
engineering format a number generally includes the units if available and uses 
SI scale factors to indicate the magnitude of the number. For example:

   | 1ns
   | 1.4204GHz

The pairing of a number and units is referred to as a quantity.

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
   '1.42e+09Hz'

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

You can adjust some of the behavior of these functions on a global basis using 
*set_preferences*:

.. code-block:: python

   >>> from engfmt import set_preferences
   >>> set_preferences(prec=2, spacer=' ')
   >>> to_eng_quantity('1.4204GHz')
   '1.42 GHz'
   >>> to_eng_quantity('1.4204GHz', prec=4)
   '1.4204 GHz'

Passing *None* as values in *set_preferences* returns the preferences to their 
default values:

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

   >>> h_line.units()
   'Hz'

   >>> h_line.is_infinite()
   False

   >>> h_line.is_nan()
   False

Exceptions
----------

A ValueError is raised if engfmt is passed a string it cannot convert into 
a number:

.. code-block:: python

   >>> try:
   ...     value, units = to_quantity('xxx')
   ... except ValueError as err:
   ...     print(str(err))
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


Installation
------------

Use 'pip install engfmt' to install. Requires Python2.7 or Python3.2 or better.

.. image:: https://travis-ci.org/KenKundert/engfmt.svg?branch=master
    :target: https://travis-ci.org/KenKundert/engfmt


Testing
-------

Run 'py.test' to run the tests.
