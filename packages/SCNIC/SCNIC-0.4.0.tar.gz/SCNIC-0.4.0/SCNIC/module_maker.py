"""Make modules of observations based on cooccurence networks and collapse table"""

from __future__ import division

import numpy as np
import pandas as pd
from biom import Table
import os
from scipy.cluster.hierarchy import complete
from scipy.spatial.distance import squareform
from skbio.tree import TreeNode
from itertools import combinations


def make_modules(dist, min_dist, obs_ids):
    # create linkage matrix using complete linkage
    Z = complete(dist)
    # make tree from linkage matrix with names from dist
    tree = TreeNode.from_linkage_matrix(Z, obs_ids)
    # get all tips so in the end we can check if we are done
    all_tips = len([i for i in tree.postorder() if i.is_tip()])
    modules = set()
    seen = set()
    dist = pd.DataFrame(squareform(dist), index=obs_ids, columns=obs_ids)
    for node in tree.levelorder():
        if node.is_tip():
            seen.add(node.name)
        else:
            tip_names = frozenset((i.name for i in node.postorder() if i.is_tip()))
            if tip_names.issubset(seen):
                continue
            dists = (dist.loc[tip1, tip2] > min_dist for tip1, tip2 in combinations(tip_names, 2))
            if any(dists):
                continue
            else:
                modules.add(tip_names)
                seen.update(tip_names)
        if len(seen) == all_tips:
            modules = sorted(modules, key=len, reverse=True)
            return modules
    raise ValueError("Well, how did I get here?")


def collapse_modules(table, modules, prefix="module"):
    """collapse created modules in a biom table, members of multiple modules will be added to the smallest module"""
    table = table.copy()
    module_array = np.zeros((len(modules), table.shape[1]))

    seen = set()
    for i, module in enumerate(modules):
        seen = seen | module
        # sum everything in the module
        module_array[i] = np.sum([table.data(feature, axis="observation") for feature in module], axis=0)

    table.filter(seen, axis='observation', invert=True)

    # make new table
    new_table_matrix = np.concatenate((table.matrix_data.toarray(), module_array))
    new_table_obs = list(table.ids(axis='observation')) + ['_'.join([prefix, str(i)]) for i in xrange(len(modules))]
    return Table(new_table_matrix, new_table_obs, table.ids())


def write_modules_to_dir(table, modules):
    # for each module merge values and print modules to file
    if not os.path.isdir("modules"):
        os.makedirs("modules")
    # reverse modules so observations will be added to smallest modules
    for i, module in enumerate(modules):
        # make biom tables for each module and write to file
        module_table = table.filter(module, axis='observation', inplace=False)
        module_table.to_json("modulemaker.py", open("modules/%s.biom" % i, 'w'))


def write_modules_to_file(modules, prefix="module"):
    # write all modules to file
    with open("modules.txt", 'w') as f:
        for i, module in enumerate(modules):
            f.write('_'.join([prefix, str(i)]) + '\t' + '\t'.join([str(j) for j in module]) + '\n')
