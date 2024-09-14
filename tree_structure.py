class Node:
    def __init__(self, value):
        self.value = value
        self.children = []

    def add_child(self, child_node):
        self.children.append(child_node)


class Tree:
    def __init__(self, root_value):
        self.root = Node(root_value)

    def add_node(self, parent_value, child_value):
        parent_node = self.find_node(self.root, parent_value)
        if parent_node:
            parent_node.add_child(Node(child_value))
        else:
            print(f"Parent node with value '{parent_value}' not found.")

    def find_node(self, node, value):
        if node.value == value:
            return node

        for child in node.children:
            result = self.find_node(child, value)
            if result:
                return result
        return None

    def display(self, node=None, level=0):
        if node is None:
            node = self.root

        print("  " * level + f"- {node.value}")
        for child in node.children:
            self.display(child, level + 1)


if __name__ == "__main__":
    # Initialize the tree with the root node
    tree = Tree("Root")

    # Add nodes to the tree
    tree.add_node("Root", "Child 1")
    tree.add_node("Root", "Child 2")
    tree.add_node("Child 1", "Child 1.1")
    tree.add_node("Child 1", "Child 1.2")
    tree.add_node("Child 2", "Child 2.1")

    # Display the tree
    print("Tree structure:")
    tree.display()
