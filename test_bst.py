from bst.bst import bst, inorder_traverse
from random import shuffle

t = bst()
r = [x for x in range(10)]
shuffle(r)
print(r)
for n in r:
    t.insert(n)

st_5 = t.find(5)

inorder_traverse((st_5))