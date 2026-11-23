import pytest
from timer import timer


def test_preserves_result_and_arguments():
    @timer(unit="ms")
    def add(a, b=10):
        """Return the sum"""
        return a + b

    assert add(3, 5) == 8
    assert add(a=3, b=5) == 8
    assert add(3) == 13
    assert add.__name__ == "add"
    assert add.__doc__ == "Return the sum"


def test_exception_path(capsys):
    error = ValueError("bad input")

    @timer(unit="ms")
    def fail():
        raise error

    with pytest.raises(ValueError) as caught:
        fail()
    assert caught.value is error
    output = capsys.readouterr().out
    assert "time taken :" in output
    assert "ms" in output
