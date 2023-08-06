.. _tutorial:

Tutorial
========

``scRutiNy`` provides two main functions:
    #. Simulate scRNA-seq data by a dynamical system from an underlying gene regulatory network

    #. Infer pseudotime and a gene regulatory network from scRNA-seq data

To simulate scRNA-seq data, ``scRutiNy`` uses the dynamical system

.. math::

    {ds^{(k)} \over dt} = -s^{(k)} + \tanh(Ws^{(k)})

(`Mjolsness, 1991`_) where :math:`s^{(k)}` is a vector of normalized log expression values in :math:`[-1,1]` of :math:`n` genes expressed in cell :math:`k` (Note that :math:`\tanh` is applied component-wise to :math:`Ws^{(k)}`). The value :math:`-1` represents the lowest possible activity level of a gene whereas the value :math:`1` represents the highest possible activity level of a gene. The matrix :math:`W`, common to the population of cells, encodes the edge weights of a genetic regulatory network. Entry :math:`w_{ij}` encodes the effect that gene :math:`j` has on gene :math:`i`. After simulating the above system, the resulting log expression values are converted to transcript counts by exponentiating the log expression values with a chosen base then rounding to non-negative integers.

To infer pseudotime from a transcript count matrix :math:`X`, which has number of genes rows and number of cells columns, we first fit a minimum spanning tree using reversed graph embedding (`Mao, 2016`) to the columns of :math:`X` considered as points in high-dimensional gene space. After a root leaf is designated, each point is projected onto the spanning tree and a pseudotime proportional to the distance from the root leaf is assigned to the cell.

To infer a genetic regulatory network from scRNA-seq data, we use cross-validated Lasso regularized regression to obtain each row of :math:`W` in the above system. More precisely, the values of :math:`s^{(k)}` are computed by dividing each cell's vector of transcript counts by its estimated cell size factor, taking the logarithm and rescaling to the interval :math:`[-1,1]`. Lasso regularized regression is used to approximate :math:`W` that satisfies

.. math::

    \tanh^{-1}\left( s^{(k)} + {s^{(k+1)} - s^{(k)} \over t_{k+1} - t_k } \right) = Ws^{(k)}

for pairs of cells that have evolved from pseudotime :math:`t_k` to :math:`t_{k+1}`.

Simulating scRNA-seq data
-------------------------

Before simulating scRNA-seq data, the user first specifies a development tree.

Inferring pseudotime and gene regulatory network
------------------------------------------------

To infer a gene regulatory network, the user first infers pseudotime.

.. _Mjolsness, 1991: https://doi.org/10.1016/S0022-5193(05)80391-1
.. _Mao, 2016: https://doi.org/10.1109/TPAMI.2016.2635657
