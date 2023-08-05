from pipe_fn import e
# e is the identity mapping


def add(this, other):
    return this + other


print([1, 2, 3] | e / sum)
# sum([1, 2, 3])

print([2, 3, -1] | e ** {'key': lambda x: -x} / sorted)  # set kwargs
# sorted([2, 3, -1], key=lambda x: -x)

print([[1], [2], [3]] | e / sum * ([],))  # set args
# sum([[1], [2], [3]], [])


print(1 | e / add * (1,))


# add(1, 1)


def double(x):
    return 2 * x


# and then composition
print(1 | (e / add * (2,) + double + double))
# double(double(add(1, 2))
