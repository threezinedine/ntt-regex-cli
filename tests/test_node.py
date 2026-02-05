from ntt_regex import Node


def test_node_init():
    node = Node()
    assert node.accepted == False


def test_node_acceptance():
    node = Node(accepted=True)
    assert node.accepted


def test_node_test_string():
    node = Node()
    assert not node.validate("").valid


def test_accepted_property_validate():
    node = Node(accepted=True)
    assert node.validate("").valid


def test_add_transition():
    """
    (A) --a--> (B, accepted)
    """
    node1 = Node()
    node2 = Node(accepted=True)
    node1.add_transition("a", node2)

    assert node1.validate("a").valid
    assert node1.validate("a").size == 1

    assert node1.validate("b").valid is False
    assert node1.validate("b").size == -1


def test_epsilon_transition():
    """
    (A) --""--> (B, accepted)
    """
    node1 = Node()
    node2 = Node(accepted=True)
    node1.add_transition("", node2)

    assert node1.validate("").valid
    assert node1.validate("").size == 0

    assert node1.validate("a").valid
    assert node1.validate("a").size == 0


def test_add_transition_multiple_steps():
    """
         --a--> (B) --b--> (C, accepted)
    (A)
         --a--> (D) --s--> (E, accepted)
    """
    nodeA = Node()
    nodeB = Node()
    nodeC = Node(accepted=True)
    nodeD = Node()
    nodeE = Node(accepted=True)

    nodeA.add_transition("a", nodeB)
    nodeB.add_transition("b", nodeC)

    nodeA.add_transition("a", nodeD)
    nodeD.add_transition("s", nodeE)

    assert nodeA.validate("ab").valid
    assert nodeA.validate("ab").size == 2

    assert nodeA.validate("as").valid
    assert nodeA.validate("as").size == 2

    assert not nodeA.validate("a").valid
    assert nodeA.validate("a").size == -1

    assert not nodeA.validate("b").valid
    assert nodeA.validate("b").size == -1

    assert not nodeA.validate("ae").valid
    assert nodeA.validate("ae").size == -1

    assert nodeA.validate("abc").valid
    assert nodeA.validate("abc").size == 2
