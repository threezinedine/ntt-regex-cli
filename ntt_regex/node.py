from dataclasses import dataclass, field


@dataclass
class ValidationResult:
    valid: bool = field(default=False)
    size: int = field(default=-1)


class Node:
    def __init__(self, accepted: bool = False) -> None:
        self._accepted = accepted
        self._transitions: dict[str, list["Node"]] = {}

    @property
    def accepted(self) -> bool:
        return self._accepted

    def validate(self, value: str, currentIndex: int = 0) -> ValidationResult:
        finalResult = ValidationResult()

        epsilon_targets = self._transitions.get("", [])
        for target in epsilon_targets:
            result = target.validate(value, currentIndex)
            if result.valid and finalResult.size < result.size:
                finalResult = result

        if self.accepted:
            return ValidationResult(True, currentIndex)

        if currentIndex >= len(value):
            if finalResult.valid:
                return finalResult
            else:
                return ValidationResult()

        targets = self._transitions.get(value[currentIndex], [])

        for target in targets:
            result = target.validate(value, currentIndex + 1)
            if result.valid and finalResult.size < result.size:
                finalResult = result

        return finalResult

    def add_transition(self, symbol: str, node: "Node") -> None:
        if symbol not in self._transitions:
            self._transitions[symbol] = []

        self._transitions[symbol].append(node)

    def __repr__(self) -> str:
        return f"Node(accepted={self._accepted}) --> Transitions: {self._transitions}"
