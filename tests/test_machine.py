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


def test_and_machine():
    machine1 = Machine("a")
    machine2 = Machine("b")

    machine = machine1 & machine2
    assert machine.validate("ab").valid is True
    assert machine.validate("ab").size == 2

    assert machine.validate("a").valid is False
    assert machine.validate("a").size is None

    assert machine.validate("b").valid is False
    assert machine.validate("b").size is None

    assert machine.validate("abc").valid is True
    assert machine.validate("abc").size == 2


def test_or_machine():
    machine1 = Machine("a")
    machine2 = Machine("b")

    machine = machine1 | machine2

    assert machine.validate("a").valid is True
    assert machine.validate("a").size == 1

    assert machine.validate("b").valid is True
    assert machine.validate("b").size == 1

    assert machine.validate("ab").valid is True
    assert machine.validate("ab").size == 1

    assert machine.validate("c").valid is False
    assert machine.validate("c").size is None
