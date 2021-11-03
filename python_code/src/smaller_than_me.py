from random import shuffle


class P:
    """
    Given nums, lo, and hi such that nums is sorted and 0 <= lo < hi < len(nums),
    returns a balanced binary search tree containing values only at the leaves.
    """

    def __init__(self, nums, lo, hi):
        if hi - lo > 1:
            self.leaf = False
            i = (lo + hi) // 2
            self.left = P(nums, lo, i)
            self.right = P(nums, i, hi)
            self.mid = nums[i - 1]
        else:
            self.leaf = True
            self.value = lo
        self.offset = 0

    def remove(self, k):
        if self.leaf:
            return self.value + self.offset
        elif k <= self.mid:
            self.right.offset -= 1
            return self.left.remove(k) + self.offset
        else:
            return self.right.remove(k) + self.offset


class Tree(object):

    def __init__(self, value):
        self.value = value
        self.value_multiplicity = 1
        self.left = None
        self.right = None
        self.order = 1
        self.left_order = 0


def insert(t: Tree, n: int):
    """
    Inserts a number n into a tree t and returns the number of nodes less than n.
    There are no attempts to keep the tree balanced.
    """
    v = t.value
    if v is None:
        t.value = n
        res = 0
    elif n < v:
        if t.left is None:
            t.left = Tree(n)
            res = 0
        else:
            res = insert(t.left, n)
        t.left_order += 1
    elif n > v:
        res = t.left_order + t.value_multiplicity
        if t.right is None:
            t.right = Tree(n)
        else:
            res += insert(t.right, n)
    else:
        t.value_multiplicity += 1
        res = t.left_order
    t.order += 1
    return res


def smaller_0(a):
    nums = a.copy()
    shuffle(nums)
    p = P(nums, 0, len(nums))
    return [p.remove(i) for i in a]


def smaller_1(a):
    t = Tree(None)
    return [insert(t, n) for n in reversed(a)][::-1]


########################################
def make_index_tree(n):
    it = iter(range(n))
    res = [0] * n

    def h(k):
        if k >= n: return
        h(2 * k + 1)
        res[k] = next(it)
        h(2 * k + 2)

    h(0)
    return res


def smaller_2(a):
    n = len(a)
    index_tree = make_index_tree(n)
    adjust = [0] * n

    def pop(i):
        def h(j, p, adj=0):
            r = index_tree[p]
            if j < r:
                res = h(j, 2 * p + 1, adj)
                adjust[p] += 1
            elif a[r] is None:
                res = h(j, 2 * p + 2, adj + adjust[p] + 1)
            elif j == r:
                res = j - adjust[p] - adj
                a[i] = None
            else:
                res = h(j, 2 * p + 2, adj + adjust[p])
            return res

        return h(i, 0)

    result = [0] * n
    b = sorted((e, i) for i, e in enumerate(a))
    for j, (_, i) in reversed(list(enumerate(b))):
        result[i] = j - pop(i)
    return result


if __name__ == '__main__':
    a = [6, 7, 4, 8, 3, 7, 4]
    print(smaller_2(a))
