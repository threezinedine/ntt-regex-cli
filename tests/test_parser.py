from ntt_regex import Parser


def test_and_machine():
    parser = Parser("ab")

    assert parser.validate("ab").valid is True
    assert parser.validate("ab").size == 2

    assert parser.validate("a").valid is False
    assert parser.validate("a").size == -1

    assert parser.validate("b").valid is False
    assert parser.validate("b").size == -1


def test_parser_init():
    parser = Parser("a|b")

    assert parser.validate("a").valid is True
    assert parser.validate("a").size == 1

    assert parser.validate("b").valid is True
    assert parser.validate("b").size == 1


def test_parse_repeat():
    parser = Parser("a*")

    assert parser.validate("").valid is True
    assert parser.validate("").size == 0

    assert parser.validate("a").valid is True
    assert parser.validate("a").size == 1

    assert parser.validate("aaaa").valid is True
    assert parser.validate("aaaa").size == 4

    assert parser.validate("b").valid is True
    assert parser.validate("b").size == 0


def test_parse_complex():
    parser = Parser("a|b*")

    assert parser.validate("a").valid is True
    assert parser.validate("a").size == 1

    assert parser.validate("").valid is True
    assert parser.validate("").size == 0

    assert parser.validate("b").valid is True
    assert parser.validate("b").size == 1

    assert parser.validate("bb").valid is True
    assert parser.validate("bb").size == 2

    assert parser.validate("c").valid is True
    assert parser.validate("c").size == 0


def test_parse_concatenated_repeat():
    parser = Parser("ab*")

    assert parser.validate("a").valid is True
    assert parser.validate("a").size == 1

    assert parser.validate("ab").valid is True
    assert parser.validate("ab").size == 2

    assert parser.validate("abb").valid is True
    assert parser.validate("abb").size == 3

    assert parser.validate("b").valid is False
    assert parser.validate("b").size == -1


def test_parse_one_or_more_repeats():
    parser = Parser("ab+")

    assert parser.validate("a").valid is False
    assert parser.validate("a").size == -1

    assert parser.validate("ab").valid is True
    assert parser.validate("ab").size == 2

    assert parser.validate("abb").valid is True
    assert parser.validate("abb").size == 3

    assert parser.validate("b").valid is False
    assert parser.validate("b").size == -1

    assert parser.validate("").valid is False
    assert parser.validate("").size == -1

    assert parser.validate("aab").valid is False
    assert parser.validate("aab").size == -1

    assert parser.validate("abab").valid is True
    assert parser.validate("abab").size == 2

    assert parser.validate("abbb").valid is True
    assert parser.validate("abbb").size == 4

    assert parser.validate("abbc").valid is True
    assert parser.validate("abbc").size == 3


def test_parse_optional():
    parser = Parser("ab?")

    assert parser.validate("a").valid is True
    assert parser.validate("a").size == 1

    assert parser.validate("ab").valid is True
    assert parser.validate("ab").size == 2

    assert parser.validate("abb").valid is True
    assert parser.validate("abb").size == 2

    assert parser.validate("b").valid is False
    assert parser.validate("b").size == -1


def test_parse_complex_optional_and_one_or_more():
    parser = Parser("a+b|c?d")

    assert parser.validate("aaab").valid is True
    assert parser.validate("aaab").size == 4

    assert parser.validate("b").valid is False
    assert parser.validate("b").size == -1

    assert parser.validate("c").valid is False
    assert parser.validate("c").size == -1

    assert parser.validate("d").valid is True
    assert parser.validate("d").size == 1

    assert parser.validate("cd").valid is True
    assert parser.validate("cd").size == 2
