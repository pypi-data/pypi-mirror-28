import os
import pickle


FRACTION_BASE_POINTS = 18
FRACTION_BASE = 10 ** FRACTION_BASE_POINTS


def to_base_value(value):
    assert isinstance(value, unicode) or isinstance(value, str)
    # Cases handled:
    # '1':       [[u'1']]
    # '1.3843':  [[u'1'], [u'3843']]
    # '1e-12':   [[u'1', u'-12']]
    # '1.3e-12': [[u'1'], [u'3', u'-12']]
    dot_split = [i.split('e') for i in value.split('.')]

    fractional_str = None
    exponent = 0
    parts_length = len(dot_split)
    assert parts_length in (1, 2)


    dot_split_0 = dot_split[0]
    dot_split_0_len = len(dot_split_0)
    assert dot_split_0_len in (1, 2)

    integer = int(dot_split_0[0])
    if dot_split_0_len == 2:
        exponent = int(dot_split_0[1])

    if parts_length == 2:
        dot_split_1 = dot_split[1]
        dot_split_1_len = len(dot_split_1)
        assert dot_split_1_len in (1, 2)
        fractional_str = dot_split_1[0]
        if dot_split_1_len == 2:
            assert dot_split_0_len == 1
            exponent = int(dot_split_1[1])

    fraction_base = FRACTION_BASE
    if exponent < 0:
        assert -exponent <= FRACTION_BASE_POINTS
        fraction_base /= 10 ** -exponent
    else:
        fraction_base *= 10 ** exponent

    fractional = 0
    if fractional_str:
        fractional_length = len(fractional_str)
        assert fractional_length <= FRACTION_BASE_POINTS

        fractional = int(fractional_str)
        fractional *= fraction_base
        fractional /= 10 ** fractional_length

    return ((integer * fraction_base) + fractional)


def multiply_safe(i, j):
    mul = i * j
    #assert (mul % FRACTION_BASE) == 0
    return mul / FRACTION_BASE


def parse_pair(symbol):
    return symbol[:3], symbol[3:]


def from_market(symbol):
    '''
    EUR/USD 1.2500 means that one euro is exchanged for 1.2500 US dollars.

    EUR is the base currency and
    USD is the quote currency
    '''
    base, quote = symbol.split('/')
    return base, quote


def to_market(symbol):
    base, quote = parse_pair(symbol)
    return "{}/{}".format(base, quote)


def load_cached(filename, do_unless_found):
    if not os.path.isfile(filename):
        with open(filename, "wb") as pickle_out:
            pickle.dump(do_unless_found(), pickle_out)

    with open(filename, "rb") as pickle_in:
        return pickle.load(pickle_in)