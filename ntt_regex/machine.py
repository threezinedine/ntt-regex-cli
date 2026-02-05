from .node import Node, ValidationResult


class Machine:
    def __init__(self, value: str | None = "") -> None:
        self._startNode: Node = Node()
        self._endNode: Node = Node(accepted=True)

        if value is not None:
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

    def __or__(self, other: "Machine") -> "Machine":
        newMachine = Machine(None)

        newMachine._startNode.add_transition("", self._startNode)
        newMachine._startNode.add_transition("", other._startNode)

        self._endNode._accepted = False  # type: ignore
        other._endNode._accepted = False  # type: ignore

        self._endNode.add_transition("", newMachine._endNode)
        other._endNode.add_transition("", newMachine._endNode)

        return newMachine

    def repeat(self) -> "Machine":
        new_machine = Machine("")

        self._endNode._accepted = False  # type: ignore

        new_machine._startNode.add_transition("", self._startNode)
        self._endNode.add_transition("", self._startNode)
        self._endNode.add_transition("", new_machine._endNode)

        return new_machine

    def __repr__(self) -> str:
        return f"Machine(startNode={self._startNode}, endNode={self._endNode})"
