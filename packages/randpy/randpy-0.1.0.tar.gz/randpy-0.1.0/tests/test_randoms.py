import datetime
import itertools

import pytest

import randpy

REPEAT_TEST_COUNT = 100


def test_random_boolean():
    values = [True, False]
    for _ in itertools.repeat(None, REPEAT_TEST_COUNT):
        assert randpy.random_boolean() in values


def test_random_integer():
    minimum = 0
    maximum = 100

    for _ in itertools.repeat(None, REPEAT_TEST_COUNT):
        assert randpy.random_integer(minimum, maximum) in range(minimum, maximum + 1)

    with pytest.raises(AssertionError):
        randpy.random_integer(2, 1)


def test_random_decimal():
    minimum = 0
    maximum = 1

    for _ in itertools.repeat(None, REPEAT_TEST_COUNT):
        value = randpy.random_decimal(minimum, maximum)
        assert value >= minimum and value <= maximum

    for _ in itertools.repeat(None, REPEAT_TEST_COUNT):
        round_by = 4
        value = randpy.random_decimal(minimum, maximum, round_by)
        assert round(value, round_by) == value

    with pytest.raises(AssertionError):
        randpy.random_integer(1, 0)


def test_random_choice():
    values = [1, 2, 3, 4, 5]

    for _ in itertools.repeat(None, REPEAT_TEST_COUNT):
        assert randpy.random_choice(values) in values


def test_random_choices():
    values = [1, 2, 3, 4, 5, 6]

    for _ in itertools.repeat(None, REPEAT_TEST_COUNT):
        count = 5
        choices = randpy.random_choices(values, count)
        assert len(choices) == count

        values_set = set(values)
        for choice in choices:
            assert choice in values_set


def test_random_string():
    for _ in itertools.repeat(None, REPEAT_TEST_COUNT):
        random_string = randpy.random_string()
        length = len(random_string)

        assert length >= 8 and length <= 100

    for _ in itertools.repeat(None, REPEAT_TEST_COUNT):
        random_string = randpy.random_string(10, 10, 'abc')

        assert len(random_string) == 10
        for c in random_string:
            assert c in 'abc'


def test_random_datetime():
    for _ in itertools.repeat(None, REPEAT_TEST_COUNT):
        random_date = randpy.random_datetime()
        assert (random_date >= datetime.datetime.now() and
                random_date <= datetime.datetime.now() + datetime.timedelta(weeks=52))
