from . import data, randoms

DIGITS = '0123456789'


def phone_number(international_code=False):
    number = randoms.random_string(10, 10, DIGITS)

    if international_code:
        number = '1' + number

    return number


def address():
    return '{} {}'.format(
        randoms.random_string(3, 3, DIGITS),
        randoms.random_choice(data.street_names)
    )


def email():
    name = randoms.random_choice(data.first_names).lower()
    domain = randoms.random_choice(data.domains)
    top_level_domain = randoms.random_choice(data.top_level_domains)

    return '{}@{}.{}'.format(name, domain, top_level_domain)


def city():
    return randoms.random_choice(data.cities)


def state(abbrev=False):
    if abbrev:
        return randoms.random_choice(list(data.states.keys()))
    else:
        return randoms.random_choice(list(data.states.values()))


def province(abbrev=False):
    if abbrev:
        return randoms.random_choice(list(data.provinces.keys()))
    else:
        return randoms.random_choice(list(data.provinces.values()))


def lorem_ipsum():
    return """
    Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor
    incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud
    exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.
    Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu
    fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in
    culpa qui officia deserunt mollit anim id est laborum.
    """


def first_name():
    return randoms.random_choice(data.first_names)


def last_name():
    return randoms.random_choice(data.last_names)


def full_name():
    return '{} {}'.format(first_name(), last_name())


def url():
    return randoms.random_choice(data.urls)
