from engfmt import *
import pytest
set_preferences(spacer=' ')

def test_misc():
    q=Quantity(1420405751.786, 'Hz')
    assert q.strip() == '1.42040575e+09'

    t=to_tuple('1420405751.786 Hz')
    assert t == (1420405751.786, 'Hz')

    t=to_text('1420405751.786 Hz')
    assert t == '1.4204 GHz'

    s=to_str('1420405751.786 Hz')
    assert s == '1420405751.786 Hz'

    f=to_float('1420405751.786 Hz')
    assert f == 1420405751.786

    t=to_text_strip('1420405751.786 Hz')
    assert t == '1.4204G'

    s=to_str_strip('1420405751.786 Hz')
    assert s == '1420405751.786'

    s=to_str_strip(1420405751.786, 'Hz')
    assert s == '1.42040575e+09'

    f=strip('1420405751.786 Hz')
    assert f == '1420405751.786'

    f=strip('14204.05751786MHz')
    assert f == '14204.05751786M'

    q=Quantity('1420405751.786 Hz', 'Hz')
    assert q.strip() == '1420405751.786'

    with pytest.raises(AssertionError):
        q=Quantity('1420405751.786 Hz', 'Ohms')

    with pytest.raises(ValueError):
        add_to_namespace('1ns')

    with pytest.raises(ValueError):
        add_to_namespace('x*y = z')
