class Node:
    def __init__(self, accepted: bool = False) -> None:
        self._accepted = accepted
        self._transitions: dict[str, list["Node"]] = {}

    @property
    def accepted(self) -> bool:
        return self._accepted

    def validate(self, string: str) -> bool:
        if len(string) == 0:
            return self.accepted

        targets = self._transitions.get(string[0], [])

        for target in targets:
            if target.validate(string[1:]):
                return True

        return False

    def add_transition(self, symbol: str, node: "Node") -> None:
        if symbol not in self._transitions:
            self._transitions[symbol] = []

        self._transitions[symbol].append(node)
