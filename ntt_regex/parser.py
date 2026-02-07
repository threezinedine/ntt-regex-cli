from .machine import Machine
from dataclasses import dataclass, field
from typing import Callable as Function, List
from enum import Enum, auto

# import partial_functions
from functools import partial


class TokenType(Enum):
    NONE = auto()
    CHAR = auto()
    OR = auto()  # |
    START = auto()  # ^
    END = auto()  # $
    REPEAT = auto()  # *
    QUESTION = auto()  # ?
    PLUS = auto()  # +
    L_RANGE = auto()  # [
    R_RANGE = auto()  # ]
    L_PAREN = auto()  # (
    R_PAREN = auto()  # )


@dataclass
class Token:
    type: TokenType = field(default=TokenType.NONE)
    value: str | None = field(default=None)


class GroupType(Enum):
    AND = auto()
    OR = auto()
    REPEAT = auto()
    RANGE = auto()
    BLOCK = auto()


@dataclass
class TokenGroup:
    tokens: list[Token] | None = field(default=None)
    groupType: GroupType = field(default=GroupType.AND)


class Parser:
    _machine: Machine | None = None
    _machineStack: list[Function[[int], None]] = []
    _machinePointer: int = 0
    _machineSavepoints: List[int] = []

    """
    Precedence (highest to lowest):
    1. range []
    2. Parentheses ()
    3. Repeat *
    4. And (concatenation)
    5. Or |

    Grammar:

    E  -> TE'
    E' -> T | ε

    T  -> CHAR
    """

    @staticmethod
    def parse(pattern: str) -> Machine:
        tokens = Parser._tokenize(pattern)
        Parser._machine = None
        Parser._machineStack = []
        Parser._machinePointer = 0
        Parser._machineSavepoints = []
        valid = Parser._parse(tokens)
        if not valid:
            raise ValueError("Invalid pattern")

        for func in Parser._machineStack:
            func()  # type: ignore

        assert Parser._machine is not None
        return Parser._machine

    @staticmethod
    def _parse(tokens: list[Token]) -> bool:
        save = Parser._savepoint()
        t_res = Parser._parse_T(tokens)
        if not t_res:
            Parser._rollback(save)
            return False

        e_prim_res = Parser._parse_E_prime(tokens)
        if not e_prim_res:
            Parser._rollback(save)
            return False

        return True

    @staticmethod
    def _savepoint() -> int:
        Parser._machineSavepoints.append(Parser._machinePointer)
        return len(Parser._machineSavepoints) - 1

    @staticmethod
    def _rollback(index: int = -1) -> None:
        if index == -1:
            index = len(Parser._machineSavepoints) - 1

        Parser._machinePointer = Parser._machineSavepoints[index]
        Parser._machineStack = Parser._machineStack[: Parser._machinePointer]

    @staticmethod
    def _parse_T(tokens: list[Token]) -> bool:
        if Parser._machinePointer >= len(tokens):
            return False

        token = tokens[Parser._machinePointer]
        if token.type == TokenType.CHAR:
            Parser._machineStack.append(partial(Parser._add_char, token.value))  # type: ignore
            Parser._machinePointer += 1
            return True

        return False

    @staticmethod
    def _parse_E_prime(tokens: list[Token]) -> bool:
        save = Parser._savepoint()

        if Parser._machinePointer >= len(tokens):
            return True

        t_res = Parser._parse_T(tokens)
        if not t_res:
            Parser._rollback(save)
            return False

        return True

    @staticmethod
    def _add_char(char: str) -> None:
        if Parser._machine is None:
            Parser._machine = Machine(char)
        else:
            Parser._machine = Parser._machine & Machine(char)

    @staticmethod
    def _tokenize(pattern: str) -> list[Token]:
        result: list[Token] = []

        for char in pattern:
            if char == "|":
                result.append(Token(TokenType.OR))
            elif char == "^":
                result.append(Token(TokenType.START))
            elif char == "$":
                result.append(Token(TokenType.END))
            elif char == "*":
                result.append(Token(TokenType.REPEAT))
            elif char == "?":
                result.append(Token(TokenType.QUESTION))
            elif char == "+":
                result.append(Token(TokenType.PLUS))
            elif char == "[":
                result.append(Token(TokenType.L_RANGE))
            elif char == "]":
                result.append(Token(TokenType.R_RANGE))
            elif char == "(":
                result.append(Token(TokenType.L_PAREN))
            elif char == ")":
                result.append(Token(TokenType.R_PAREN))
            else:
                result.append(Token(TokenType.CHAR, char))

        return result

    @staticmethod
    def _parse_or(tokens: list[Token]) -> Machine:
        left_token = tokens[0]
        right_token = tokens[2]

        if left_token.type == TokenType.CHAR and right_token.type == TokenType.CHAR:
            left_machine = Machine(left_token.value)
            right_machine = Machine(right_token.value)

            return left_machine | right_machine

        raise NotImplementedError("Only simple 'a|b' patterns are implemented.")
