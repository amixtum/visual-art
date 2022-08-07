class rbtree:
    def __init__(self, data=None, parent=None, l_child=None, r_child=None, size=1):
        self.data = data
        self.parent = parent
        self.l_child = l_child
        self.r_child = r_child
        self.size = size
    
    def empty(self):
        return self.data is None
    
    def is_root(self):
        return self.parent is None 
    
    def insert(self, item):
        if self.empty():
            self.data = item 
            self.size = 1

        else:
            it = self
            while True: # will return once it finds null pointer
                while item < it.data:
                    it.size += 1

                    if it.l_child is not None:
                        it = it.l_child

                    else:
                        it.l_child = bst(data=item, parent=it, l_child=None, r_child=None, size=1)
                        return it.l_child

                while item >= it.data:
                    it.size += 1

                    if it.r_child is not None:
                        it = it.r_child

                    else:
                        it.r_child = bst(data=item, parent=it, l_child=None, r_child=None, size=1)
                        return it.r_child

    def find(self, item):
        it = self
        done = False
        while not done: # not an infinite loop
            if item == it.data:
                return it

            while item < it.data:
                if it.l_child is not None:
                    it = it.l_child
                else:
                    return None 

            while item > it.data:
                if it.r_child is not None:
                    it = it.r_child
                else:
                    return None

        return None
    
    def predecessor(self, key):
        it = self
        tree = self.find(key)
        done = False
        if tree is not None:
            while not done:
                if tree.data == it.data:
                    if it.l_child is not None:
                        while it.r_child is not None:
                            it = it.r_child
                        return it 
                    else:
                        while it.data >= tree.data:
                            if it.parent is not None:
                                it = it.parent
                            else:
                                return None
                        return it
        else:
            return None

    def successor(self, key):
        it = self
        tree = self.find(key)
        done = False
        if tree is not None:
            while not done:
                if tree.data == it.data:
                    if it.r_child is not None:
                        while it.l_child is not None:
                            it = it.l_child
                        return it 

                    else:
                        while it.data <= tree.data:
                            if it.parent is not None:
                                it = it.parent

                            else:
                                return None

                        return it

        else:
            return None
                    
    def delete(self, item):
        to_delete = self.find(item)
        if to_delete is not None:
            if to_delete.l_child is None and to_delete.r_child is None:
                if to_delete.parent.l_child == to_delete:
                    to_delete.parent.l_child = None

                elif to_delete.parent.r_child == to_delete:
                    to_delete.parent.r_child = None

                size_it = to_delete.parent
                while size_it is not None:
                    size_it.size -= 1
                    size_it = size_it.parent
                # to_delete.parent = None ?

            elif to_delete.l_child is None:
                if to_delete.parent.l_child == to_delete:
                    to_delete.parent.l_child = to_delete.r_child

                elif to_delete.parent.r_child == to_delete:
                    to_delete.parent.r_child = to_delete.r_child

                to_delete.r_child.parent = to_delete.parent

                size_it = to_delete.parent
                while size_it is not None:
                    size_it.size -= 1
                    size_it = size_it.parent

            elif to_delete.r_child is None:
                if to_delete.parent.l_child == to_delete:
                    to_delete.parent.l_child = to_delete.l_child

                elif to_delete.parent.r_child == to_delete:
                    to_delete.parent.r_child = to_delete.l_child

                to_delete.l_child.parent = to_delete.parent

                size_it = to_delete.parent
                while size_it is not None:
                    size_it.size -= 1
                    size_it = size_it.parent

            else:
                pred = self.predecessor(to_delete.data)

                if pred is not None:
                    to_delete.data = pred.data

                    if pred.parent.l_child == pred:
                        pred.parent.l_child = pred.l_child

                    elif pred.parent.r_child == pred:
                        pred.parent.r_child = pred.l_child
                    
                    size_it = pred.parent
                    while size_it is not None:
                        size_it.size -= 1
                        size_it = size_it.parent
    
    def select(self, index):
        return self.__select(self, index)
    
    def __select(self, node, index):
        if index >= node.size:
            return None
        a = 0
        if node.l_child is not None:
            a = node.l_child.size

        if a == index - 1:
            return node

        elif a > index - 1:
            return self.__select(node.l_child, index)
        
        else: # a < index - 1
            return self.__select(node.r_child, index - a - 1)
    
    def rank(self, node):
        if node is not None:
            if self.find(node.data) is not None:
                return self.__rank(self, node.data)
            return -1
        return -1
    
    def __rank(self, node, x):
        if node is None:
            return 0

        if node.data <= x:
            return 1 + self.__rank(node.l_child, x) + self.__rank(node.r_child, x)

        else:
            return self.__rank(node.l_child, x)


def inorder_traverse(tree):
    if tree is None:
        return
    inorder_traverse(tree.l_child) 
    print(tree.data)
    inorder_traverse(tree.r_child)

