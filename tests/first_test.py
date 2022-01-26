import pytest


def add(a: int, b: int):
    if type(a) == 'str' or type(b) == 'str':
        raise Exception('Invalid Data Type')
    return a + b


def test_add_default():
    assert add(7, 7) == 14


@pytest.mark.parametrize(['a', 'b', 'c'],[
    (5, 4, 9),
    (5, 5, 10),
    (4, 4, 8)
])
def test_add_parameterized(a, b, c):
    assert add(a, b) == c


@pytest.fixture
def default_func_call():
    print('in fixture')
    return 'hello'


def test_add_fixtured(default_func_call):
    print('in test')
    print(default_func_call)
    assert add(7, 7) == 14


@pytest.mark.parametrize(['a', 'b', 'c'],[
    (5, 4, 9),
    (5, 5, 10),
    (4, 4, 8)
])
def test_add_parameterized_and_fixtured(default_func_call, a, b, c):
    print('in test')
    print(default_func_call)
    assert add(a, b) == c


def test_add_with_string():
    with pytest.raises(Exception):
        assert add('ram', 2)