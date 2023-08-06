from sklearn.decomposition import PCA
from matplotlib.animation import ArtistAnimation
import matplotlib.pyplot as plt
import numpy as np


def plot_scRNAseq_data(data, cells=None, t=None, color_by='time'):

    data_pca = PCA(n_components=2).fit_transform(data.T)

    fig = plt.figure()
    ax = plt.gca()

    if color_by == 'time':
        c = t
        cmap = plt.get_cmap('Reds')
    elif color_by == 'cell_type':
        cell_types = np.unique(cells)
        c = np.array(
            [np.where(cell_types == cell)[0][0] for cell in cells],
            dtype=float)
        c /= c.max()
        cmap = plt.get_cmap('viridis')

    ax.scatter(*data_pca.T, c=c, cmap=cmap)
    ax.set_xlabel('Component 1')
    ax.set_ylabel('Component 2')

    return fig

def animate_scRNAseq_data(data,
                          cells=None,
                          t=None,
                          n_frames=100,
                          color_by='cell_type'):

    fig = plt.figure(figsize=(6, 6))
    ax = fig.gca()
    ax.set_xlabel('Component 1')
    ax.set_ylabel('Component 2')

    artists = []

    data_final = np.array([expr[-1] for expr in data])
    pca = PCA(n_components=2).fit(data_final)

    if color_by == 'time':
        c = t
        cmap = plt.get_cmap('Reds')
    elif color_by == 'cell_type':
        cell_types = np.unique(cells)
        c = np.array(
            [np.where(cell_types == cell)[0][0] for cell in cells],
            dtype=float)
        c /= c.max()
        cmap = plt.get_cmap('viridis')

    ages = np.array([len(expr) for expr in data])

    for age in np.linspace(0, ages.max(), n_frames, dtype=int):
        data_t = np.array([expr[min(age, len(expr) - 1)] for expr in data])
        data_t_pca = pca.transform(data_t)
        artists.append([ax.scatter(*data_t_pca.T, c=c, cmap=cmap)])

    anim = ArtistAnimation(fig, artists, interval=60, blit=True)

    return anim

def plot_pseudotime_tree(tr, data, cells=None, t=None, color_by='time'):

    if color_by == 'time':
        c = t
        cmap = plt.get_cmap('Reds')
    elif color_by == 'cell_type':
        cell_types = np.unique(cells)
        c = np.array(
            [np.where(cell_types == cell)[0][0] for cell in cells],
            dtype=float)
        c /= c.max()
        cmap = plt.get_cmap('viridis')

    pca = PCA(n_components=2).fit(np.hstack((data, tr.v)).T)
    data_pca = pca.transform(data.T)

    fig = plt.figure(figsize=(8, 8))
    ax = plt.gca()
    ax.scatter(*data_pca.T, c=c, cmap=cmap)

    v_pca = pca.transform(tr.v.T)
    idxs = np.stack(np.where(tr.a), 1)
    for idx1, idx2 in idxs:
        x1, y1 = v_pca[idx1]
        x2, y2 = v_pca[idx2]
        ax.plot([x1, x2], [y1, y2], 'k-', lw=0.5)
    ax.scatter(*v_pca.T, color='k', s=2)
    ax.scatter(*v_pca[[tr.root]].T, color='k', s=200)

    ax.set_xlabel('Component 1')
    ax.set_ylabel('Component 2')

    return fig
