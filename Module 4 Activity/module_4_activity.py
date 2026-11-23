# Module 4 Activity

import csv
import os

class TreeNode:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None
        self.height = 1
        self.count = 1

def getHeight(node):
    if node:
        return node.height
    else:
        return 0

def getBalance(node):
    if node:
        balance = getHeight(node.left) - getHeight(node.right)
        return balance
    else:
        return 0

def rightRotate(node: TreeNode) -> TreeNode:
    # rotate nodes
    lChild = node.left
    lrGrand = lChild.right
    lChild.right = node
    node.left = lrGrand

    # Update heights after rotation
    node.height = 1 + max(getHeight(node.left), getHeight(node.right))
    lChild.height = 1 + max(getHeight(lChild.left), getHeight(lChild.right))
    # returns the new root of the subtree
    return lChild

def leftRotate(node: TreeNode) -> TreeNode:
    # rotate nodes
    rChild = node.right
    rlGrand = rChild.left
    rChild.left = node
    node.right = rlGrand

    # Update heights after rotation
    node.height = 1 + max(getHeight(node.left), getHeight(node.right))
    rChild.height = 1 + max(getHeight(rChild.left), getHeight(rChild.right))
    # returns the new root of the subtree
    return rChild

def insert(node: TreeNode, val) -> TreeNode:
    # base case: inserts at a null position, causing recursive stack to unwind
    if not node:
        return TreeNode(val)

    # recursive tree traversal for insertion
    if val < node.val:
        node.left = insert(node.left, val)
    elif val > node.val:
        node.right = insert(node.right, val)
    else:
        node.count += 1
        return node

    # update the height of nodes and get balance as recursive stack unwinds
    node.height = 1 + max(getHeight(node.left), getHeight(node.right))
    balance = getBalance(node)

    # Balance factors are greater than 1. Left starting:
    # Node was inserted below the left child and left subtree
    if balance > 1 and val < node.left.val:
        return rightRotate(node)

    # Node was inserted below the left child and right subtree
    if balance > 1 and val > node.left.val:
        node.left = leftRotate(node.left)
        return rightRotate(node)

    # Balance factors are less than -1. Right starting:
    # Node was inserted below the right child and left subtree
    if balance < -1 and val < node.right.val:
        node.right = rightRotate(node.right)
        return leftRotate(node)
    
    # Node was inserted below the right child and right subtree
    if balance < -1 and val > node.right.val:
        return leftRotate(node)

    return node

# In-order traversal of the AVL tree to print first 50 nodes in sorted order
def inOrderTraversal(node: TreeNode, count = 0):
    if not node or count >= 50:
        return count
    
    count = inOrderTraversal(node.left, count)
    if count < 49:
        print(node.val, end = ', ')
        count += 1
    elif count == 49:
        print(node.val, end = '')
        count += 1

    count = inOrderTraversal(node.right, count)
    return count

# Searches tree for a specific value and returns boolean indicating if found, number of nodes traversed, and node's count if found
def searchTree(node: TreeNode, val):
    trav = 0

    while node:
        trav += 1

        if val == node.val:
            return True, trav, node.count
        elif val < node.val:
            node = node.left
        else:
            node = node.right

    return False, trav, 0

if __name__ == "__main__":
    basePath = os.path.dirname(__file__)
    filePath = os.path.join(basePath, 'resources/Module_4-1_Data_Set-3.csv')
    AVL_Tree = None

    try:
        with open(filePath, newline = '') as file:
            reader = csv.reader(file, delimiter = '|')
            header = next(reader, None) 

            for row in reader:
                # process each row and insert string val into AVL tree
                val = row[1].strip().lower()
                AVL_Tree = insert(AVL_Tree, val)

    except FileNotFoundError:
        print(f"File not found: {filePath}")
    except Exception as e:
        print(f"An error occurred: {e}")

    # in-order traversal of the AVL tree
    print("First 50 nodes of in-order traversal of the AVL tree:")
    inOrderTraversal(AVL_Tree)
    print()

    # search for a specific value in the AVL tree
    print()
    searchValue = "abacus" # can be changed to search for other values
    print(f'Searching for value "{searchValue}"')
    found, trav, nodeCount = searchTree(AVL_Tree, searchValue)
    if not found:
        print(f'"{searchValue}" was not found in AVL tree. Searched {trav} nodes.')
    else:
        print(f'"{searchValue}" was found in AVL tree. Searched {trav} nodes. Node count: {nodeCount}.')
