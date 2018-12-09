from pprint import pprint
from collections import defaultdict


def resolve(current_node, nodes):
    result = ""
    while len(result) < len(nodes):
        result += current_node.name
        current_node.resolved = True
        try:
            current_node = sorted([node for node in nodes if node.is_available], key=lambda n: n.name)[0]
        except IndexError:
            # last one
            pass
    return result


class Node(object):
    def __init__(self, name, parents, children):
        self.parents = parents
        self.children = children
        self.resolved = False
        self.name = name

    @classmethod
    def init_empty(self):
        return Node("", [],  [])

    @property
    def is_available(self):
        return all([p.resolved for p in self.parents]) and not self.resolved

    @property
    def is_root(self):
        return len(self.parents) == 0

    def add_child(self, *children):
        self.children.extend(children)

    def __repr__(self):
        return "<{} available:{} children:{}>".format(self.name, self.is_available, ','.join([x.name for x in self.children]))


if __name__ == '__main__':
    data = map(lambda x: x.split(), open('input7').read().splitlines())
    nodes = defaultdict(Node.init_empty)
    mapping = defaultdict(list)

    for d in data:
        parent, child = d[1], d[-3]
        parent_node = nodes[parent]
        child_node = nodes[child]
        child_node.name = child
        parent_node.name = parent
        parent_node.add_child(child_node)
        child_node.parents.append(parent_node)
        mapping[parent].append(child)

    entrypoint = sorted([v for k, v in nodes.items() if v.is_root and v.is_available], key=lambda x: x.name)[0]
    pprint(mapping)
    pprint(nodes)
    print("Part 1: " + resolve(entrypoint, nodes.values()))
