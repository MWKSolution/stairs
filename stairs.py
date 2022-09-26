from collections import deque
from itertools import accumulate
from mwk_logger import timer


class Node:
    def __init__(self, vlist, total, value=0, vsum=0, steps=[]):
        self.value = value
        self.vsum = vsum
        self.nodes = []
        self.steps = steps
        self.match = False
        if self.vsum == total:
            self.match = True
        else:
            for i in vlist:
                if self.vsum + i <= total:
                    pr_steps = self.steps[:]
                    pr_steps.append(i)
                    self.nodes.append(Node(vlist, total, i, self.vsum + i, pr_steps))

    def get_possible_recur(self, poss):  # preorder traversal (root, children)
        if self.match:
            poss.append(self.steps)
        for i in self.nodes:
            i.get_possible_recur(poss)
        return poss

    def get_possible_iter(self):  # iteration traversal
        stack = deque()
        poss = []
        current = self
        while current.nodes or stack:
            if current.match:
                poss.append(current.steps)
            for i in current.nodes:
                stack.append(i)
            current = stack.pop()
        if current.match:
            poss.append(current.steps)
        return poss


class Stairs:
    def __init__(self, stairs, steps):
        self.steps = set(steps)
        self.n = len(stairs) + 1

    @staticmethod
    def get_values_from_tree(possibles):
        # possible steps converted to indexes in stairs
        # get rid of first an last, first is -1, last poinst to one step after stairs
        indexes = [list(accumulate(i, initial=-1))[1:-1] for i in possibles]
        # calculate sum for each possible way
        sums = [sum((stairs[k] for k in i)) for i in indexes]
        return sums

    def full_recur(self, n, steps, all, current):
        current.append(n)
        if n == 0:
            all.append(current.copy())
            current.pop()
            return all, current
        elif n < 0:
            current.pop()
            return all, current
        else:
            for i in steps:
                all, _ = self.full_recur(n - i, steps, all, current)
            current.pop()
            return all, current

    @staticmethod
    def get_values_from_full_recur(back_poss_positons):
        # make indexes from positions
        indexes = [[j-1 for j in list(i)[1:-1]] for i in back_poss_positons]
        # calculate sum for each possible way
        return [sum((stairs[k] for k in i)) for i in indexes]

    @timer
    def get_tree_recur(self):
        tree = Node(self.steps, self.n)
        possibles = tree.get_possible_recur([])
        return possibles, self.get_values_from_tree(possibles)

    @timer
    def get_tree_iter(self):
        tree = Node(self.steps, self.n)
        possibles = tree.get_possible_iter()
        return possibles, self.get_values_from_tree(possibles)

    @timer
    def get_full_recur(self):
        d = deque()
        back_poss_positons, _ = self.full_recur(self.n, self.steps, [], d)
        t = []
        for i in back_poss_positons:
            l = list(i)
            l.reverse()
            t.append(l)
        possibles = [[j-k for j, k in zip(i[1:], i[:-1])] for i in t]
        return possibles, self.get_values_from_full_recur(back_poss_positons)


if __name__ == '__main__':

    stairs = [10, 15, 25, 45]
    steps = [1, 2]

    s = Stairs(stairs, steps)
    x1 = s.get_tree_recur()
    x2 = s.get_tree_iter()
    x3 = s.get_full_recur()
    for i in [x1, x2, x3]:
        print('Possibles: ', i[0])
        print('Values: ', i[1])
        print('MIN: ', min(i[1]) if i[1] else 'No way!')





