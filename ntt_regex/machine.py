from .node import Node, ValidationResult


class Machine:
    def __init__(self, value: str = "") -> None:
        self._startNode: Node = Node()
        self._endNode: Node = Node(accepted=True)
        self._startNode.add_transition(value, self._endNode)

    def validate(self, string: str) -> ValidationResult:
        return self._startNode.validate(string)
