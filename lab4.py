# Data Structures
# Adrian Sanchez
# Lab 3 - Option B
# Diego Aguirre
# 10/22/19
# Purpose: To store words in the english dictionary, which later is used with different types of BST's to find all of the permuatations or anagrams of the word
#          //using AVL tree as well as Red and Black tree

#node used for AVL tree
class TreeNode(object):
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None
        self.height = 1

#AVL tree implementation
class AVLTree(object):

    def insert(self, root, key):
        if not root:
            return TreeNode(key)
        elif key < root.val:
            root.left = self.insert(root.left, key)
        else:
            root.right = self.insert(root.right, key)
        
        root.height = 1 + max(self.getHeight(root.left), self.getHeight(root.right))

        balance = self.getBalance(root)

        if balance > 1 and key < root.left.val:
            return self.rightRotate(root)

        if balance < -1 and key > root.right.val:
            return self.leftRotate(root)

        if balance > 1 and key > root.left.val:
            root.left = self.leftRotate(root.left)
            return self.rightRotate(root)

        if balance < -1 and key < root.right.val:
            root.right = self.rightRotate(root.right)
            return self.leftRotate(root)

        return root

    def leftRotate(self, z):

        y = z.right
        T2 = y.left

        y.left = z
        z.right = T2

        z.height = 1 + max(self.getHeight(z.left), self.getHeight(z.right))
        y.height = 1 + max(self.getHeight(y.left), self.getHeight(y.right))

        return y

    def rightRotate(self, z):

        y = z.left
        T3 = y.right

        y.right = z
        z.left = T3

        z.height = 1 + max(self.getHeight(z.left), self.getHeight(z.right))
        y.height = 1 + max(self.getHeight(y.left), self.getHeight(y.right))

        return y

    def getHeight(self, root):
        if not root:
            return 0

        return root.height

    def getBalance(self, root):
        if not root:
            return 0

        return self.getHeight(root.left) - self.getHeight(root.right)

    def search(self, root, key):
        if root is None:
            return False
        if root.val == key:
            return True
        if root.val > key:
            return self.search(root.left, key)
        else:
            return self.search(root.right, key)

#Red and black tree implementation
BLACK = 'BLACK'
RED = 'RED'
NIL = 'NIL'

class Node:
    def __init__(self, value, color, parent, left=None, right=None):
        self.value = value
        self.color = color
        self.parent = parent
        self.left = left
        self.right = right


