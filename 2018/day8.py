def resolve_sum(tree):
    num_children, num_metadata = tree.pop(), tree.pop()
    total_metadata = 0
    for i in range(num_children):
        tree, metadata = resolve_sum(tree)
        total_metadata += metadata

    for i in range(num_metadata):
        total_metadata += tree.pop()

    return tree, total_metadata


def resolve_sum_indexes(tree):
    num_children, num_metadata = tree.pop(), tree.pop()
    child_metadata = []
    for i in range(num_children):
        tree, metadata = resolve_sum_indexes(tree)
        child_metadata.append(metadata)

    total_metadata = 0
    if num_children:
        for i in range(num_metadata):
            try:
                idx = tree.pop()
                if idx > 0:
                    total_metadata += child_metadata[idx - 1]
            except IndexError:
                # reference to non-existing child
                pass
    else:
        total_metadata += sum([tree.pop() for x in range(num_metadata)])

    return tree, total_metadata


if __name__ == '__main__':
    data = [int(x) for x in open('input8').read().split()]
    data.reverse()
    print("Part 1: " + str(resolve_sum(data.copy())[1]))
    print("Part 2: " + str(resolve_sum_indexes(data)[1]))
