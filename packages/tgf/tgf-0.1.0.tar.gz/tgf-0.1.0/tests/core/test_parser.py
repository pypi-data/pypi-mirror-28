import json

import six

from tgf.core.parser import parse_string, serialize_to_string, serialize_json_to_string
from tgf.core.tree import Tree, Node

xml_1 = """
<tgf version="1.0">
    <tree>
        <node type="Text" root="true">
            <attribute name="title">Some title</attribute>
            <attribute name="titleTranslation">Title translation</attribute>
            <node type="Phrase">
                <attribute name="phrase">Dette er en frase</attribute>
            </node>
        </node>
    </tree>
    <metadata>

    </metadata>
</tgf>
"""


def test_parser_returns_tree():
    tree = parse_string(xml_1)
    assert isinstance(tree, Tree)


def test_parser_returns_nested_nodes():
    tree = parse_string(xml_1)

    assert len(tree.roots) > 0
    root = tree.roots[0]
    assert isinstance(root, Node)
    assert root.node_type == 'Text'

    children = root.child_nodes
    assert len(children) == 1

    phrase_child = children[0]

    assert phrase_child.node_type == "Phrase"
    assert 'phrase' in phrase_child.attributes
    assert phrase_child.attributes['phrase'] == 'Dette er en frase'


def test_serialize_to_string():
    tree = parse_string(xml_1)

    # We use lower here, as there are some case inconsistencies across
    # python versions
    serialized = serialize_to_string(tree).lower()
    assert "<?xml version='1.0' encoding='utf-8'?>".lower() in serialized
    assert "<tgf version=\"1.0\">" in serialized
    assert "<tree>" in serialized
    assert "<node type=\"text\">" in serialized
    assert "<node type=\"phrase\">" in serialized
    assert "<attribute name=\"title\">some title</attribute>" in serialized
    assert "<attribute name=\"phrase\">dette er en frase</attribute>" in serialized


def test_serialize_json_to_string():
    tree = parse_string(xml_1)
    serialized = serialize_json_to_string(tree)

    assert isinstance(serialized, six.string_types)
    assert "\"roots\"" in serialized
    assert "phrase" in serialized
    assert "titleTranslation" in serialized
    assert "children" in serialized


def test_serialize_json_to_string_and_reverse_produces_identical_results():
    tree = parse_string(xml_1)
    new_tree = json.loads((serialize_json_to_string(tree)))

    assert tree.to_dict() == new_tree


