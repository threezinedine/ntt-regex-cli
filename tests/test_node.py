from ntt_regex import Node


def test_node_init():
    node = Node()
    assert node.accepted == False


def test_node_acceptance():
    node = Node(accepted=True)
    assert node.accepted


def test_node_test_string():
    node = Node()
    assert not node.validate("")


def test_accepted_property_validate():
    node = Node(accepted=True)
    assert node.validate("")


def test_add_transition():
    """
    (A) --a--> (B, accepted)
    """
    node1 = Node()
    node2 = Node(accepted=True)
    node1.add_transition("a", node2)

    assert node1.validate("a")


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

    assert nodeA.validate("ab")
    assert nodeA.validate("as")
    assert not nodeA.validate("a")
    assert not nodeA.validate("b")
    assert not nodeA.validate("ae")
    assert not nodeA.validate("abc")
