from ntt_regex import Machine


def test_machine_init():
    machine = Machine()
    assert machine.validate("").valid is True
    assert machine.validate("").size == 0

    assert machine.validate("a").valid is True
    assert machine.validate("a").size == 0


def test_machine_with_value():
    machine = Machine("a")
    assert machine.validate("abc").valid is True
    assert machine.validate("abc").size == 1

    assert machine.validate("a").valid is True
    assert machine.validate("a").size == 1

    assert machine.validate("").valid is False
    assert machine.validate("").size is None

    assert machine.validate("b").valid is False
    assert machine.validate("b").size is None
