EngFmt - Engineering Format
===========================

A light-weight package used to read and write numbers in engineering format. In 
engineering format a number generally includes the units if available and uses 
SI scale factors to indicate the magnitude of the number. For example:

   | 1ns
   | 1.4204GHz

Generally one uses the shortcut functions to convert numbers to and from 
engineering format:

.. code-block:: python

   >>> from engfmt import from_eng_fmt
   >>> from_eng_fmt('1.4204GHz')
   (1420400000.0, 'Hz')

   >>> from engfmt import to_eng_fmt
   >>> to_eng_fmt(1420400000.0, 'Hz')
   '1.4204GHz'

   >>> from engfmt import strip_units
   >>> strip_units('1.4204GHz')
   '1.4204G'

   >>> from engfmt import to_number
   >>> to_number('1.4204GHz')
   1420400000.0

   >>> from engfmt import to_number_as_str
   >>> to_number_as_str('1.4204GHz')
   '1.4204e9'

You can adjust some of the behavior of these functions on a global basis using 
set_preferences:

.. code-block:: python

   >>> from engfmt import set_preferences
   >>> set_preferences(prec=2, spacer=' ')
   >>> to_eng_fmt('1.4204GHz')
   '1.42 GHz'
   >>> to_eng_fmt('1.4204GHz', prec=4)
   '1.4204 GHz'

Notice that we can specify the number to both to_eng_fmt and from_eng_fmt as 
either a string or as a float and string for the units. Also note that you can 
override the precision on the to_eng_fmt function.

Quantity Class
--------------

Though rarely used, the engfmt package defines the Quantity class, which is 
a bit more flexible than the shortcut functions:

.. code-block:: python

   >>> from engfmt import Quantity
   >>> h_line = Quantity('1420.405751786 MHz')
   >>> str(h_line)
   '1.42 GHz'
   >>> h_line.render(4)
   '1.4204 GHz'
   >>> h_line.value()
   1420405751.786
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
   ...     value, units = from_eng_fmt('xxx')
   ... except ValueError as err:
   ...     print(str(err))
   xxx: not a valid number.


Installation
------------

Use 'pip install engfmt' to install. Requires Python2.6 or Python3.2 or better.

.. image:: https://travis-ci.org/KenKundert/engfmt.svg?branch=master
    :target: https://travis-ci.org/KenKundert/engfmt


Testing
-------

Run 'py.test' to run the tests.
