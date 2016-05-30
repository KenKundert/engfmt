from engfmt import Quantity, set_preferences
set_preferences(spacer=' ')

def test_format():
    q=Quantity('1420.405751786 MHz')
    assert '{}'.format(q) == '1.4204 GHz'
    assert '{:.8q}'.format(q) == '1.42040575 GHz'
    assert '{:.8}'.format(q) == '1.42040575 GHz'
    assert '{:r}'.format(q) == '1.4204G'
    assert '{:f}'.format(q) == '1420405751.786000'
    assert '{:e}'.format(q) == '1.420406e+09'
    assert '{:g}'.format(q) == '1.42041e+09'

    q=Quantity('2n')
    assert float(q) == 2e-9
