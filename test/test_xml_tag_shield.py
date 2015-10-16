from browsergui.elements import XMLTagShield

from . import BrowserGUITestCase

class XMLTagShieldTest(BrowserGUITestCase):

  def setUp(self):
    self.shield = XMLTagShield(tag_name='a')

  def test_children(self):
    self.assertEqual([], self.shield.children)
    left = XMLTagShield('l')
    right = XMLTagShield('r')
    self.shield.tag.appendChild(left.tag)
    self.assertEqual([left], self.shield.children)
    self.shield.tag.appendChild(right.tag)
    self.assertEqual([left, right], self.shield.children)
    self.shield.tag.removeChild(left.tag)
    self.assertEqual([right], self.shield.children)

  def test_children__deep(self):
    intermediate = self.shield.tag.ownerDocument.createElement('x')
    left = XMLTagShield('l')
    right = XMLTagShield('r')
    self.shield.tag.appendChild(intermediate)
    self.shield.tag.appendChild(right.tag)
    intermediate.appendChild(left.tag)
    self.assertEqual([left,right], self.shield.children)

  def test_children__prunes_at_immediate_children(self):
    child = XMLTagShield('c')
    grandchild = XMLTagShield('gc')
    self.shield.tag.appendChild(child.tag)
    child.tag.appendChild(grandchild.tag)
    self.assertEqual([child], self.shield.children)

  def test_parent(self):
    parent = XMLTagShield('p')
    parent.tag.appendChild(self.shield.tag)
    self.assertEqual(parent, self.shield.parent)

  def test_parent_deep(self):
    parent = XMLTagShield('p')
    intermediate = self.shield.tag.ownerDocument.createElement('x')
    parent.tag.appendChild(intermediate)
    intermediate.appendChild(self.shield.tag)
    self.assertEqual(parent, self.shield.parent)

  def test_ancestors(self):
    self.assertEqual([], self.shield.ancestors)

    child = XMLTagShield('c')
    grandchild = XMLTagShield('gc')
    self.shield.tag.appendChild(child.tag)
    child.tag.appendChild(grandchild.tag)
    self.assertEqual([child, self.shield], grandchild.ancestors)

  def test_orphaned(self):
    self.assertTrue(self.shield.orphaned)
    XMLTagShield('p').tag.appendChild(self.shield.tag)
    self.assertFalse(self.shield.orphaned)

  def test_root(self):
    self.assertEqual(self.shield, self.shield.root)

    parent = XMLTagShield('p')
    parent.tag.appendChild(self.shield.tag)
    self.assertEqual(parent, self.shield.root)

    intermediate = self.shield.tag.ownerDocument.createElement('x')
    grandparent = XMLTagShield('gp')
    grandparent.tag.appendChild(intermediate)
    intermediate.appendChild(parent.tag)
    self.assertEqual(grandparent, self.shield.root)
