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


# def test_parse_repeat():
#     pattern = "a*"
#     parser = Parser.parse(pattern)

#     assert parser.validate("").valid is True
#     assert parser.validate("").size == 0

#     assert parser.validate("a").valid is True
#     assert parser.validate("a").size == 1

#     assert parser.validate("aaaa").valid is True
#     assert parser.validate("aaaa").size == 4

#     assert parser.validate("b").valid is True
#     assert parser.validate("b").size == 0


# def test_parse_complex():
#     pattern = "a|b*"
#     parser = Parser.parse(pattern)

#     assert parser.validate("a").valid is True
#     assert parser.validate("a").size == 1

#     assert parser.validate("").valid is True
#     assert parser.validate("").size == 0

#     assert parser.validate("b").valid is True
#     assert parser.validate("b").size == 1

#     assert parser.validate("bb").valid is True
#     assert parser.validate("bb").size == 2

#     assert parser.validate("c").valid is True
#     assert parser.validate("c").size == 0


# def test_parse_concatenated_repeat():
#     pattern = "ab*"
#     parser = Parser.parse(pattern)

#     assert parser.validate("a").valid is True
#     assert parser.validate("a").size == 1

#     assert parser.validate("ab").valid is True
#     assert parser.validate("ab").size == 2

#     assert parser.validate("abb").valid is True
#     assert parser.validate("abb").size == 3

#     assert parser.validate("b").valid is False
#     assert parser.validate("b").size == -1
