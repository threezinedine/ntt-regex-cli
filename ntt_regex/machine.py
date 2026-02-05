from .node import Node, ValidationResult


class Machine:
    def __init__(self, value: str = "") -> None:
        self._startNode: Node = Node()
        self._endNode: Node = Node(accepted=True)
        self._startNode.add_transition(value, self._endNode)

    def validate(self, string: str) -> ValidationResult:
        return self._startNode.validate(string)

    def __and__(self, other: "Machine") -> "Machine":
        new_machine = Machine()
        new_machine._startNode = self._startNode

        self._endNode.add_transition("", other._startNode)
        new_machine._endNode = other._endNode

        self._endNode._accepted = False  # type: ignore

        return new_machine
