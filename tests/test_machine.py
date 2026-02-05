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
    assert machine.validate("").size == -1

    assert machine.validate("b").valid is False
    assert machine.validate("b").size == -1


def test_and_machine():
    # ab
    machine1 = Machine("a")
    machine2 = Machine("b")

    machine = machine1 & machine2
    assert machine.validate("ab").valid is True
    assert machine.validate("ab").size == 2

    assert machine.validate("a").valid is False
    assert machine.validate("a").size == -1

    assert machine.validate("b").valid is False
    assert machine.validate("b").size == -1

    assert machine.validate("abc").valid is True
    assert machine.validate("abc").size == 2


def test_or_machine():
    # a|b
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
    assert machine.validate("c").size == -1


def test_repeated_machine():
    # a*
    machine = Machine("a")

    machine = machine.repeat()

    print(machine)

    assert machine.validate("a").valid is True
    assert machine.validate("a").size == 1

    assert machine.validate("aaaa").valid is True
    assert machine.validate("aaaa").size == 4

    assert machine.validate("b").valid is True
    assert machine.validate("b").size == 0

    assert machine.validate("aaab").valid is True
    assert machine.validate("aaab").size == 3

    assert machine.validate("").valid is True
    assert machine.validate("").size == 0


def test_complex_machine():
    # (a|b)*c
    machine_a = Machine("a")
    machine_b = Machine("b")
    machine_c = Machine("c")

    machine = (machine_a | machine_b).repeat() & machine_c

    assert machine.validate("aaabbbabc").valid is True
    assert machine.validate("aaabbbabc").size == 9

    assert machine.validate("abababac").valid is True
    assert machine.validate("abababac").size == 8

    assert machine.validate("c").valid is True
    assert machine.validate("c").size == 1

    assert machine.validate("aaabbbab").valid is False
    assert machine.validate("aaabbbab").size == -1

    assert machine.validate("").valid is False
    assert machine.validate("").size == -1
