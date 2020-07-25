# modified from the MIT 6006 website

class BST(object):
    """
Simple binary search tree implementation.
This BST supports insert, find, and delete-min operations.
Each tree contains some (possibly 0) BSTnode objects, representing nodes,
and a pointer to the root.
"""

    def __init__(self):
        self.root = None

    def insert(self, t):
        """Insert key t into this BST, modifying it in-place."""
        new = BSTnode(t)
        if self.root is None:
            self.root = new
        else:
            node = self.root
            while True:
                if t < node.key:
                    # Go left
                    if node.left is None:
                        node.left = new
                        new.parent = node
                        break
                    node = node.left
                else:
                    # Go right
                    if node.right is None:
                        node.right = new
                        new.parent = node
                        break
                    node = node.right
        return new

    def delete(self, key):
        # from provided solution
        node = self.find(key)
        if node is None:
            return None
        if node is self.root:
            pseudo_root = BSTnode(None)
            pseudo_root.left = self.root
            self.root.parent = pseudo_root
            deleted_node = self.root.delete()
            self.root = pseudo_root.left
            if self.root is not None:
                self.root.parent = None
            return deleted_node
        else:
            return node.delete()

    def find(self, t):
        """Return the node for key t if is in the tree, or None otherwise."""
        node = self.root
        while node is not None:
            if t == node.key:
                return node
            elif t < node.key:
                node = node.left
            else:
                node = node.right
        return None

    def delete_min(self):
        """Delete the minimum key (and return the old node containing it)."""
        if self.root is None:
            return None, None
        else:
            # Walk to leftmost node.
            node = self.root
            while node.left is not None:
                node = node.left
            # Remove that node and promote its right subtree.
            if node.parent is not None:
                node.parent.left = node.right
            else: # The root was smallest.
                self.root = node.right
            if node.right is not None:
                node.right.parent = node.parent
            parent = node.parent
            node.disconnect()
            return node, parent

    def lca(self, low_key, high_key):
        return self.root and self.root.lca(low_key, high_key)

    def list(self, low_key, high_key):
        """A list containing the nodes with keys between low_key and high_key."""
        result = []
        lca = self.lca(low_key, high_key)
        if lca is not None:
            lca.list(low_key, high_key, result)
        return result
    
    def rank(self, key):
        """Number of keys <= the given key in the tree."""
        if self.root is not None:
            return self.root.rank(key)
        return 0

    def __str__(self):
        if self.root is None: return '<empty tree>'
        def recurse(node):
            if node is None: return [], 0, 0
            label = str(node.key)
            left_lines, left_pos, left_width = recurse(node.left)
            right_lines, right_pos, right_width = recurse(node.right)
            middle = max(right_pos + left_width - left_pos + 1, len(label), 2)
            pos = left_pos + middle // 2
            width = left_pos + middle + right_width - right_pos
            while len(left_lines) < len(right_lines):
                left_lines.append(' ' * left_width)
            while len(right_lines) < len(left_lines):
                right_lines.append(' ' * right_width)
            if (middle - len(label)) % 2 == 1 and node.parent is not None and \
               node is node.parent.left and len(label) < middle:
                label += '.'
            label = label.center(middle, '.')
            if label[0] == '.': label = ' ' + label[1:]
            if label[-1] == '.': label = label[:-1] + ' '
            lines = [' ' * left_pos + label + ' ' * (right_width - right_pos),
                     ' ' * left_pos + '/' + ' ' * (middle-2) +
                     '\\' + ' ' * (right_width - right_pos)] + \
              [left_line + ' ' * (width - left_width - right_width) +
               right_line
               for left_line, right_line in zip(left_lines, right_lines)]
            return lines, pos, width
        return '\n'.join(recurse(self.root) [0])

class BSTnode(object):
    """
Representation of a node in a binary search tree.
Has a left child, right child, and key value.
"""
    def __init__(self, t):
        """Create a new leaf with key t."""
        self.key = t
        self.disconnect()
    def disconnect(self):
        self.left = None
        self.right = None
        self.parent = None
    
    def min(self):
        if self.left is None:
            return self
        return self.left.min()
    def successor(self):
        if self.right is not None:
            return self.right.min()
        current = self
        while current.parent is not None and current is current.parent.right:
            current = current.parent
        return current.parent

    def delete(self):
        if self.left is None or self.right is None:
            if self is self.parent.left:
                self.parent.left = self.left or self.right
                if self.parent.left is not None:
                    self.parent.left.parent = self.parent
            else:
                self.parent.right = self.left or self.right
                if self.parent.right is not None:
                    self.parent.right.parent = self.parent
            return self
        else:
            s = self.successor()
            # NOTE: deleting before swapping the keys so the BST RI is never violated.
            deleted_node = s.delete()
            self.key, s.key = s.key, self.key
            return deleted_node
    def rank(self, key):
        """Number of keys <= the given key in the subtree rooted at this node."""
        if key < self.key:
            if self.left is not None:
                return self.left.rank(key)
            else:
                return 0
        if self.left:
            lrank = 1 + self.left.gamma
        else:
            lrank = 1
        if key > self.key and self.right is not None:
            return lrank + self.right.rank(key)
        return lrank
    def lca(self, low_key, high_key):
        if low_key <= self.key <= high_key:
            return self
        if low_key < self.key:
            return self.left and self.left.lca(low_key, high_key)
        else:
            return self.right and self.right.lca(low_key, high_key)
    def list(self, low_key, high_key, result):
        if low_key <= self.key <= high_key:
            result.append(self)
        if self.left is not None and low_key <= self.key:
            self.left.list(low_key, high_key, result)
        if self.right is not None and self.key <= high_key:
            self.right.list(low_key, high_key, result)

def test(args=None, BSTtype=BST):
    import random, sys
    if not args:
        args = sys.argv[1:]
    if not args:
        print 'usage: %s <number-of-random-items | item item item ...>' % \
            sys.argv[0]
        sys.exit()
    elif len(args) == 1:
        items = (random.randrange(100) for i in xrange(int(args[0])))
    else:
        items = [int(i) for i in args]

    tree = BSTtype()
    print tree
    for item in items:
        tree.insert(item)
        print
        print tree

if __name__ == '__main__': test()
