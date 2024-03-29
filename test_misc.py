# encoding: utf8

from engfmt import *
import pytest
set_preferences(spacer=' ')

def test_misc():
    q=Quantity(1420405751.786, 'Hz')
    assert q.strip() == '1.42040575e+09'

    t=quant_to_tuple('1420405751.786 Hz')
    assert t == (1420405751.786, 'Hz')

    t=quant_to_eng('1420405751.786 Hz')
    assert t == '1.4204 GHz'

    # fails for python2
    #t=quant_to_sci('1420405751.786 Hz')
    #assert t == '1.4204×10⁰⁹ Hz'

    s=quant_to_str('1420405751.786 Hz')
    assert s == '1420405751.786 Hz'

    f=quant_to_float('1420405751.786 Hz')
    assert f == 1420405751.786

    t=quant_to_unitless_eng('1420405751.786 Hz')
    assert t == '1.4204G'

    s=quant_to_unitless_str('1420405751.786 Hz')
    assert s == '1420405751.786'

    s=quant_to_unitless_str(1420405751.786, 'Hz')
    assert s == '1.42040575e+09'

    f=quant_strip('1420405751.786 Hz')
    assert f == '1420405751.786'

    f=quant_strip('14204.05751786MHz')
    assert f == '14204.05751786M'

    q=Quantity('1420405751.786 Hz', 'Hz')
    assert q.strip() == '1420405751.786'

    q=Quantity('1420405751.786 Hz')
    assert q.is_nan() == False

    q=Quantity('1420405751.786 Hz')
    assert q.is_infinite() == False

    q=Quantity('NaN Hz')
    assert q.is_nan() == True

    q=Quantity('NaN Hz')
    assert q.is_infinite() == False

    q=Quantity('inf Hz')
    assert q.is_nan() == False

    q=Quantity('inf Hz')
    assert q.is_infinite() == True

    with pytest.raises(AssertionError):
        q=Quantity('1420405751.786 Hz', 'Ohms')

    with pytest.raises(ValueError):
        add_to_namespace('1ns')

    with pytest.raises(ValueError):
        add_to_namespace('x*y = z')
