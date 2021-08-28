from engfmt import Quantity, set_preferences

class Case:
    def __init__(self, name, text, raw, formatted, prefs=None):
        self.name = name
        self.text = text
        self.raw = raw
        self.formatted = formatted
        self.prefs = prefs

test_cases = [
    Case('grange', '0', ('0', ''), '0'),
    Case('waltz', '0s', ('0', 's'), '0s'),
    Case('allay', '0 s', ('0', 's'), '0s'),
    Case('tribute', '$0', ('0', '$'), '$0'),
    Case('lunatic', '1', ('1', ''), '1'),
    Case('seafront', '1s', ('1', 's'), '1s'),
    Case('birthday', '1 s', ('1', 's'), '1s'),
    Case('energy', '$1', ('1', '$'), '$1'),

    # test all the scale factors
    Case('quill', '1ys', ('1e-24', 's'), '1e-24s'),
    Case('joust', '1zs', ('1e-21', 's'), '1e-21s'),
    Case('streak', '1as', ('1e-18', 's'), '1as'),
    Case('mutiny', '1fs', ('1e-15', 's'), '1fs'),
    Case('banker', '1ps', ('1e-12', 's'), '1ps'),
    Case('conquer', '1ns', ('1e-9', 's'), '1ns'),
    Case('share', '1us', ('1e-6', 's'), '1us'),
    Case('witch', '1ms', ('1e-3', 's'), '1ms'),
    Case('finance', '1_s', ('1', 's'), '1s'),
    Case('ecologist', '1ks', ('1e3', 's'), '1ks'),
    Case('insulate', '1Ks', ('1e3', 's'), '1ks'),
    Case('apprehend', '1Ms', ('1e6', 's'), '1Ms'),
    Case('hoarding', '1Gs', ('1e9', 's'), '1Gs'),
    Case('scrum', '1Ts', ('1e12', 's'), '1Ts'),
    Case('tissue', '1Ps', ('1e15', 's'), '1e15s'),
    Case('panorama', '1Es', ('1e18', 's'), '1e18s'),
    Case('quest', '1Zs', ('1e21', 's'), '1e21s'),
    Case('suture', '1Ys', ('1e24', 's'), '1e24s'),

    # test various forms of the mantissa when using scale factors
    Case('delicacy', '1ns', ('1e-9', 's'), '1ns'),
    Case('huntsman', '1 ns', ('1e-9', 's'), '1ns'),
    Case('weighty', '10ns', ('10e-9', 's'), '10ns'),
    Case('madrigal', '100ns', ('100e-9', 's'), '100ns'),
    Case('comport', '.1ns', ('.1e-9', 's'), '100ps'),
    Case('character', '.1 ns', ('.1e-9', 's'), '100ps'),
    Case('sharpen', '.10ns', ('.10e-9', 's'), '100ps'),
    Case('resonate', '.100ns', ('.100e-9', 's'), '100ps'),
    Case('replica', '1.ns', None, '1ns'),
    Case('parachute', '1. ns', None, '1ns'),
    Case('merger', '10.ns', None, '10ns'),
    Case('grating', '100.ns', None, '100ns'),
    Case('enjoyment', '1.0ns', ('1.0e-9', 's'), '1ns'),
    Case('refit', '1.0 ns', ('1.0e-9', 's'), '1ns'),
    Case('thread', '10.0ns', ('10.0e-9', 's'), '10ns'),
    Case('upright', '100.0ns', ('100.0e-9', 's'), '100ns'),
    Case('inscribe', '1.00ns', ('1.00e-9', 's'), '1ns'),
    Case('warrior', '1.00 ns', ('1.00e-9', 's'), '1ns'),
    Case('paranoiac', '10.00ns', ('10.00e-9', 's'), '10ns'),
    Case('genie', '100.00ns', ('100.00e-9', 's'), '100ns'),
    Case('persimmon', '-1.00ns', ('-1.00e-9', 's'), '-1ns'),
    Case('barnacle', '-1.00 ns', ('-1.00e-9', 's'), '-1ns'),
    Case('dialog', '-10.00ns', ('-10.00e-9', 's'), '-10ns'),
    Case('bright', '-100.00ns', ('-100.00e-9', 's'), '-100ns'),
    Case('mutate', '+1.00ns', ('+1.00e-9', 's'), '1ns'),
    Case('session', '+1.00 ns', ('+1.00e-9', 's'), '1ns'),
    Case('capillary', '+10.00ns', ('+10.00e-9', 's'), '10ns'),
    Case('twinkle', '+100.00ns', ('+100.00e-9', 's'), '100ns'),

    # test various forms of the mantissa when using exponents
    Case('hairpiece', '1e-9s', ('1e-9', 's'), '1ns'),
    Case('marble', '10E-9s', ('10e-9', 's'), '10ns'),
    Case('boomerang', '100e-9s', ('100e-9', 's'), '100ns'),
    Case('antiquity', '.1e-9s', ('.1e-9', 's'), '100ps'),
    Case('redhead', '.10E-9s', ('.10e-9', 's'), '100ps'),
    Case('rarity', '.100e-9s', ('.100e-9', 's'), '100ps'),
    Case('latecomer', '1.e-9s', None, '1ns'),
    Case('blackball', '10.E-9s', None, '10ns'),
    Case('sweetener', '100.e-9s', None, '100ns'),
    Case('kidney', '1.0E-9s', ('1.0e-9', 's'), '1ns'),
    Case('erode', '10.0e-9s', ('10.0e-9', 's'), '10ns'),
    Case('omelet', '100.0E-9s', ('100.0e-9', 's'), '100ns'),
    Case('mealy', '1.00e-9s', ('1.00e-9', 's'), '1ns'),
    Case('chaser', '10.00E-9s', ('10.00e-9', 's'), '10ns'),
    Case('skitter', '100.00e-9s', ('100.00e-9', 's'), '100ns'),
    Case('romantic', '-1.00E-9s', ('-1.00e-9', 's'), '-1ns'),
    Case('bohemian', '-10.00e-9s', ('-10.00e-9', 's'), '-10ns'),
    Case('forbid', '-100.00E-9s', ('-100.00e-9', 's'), '-100ns'),
    Case('quartet', '+1.00e-9s', ('+1.00e-9', 's'), '1ns'),
    Case('presume', '+10.00E-9s', ('+10.00e-9', 's'), '10ns'),
    Case('trouper', '+100.00e-9s', ('+100.00e-9', 's'), '100ns'),
    Case('particle', '+.1E-9s', ('+.1e-9', 's'), '100ps'),
    Case('defeat', '+.10e-9s', ('+.10e-9', 's'), '100ps'),
    Case('oxcart', '+.100E-9s', ('+.100e-9', 's'), '100ps'),
    Case('creaky', '-.1e-9s', ('-.1e-9', 's'), '-100ps'),
    Case('gentleman', '-.10E-9s', ('-.10e-9', 's'), '-100ps'),
    Case('spangle', '-.100e-9s', ('-.100e-9', 's'), '-100ps'),

    # test various forms of the mantissa alone
    Case('educate', '100000.0s', ('100000.0', 's'), '100ks'),
    Case('headline', '100000 s', ('100000', 's'), '100ks'),
    Case('protein', '10000s', ('10000', 's'), '10ks'),
    Case('increase', '10000.0 s', ('10000.0', 's'), '10ks'),
    Case('response', '1000.0s', ('1000.0', 's'), '1ks'),
    Case('parodist', '1000 s', ('1000', 's'), '1ks'),
    Case('speck', '100s', ('100', 's'), '100s'),
    Case('chihuahua', '100.0 s', ('100.0', 's'), '100s'),
    Case('couch', '10.0s', ('10.0', 's'), '10s'),
    Case('highbrow', '10 s', ('10', 's'), '10s'),
    Case('haughty', '1s', ('1', 's'), '1s'),
    Case('break', '1.0 s', ('1.0', 's'), '1s'),
    Case('gutter', '0.1s', ('0.1', 's'), '100ms'),
    Case('ability', '0.1 s', ('0.1', 's'), '100ms'),
    Case('atone', '0.01s', ('0.01', 's'), '10ms'),
    Case('essential', '0.01 s', ('0.01', 's'), '10ms'),
    Case('godmother', '0.001s', ('0.001', 's'), '1ms'),
    Case('temper', '0.001 s', ('0.001', 's'), '1ms'),
    Case('verse', '0.0001s', ('0.0001', 's'), '100us'),
    Case('fifth', '0.0001 s', ('0.0001', 's'), '100us'),
    Case('horsewhip', '0.00001s', ('0.00001', 's'), '10us'),
    Case('larch', '0.00001 s', ('0.00001', 's'), '10us'),

    # test various forms of units
    Case('impute', '1ns', ('1e-9', 's'), '1ns'),
    Case('eyesore', '1e-9s', ('1e-9', 's'), '1ns'),
    Case('aspirant', '1n', ('1e-9', ''), '1n'),
    Case('delete', '1e-9', ('1e-9', ''), '1n'),
    Case('flummox', '1 ns', ('1e-9', 's'), '1ns'),
    Case('foster', '1 e-9 s', None, '1ns'),
    Case('deforest', '1n s', None, '1ns'),
    Case('fortune', '1e-9 s', ('1e-9', 's'), '1ns'),
    Case('starchy', '1nm/s', ('1e-9', 'm/s'), '1nm/s'),
    Case('preamble', '1e-9m/s', ('1e-9', 'm/s'), '1nm/s'),
    Case('haversack', '1 nm/s', ('1e-9', 'm/s'), '1nm/s'),
    Case('sprinter', '1e-9 m/s', ('1e-9', 'm/s'), '1nm/s'),
    Case('descend', '1nJ-s', ('1e-9', 'J-s'), '1nJ-s'),
    Case('milieu', '1e-9J-s', ('1e-9', 'J-s'), '1nJ-s'),
    Case('force', '1 nJ-s', ('1e-9', 'J-s'), '1nJ-s'),
    Case('athletic', '1e-9 J-s', ('1e-9', 'J-s'), '1nJ-s'),
    Case('scaffold', '1nm(s^-1)', ('1e-9', 'm(s^-1)'), '1nm(s^-1)'),
    Case('incur', '1e-9m(s^-1)', ('1e-9', 'm(s^-1)'), '1nm(s^-1)'),
    Case('hornet', '1 nm(s^-1)', ('1e-9', 'm(s^-1)'), '1nm(s^-1)'),
    Case('fledgling', '1e-9 m(s^-1)', ('1e-9', 'm(s^-1)'), '1nm(s^-1)'),
    Case('amnesty', '1nm/s^2', ('1e-9', 'm/s^2'), '1nm/s^2'),
    Case('carpet', '1e-9m/s^2', ('1e-9', 'm/s^2'), '1nm/s^2'),
    Case('intrigue', '1 nm/s^2', ('1e-9', 'm/s^2'), '1nm/s^2'),
    Case('picky', '1e-9 m/s^2', ('1e-9', 'm/s^2'), '1nm/s^2'),

    # test currency
    Case('bishop', '$10K', ('10e3', '$'), '$10k'),
    Case('colonnade', '$10', ('10', '$'), '$10'),
    Case('wizard', '$10.00', ('10.00', '$'), '$10'),
    Case('stork', '$10e9', ('10e9', '$'), '$10G'),
    Case('walkover', '$0.01', ('0.01', '$'), '$10m'),
    Case('kinswoman', '$.01', ('.01', '$'), '$10m'),
    Case('valuable', '$1.', None, '$1'),
    Case('kiddie', '-$10K', ('-10e3', '$'), '-$10k'),
    Case('breather', '-$10', ('-10', '$'), '-$10'),
    Case('recoil', '-$10.00', ('-10.00', '$'), '-$10'),
    Case('wrestle', '-$10e9', ('-10e9', '$'), '-$10G'),
    Case('theorist', '-$0.01', ('-0.01', '$'), '-$10m'),
    Case('neurone', '-$.01', ('-.01', '$'), '-$10m'),
    Case('crevice', '-$1.', None, '-$1'),
    Case('bodice', '+$10K', ('+10e3', '$'), '$10k'),
    Case('homicide', '+$10', ('+10', '$'), '$10'),
    Case('resurface', '+$10.00', ('+10.00', '$'), '$10'),
    Case('guidebook', '+$10e9', ('+10e9', '$'), '$10G'),
    Case('weaken', '+$0.01', ('+0.01', '$'), '$10m'),
    Case('subtlety', '+$.01', ('+.01', '$'), '$10m'),
    Case('flywheel', '+$1.', None, '$1'),

    # unusual numbers
    Case('sheathe', 'inf', ('inf', ''), 'inf'),
    Case('integrate', 'inf Hz', ('inf', 'Hz'), 'inf Hz'),
    Case('witter', '$inf', ('inf', '$'), '$inf'),
    Case('smoker', '-inf', ('-inf', ''), '-inf'),
    Case('spittoon', '-inf Hz', ('-inf', 'Hz'), '-inf Hz'),
    Case('outcome', '-$inf', ('-inf', '$'), '-$inf'),
    Case('baroness', 'nan', ('nan', ''), 'nan'),
    Case('province', 'nan Hz', ('nan', 'Hz'), 'nan Hz'),
    Case('infidel', '$nan', ('nan', '$'), '$nan'),
    Case('honey', '+nan', ('+nan', ''), 'nan'),
    Case('frighten', '+nan Hz', ('+nan', 'Hz'), 'nan Hz'),
    Case('acrobat', '+$nan', ('+nan', '$'), '$nan'),
    Case('firefly', 'INF', ('inf', ''), 'inf'),
    Case('farmland', 'INF Hz', ('inf', 'Hz'), 'inf Hz'),
    Case('osteopath', '$INF', ('inf', '$'), '$inf'),
    Case('chickpea', '-INF', ('-inf', ''), '-inf'),
    Case('bawdy', '-INF Hz', ('-inf', 'Hz'), '-inf Hz'),
    Case('pursuer', '-$INF', ('-inf', '$'), '-$inf'),
    Case('suffuse', 'NAN', ('nan', ''), 'nan'),
    Case('vacillate', 'NAN Hz', ('nan', 'Hz'), 'nan Hz'),
    Case('tangerine', '$NAN', ('nan', '$'), '$nan'),
    Case('southward', '+NAN', ('+nan', ''), 'nan'),
    Case('wander', '+NAN Hz', ('+nan', 'Hz'), 'nan Hz'),
    Case('stack', '+$NAN', ('+nan', '$'), '$nan'),

    # preferences
    Case('flotation', '1420.405751786 MHz', ('1420.405751786e6', 'Hz'), '1GHz', {'hprec':0}),
    Case('bodyguard', '1420.405751786 MHz', ('1420.405751786e6', 'Hz'), '1.4GHz', {'hprec':1}),
    Case('radiogram', '1420.405751786 MHz', ('1420.405751786e6', 'Hz'), '1.42GHz', {'hprec':2}),
    Case('omnibus', '1420.405751786 MHz', ('1420.405751786e6', 'Hz'), '1.42GHz', {'hprec':3}),
    Case('transmit', '1420.405751786 MHz', ('1420.405751786e6', 'Hz'), '1.4204GHz', {'hprec':4}),
    Case('morality', '1420.405751786 MHz', ('1420.405751786e6', 'Hz'), '1.42041GHz', {'hprec':5}),
    Case('reward', '1420.405751786 MHz', ('1420.405751786e6', 'Hz'), '1.420406GHz', {'hprec':6}),
    Case('smudge', '1420.405751786 MHz', ('1420.405751786e6', 'Hz'), '1.4204058GHz', {'hprec':7}),
    Case('animator', '1420.405751786 MHz', ('1420.405751786e6', 'Hz'), '1.42040575GHz', {'hprec':8}),
    Case('woodwind', '1420.405751786 MHz', ('1420.405751786e6', 'Hz'), '1.420405752GHz', {'hprec':9}),
    Case('underpay', '1420.405751786 MHz', ('1420.405751786e6', 'Hz'), '1.4204057518GHz', {'hprec':10}),
    Case('horoscope', '1420.405751786 MHz', ('1420.405751786e6', 'Hz'), '1.42040575179GHz', {'hprec':11}),
    Case('drivel', '1420.405751786 MHz', ('1420.405751786e6', 'Hz'), '1.420405751786GHz', {'hprec':12}),
    Case('railcard', '1420.405751786 MHz', ('1420.405751786e6', 'Hz'), '1.420405751786GHz', {'hprec':13}),
    Case('elixir', '1420.405751786 MHz', ('1420.405751786e6', 'Hz'), '1.4204 GHz', {'hprec':None, 'spacer':' '}),
    Case('henna', '3.141592 Hz', ('3.141592', 'Hz'), '3.1416_Hz', {'unity':'_', 'spacer':''}),
    Case('eastward', '3.141592 Hz', ('3.141592', 'Hz'), '3.1416 Hz', {'spacer':' '}),
    Case('string', '1420.405751786MHz', ('1420.405751786e6', 'Hz'), '1.4204e9Hz', {'output':''}),
    Case('airliner', '1ns', ('1', 'ns'), '1ns', {'ignore_sf':True}),
]

def test_number_recognition():
    names = set()
    for case in test_cases:
        assert case.name not in names
        names.add(case.name)

        set_preferences(
            hprec=None, mprec=None, spacer=None, unity=None, output=None,
            ignore_sf=None, assign_fmt=None, assign_rec=None
        )
        try:
            if case.prefs:
                set_preferences(**case.prefs)
            q = Quantity(case.text)
            assert ((q.to_unitless_str(), q.units) == case.raw), case.name
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
    set_preferences(
        hprec=None, mprec=None, spacer=None, unity=None, output=None,
        ignore_sf=None, assign_fmt=None, assign_rec=None
    )
