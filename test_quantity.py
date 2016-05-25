from engfmt import Quantity, set_preferences

class TestCase:
    def __init__(self, name, text, raw, formatted, prefs=None):
        self.name = name
        self.text = text
        self.raw = raw
        self.formatted = formatted
        self.prefs = prefs

test_cases = [
    TestCase('grange', '0', ('0', ''), '0'),
    TestCase('waltz', '0s', ('0', 's'), '0s'),
    TestCase('allay', '0 s', ('0', 's'), '0s'),
    TestCase('tribute', '$0', ('0', '$'), '$0'),
    TestCase('lunatic', '1', ('1', ''), '1'),
    TestCase('seafront', '1s', ('1', 's'), '1s'),
    TestCase('birthday', '1 s', ('1', 's'), '1s'),
    TestCase('energy', '$1', ('1', '$'), '$1'),

    # test all the scale factors
    TestCase('quill', '1ys', ('1e-24', 's'), '1e-24s'),
    TestCase('joust', '1zs', ('1e-21', 's'), '1e-21s'),
    TestCase('streak', '1as', ('1e-18', 's'), '1as'),
    TestCase('mutiny', '1fs', ('1e-15', 's'), '1fs'),
    TestCase('banker', '1ps', ('1e-12', 's'), '1ps'),
    TestCase('conquer', '1ns', ('1e-9', 's'), '1ns'),
    TestCase('share', '1us', ('1e-6', 's'), '1us'),
    TestCase('witch', '1ms', ('1e-3', 's'), '1ms'),
    TestCase('finance', '1_s', ('1', 's'), '1s'),
    TestCase('ecologist', '1ks', ('1e3', 's'), '1ks'),
    TestCase('insulate', '1Ks', ('1e3', 's'), '1ks'),
    TestCase('apprehend', '1Ms', ('1e6', 's'), '1Ms'),
    TestCase('hoarding', '1Gs', ('1e9', 's'), '1Gs'),
    TestCase('scrum', '1Ts', ('1e12', 's'), '1Ts'),
    TestCase('tissue', '1Ps', ('1e15', 's'), '1e15s'),
    TestCase('panorama', '1Es', ('1e18', 's'), '1e18s'),
    TestCase('quest', '1Zs', ('1e21', 's'), '1e21s'),
    TestCase('suture', '1Ys', ('1e24', 's'), '1e24s'),

    # test various forms of the mantissa when using scale factors
    TestCase('delicacy', '1ns', ('1e-9', 's'), '1ns'),
    TestCase('huntsman', '1 ns', ('1e-9', 's'), '1ns'),
    TestCase('weighty', '10ns', ('10e-9', 's'), '10ns'),
    TestCase('madrigal', '100ns', ('100e-9', 's'), '100ns'),
    TestCase('comport', '.1ns', ('.1e-9', 's'), '100ps'),
    TestCase('character', '.1 ns', ('.1e-9', 's'), '100ps'),
    TestCase('sharpen', '.10ns', ('.10e-9', 's'), '100ps'),
    TestCase('resonate', '.100ns', ('.100e-9', 's'), '100ps'),
    TestCase('replica', '1.ns', None, '1ns'),
    TestCase('parachute', '1. ns', None, '1ns'),
    TestCase('merger', '10.ns', None, '10ns'),
    TestCase('grating', '100.ns', None, '100ns'),
    TestCase('enjoyment', '1.0ns', ('1.0e-9', 's'), '1ns'),
    TestCase('refit', '1.0 ns', ('1.0e-9', 's'), '1ns'),
    TestCase('thread', '10.0ns', ('10.0e-9', 's'), '10ns'),
    TestCase('upright', '100.0ns', ('100.0e-9', 's'), '100ns'),
    TestCase('inscribe', '1.00ns', ('1.00e-9', 's'), '1ns'),
    TestCase('warrior', '1.00 ns', ('1.00e-9', 's'), '1ns'),
    TestCase('paranoiac', '10.00ns', ('10.00e-9', 's'), '10ns'),
    TestCase('genie', '100.00ns', ('100.00e-9', 's'), '100ns'),
    TestCase('persimmon', '-1.00ns', ('-1.00e-9', 's'), '-1ns'),
    TestCase('barnacle', '-1.00 ns', ('-1.00e-9', 's'), '-1ns'),
    TestCase('dialog', '-10.00ns', ('-10.00e-9', 's'), '-10ns'),
    TestCase('bright', '-100.00ns', ('-100.00e-9', 's'), '-100ns'),
    TestCase('mutate', '+1.00ns', ('+1.00e-9', 's'), '1ns'),
    TestCase('session', '+1.00 ns', ('+1.00e-9', 's'), '1ns'),
    TestCase('capillary', '+10.00ns', ('+10.00e-9', 's'), '10ns'),
    TestCase('twinkle', '+100.00ns', ('+100.00e-9', 's'), '100ns'),

    # test various forms of the mantissa when using exponents
    TestCase('hairpiece', '1e-9s', ('1e-9', 's'), '1ns'),
    TestCase('marble', '10E-9s', ('10e-9', 's'), '10ns'),
    TestCase('boomerang', '100e-9s', ('100e-9', 's'), '100ns'),
    TestCase('antiquity', '.1e-9s', ('.1e-9', 's'), '100ps'),
    TestCase('redhead', '.10E-9s', ('.10e-9', 's'), '100ps'),
    TestCase('rarity', '.100e-9s', ('.100e-9', 's'), '100ps'),
    TestCase('latecomer', '1.e-9s', None, '1ns'),
    TestCase('blackball', '10.E-9s', None, '10ns'),
    TestCase('sweetener', '100.e-9s', None, '100ns'),
    TestCase('kidney', '1.0E-9s', ('1.0e-9', 's'), '1ns'),
    TestCase('erode', '10.0e-9s', ('10.0e-9', 's'), '10ns'),
    TestCase('omelet', '100.0E-9s', ('100.0e-9', 's'), '100ns'),
    TestCase('mealy', '1.00e-9s', ('1.00e-9', 's'), '1ns'),
    TestCase('chaser', '10.00E-9s', ('10.00e-9', 's'), '10ns'),
    TestCase('skitter', '100.00e-9s', ('100.00e-9', 's'), '100ns'),
    TestCase('romantic', '-1.00E-9s', ('-1.00e-9', 's'), '-1ns'),
    TestCase('bohemian', '-10.00e-9s', ('-10.00e-9', 's'), '-10ns'),
    TestCase('forbid', '-100.00E-9s', ('-100.00e-9', 's'), '-100ns'),
    TestCase('quartet', '+1.00e-9s', ('+1.00e-9', 's'), '1ns'),
    TestCase('presume', '+10.00E-9s', ('+10.00e-9', 's'), '10ns'),
    TestCase('trouper', '+100.00e-9s', ('+100.00e-9', 's'), '100ns'),
    TestCase('particle', '+.1E-9s', ('+.1e-9', 's'), '100ps'),
    TestCase('defeat', '+.10e-9s', ('+.10e-9', 's'), '100ps'),
    TestCase('oxcart', '+.100E-9s', ('+.100e-9', 's'), '100ps'),
    TestCase('creaky', '-.1e-9s', ('-.1e-9', 's'), '-100ps'),
    TestCase('gentleman', '-.10E-9s', ('-.10e-9', 's'), '-100ps'),
    TestCase('spangle', '-.100e-9s', ('-.100e-9', 's'), '-100ps'),

    # test various forms of the mantissa alone
    TestCase('educate', '100000.0s', ('100000.0', 's'), '100ks'),
    TestCase('headline', '100000 s', ('100000', 's'), '100ks'),
    TestCase('protein', '10000s', ('10000', 's'), '10ks'),
    TestCase('increase', '10000.0 s', ('10000.0', 's'), '10ks'),
    TestCase('response', '1000.0s', ('1000.0', 's'), '1ks'),
    TestCase('parodist', '1000 s', ('1000', 's'), '1ks'),
    TestCase('speck', '100s', ('100', 's'), '100s'),
    TestCase('chihuahua', '100.0 s', ('100.0', 's'), '100s'),
    TestCase('couch', '10.0s', ('10.0', 's'), '10s'),
    TestCase('highbrow', '10 s', ('10', 's'), '10s'),
    TestCase('haughty', '1s', ('1', 's'), '1s'),
    TestCase('break', '1.0 s', ('1.0', 's'), '1s'),
    TestCase('gutter', '0.1s', ('0.1', 's'), '100ms'),
    TestCase('ability', '0.1 s', ('0.1', 's'), '100ms'),
    TestCase('atone', '0.01s', ('0.01', 's'), '10ms'),
    TestCase('essential', '0.01 s', ('0.01', 's'), '10ms'),
    TestCase('godmother', '0.001s', ('0.001', 's'), '1ms'),
    TestCase('temper', '0.001 s', ('0.001', 's'), '1ms'),
    TestCase('verse', '0.0001s', ('0.0001', 's'), '100us'),
    TestCase('fifth', '0.0001 s', ('0.0001', 's'), '100us'),
    TestCase('horsewhip', '0.00001s', ('0.00001', 's'), '10us'),
    TestCase('larch', '0.00001 s', ('0.00001', 's'), '10us'),

    # test various forms of units
    TestCase('impute', '1ns', ('1e-9', 's'), '1ns'),
    TestCase('eyesore', '1e-9s', ('1e-9', 's'), '1ns'),
    TestCase('aspirant', '1n', ('1e-9', ''), '1n'),
    TestCase('delete', '1e-9', ('1e-9', ''), '1n'),
    TestCase('flummox', '1 ns', ('1e-9', 's'), '1ns'),
    TestCase('foster', '1 e-9 s', None, '1ns'),
    TestCase('deforest', '1n s', None, '1ns'),
    TestCase('fortune', '1e-9 s', ('1e-9', 's'), '1ns'),
    TestCase('starchy', '1nm/s', ('1e-9', 'm/s'), '1nm/s'),
    TestCase('preamble', '1e-9m/s', ('1e-9', 'm/s'), '1nm/s'),
    TestCase('haversack', '1 nm/s', ('1e-9', 'm/s'), '1nm/s'),
    TestCase('sprinter', '1e-9 m/s', ('1e-9', 'm/s'), '1nm/s'),
    TestCase('descend', '1nJ-s', ('1e-9', 'J-s'), '1nJ-s'),
    TestCase('milieu', '1e-9J-s', ('1e-9', 'J-s'), '1nJ-s'),
    TestCase('force', '1 nJ-s', ('1e-9', 'J-s'), '1nJ-s'),
    TestCase('athletic', '1e-9 J-s', ('1e-9', 'J-s'), '1nJ-s'),
    TestCase('scaffold', '1nm(s^-1)', ('1e-9', 'm(s^-1)'), '1nm(s^-1)'),
    TestCase('incur', '1e-9m(s^-1)', ('1e-9', 'm(s^-1)'), '1nm(s^-1)'),
    TestCase('hornet', '1 nm(s^-1)', ('1e-9', 'm(s^-1)'), '1nm(s^-1)'),
    TestCase('fledgling', '1e-9 m(s^-1)', ('1e-9', 'm(s^-1)'), '1nm(s^-1)'),
    TestCase('amnesty', '1nm/s^2', ('1e-9', 'm/s^2'), '1nm/s^2'),
    TestCase('carpet', '1e-9m/s^2', ('1e-9', 'm/s^2'), '1nm/s^2'),
    TestCase('intrigue', '1 nm/s^2', ('1e-9', 'm/s^2'), '1nm/s^2'),
    TestCase('picky', '1e-9 m/s^2', ('1e-9', 'm/s^2'), '1nm/s^2'),

    # test currency
    TestCase('bishop', '$10K', ('10e3', '$'), '$10k'),
    TestCase('colonnade', '$10', ('10', '$'), '$10'),
    TestCase('wizard', '$10.00', ('10.00', '$'), '$10'),
    TestCase('stork', '$10e9', ('10e9', '$'), '$10G'),
    TestCase('walkover', '$0.01', ('0.01', '$'), '$10m'),
    TestCase('kinswoman', '$.01', ('.01', '$'), '$10m'),
    TestCase('valuable', '$1.', None, '$1'),
    TestCase('kiddie', '-$10K', ('-10e3', '$'), '-$10k'),
    TestCase('breather', '-$10', ('-10', '$'), '-$10'),
    TestCase('recoil', '-$10.00', ('-10.00', '$'), '-$10'),
    TestCase('wrestle', '-$10e9', ('-10e9', '$'), '-$10G'),
    TestCase('theorist', '-$0.01', ('-0.01', '$'), '-$10m'),
    TestCase('neurone', '-$.01', ('-.01', '$'), '-$10m'),
    TestCase('crevice', '-$1.', None, '-$1'),
    TestCase('bodice', '+$10K', ('+10e3', '$'), '$10k'),
    TestCase('homicide', '+$10', ('+10', '$'), '$10'),
    TestCase('resurface', '+$10.00', ('+10.00', '$'), '$10'),
    TestCase('guidebook', '+$10e9', ('+10e9', '$'), '$10G'),
    TestCase('weaken', '+$0.01', ('+0.01', '$'), '$10m'),
    TestCase('subtlety', '+$.01', ('+.01', '$'), '$10m'),
    TestCase('flywheel', '+$1.', None, '$1'),

    # unusual numbers
    TestCase('sheathe', 'inf', ('inf', ''), 'inf'),
    TestCase('integrate', 'inf Hz', ('inf', 'Hz'), 'inf Hz'),
    TestCase('witter', '$inf', ('inf', '$'), '$inf'),
    TestCase('smoker', '-inf', ('-inf', ''), '-inf'),
    TestCase('spittoon', '-inf Hz', ('-inf', 'Hz'), '-inf Hz'),
    TestCase('outcome', '-$inf', ('-inf', '$'), '-$inf'),
    TestCase('baroness', 'nan', ('nan', ''), 'nan'),
    TestCase('province', 'nan Hz', ('nan', 'Hz'), 'nan Hz'),
    TestCase('infidel', '$nan', ('nan', '$'), '$nan'),
    TestCase('honey', '+nan', ('+nan', ''), 'nan'),
    TestCase('frighten', '+nan Hz', ('+nan', 'Hz'), 'nan Hz'),
    TestCase('acrobat', '+$nan', ('+nan', '$'), '$nan'),
    TestCase('firefly', 'INF', ('inf', ''), 'inf'),
    TestCase('farmland', 'INF Hz', ('inf', 'Hz'), 'inf Hz'),
    TestCase('osteopath', '$INF', ('inf', '$'), '$inf'),
    TestCase('chickpea', '-INF', ('-inf', ''), '-inf'),
    TestCase('bawdy', '-INF Hz', ('-inf', 'Hz'), '-inf Hz'),
    TestCase('pursuer', '-$INF', ('-inf', '$'), '-$inf'),
    TestCase('suffuse', 'NAN', ('nan', ''), 'nan'),
    TestCase('vacillate', 'NAN Hz', ('nan', 'Hz'), 'nan Hz'),
    TestCase('tangerine', '$NAN', ('nan', '$'), '$nan'),
    TestCase('southward', '+NAN', ('+nan', ''), 'nan'),
    TestCase('wander', '+NAN Hz', ('+nan', 'Hz'), 'nan Hz'),
    TestCase('stack', '+$NAN', ('+nan', '$'), '$nan'),

    # preferences
    TestCase('flotation', '1420.405751786 MHz', ('1420.405751786e6', 'Hz'), '1GHz', {'prec':0}),
    TestCase('bodyguard', '1420.405751786 MHz', ('1420.405751786e6', 'Hz'), '1.4GHz', {'prec':1}),
    TestCase('radiogram', '1420.405751786 MHz', ('1420.405751786e6', 'Hz'), '1.42GHz', {'prec':2}),
    TestCase('omnibus', '1420.405751786 MHz', ('1420.405751786e6', 'Hz'), '1.42GHz', {'prec':3}),
    TestCase('transmit', '1420.405751786 MHz', ('1420.405751786e6', 'Hz'), '1.4204GHz', {'prec':4}),
    TestCase('morality', '1420.405751786 MHz', ('1420.405751786e6', 'Hz'), '1.42041GHz', {'prec':5}),
    TestCase('reward', '1420.405751786 MHz', ('1420.405751786e6', 'Hz'), '1.420406GHz', {'prec':6}),
    TestCase('smudge', '1420.405751786 MHz', ('1420.405751786e6', 'Hz'), '1.4204058GHz', {'prec':7}),
    TestCase('animator', '1420.405751786 MHz', ('1420.405751786e6', 'Hz'), '1.42040575GHz', {'prec':8}),
    TestCase('woodwind', '1420.405751786 MHz', ('1420.405751786e6', 'Hz'), '1.420405752GHz', {'prec':9}),
    TestCase('underpay', '1420.405751786 MHz', ('1420.405751786e6', 'Hz'), '1.4204057518GHz', {'prec':10}),
    TestCase('horoscope', '1420.405751786 MHz', ('1420.405751786e6', 'Hz'), '1.42040575179GHz', {'prec':11}),
    TestCase('drivel', '1420.405751786 MHz', ('1420.405751786e6', 'Hz'), '1.420405751786GHz', {'prec':12}),
    TestCase('railcard', '1420.405751786 MHz', ('1420.405751786e6', 'Hz'), '1.420405751786GHz', {'prec':13}),
    TestCase('elixir', '1420.405751786 MHz', ('1420.405751786e6', 'Hz'), '1.4204 GHz', {'prec':None, 'spacer':' '}),
    TestCase('henna', '3.141592 Hz', ('3.141592', 'Hz'), '3.1416_Hz', {'unity':'_', 'spacer':''}),
    TestCase('eastward', '3.141592 Hz', ('3.141592', 'Hz'), '3.1416 Hz', {'spacer':' '}),
    TestCase('string', '1420.405751786 MHz', ('1420.405751786e6', 'Hz'), '1.4204e9 Hz', {'output':''}),
]

names = set()
def test_number_recognition():
    for case in test_cases:
        assert case.name not in names
        names.add(case.name)
        try:
            if case.prefs:
                set_preferences(**case.prefs)
            q = Quantity(case.text)
            assert ((q.to_flt_number(), q.units()) == case.raw), case.name
            assert (str(q) == case.formatted), case.name
            # assure that the output value can be read as an input
            Quantity(str(q))
        except AssertionError:
            raise
        except ValueError:
            assert None is case.raw, case.name
        except Exception:
            print('%s: unexpected exception occurred.' % case.name)
            raise
    set_preferences(prec=None, spacer=None, unity=None, output=None)
