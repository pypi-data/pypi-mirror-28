from randpy import data, generators


def test_phone_number():
    phone_number = generators.phone_number()

    assert len(phone_number) == 10
    assert phone_number.isdigit()

    internal_phone_number = generators.phone_number(international_code=True)

    assert len(internal_phone_number) == 11
    assert internal_phone_number.isdigit()


def test_address():
    number, street_name = generators.address().split(' ', 1)

    assert number.isdigit()
    assert street_name in data.street_names


def test_email():
    name, host = generators.email().split('@', 1)
    domain, top_level_domain = host.split('.')

    assert name.title() in data.first_names
    assert domain in data.domains
    assert top_level_domain in data.top_level_domains


def test_city():
    assert generators.city() in data.cities


def test_state():
    assert generators.state() in list(data.states.values())
    assert generators.state(abbrev=True) in list(data.states.keys())


def test_province():
    assert generators.province() in list(data.provinces.values())
    assert generators.province(abbrev=True) in list(data.provinces.keys())


def test_lorem_ipsum():
    assert len(generators.lorem_ipsum()) > 0


def test_first_name():
    assert generators.first_name() in data.first_names


def test_last_name():
    assert generators.last_name() in data.last_names


def test_full_name():
    first_name, last_name = generators.full_name().split(' ')

    assert first_name in data.first_names
    assert last_name in data.last_names


def test_url():
    assert generators.url() in data.urls
