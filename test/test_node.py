import unittest
from browsergui.elements._node import Node, LeafNode, SequenceNode, OrphanedError, NotOrphanedError


class NodeTest(unittest.TestCase):
  def test_children_raises_error_for_plain_node(self):
    with self.assertRaises(NotImplementedError):
      Node().children

  def test_parent_is_initially_None(self):
    self.assertIsNone(Node().parent)

  def test_parent_can_be_set(self):
    child = Node()
    parent = Node()
    child.parent = parent
    self.assertEqual(child.parent, parent)

  def test_parent_can_be_unset(self):
    child = Node()
    parent = Node()
    child.parent = parent
    child.parent = None
    self.assertIsNone(child.parent)

  def test_set_parent_raises_error_if_parent_already_exists(self):
    child = Node()
    parent = Node()
    child.parent = parent

    abductor = Node()
    with self.assertRaises(NotOrphanedError):
      child.parent = abductor

    self.assertEqual(child.parent, parent)

  def test_parent_links_are_weak(self):
    child = Node()
    child.parent = Node()

    # The parent should have been immediately garbage-collected,
    # so the child's parent should be None now.
    self.assertIsNone(child.parent)

  def test_orphaned(self):
    child = Node()
    parent = Node()

    self.assertTrue(child.orphaned)
    child.parent = parent
    self.assertFalse(child.orphaned)

  def test_root(self):
    child = Node()
    parent = Node()
    grandparent = Node()

    self.assertEqual(child, child.root)
    child.parent = parent
    self.assertEqual(parent, child.root)
    parent.parent = grandparent
    self.assertEqual(grandparent, child.root)

  def test_walk(self):
    top = SequenceNode()
    left = SequenceNode()
    right = SequenceNode()
    bottom_right = LeafNode()

    self.assertEqual([top], list(top.walk()))

    top.append(left)
    self.assertEqual([top, left], list(top.walk()))

    right.append(bottom_right)
    top.append(right)
    self.assertEqual([top, left, right, bottom_right], list(top.walk()))

    self.assertEqual([right, bottom_right], list(right.walk()))

class SequenceNodeTest(unittest.TestCase):
  def test_constructor(self):
    a = LeafNode()
    b = LeafNode()

    self.assertEqual([], list(SequenceNode().children))

    parent = SequenceNode((a, b))
    self.assertEqual(parent, a.parent)
    self.assertEqual(parent, b.parent)
    self.assertEqual([a, b], list(parent.children))

  def test_append(self):
    node = SequenceNode()
    left = LeafNode()
    right = LeafNode()

    node.append(left)
    self.assertEqual([left], list(node.children))
    self.assertEqual(node, left.parent)

    node.append(right)
    self.assertEqual([left, right], list(node.children))

  def test_insert_before(self):
    node = SequenceNode()
    left = LeafNode()
    right = LeafNode()

    node.append(right)
    node.insert_before(left, reference_child=right)
    self.assertEqual([left, right], list(node.children))

  def test_insert_after(self):
    node = SequenceNode()
    left = LeafNode()
    right = LeafNode()

    node.append(left)
    node.insert_after(right, reference_child=left)
    self.assertEqual([left, right], list(node.children))

  def test_disown(self):
    node = SequenceNode()
    child = LeafNode()
    node.append(child)

    node.disown(child)
    self.assertIsNone(child.parent)
    self.assertEqual([], list(node.children))
