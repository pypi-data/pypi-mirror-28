import datetime
import random
import string


def random_boolean():
    return random.randint(0, 1) == 0


def random_integer(minimum, maximum):
    assert minimum <= maximum, 'minimum cannot be greater than maximum'
    return random.randint(minimum, maximum)


def random_decimal(minimum, maximum, digits=2):
    assert minimum <= maximum, 'minimum cannot be greater than maximum'
    return round(random.uniform(minimum, maximum), digits)


def random_choice(choices):
    return random.choice(choices)


def random_choices(choices, count):
    results = []
    for value in range(count):
        results.append(random_choice(choices))
    return results


def random_string(minimum=8, maximum=100, characters=None):
    assert minimum <= maximum, 'minimum cannot be greater than maximum'

    if not characters:
        characters = string.ascii_letters

    return ''.join(random_choices(characters, random_integer(minimum, maximum)))


def random_datetime(begin=None, end=None):
    if not begin:
        begin = datetime.datetime.now()

    if not end:
        end = begin + datetime.timedelta(weeks=52)

    assert begin <= end, 'begin cannot be after end'

    delta = end - begin
    offset = random.randrange((delta.days * 24 * 60 * 60) + delta.seconds)
    return begin + datetime.timedelta(seconds=offset)
