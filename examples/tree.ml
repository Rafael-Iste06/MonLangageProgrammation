root = TreeNode(1)
child1 = TreeNode(2)
child2 = TreeNode(3)

root.add_child(child1)
root.add_child(child2)

print(root.value)
print(root.children[0].value)
print(root.children[1].value)