from engfmt import Quantity, to_text, set_preferences
set_preferences(spacer=' ')

def test_constants():
    assert '{:.12q}'.format(Quantity('h')) == '662.606957e-36 J-s'
    assert '{:.12q}'.format(Quantity('k')) == '13.806488e-24 J/K'
    assert '{:.12q}'.format(Quantity('q')) == '160.2176565e-21 C'
    assert '{:.12q}'.format(Quantity('c')) == '299.792458 Mm/s'
    assert '{:.12q}'.format(Quantity('C0')) == '273.15 K'
    assert '{:.12q}'.format(Quantity('eps0')) == '8.854187817 pF/m'
    assert '{:.12q}'.format(Quantity('mu0')) == '1.256637061436 uH/m'
    assert '{:.12q}'.format(Quantity('Z0')) == '376.730313461 Ohms'

    assert to_text('h') == '662.61e-36 J-s'
    assert to_text('k') == '13.806e-24 J/K'
    assert to_text('q') == '160.22e-21 C'
    assert to_text('c') == '299.79 Mm/s'
    assert to_text('C0') == '273.15 K'
    assert to_text('eps0') == '8.8542 pF/m'
    assert to_text('mu0') == '1.2566 uH/m'
    assert to_text('Z0') == '376.73 Ohms'
