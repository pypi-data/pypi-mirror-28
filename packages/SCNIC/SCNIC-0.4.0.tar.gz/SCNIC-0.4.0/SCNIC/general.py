from __future__ import division

from scipy.stats import linregress
import numpy as np
import networkx as nx
from biom.table import Table
import pandas as pd
from datetime import datetime
from collections import OrderedDict
from numpy.random import multivariate_normal


__author__ = 'shafferm'


"""functions used widely"""


class Logger(OrderedDict):
    """"""
    # TODO: break up into sections for correls making, network making and module making
    def __init__(self, output):
        super(Logger, self).__init__()
        self.output_file = output
        self['start time'] = datetime.now()

    def output_log(self):
        with open(self.output_file, 'w') as f:
            self['finish time'] = datetime.now()
            self['elapsed time'] = self['finish time'] - self['start time']
            for key, value in self.iteritems():
                f.write(key + ': ' + str(value) + '\n')


def sparcc_paper_filter(table):
    """if a observation averages more than 2 reads per sample then keep,
    if a sample has more than 500 reads then keep"""
    table = table.copy()
    table.filter(table.ids(axis='sample')[table.sum(axis='sample') > 500], axis='sample')
    table.filter(table.ids(axis='observation')[table.sum(axis='observation') / table.shape[1] >= 2], axis="observation")
    return table


def df_to_biom(df):
    return Table(np.transpose(df.as_matrix()), list(df.columns), list(df.index))


def biom_to_df(biom):
    return pd.DataFrame(np.transpose(biom.matrix_data.todense()), index=biom.ids(),
                        columns=biom.ids(axis="observation"))


def get_metadata_from_table(table):
    metadata = dict()
    for _, otu_i, metadata_i in table.iter(axis="observation"):
        if metadata_i is not None:
            metadata[otu_i] = metadata_i
    return metadata


def bh_adjust(pvalues):
    """
    benjamini-hochberg p-value adjustment stolen from
    http://stackoverflow.com/questions/7450957/how-to-implement-rs-p-adjust-in-python

    Parameters
    ----------
    pvalues: an iterable of p-values

    Returns
    -------
    new_pvalues: a numpy array of BH adjusted p-values
    """
    pvalues = np.array(pvalues)
    n = pvalues.shape[0]
    new_pvalues = np.empty(n)
    values = [(pvalue, i) for i, pvalue in enumerate(pvalues)]
    values.sort()
    values.reverse()
    new_values = []
    for i, vals in enumerate(values):
        rank = n - i
        pvalue, index = vals
        new_values.append((n/rank) * pvalue)
    for i in xrange(0, int(n)-1):
        if new_values[i] < new_values[i+1]:
            new_values[i+1] = new_values[i]
    for i, vals in enumerate(values):
        pvalue, index = vals
        new_pvalues[index] = new_values[i]
    return new_pvalues


def bonferroni_adjust(pvalues):
    pvalues = np.array(pvalues)
    n = float(pvalues.shape[0])
    new_pvalues = n * pvalues
    return new_pvalues


def correls_to_net(correls, min_p=None, min_r=None, conet=False, metadata=None):
    """correls is a pandas dataframe which has columns feature1, feature2, r and optionally p and p_adj and optionally
    any others"""
    if metadata is None:
        metadata = []

    if min_p is None and min_r is None:
        min_p = .05

    if conet:
        correls = correls[correls.r > 0]

    if min_p is not None:
        # filter to only include significant correlations
        if 'p_adj' in correls.columns:
            correls = correls[correls.p_adj < min_p]
        elif 'p' in correls.columns:
            correls = correls[correls.p < min_p]
        else:
            raise ValueError("No p or p_adj in correls")

    if min_r is not None:
        if conet:
            correls = correls[correls.r > min_r]
        else:
            correls = correls[np.abs(correls.r) > min_r]

    graph = nx.Graph()
    for _, correl in correls.iterrows():
        graph.add_node(correl.feature1)
        if correl.feature1 in metadata:
            for key in metadata[correl.feature1]:
                graph_key = str(key).replace('_', '')
                if metadata[correl.feature1][key] is None:
                    continue
                if hasattr(metadata[correl.feature1][key], '__iter__'):
                    graph.node[correl.feature1][graph_key] = ';'.join(metadata[correl.feature1][key])
                else:
                    graph.node[correl.feature1][graph_key] = metadata[correl.feature1][key]

        graph.add_node(correl.feature2)
        if correl.feature2 in metadata:
            for key in metadata[correl.feature2]:
                graph_key = str(key).replace('_', '')
                if metadata[correl.feature2][key] is None:
                    continue
                if hasattr(metadata[correl.feature2][key], '__iter__'):
                    graph.node[correl.feature2][graph_key] = ';'.join(metadata[correl.feature2][key])
                else:
                    graph.node[correl.feature2][graph_key] = metadata[correl.feature2][key]
        graph.add_edge(correl.feature1, correl.feature2)
        for i in correl.index[2:]:
            graph_key = i.replace('_', '')
            graph.edges[correl.feature1, correl.feature2][graph_key] = correl[i]
    return graph


