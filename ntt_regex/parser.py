from .machine import Machine, ValidationResult
from dataclasses import dataclass, field
from typing import Any, List
from enum import Enum, auto


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
    ONE_MORE = auto()
    OPTIONAL = auto()
    RANGE = auto()
    BLOCK = auto()


@dataclass
class TokenGroup:
    tokens: list[Token] | None = field(default=None)
    groupType: GroupType = field(default=GroupType.AND)


class Parser:
    """
    Precedence (highest to lowest):
    1. range []
    2. Parentheses ()
    3. Repeat *
    4. And (concatenation)
    5. Or |

    Grammar:

    H  -> EH';

    H' -> ε
          | '|' E
          ;

    E  -> TE'
          ;

    E' -> T
          | ε
          ;

    T  -> K
          | KF
          ;

    F  -> | ε
          | '*'
          | '?'
          | '+'
          ;

    K  -> CHAR
          ;
    """

    def __init__(self, pattern: str) -> None:
        self._machine: Machine | None = None
        self._machinePointer: int = 0
        self._machineSavepoints: List[int] = []
        self._tokens: list[Token] = []
        self._tokenize(pattern)

        ast = self.H()
        print(ast)
        if ast is None:
            raise ValueError("Invalid pattern")

        self._machine = self.build_machine(ast)

        assert self._machine is not None

    def build_machine(self, ast: list[Any]) -> Machine | None:
        if len(ast) == 0:
            return Machine()

        if ast[0] == GroupType.AND:
            assert len(ast) == 3
            left_machine = self.build_machine(ast[1])
            right_machine = self.build_machine(ast[2])
            assert left_machine is not None
            assert right_machine is not None
            return left_machine & right_machine
        elif ast[0] == GroupType.OR:
            assert len(ast) == 3
            left_machine = self.build_machine(ast[1])
            right_machine = self.build_machine(ast[2])
            assert left_machine is not None
            assert right_machine is not None
            return left_machine | right_machine
        elif isinstance(ast[0], str):
            return Machine(ast[0])
        elif ast[0] == GroupType.REPEAT:
            assert len(ast) == 2
            sub_machine = self.build_machine(ast[1])
            assert sub_machine is not None
            return sub_machine.repeat()
        elif ast[0] == GroupType.ONE_MORE:
            assert len(ast) == 2
            sub_machine = self.build_machine(ast[1])
            assert sub_machine is not None
            return sub_machine & sub_machine.repeat()
        elif ast[0] == GroupType.OPTIONAL:
            assert len(ast) == 2
            sub_machine = self.build_machine(ast[1])
            assert sub_machine is not None
            return sub_machine | Machine()

        return None

    def H(self) -> list[Any] | None:
        save = self._savepoint()

        e = self.E()
        if e is None:
            self._rollback(save)
            return None

        h_prime = self.H_prime()
        if h_prime is not None:
            return [h_prime[0], e, h_prime[1]]

        self._rollback(save)
        return e

    def H_prime(self) -> list[Any] | None:
        save = self._savepoint()

        if self._machinePointer >= len(self._tokens):
            self._rollback(save)
            return None

        token = self._tokens[self._machinePointer]
        if token.type != TokenType.OR:
            self._rollback(save)
            return None

        self._machinePointer += 1

        e = self.E()
        if e is None:
            self._rollback(save)
            return None

        return [GroupType.OR, e]

    def E(self) -> list[Any] | None:
        save = self._savepoint()

        te_prime = self.TE_prime()
        if te_prime is not None:
            return te_prime

        self._rollback(save)

        t_or_e_prime = self.T_or_E_prime()
        if t_or_e_prime is not None:
            return t_or_e_prime

        self._rollback(save)
        return None

    def TE_prime(self) -> list[Any] | None:
        save = self._savepoint()

        t = self.T()
        if t is None:
            self._rollback(save)
            return None

        e_prime = self.E_prime()
        if e_prime is None:
            self._rollback(save)
            return None

        return [GroupType.AND, t, e_prime]

    def T_or_E_prime(self) -> list[Any] | None:
        save = self._savepoint()

        if self._machinePointer + 2 > len(self._tokens):
            self._rollback(save)
            return None

        t = self.T()
        if t is None:
            self._rollback(save)
            return None

        token = self._tokens[self._machinePointer]
        if token.type != TokenType.OR:
            self._rollback(save)
            return None

        self._machinePointer += 1

        e_prime = self.E_prime()
        if e_prime is None:
            self._rollback(save)
            return None

        return [GroupType.OR, t, e_prime]

    def check_token(self, token_type: TokenType) -> bool:
        if self._machinePointer >= len(self._tokens):
            return False

        token = self._tokens[self._machinePointer]
        if token.type == token_type:
            self._machinePointer += 1
            return True

        return False

    def _savepoint(self) -> int:
        self._machineSavepoints.append(self._machinePointer)
        return len(self._machineSavepoints) - 1

    def _rollback(self, index: int = -1) -> None:
        if index == -1:
            index = len(self._machineSavepoints) - 1

        self._machinePointer = self._machineSavepoints[index]

    def T(self) -> list[Any] | None:
        save = self._savepoint()

        k = self.K()
        if k is None:
            self._rollback(save)
            return None

        f = self.F()
        if f is not None:
            if f == "*":
                return [GroupType.REPEAT, k]
            if f == "?":
                return [GroupType.OPTIONAL, k]
            if f == "+":
                return [GroupType.ONE_MORE, k]

            return k

        self._rollback(save)

        k = self.K()
        if k is not None:
            return k

        return None

    def F(self) -> str | None:
        if self._machinePointer >= len(self._tokens):
            return ""

        token = self._tokens[self._machinePointer]
        if token.type == TokenType.REPEAT:
            self._machinePointer += 1
            return "*"
        elif token.type == TokenType.QUESTION:
            self._machinePointer += 1
            return "?"
        elif token.type == TokenType.PLUS:
            self._machinePointer += 1
            return "+"

        return None

    def K(self) -> list[Any] | None:
        if self._machinePointer >= len(self._tokens):
            return None

        token = self._tokens[self._machinePointer]
        if token.type == TokenType.CHAR:
            self._machinePointer += 1
            return [token.value]

        return None

    def E_prime(self) -> list[Any] | None:
        save = self._savepoint()

        if self._machinePointer >= len(self._tokens):
            return []

        self._rollback(save)

        t = self.T()
        if t is not None:
            return t

        self._rollback(save)

        return None

    def _add_char(self, char: str) -> None:
        if self._machine is None:
            self._machine = Machine(char)
        else:
            self._machine = self._machine & Machine(char)

    def _tokenize(self, pattern: str):
        self._tokens = []

        for char in pattern:
            if char == "|":
                self._tokens.append(Token(TokenType.OR))
            elif char == "^":
                self._tokens.append(Token(TokenType.START))
            elif char == "$":
                self._tokens.append(Token(TokenType.END))
            elif char == "*":
                self._tokens.append(Token(TokenType.REPEAT))
            elif char == "?":
                self._tokens.append(Token(TokenType.QUESTION))
            elif char == "+":
                self._tokens.append(Token(TokenType.PLUS))
            elif char == "[":
                self._tokens.append(Token(TokenType.L_RANGE))
            elif char == "]":
                self._tokens.append(Token(TokenType.R_RANGE))
            elif char == "(":
                self._tokens.append(Token(TokenType.L_PAREN))
            elif char == ")":
                self._tokens.append(Token(TokenType.R_PAREN))
            else:
                self._tokens.append(Token(TokenType.CHAR, char))

    def validate(self, string: str) -> ValidationResult:
        if self._machine is None:
            raise ValueError("Parser has not been initialized properly.")

        return self._machine.validate(string)
