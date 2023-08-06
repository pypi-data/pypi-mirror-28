import pytest

from tgf.core.tree import Tree, Node


def test_init_tree():
    tree = Tree()

    assert tree.roots == []


def test_init_node():
    node = Node()

    assert node.attributes == {}
    assert node.child_nodes == []
    assert node.node_type == ""
    assert node.root is None


def test_init_node_with_defaults():
    root = Node()
    child = Node()

    attributes = {'key': 'val'}
    node = Node(
        root=root,
        attributes=attributes,
        children=[child]
    )

    assert node.child_nodes == [child]
    assert 'key' in node.attributes
    assert node.attributes['key'] == 'val'


def test_node_add_attribute():
    node = Node()

    node.add_attribute('key', 'val')
    assert 'key' in node.attributes
    assert node.attributes['key'] == 'val'


def test_node_add_attributes():
    node = Node()
    node.add_attributes({'key1': 'val1', 'key2': 'val2'})

    assert 'key1' in node.attributes
    assert node.attributes['key1'] == 'val1'

    assert 'key2' in node.attributes
    assert node.attributes['key2'] == 'val2'


def test_node_add_attributes_kwargs():
    node = Node()

    node.add_attributes(key='val')
    assert 'key' in node.attributes
    assert node.attributes['key'] == 'val'


def test_node_add_attributes_bad_input():
    node = Node()
    with pytest.raises(Exception):
        node.add_attributes([])
    with pytest.raises(Exception):
        node.add_attributes(2)
    with pytest.raises(Exception):
        node.add_attributes("Hello")


def test_node_remove_attribute():
    node = Node()
    node.add_attributes(key='val')

    assert 'key' in node.attributes

    node.remove_attribute('key')

    assert 'key' not in node.attributes
    assert node.attributes == {}


def test_node_remove_attribute_bad_input():
    node = Node()
    node.add_attributes(key='val')
    with pytest.raises(TypeError):
        node.remove_attribute([])


def test_node_add_child():
    node = Node()
    child = Node()

    node.add_child(child)

    assert child in node.child_nodes


def test_node_add_child_bad_input():
    node = Node()
    with pytest.raises(Exception):
        node.add_child("1egrerg")

    with pytest.raises(Exception):
        node.add_child(4)

    with pytest.raises(Exception):
        node.add_child({'child_attr': 'val'})


def test_node_add_children():
    node = Node()

    child1 = Node()
    child2 = Node()

    node.add_children([child1, child2])

    assert child1 in node.child_nodes
    assert child2 in node.child_nodes


def test_node_add_children_bad_input():
    node = Node()
    child1 = "aeraerwg"
    child2 = Node()

    with pytest.raises(Exception):
        node.add_children([child1, child2])


def test_node_getitem():
    node = Node()
    node.add_attribute('key', 'value')
    assert node['key'] == 'value'


def test_node_setitem():
    node = Node()
    node['key'] = 'value'

    assert 'key' in node.attributes
    assert node.attributes['key'] == 'value'


def test_node_to_dict_simple():
    node = Node()
    node.add_attributes({'key1': 'val', 'key2': 'val2'})

    dict_repr = node.to_dict()
    assert isinstance(dict_repr, dict)
    assert dict_repr['key1'] == 'val'
    assert dict_repr['key2'] == 'val2'


def test_node_with_children_to_dict():
    node = Node()
    node_2 = Node()

    node.add_attributes({'key1': 'val'})
    node_2.add_attributes({'key2': 'val2', 'key3': 'val3'})
    node.add_child(node_2)

    dict_repr = node.to_dict()
    assert isinstance(dict_repr, dict)
    assert 'children' in dict_repr
    assert dict_repr['children'][0]['key2'] == 'val2'
    assert dict_repr['children'][0]['key3'] == 'val3'


def test_tree_to_dict():
    node = Node()
    node.add_attribute('key', 'val')

    node_2 = Node()
    node_2.add_attribute('key2', 'val2')
    node.add_child(node_2)

    tree = Tree()
    tree.add_root(node)

    dict_repr = tree.to_dict()
    assert 'roots' in dict_repr
    roots = dict_repr['roots']

    assert len(roots) == 1

    assert 'key' in roots[0]
    assert 'children' in roots[0]
    assert 'key2' in roots[0]['children'][0]