def filter_table(table, min_samples=None, to_file=False):
    """filter relative abundance table, by default throw away things greater than 1/3 zeros"""
    table = table.copy()
    # first sample filter
    if min_samples is not None:
        to_keep = [i for i in table.ids(axis='observation')
                   if sum(table.data(i, axis='observation') != 0) >= min_samples]
    else:
        to_keep = [i for i in table.ids(axis='observation')
                   if sum(table.data(i, axis='observation') != 0) >= table.shape[1]/3]
    table.filter(to_keep, axis='observation')

    if to_file:
        table.to_json('filter_table', open("filtered_tab.biom", 'w'))
        # open("filtered_rel_abund.txt", 'w').write(table.to_tsv())

    return table


def simulate_correls(corr_stren=(.99, .99), std=(1, 1, 1, 2, 2), means=(100, 100, 100, 100, 100), size=30,
                     noncors=10, noncors_mean=100, noncors_std=100, subsample=None, log=False):
    """
    Generates a correlation matrix with diagonal of stds based on input parameters and fills rest of matrix with
    uncorrelated values all with same  mean and standard deviations. Output should have a triangle of correlated
    observations and a pair all other observations should be uncorrelated. Correlation to covariance calculated by
    cor(X,Y)=cov(X,Y)/sd(X)sd(Y).

    Parameters
    ----------
    corr_stren: tuple of length 2, correlations in triangle and in pair
    std: tuple of length 5, standard deviations of each observation
    means: tuple of length 5, mean of each observation
    size: number of samples to generate from the multivariate normal distribution
    noncors: number of uncorrelated values
    noncors_mean: mean of uncorrelated values
    noncors_std: standard deviation of uncorrelated values
    subsample: Rarefy data to give threshold
    log: logonentiate mean values, if you are trying to detect log correlation

    Returns
    -------
    table: a biom table with (size) samples and (5+noncors) observations
    """
    cor = [[std[0], corr_stren[0], corr_stren[0], 0., 0.],  # define the correlation matrix for the triangle and pair
           [corr_stren[0], std[1], corr_stren[0], 0., 0.],
           [corr_stren[0], corr_stren[0], std[2], 0., 0.],
           [0., 0., 0., std[3], corr_stren[1]],
           [0., 0., 0., corr_stren[1], std[4]]]
    cor = np.array(cor)
    cov = np.zeros(np.array(cor.shape) + noncors)  # generate empty covariance matrix to be filled
    for i in xrange(cor.shape[0]):  # fill in all but diagonal of covariance matrix, first 5
        for j in xrange(i + 1, cor.shape[0]):
            curr_cov = cor[i, j] * cor[i, i] * cor[j, j]
            cov[i, j] = curr_cov
            cov[j, i] = curr_cov
    for i in xrange(cor.shape[0]):  # fill diagonal of covariance matrix, first 5
        cov[i, i] = np.square(cor[i, i])
    means = list(means)
    for i in xrange(cor.shape[0], cov.shape[0]):  # fill diagonal of covariance, 6 to end and populate mean list
        cov[i, i] = noncors_std
        means.append(noncors_mean)

    if log:
        # if log then log the array
        means = np.log(np.array(means))

    # fill the count table
    counts = multivariate_normal(means, cov, size).T

    if log:
        counts = np.log(counts)

    counts = np.round(counts)

    observ_ids = ["Observ_" + str(i) for i in xrange(cov.shape[0])]
    sample_ids = ["Sample_" + str(i) for i in xrange(size)]
    table = Table(counts, observ_ids, sample_ids)

    if subsample is not None:
        table = table.subsample(subsample)

    return table
