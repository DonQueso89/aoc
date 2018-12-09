from collections import defaultdict


def resolve_time(nodes, num_workers):
    done = ""
    time_spent = 0
    workers = {}
    available_nodes = sorted([v for v in nodes if v.is_root and v.is_available], key=lambda x: x.name)
    while len(done) < len(nodes):
        # Populate workers
        for node in available_nodes:
            if len(workers) < num_workers:
                workers[node.name] = node
        # Do work
        for node in workers:
            workers[node].tick()
        # Release resolvable nodes
        in_progress = list(workers.keys())
        for node in in_progress:
            if workers[node].resolved:
                done += workers.pop(node).name
        available_nodes = sorted([node for node in nodes if node.is_available], key=lambda n: n.name)
        time_spent += 1
    return time_spent


class Node(object):
    def __init__(self, name, parents, children):
        self.parents = parents
        self.children = children
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

    @property
    def resolved(self):
        return self.duration == 0

    def set_name(self, name):
        self.name = name
        self.duration = 60 + (ord(name) - 64)

    def add_child(self, *children):
        self.children.extend(children)

    def tick(self):
        self.duration -= 1

    def __repr__(self):
        return "<{} children:{} duration: {}>".format(self.name, ','.join([x.name for x in self.children]), self.duration)


if __name__ == '__main__':
    data = map(lambda x: x.split(), open('input7').read().splitlines())
    nodes = defaultdict(Node.init_empty)
    mapping = defaultdict(list)

    for d in data:
        parent, child = d[1], d[-3]
        parent_node = nodes[parent]
        child_node = nodes[child]
        child_node.set_name(child)
        parent_node.set_name(parent)
        parent_node.add_child(child_node)
        child_node.parents.append(parent_node)
        mapping[parent].append(child)

    time_spent = resolve_time(nodes.values(), 5)
    print("Part 2: " + str(time_spent))
