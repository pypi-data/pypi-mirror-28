import numpy as np
import multiprocessing as mp
from sklearn.linear_model import LassoCV
from scipy.sparse import lil_matrix

def warn(*args, **kwargs):
    pass

import warnings
warnings.warn = warn

def fit_grn_row((i, x, y, eps, max_iter, verbose)):
    model = LassoCV(eps=eps, max_iter=max_iter).fit(x, y)
    if verbose:
	print 'row:', i, 'nnz:', (~np.isclose(model.coef_, 0)).sum(), 'score:', model.score(x, y), 'reg param', model.alpha_
    return model.coef_


def fit_grn(data, t, dt=0.1, dt_eps=1e-3, eps=1e-2, max_iter=500, n_processes=None, verbose=False):

    order = np.argsort(t)
    t_sorted = t[order]
    x = data[:, order]

    pairs = []
    for it, ti in enumerate(t_sorted):
        tmp = np.abs(t_sorted - (ti + dt))
        idx = np.argmin(tmp)
        if tmp[idx] < dt_eps:
            pairs.append([it, idx])
    pairs = np.array(pairs).T

    x1 = x[:, pairs[0]]
    x2 = x[:, pairs[1]]
    dx = x2 - x1
    dt = t_sorted[pairs[1]] - t_sorted[pairs[0]]
    dt /= dt.min()
    y = x1 + dx / dt
    y = np.arctanh(y)
    x1 = x1.T

    if n_processes is None:
        n_processes = mp.cpu_count()
    pool = mp.Pool(processes=n_processes)

    kwds = (eps, max_iter, verbose)
    args = [(iy, x1, yi) + kwds for iy, yi in enumerate(y)]

    res = pool.map_async(fit_grn_row, args)
    res.wait()

    w_rows = res.get()

    pool.close()
    pool.terminate()
    pool.join()

    n = data.shape[0]
    w_fit = lil_matrix((n, n))
    for irow, row in enumerate(w_rows):
        w_fit[irow] = row

    return w_fit.tocsr()

def grn_structure_score(w, w_fit):

    # def csr_ij(w):
    #     ij = []
    #     for row, (ptr1, ptr2) in enumerate(zip(w.indptr[:-1], w.indptr[1:])):
    #         for col in w.indices[ptr1:ptr2]:
    #         ij.append((row,col))
    #     return ij
    # w_ij = set(csr_ij(w))
    # w_fit_ij = set(csr_ij(w_fit))
    # common = list(w_ij.intersection(w_fit_ij))
    # uncommon = [list(w_ij-common), list(w_fit_ij-common)]
    # m = len(common), len(uncommon[0]), len(uncommon[1])
    # score = (n*n - np.sum(m)) + m[0] - m[1] - m[2]
    # score /= float(n*n)
    # return score

    return (w.toarray().astype(bool) == w_fit.toarray().astype(bool)).mean()



