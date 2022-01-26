import pytest


def add(a: int, b: int):
    return a + b


@pytest.mark.parametrize(['a', 'b', 'c'],[
    (5, 4, 9),
    (5, 5, 10),
    (4, 4, 8)
])
def test_add(a, b, c):
    assert add(a, b) == c