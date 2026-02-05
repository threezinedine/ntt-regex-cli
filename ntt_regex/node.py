from dataclasses import dataclass, field


@dataclass
class ValidationResult:
    valid: bool = field(default=False)
    size: int | None = field(default=None)


class Node:
    def __init__(self, accepted: bool = False) -> None:
        self._accepted = accepted
        self._transitions: dict[str, list["Node"]] = {}

    @property
    def accepted(self) -> bool:
        return self._accepted

    def validate(self, value: str) -> ValidationResult:
        epsilon_targets = self._transitions.get("", [])
        for target in epsilon_targets:
            result = target.validate(value)
            if result.valid:
                return ValidationResult(True, result.size)

        if self.accepted:
            return ValidationResult(True, 0)
        # if len(value) == 0:
        #     return ValidationResult(self.accepted, 0 if self.accepted else None)

        if len(value) == 0:
            return ValidationResult()

        targets = self._transitions.get(value[0], [])

        for target in targets:
            result = target.validate(value[1:])
            if result.valid:
                return ValidationResult(
                    True, result.size + 1 if result.size is not None else 1
                )

        return ValidationResult()

    def add_transition(self, symbol: str, node: "Node") -> None:
        if symbol not in self._transitions:
            self._transitions[symbol] = []

        self._transitions[symbol].append(node)