class RedBlackTree:
    # every node has no children or leaf initially
    NIL_LEAF = Node(value=None, color=NIL, parent=None)

    def __init__(self):
        self.count = 0
        self.root = None
        self.ROTATIONS = {
            # Facilitates delition and rotation 
            'L': self._right_rotation,
            'R': self._left_rotation
        }

    def __iter__(self):
        if not self.root:
            return list()
        yield from self.root.__iter__()

    def add(self, value):
        if not self.root:
            self.root = Node(value, color=BLACK, parent=None, left=self.NIL_LEAF, right=self.NIL_LEAF)
            self.count += 1
            return
        parent, node_dir = self._find_parent(value)
        if node_dir is None:
            return  # value is in the tree
        new_node = Node(value=value, color=RED, parent=parent, left=self.NIL_LEAF, right=self.NIL_LEAF)
        if node_dir == 'L':
            parent.left = new_node
        else:
            parent.right = new_node

        self._try_rebalance(new_node)
        self.count += 1

    #Returns a boolean indicating if the given value is present in the tree
    def contains(self, value) -> bool:
        return bool(self.find_node(value))

    #checks if there is a need to rebalance the tree
    def _try_rebalance(self, node):
        parent = node.parent
        value = node.value
        if (parent is None  or parent.parent is None  
           or (node.color != RED or parent.color != RED)):  # no need to rebalance
            return
        grandfather = parent.parent
        node_dir = 'L' if parent.value > value else 'R'
        parent_dir = 'L' if grandfather.value > parent.value else 'R'
        uncle = grandfather.right if parent_dir == 'L' else grandfather.left
        general_direction = node_dir + parent_dir

        if uncle == self.NIL_LEAF or uncle.color == BLACK:
            # rotate
            if general_direction == 'LL':
                self._right_rotation(node, parent, grandfather, to_recolor=True)
            elif general_direction == 'RR':
                self._left_rotation(node, parent, grandfather, to_recolor=True)
            elif general_direction == 'LR':
                self._right_rotation(node=None, parent=node, grandfather=parent)
                # node becomes parent due to rotation
                self._left_rotation(node=parent, parent=node, grandfather=grandfather, to_recolor=True)
            elif general_direction == 'RL':
                self._left_rotation(node=None, parent=node, grandfather=parent)
                # node becomes parent due to rotation
                self._right_rotation(node=parent, parent=node, grandfather=grandfather, to_recolor=True)
            else:
                raise Exception("What? Cant".format(general_direction))
        else:  
            self._recolor(grandfather)

    #adjusts parents of subtrees
    def __update_parent(self, node, parent_old_child, new_parent):
        node.parent = new_parent
        if new_parent:
            # Determine the old child's position in order to put node there
            if new_parent.value > parent_old_child.value:
                new_parent.left = node
            else:
                new_parent.right = node
        else:
            self.root = node

    def _right_rotation(self, node, parent, grandfather, to_recolor=False):
        grand_grandfather = grandfather.parent
        self.__update_parent(node=parent, parent_old_child=grandfather, new_parent=grand_grandfather)

        old_right = parent.right
        parent.right = grandfather
        grandfather.parent = parent

        grandfather.left = old_right  # save the old right values
        old_right.parent = grandfather

        if to_recolor:
            parent.color = BLACK
            node.color = RED
            grandfather.color = RED

    def _left_rotation(self, node, parent, grandfather, to_recolor=False):
        grand_grandfather = grandfather.parent
        self.__update_parent(node=parent, parent_old_child=grandfather, new_parent=grand_grandfather)

        old_left = parent.left
        parent.left = grandfather
        grandfather.parent = parent

        grandfather.right = old_left  # save the old left values
        old_left.parent = grandfather

        if to_recolor:
            parent.color = BLACK
            node.color = RED
            grandfather.color = RED

    def _recolor(self, grandfather):
        grandfather.right.color = BLACK
        grandfather.left.color = BLACK
        if grandfather != self.root:
            grandfather.color = RED
        self._try_rebalance(grandfather)

    def _find_parent(self, value):
        def inner_find(parent):
            if value == parent.value:
                return None, None
            elif parent.value < value:
                if parent.right.color == NIL:  # done
                    return parent, 'R'
                return inner_find(parent.right)
            elif value < parent.value:
                if parent.left.color == NIL:  # done
                    return parent, 'L'
                return inner_find(parent.left)

        return inner_find(self.root)

    def find_node(self, value):
        def inner_find(root):
            if root is None or root == self.NIL_LEAF:
                return None
            if value > root.value:
                return inner_find(root.right)
            elif value < root.value:
                return inner_find(root.left)
            else:
                return root

        found_node = inner_find(self.root)
        return found_node

class BTreeNode:
    # Constructor
    def __init__(self, keys=[], children=[], is_leaf=True, max_num_keys=5):
        self.keys = keys
        self.children = children
        self.is_leaf = is_leaf
        if max_num_keys < 3:  # max_num_keys must be odd and greater or equal to 3
            max_num_keys = 3
        if max_num_keys % 2 == 0:  # max_num_keys must be odd and greater or equal to 3
            max_num_keys += 1
        self.max_num_keys = max_num_keys

    def is_full(self):
        return len(self.keys) >= self.max_num_keys


