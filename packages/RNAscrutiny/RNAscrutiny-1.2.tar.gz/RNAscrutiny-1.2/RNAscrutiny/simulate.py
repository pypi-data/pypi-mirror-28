import multiprocessing as mp
import numpy as np
from collections import OrderedDict
import copy


class development_tree(object):
    def __init__(self, w, cell_types, parent_types, frac_tf_per_branch=0.01):
        self.w = w
        self.cell_types = cell_types
        self.parent_types = OrderedDict(zip(cell_types, parent_types))
        self.n = w.shape[0]
        self.frac_tf_per_branch = frac_tf_per_branch
        self.n_tf_per_branch = int(frac_tf_per_branch * self.n)

        self.get_stem_cell_type()
        self.get_tfs()
        self.get_paths()
        self.get_equilibrium_ts()
        self.get_s0()

    def get_stem_cell_type(self):
        self.stem_cell_type = None
        for cell_type, parent_type in self.parent_types.iteritems():
            if parent_type is None:
                self.stem_cell_type = cell_type
                break
        if self.stem_cell_type is None:
            print 'development_tree: At least one parent cell type must be None.'
            exit

    def get_tfs(self):

        self.regulators = np.where(np.abs(self.w).sum(0) > 0)[1]
        self.tfs = {}

        def __get_tf(cell_type):
            if cell_type == self.stem_cell_type:
                tf = np.random.choice(self.regulators, self.n_tf_per_branch)
                sign = np.sign(np.array(self.w[:, tf].sum(0))[0])
                self.tfs[cell_type] = dict(zip(tf, sign))
            else:
                old_tf = list(self.tfs[self.parent_types[cell_type]].keys())
                unused_regulators = list(set(self.regulators) - set(old_tf))
                new_tf = list(
                    np.random.choice(
                        unused_regulators,
                        self.n_tf_per_branch, ))
                # old_tf = list(
                #     np.random.choice(
                #         old_tf,
                #         int(len(old_tf) * (1 - self.frac_tf_per_branch)),
                #         replace=False))
                tf = old_tf + new_tf
                sign = np.sign(np.array(self.w[:, tf].sum(0))[0])
                self.tfs[cell_type] = dict(zip(tf, sign))
            for child_type, parent_type in self.parent_types.iteritems():
                if parent_type == cell_type:
                    __get_tf(child_type)

        __get_tf(self.stem_cell_type)

    def get_paths(self):
        def __get_path(cell_type, path):
            path.insert(0, cell_type)
            if cell_type == self.stem_cell_type:
                return path
            for child_type, parent_type in self.parent_types.iteritems():
                if child_type == cell_type:
                    return __get_path(parent_type, path)

        self.paths = {}
        for cell_type in self.cell_types:
            self.paths[cell_type] = __get_path(cell_type, [])

    def get_equilibrium_ts(self, t0=0.0, dt=0.1, tn=1e3, eps=1e-5, n_ic=5):

        t = np.arange(t0, tn, dt)
        nt = t.shape[0]

        self.equilibrium_ts = np.empty(len(self.cell_types))

        def __get_equilibrium_t(tf={}):
            t_inf = np.empty(n_ic)
            s = np.empty((self.n, nt + 1))
            for iic in range(n_ic):
                s[:, 0] = np.random.uniform(-1, 1, size=self.n)
                for gene, sign in tf.iteritems():
                    s[gene, 0] = sign
                for it, ti in enumerate(t):
                    s[:, it + 1] = s[:, it] + (
                        -s[:, it] + np.tanh(self.w * s[:, it])) * dt
                    for gene, sign in tf.iteritems():
                        s[gene, it + 1] = sign
                    if np.linalg.norm(s[:, it + 1] - s[:, it]
                                      ) / np.linalg.norm(s[:, it]) < eps:
                        t_inf[iic] = ti
                        break
                if ti == t[-1]:
                    break
            t_inf = t_inf.mean() if ti != t[-1] else tn
            return t_inf

        self.equilibrium_ts = {}
        for cell_type in self.cell_types:
            self.equilibrium_ts[cell_type] = __get_equilibrium_t(
                tf=self.tfs[cell_type])

    def get_s0(self, t0=0.0, dt=0.1, tn=1e3, eps=1e-5):

        t = np.arange(t0, tn, dt)
        nt = t.shape[0]

        s = np.random.uniform(-1, 1, size=self.n)
        for gene, sign in self.tfs['stem'].iteritems():
            s[gene] = sign
        for it, ti in enumerate(t):
            next_s = s + (-s + np.tanh(self.w * s)) * dt
            for gene, sign in self.tfs['stem'].iteritems():
                next_s[gene] = sign
            if np.linalg.norm(next_s - s) / np.linalg.norm(s) < eps:
                break
            s = next_s.copy()
        self.s0 = s


def simulate_cell((icell, cell, dev_tree, nt, dt, dw_scale, tf_weight,
                   verbose)):

    w = dev_tree.w
    n = w.shape[0]

    s = [dev_tree.s0]
    path = dev_tree.paths[cell]

    for ibranch, branch in enumerate(path):

        tn = dt * (nt[ibranch] + 1)
        t = np.arange(0.0, tn, dt)

        for it, ti in enumerate(t):
            dw = np.random.normal(loc=0, scale=dt, size=n)
            s.append(s[-1] +
                     (-s[-1] + np.tanh(w * s[-1] + dw_scale * dw)) * dt)
            for gene, sign in dev_tree.tfs[branch].iteritems():
                s[-1][gene] = (
                    1.0 - tf_weight * dt) * s[-1][gene] + tf_weight * dt * sign

    if verbose:
        print 'cell:', icell, 'type:', cell, 'age:', len(s)

    return np.array(s)


def simulate_scRNAseq_data(dev_tree,
                           n_cells,
                           time_dist='uniform',
                           dt=0.1,
                           dw_scale=0.1,
                           tf_weight=0.5,
                           frac_dropout=0.0,
                           r_dispersion=False,
                           r_loc=1.0,
                           r_scale=0.1,
                           n_processes=None,
                           verbose=False):

    cells = np.repeat(dev_tree.cell_types, n_cells)

    kwds = (dt, dw_scale, tf_weight, verbose)

    if time_dist == 'uniform':
        dist = np.random.uniform
    elif time_dist == 'poisson':
        dist = np.random.poisson
    nt = [[
        dist(dev_tree.equilibrium_ts[branch] // dt)
        for branch in dev_tree.paths[cell]
    ] for cell in cells]

    args = ((icell, cell, copy.deepcopy(dev_tree), nt[icell]) + kwds
            for icell, cell in enumerate(cells))

    if n_processes is None:
        n_processes = mp.cpu_count()
    pool = mp.Pool(processes=n_processes, maxtasksperchild=16)

    res = pool.map_async(simulate_cell, args)
    res.wait()

    history = res.get()

    pool.close()
    pool.terminate()
    pool.join()

    ages = np.array([len(expr) for expr in history], dtype=float)
    ages -= ages.min()
    ages /= ages.max()

    data = np.array([expr[-1] for expr in history])

    n_genes = data.shape[1]

    # dropout and radius dispersion
    n_dropout = int(frac_dropout * n_genes)
    for irow, row in enumerate(data):
        dropout = np.random.choice(n_genes, size=n_dropout)
        row[dropout] = 0.0
        if r_dispersion:
            r = np.random.normal(loc=r_loc, scale=r_scale)
            r = max(0, r)
            row *= r * r * r
        data[irow] = row

    # cols: cells, rows: genes
    data = data.T

    return data, history, cells, ages
