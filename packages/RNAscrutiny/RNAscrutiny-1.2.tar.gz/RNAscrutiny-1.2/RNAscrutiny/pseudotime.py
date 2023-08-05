import time
import matplotlib.pyplot as plt
from scipy.sparse.csgraph import minimum_spanning_tree, laplacian
import numpy as np
from sklearn.cluster import KMeans
import tree

reload(tree)
from sklearn.decomposition import PCA


# reversed graph embedding
def rge(x, c, max_iter=100, eps=1e-5, sig=0.1, gam=1.0, verbose=False):

    START = time.time()
    if verbose:
        print 'RGE'
        plt.ion()

    objs = []

    for it in range(max_iter):

        phi = (c**2).sum(0)[:, np.newaxis] - 2.0 * c.T.dot(c) + (c**2).sum(0)
        phi[np.diag_indices_from(phi)] = 0.0
        stree = minimum_spanning_tree(phi).todense()
        w = stree + stree.T
        w = w.astype(bool).astype(np.float64)
        obj_w = stree.sum()
        dist_xc = (x**2).sum(0)[:, np.newaxis] - 2.0 * x.T.dot(c) + (c**
                                                                     2).sum(0)
        min_dist = dist_xc.min(1)
        dist_xc -= min_dist[:, np.newaxis]
        phi_xc = np.exp(-dist_xc / sig)
        p = phi_xc / phi_xc.sum(1)[:, np.newaxis]
        obj_p = -sig * (np.log(phi_xc.sum(1)) - min_dist / sig).sum()

        obj = obj_w + gam * obj_p
        objs.append(obj)

        if verbose:
            print 'iter', it, 'obj =', obj
        if it > 0:
            relative_diff = abs(objs[it - 1] - obj) / abs(objs[it - 1])
            if relative_diff < eps:
                if verbose:
                    print 'eps =', relative_diff, 'converge'
                break
        if it >= max_iter:
            if verbose:
                print 'eps =', relative_diff, 'reached max iters'
            break

        q = -w.copy()
        q[np.diag_indices_from(q)] += w.sum(0)
        q *= 2.0
        q[np.diag_indices_from(q)] += gam * p.sum(0)
        b = gam * x.dot(p)
        c = np.linalg.solve(q.T, b.T).T

    if verbose:
        print(w.sum(0) == 1).sum(), 'leaves'
        print 'TOTAL', round(time.time() - START, 2), 's'

    return c, stree


def pseudotime(data,
               cells,
               var_explained=0.99,
               m=None,
               k=None,
               resid_factor=1.0,
               max_iter=1,
               eps=1e-5,
               sig=0.1,
               gam=1.0,
               verbose=False):

    x = data.copy().astype(np.float64)
    if m is None:
        pca_evrcs = PCA().fit(x.T).explained_variance_ratio_.cumsum()
        m = (pca_evrcs < var_explained).sum()
        m = max(2, m)
    pca = PCA(n_components=m)
    x = pca.fit_transform(x.T).T
    ev = pca.explained_variance_ratio_.cumsum()[m - 1]
    if verbose:
        print 'pca, n_components =', m, 'var explained', round(ev, 3)

    shift = x.mean(1)[:, np.newaxis]
    x -= shift
    scale = np.abs(x).max(1)[:, np.newaxis]
    x /= scale

    # k means
    n = max(x.shape)
    start = time.time()
    if k is None:
        k = n

    c = KMeans(n_clusters=k).fit(x.T).cluster_centers_.T

    if verbose:
        print 'k-means, k =', k, round(time.time() - start, 2), 's'

    for it in range(max_iter):

        last_x = x.copy()
        last_c = c.copy()

        c, stree = rge(x, c, eps=eps, sig=sig, gam=gam, verbose=verbose)

        e_idx = np.stack(np.where(stree))
        e = c[:, e_idx]
        x2 = (x * x).sum(0)[:, np.newaxis]
        d = x2 - 2.0 * x.T.dot(e[:, 0]) + (e[:, 0]**2).sum(0)
        d += x2 - 2.0 * x.T.dot(e[:, 1]) + (e[:, 1]**2).sum(0)
        idx = d.argmin(1)

        a = np.diff(e[..., idx], axis=1).squeeze()
        b = x - e[:, 0, idx]

        proj = []
        for i, (ai, bi) in enumerate(zip(a.T, b.T)):
            proj.append(ai.dot(bi) / ai.dot(ai))
            r = bi - proj[-1] * ai
            bi -= resid_factor * r
            x[:, i] = bi + e[:, 0, idx[i]]

        proj = np.array(proj)
        e = e_idx[:, idx].T

        c_err = ((c - last_c)**2).sum(0) / (c**2).sum(0)
        x_err = ((x - last_x)**2).sum(0) / (x**2).sum(0)

        if verbose:
            print it, c_err.mean(), x_err.mean()

        if c_err.mean() < eps and x_err.mean() < eps:
            break

    stree = np.array(stree)

    x, c = scale * x, scale * c
    x, c = shift + x, shift + c

    x = pca.inverse_transform(x.T).T
    c = pca.inverse_transform(c.T).T

    if verbose:
        fig = plt.figure(figsize=(8, 8))
        ax = plt.gca()
        pca = PCA(n_components=2).fit(np.hstack((x, c)).T)
        x_pca = pca.transform(x.T)
        c_pca = pca.transform(c.T)
        ax.scatter(*x_pca.T, color='k')
        idxs = np.stack(np.where(stree), 1)
        for idx1, idx2 in idxs:
            x1, y1 = c_pca[idx1]
            x2, y2 = c_pca[idx2]
            ax.plot([x1, x2], [y1, y2], 'k-', lw=0.5)
        ax.scatter(*c_pca.T, color='k', s=2)
        ax.axis('off')
        plt.show()

    tr = tree.tree(c, stree)

    stem_cell_data = data[:, cells == 'stem']
    tr.set_root(stem_cell_data)

    tr.get_pseudotime()

    t = []
    for ie, ei in enumerate(e):
        v1, v2 = ei
        t1, t2 = tr.t[v1], tr.t[v2]
        t.append(t1 + proj[ie] * (t2 - t1))

    t = np.array(t)
    t -= t.min()
    t /= t.max()

    return t, tr