class BTree:
    # Constructor
    def __init__(self, max_num_keys=5):
        self.max_num_keys = max_num_keys
        self.root = BTreeNode(max_num_keys=max_num_keys)

    def find_child(self, k, node=None):
        # Determines value of c, such that k must be in subtree node.children[c], if k is in the BTree
        if node is None:
            node = self.root

        for i in range(len(node.keys)):
            if k < node.keys[i]:
                return i
        return len(node.keys)

    def insert_internal(self, i, node=None):

        if node is None:
            node = self.root

        # node cannot be Full
        if node.is_leaf:
            self.insert_leaf(i, node)
        else:
            k = self.find_child(i, node)
            if node.children[k].is_full():
                m, l, r = self.split(node.children[k])
                node.keys.insert(k, m)
                node.children[k] = l
                node.children.insert(k + 1, r)
                k = self.find_child(i, node)
            self.insert_internal(i, node.children[k])

    def split(self, node=None):
        if node is None:
            node = self.root
        # print('Splitting')
        # PrintNode(T)
        mid = node.max_num_keys // 2
        if node.is_leaf:
            left_child = BTreeNode(node.keys[:mid], max_num_keys=node.max_num_keys)
            right_child = BTreeNode(node.keys[mid + 1:], max_num_keys=node.max_num_keys)
        else:
            left_child = BTreeNode(node.keys[:mid], node.children[:mid + 1], node.is_leaf, max_num_keys=node.max_num_keys)
            right_child = BTreeNode(node.keys[mid + 1:], node.children[mid + 1:], node.is_leaf, max_num_keys=node.max_num_keys)
        return node.keys[mid], left_child, right_child

    def insert_leaf(self, i, node=None):
        if node is None:
            node = self.root

        node.keys.append(i)
        node.keys.sort()

    def leaves(self, node=None):
        if node is None:
            node = self.root
        # Returns the leaves in a b-tree
        if node.is_leaf:
            return [node.keys]
        s = []
        for c in node.children:
            s = s + self.leaves(c)
        return s

    def insert(self, i, node=None):
        if node is None:
            node = self.root
        if not node.is_full():
            self.insert_internal(i, node)
        else:
            m, l, r = self.split(node)
            node.keys = [m]
            node.children = [l, r]
            node.is_leaf = False
            k = self.find_child(i, node)
            self.insert_internal(i, node.children[k])

    def height(self, node=None):
        if node is None:
            node = self.root
        if node.is_leaf:
            return 0
        return 1 + self.height(node.children[0])

    def print(self, node=None):
        # Prints keys in tree in ascending order
        if node is None:
            node = self.root

        if node.is_leaf:
            for t in node.keys:
                print(t, end=' ')
        else:
            for i in range(len(node.keys)):
                self.print(node.children[i])
                print(node.keys[i], end=' ')
            self.print(node.children[len(node.keys)])

    def print_d(self, space, node=None):
        if node is None:
            node = self.root
        # Prints keys and structure of B-tree
        if node.is_leaf:
            for i in range(len(node.keys) - 1, -1, -1):
                print(space, node.keys[i])
        else:
            self.print_d(space + '   ', node.children[len(node.keys)])
            for i in range(len(node.keys) - 1, -1, -1):
                print(space, node.keys[i])
                self.print_d(space + '   ', node.children[i])

    def search(self, k, node=None):
        if node is None:
            node = self.root
        # Returns node where k is, or None if k is not in the tree
        if k in node.keys:
            return node
        if node.is_leaf:
            return None
        return self.search(k, node.children[self.find_child(k, node)])

    def _set_x(self, dx, node=None):
        if node is None:
            node = self.root
        # Finds x-coordinate to display each node in the tree
        if node.is_leaf:
            return
        else:
            for c in node.children:
                self._set_x(dx, c)
            d = (dx[node.children[0].keys[0]] + dx[node.children[-1].keys[0]] + 10 * len(node.children[-1].keys)) / 2
            dx[node.keys[0]] = d - 10 * len(node.keys) / 2

    def _draw_btree(self, dx, y, y_inc, fs, ax, node=None):
        if node is None:
            node = self.root
        # Function to display b-tree to the screen
        # It works fine for trees with up to about 70 keys
        xs = dx[node.keys[0]]
        if node.is_leaf:
            for itm in node.keys:
                ax.plot([xs, xs + 10, xs + 10, xs, xs], [y, y, y - 10, y - 10, y], linewidth=1, color='k')
                ax.text(xs + 5, y - 5, str(itm), ha="center", va="center", fontsize=fs)
                xs += 10
        else:
            for i in range(len(node.keys)):
                xc = dx[node.children[i].keys[0]] + 5 * len(node.children[i].keys)
                ax.plot([xs, xs + 10, xs + 10, xs, xs], [y, y, y - 10, y - 10, y], linewidth=1, color='k')
                ax.text(xs + 5, y - 5, str(node.keys[i]), ha="center", va="center", fontsize=fs)
                ax.plot([xs, xc], [y - 10, y - y_inc], linewidth=1, color='k')
                self._draw_btree(dx, y - y_inc, y_inc, fs, ax, node.children[i])
                xs += 10
            xc = dx[node.children[-1].keys[0]] + 5 * len(node.children[-1].keys)
            ax.plot([xs, xc], [y - 10, y - y_inc], linewidth=1, color='k')
            self._draw_btree(dx, y - y_inc, y_inc, fs, ax, node.children[-1])

    def draw(self):
        # Find x-coordinates of leaves
        ll = self.leaves()
        dx = {}
        d = 0
        for l in ll:
            dx[l[0]] = d
            d += 10 * (len(l) + 1)
            # Find x-coordinates of internal nodes
        self._set_x(dx)
