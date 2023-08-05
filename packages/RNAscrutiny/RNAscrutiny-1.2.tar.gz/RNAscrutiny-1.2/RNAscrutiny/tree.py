import numpy as np


class tree(object):
    def __init__(self, v, w):
        self.v = v
        self.w = w
        self.a = (w + w.T).astype(bool).astype(int)
        self.leaves = np.where(self.a.sum(1) == 1)[0]
        self.branch_points = np.where(self.a.sum(1) > 2)[0]
        self.root = None

    def set_root(self, stem_cell_data=None):
        leaf_data = self.v[:, self.leaves]
        dist = (leaf_data**2).sum(0)[:, np.newaxis] - 2.0 * leaf_data.T.dot(
            stem_cell_data) + (stem_cell_data**2).sum(0)
        self.root = self.leaves[np.argmin(dist.sum(1))]

    def get_branch(self, start):
        branch = [start[0], start[1]]
        e = [start[0], start[1]]
        starts = []
        while True:
            ee = np.where(self.a[e[-1]])[0]
            eee = list(set(ee) - {e[-2]})

            if e[-1] in self.branch_points:  # len(ee) > 2
                # print start, 'branch point'
                starts = np.stack((np.repeat(e[-1], len(eee)), eee), 1)
                break

            if e[-1] in self.leaves:  # len(ee) = 1
                # print 'start', 'leaf'
                break

            e = [e[-1], eee[0]]

            branch.append(e[-1])
            # print start, branch

        self.branches.append(branch)

        for start in starts:
            self.get_branch(start)

    def get_pseudotime(self):
        if self.root is None:
            # print 'root is not defined, choosing at random'
            self.root = np.random.choice(self.leaves)
        self.branches = []
        start = [self.root, np.where(self.a[self.root])[0][0]]
        self.get_branch(start)

        self.dt = [
            # np.repeat(1.0, len(branch))
            np.sqrt((np.diff(self.v[:, branch])**2).sum(0))
            for branch in self.branches
        ]

        self.t = np.zeros(self.a.shape[0])
        for branch, dti in zip(self.branches, self.dt):
            for i in range(len(branch) - 1):
                self.t[branch[i + 1]] = self.t[branch[i]] + dti[i]
