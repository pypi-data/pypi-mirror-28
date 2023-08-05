import pandas as pd
import numpy as np
from scipy.sparse import lil_matrix

def get_trrust_grn(organism='human'):

    raw_data = pd.read_csv(
        'http://www.grnpedia.org/trrust/data/trrust_rawdata.%s.tsv' %
        (organism, ),
        sep='\t',
        usecols=[0, 1, 2],
        header=None)

    genes = np.unique(raw_data.iloc[:, :2].values.flatten())
    n = genes.shape[0]

    w = lil_matrix((n, n))

    for row, (out_gene, in_gene, sign) in raw_data.iterrows():
        i = np.where(genes == in_gene)[0][0]
        j = np.where(genes == out_gene)[0][0]
        if sign == 'Activation':
            wij = 1.0
            # wij = np.random.uniform(0, 1)
        elif sign == 'Repression':
            wij = -1.0
            # wij = np.random.uniform(-1, 0)
        else:
            wij = np.random.uniform(-1, 1)
        w[i, j] = wij

    return w.tocsr(), genes

def get_grn(name='TRRUST', organism='human'):
    if name == 'TRRUST':
        w, genes = get_trrust_grn(organism=organism)
    return w, genes
