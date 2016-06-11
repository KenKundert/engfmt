from engfmt import Quantity, quant_to_eng, set_preferences
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

    assert quant_to_eng('h') == '662.61e-36 J-s'
    assert quant_to_eng('k') == '13.806e-24 J/K'
    assert quant_to_eng('q') == '160.22e-21 C'
    assert quant_to_eng('c') == '299.79 Mm/s'
    assert quant_to_eng('C0') == '273.15 K'
    assert quant_to_eng('eps0') == '8.8542 pF/m'
    assert quant_to_eng('mu0') == '1.2566 uH/m'
    assert quant_to_eng('Z0') == '376.73 Ohms'