#############################################################
def print_anagrams_avl(word, prefix=""):
   if len(word) <= 1:
       str = prefix + word

       if (avl_tree.search(root, str) == True):
          print(prefix + word)
   else:
       for i in range(len(word)):
           cur = word[i: i + 1]
           before = word[0: i] # letters before cur
           after = word[i + 1:] # letters after cur
           if cur not in before: # Check if permutations of cur have not been generated.
              print_anagrams_avl(before + after, prefix + cur)

def print_anagrams_rb(word, prefix=""):
   if len(word) <= 1:
       str = prefix + word

       if (rb_tree.contains(str)):
           print(prefix + word)
   else:
       for i in range(len(word)):
           cur = word[i: i + 1]
           before = word[0: i] # letters before cur
           after = word[i + 1:] # letters after cur
           if cur not in before: # Check if permutations of cur have not been generated.
               print_anagrams_rb(before + after, prefix + cur)

def print_anagrams_BT(word, prefix=""):
   if len(word) <= 1:
       #str = prefix + word
       str = prefix + word
################################
       if (b_tree.search(str,b_tree.root)):
           print(prefix + word)
############
   else:
       for i in range(len(word)):
           cur = word[i: i + 1]
           before = word[0: i] # letters before cur
           after = word[i + 1:] # letters after cur
           if cur not in before: # Check if permutations of cur have not been generated.
               print_anagrams_BT(before + after, prefix + cur)
             
def count_anagrams_avl(word, prefix=""):
    count = 0
    if len(word) <= 1:
       str = prefix + word

       if (avl_tree.search(root, str) == True):
           return 1 
    else:
       for i in range(len(word)):
           cur = word[i: i + 1]
           before = word[0: i] # letters before cur
           after = word[i + 1:] # letters after cur

           if cur not in before: # Check if permutations of cur have not been generated.
              count += count_anagrams_avl(before + after, prefix + cur) # recursive call that will add count
    return count

def count_anagrams_rb(word, prefix=""):
    count = 0
    if len(word) <= 1:
       str = prefix + word

       if (rb_tree.contains(str)):
           return 1
           # print(prefix + word)
    else:
       for i in range(len(word)):
           cur = word[i: i + 1]
           before = word[0: i] # letters before cur
           after = word[i + 1:] # letters after cur

           if cur not in before: # Check if permutations of cur have not been generated.
               count += count_anagrams_rb(before + after, prefix + cur)
    return count

def count_anagrams_BT(word, prefix=""):
    count = 0
    if len(word) <= 1:
       str = prefix + word

       if (b_tree.search(str,b_tree.root)):
           return 1
           # print(prefix + word)
    else:
       for i in range(len(word)):
           cur = word[i: i + 1]
           before = word[0: i] # letters before cur
           after = word[i + 1:] # letters after cur

           if cur not in before: # Check if permutations of cur have not been generated.
               count += count_anagrams_BT(before + after, prefix + cur)
    return count

def find_max_anagrams(list): # this method will find the word with the most amount of anagrams given a list
    max = 0
    word = ""
    for i in range(len(list)):
        num = count_anagrams_avl(list[i]) # sets the returned value of the method to num
        if num > max: # if num is greater than max, this if-statement will execute
            max = num
            word = list[i]
    print(word) #prints the word with the most amount of anagrams

list = []
max_list = []
with open("words.txt", "r") as f: 
    for line in f:
        current_line = line.split()
        word = current_line[0]
        list.append(word)
        max_list.append(word)

print("Enter a word you'd like to know the anagrams for")
word = input()
print("Enter 1 for an AVL tree organization")
print("Enter 2 for a Red and Black tree organization")
print("Enter 3 for a B-Tree organization")
inp = input()

if int(inp) == 1:
    print("Working on it... filling tree...")
    avl_tree = AVLTree()
    root = None
    for i in range(len(list)):
        root = avl_tree.insert(root, list[i])
    print_anagrams_avl(word)
    print("There are ")
    print(count_anagrams_avl(word))
    print(" number of anagrams for the word " + word)

if int(inp) == 2:
    print("Working on it... filling tree...")
    rb_tree = RedBlackTree()
    for i in range(len(list)):
        rb_tree.add(list[i])
    print_anagrams_rb(word)
    print("There are ")
    print(count_anagrams_rb(word))
    print("number of anagrams for the word " + word)

if int(inp) == 3:
    print("Working on it... filling tree...")
    b_tree = BTree()
    for i in range(len(list)):
        b_tree.insert(list[i])
    print_anagrams_BT(word)
    print("There are ")
    print(count_anagrams_BT(word))
    print("number of anagrams for the word " + word)
    
#print("Processing the word with the most amount of anagrams in given list...")
#find_max_anagrams(max_list)
