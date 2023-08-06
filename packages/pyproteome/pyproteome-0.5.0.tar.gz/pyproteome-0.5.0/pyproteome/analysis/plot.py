"""
Plot calculated levels of a given sequence across channels or groups.
"""

from __future__ import division

# Built-ins
from collections import OrderedDict
import itertools
import logging
import os
import re

# Core data analysis libraries
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
from scipy.stats import ttest_ind

import pyproteome as pyp


LOGGER = logging.getLogger("pyproteome.plot")


def _make_folder(data=None, folder_name=None):
    if folder_name is None:
        folder_name = os.path.join(
            data.name
            if data is not None else
            os.getcwd(),
            "Peptides",
        )

    return pyp.utils.makedirs(folder_name)


def plot(
    data, f=None,
    title=None,
    folder_name=None,
    figsize=(12, 8),
):
    """
    Plot the levels of a sequence across multiple channels.

    Parameters
    ----------
    data : :class:`DataSet<pyproteome.data_sets.DataSet>`
    sequence : str or :class:`Sequence<pyproteome.sequence.Sequence>`
    title : str, optional
    figsize : tuple of int, int
    """
    folder_name = _make_folder(data, folder_name=folder_name)

    channel_names = [
        channel_name
        for group in data.groups.values()
        for channel_name in group
        if channel_name in data.channels
    ]
    channel_names = list(OrderedDict.fromkeys(channel_names))
    channels = [
        data.channels[channel_name]
        for channel_name in channel_names
    ]

    if f:
        data = data.filter(f)

    figures = []

    for _, row in data.psms.iterrows():
        seq = str(row["Sequence"])

        values = row[channels]
        mask = ~pd.isnull(row[channels])

        names = pd.Series(channel_names, index=values.index)[mask]
        values = values[mask]

        fig, ax = plt.subplots(figsize=figsize)

        indices = np.arange(len(values))
        bar_width = .35
        ax.bar(indices, values.as_matrix(), bar_width)
        ax.set_xticks(indices)
        ax.set_xticklabels(
            names,
            fontsize=20,
            rotation=45,
            horizontalalignment="right",
        )

        mod_str = row["Modifications"].__str__(prot_index=0)

        ax.set_title(
            title
            if title else
            "{} ({}{})".format(
                seq,
                " / ".join(row["Proteins"].genes)[:20],
                (" " + mod_str) if mod_str else "",
            )
        )

        ax.set_ylabel(
            "Cummulative Intensity" +
            (" (Normalized)" if data.intra_normalized else "")
        )

        ax.title.set_fontsize(28)
        ax.yaxis.label.set_fontsize(20)

        fig.savefig(
            os.path.join(
                folder_name,
                re.sub(
                    "[?/]",
                    "_",
                    "{} - {} - all.png".format(
                        "+".join(row["Proteins"].genes)[:100],
                        row["Sequence"],
                    ),
                ),
            ),
            bbox_inches="tight",
            dpi=pyp.DEFAULT_DPI,
            transparent=True,
        )

        figures.append((fig, ax))

    return figures


def plot_group(
    data,
    f=None,
    cmp_groups=None,
    title=None,
    folder_name=None,
    figsize=(6, 4),
):
    """
    Plot the levels of a sequence across each group.

    Parameters
    ----------
    data : :class:`DataSet<pyproteome.data_sets.DataSet>`
    sequences : list of str
    """
    folder_name = _make_folder(data, folder_name=folder_name)

    if cmp_groups is None:
        cmp_groups = [list(data.groups.keys())]

    if f:
        data = data.filter(f)

    figures = []

    for _, row in data.psms.iterrows():
        values = []

        for groups in cmp_groups:
            group_vals = pd.Series([
                row[[
                    data.channels[name]
                    for name in data.groups[group]
                    if name in data.channels
                ]]
                for group in groups
            ], index=groups, dtype=object)

            group_vals = pd.Series([
                group[~pd.isnull(group)]
                for group in group_vals
            ], index=group_vals.index, dtype=object)

            group_vals = group_vals[
                group_vals.apply(lambda x: x.shape[0] > 0)
            ]

            # Check normalization group is not null and at least one other
            # group of channels is not null
            if (
                group_vals.shape[0] < 1 or (
                    len(cmp_groups) > 1 and
                    groups[0] not in group_vals.index
                ) or all(
                    group not in group_vals.index
                    for group in groups[1:]
                )
            ):
                continue

            normalize = group_vals.iloc[0].mean()

            group_vals = pd.Series([
                group / normalize
                for group in group_vals
            ], index=group_vals.index, dtype=object)

            values.append(group_vals)

        labels = [
            name
            for group in values
            for name in group.index
        ]

        means = [
            i.mean()
            for vals in values
            for i in vals
        ]

        errs = [
            i.std()
            for vals in values
            for i in vals
        ]

        fig, ax = plt.subplots(figsize=figsize)

        indices = np.arange(len(means))
        width = .5
        ax.bar(
            indices,
            means,
            width=width,
            yerr=errs,
            # error_kw=dict(ecolor='k', lw=.25, capsize=.25, capthick=.25),
        )

        ax.set_ylabel(
            "{} Signal".format(
                "Relative" if cmp_groups else "Cumulative",
            ),
            fontsize=20,
        )
        ax.ticklabel_format(style="plain")

        for label in ax.get_yticklabels():
            label.set_fontsize(20)

        ax.set_xticks(indices)
        ax.set_xticklabels(labels, fontsize=20)

        mod_str = row["Modifications"].__str__(prot_index=0)

        ax.set_title(
            title
            if title else
            "{} ({}{})".format(
                row["Sequence"],
                " / ".join(row["Proteins"].genes)[:20],
                (" " + mod_str) if mod_str else "",
            ),
            fontsize=32,
        )
        ax.xaxis.grid(False)

        # if not means[0].any():
        #     return f

        # if len(means[0]) > 1:
        #     pep_seqs = row["Sequence"]
        #     ax.legend([
        #         "{} ({} - {})".format(
        #             str(seq),
        #             seq.protein_matches[0].rel_pos,
        #             seq.protein_matches[0].rel_pos + len(seq.pep_seq),
        #         )
        #         for seq in pep_seqs
        #     ])
        #     return f, ax

        y_max = max(means) + max(errs)

        def stars(p):
            if p < 0.0001:
                return "****"
            elif (p < 0.001):
                return "***"
            elif (p < 0.01):
                return "**"
            elif (p < 0.05):
                return "*"
            else:
                return "-"

        offset = 0

        v = [
            vals
            for group_vals in values
            for vals in group_vals
        ]

        for (
            (index_a, values_a, label_a), (index_b, values_b, label_b),
        ) in itertools.combinations(zip(indices, v, labels), 2):
            if cmp_groups and not any(
                label_a in group and
                label_b in group
                for group in cmp_groups
            ):
                continue

            pval = ttest_ind(
                values_a.as_matrix(),
                values_b.as_matrix(),
            ).pvalue

            if pval < 0.05:
                ax.set_ylim(
                    ymax=max([
                        ax.get_ylim()[1],
                        y_max * (1 + offset * 0.1 + 0.15),
                    ]),
                )
                ax.annotate(
                    "",
                    xy=(
                        index_a,
                        y_max * (1.05 + offset * 0.1)
                    ),
                    xytext=(
                        index_b,
                        y_max * (1.05 + offset * 0.1)
                    ),
                    xycoords='data',
                    textcoords='data',
                    arrowprops=dict(
                        arrowstyle="-",
                        ec='#000000',
                    ),
                )
                ax.text(
                    x=np.mean([index_a, index_b]),
                    y=y_max * (1.07 + offset * 0.1),
                    s=stars(pval),
                    horizontalalignment='center',
                    verticalalignment='center',
                )

                offset += 1

            fig.savefig(
                os.path.join(
                    folder_name,
                    re.sub(
                        "[?/]",
                        "_",
                        "{} - {} - groups.png".format(
                            "+".join(row["Proteins"].genes)[:50],
                            row["Sequence"],
                        ),
                    ),
                ),
                bbox_inches="tight",
                dpi=pyp.DEFAULT_DPI,
                transparent=True,
            )
            figures.append((fig, ax))

    return figures


def plot_all(
    data,
    f=None,
    figsize=(16, 8),
    individual=True,
    between=True,
    cmp_groups=None,
    folder_name=None,
):
    folder_name = _make_folder(data, folder_name=folder_name)

    figures = []

    if individual:
        figures += plot(
            data,
            f=f,
            figsize=figsize,
            folder_name=folder_name,
        )

    if between:
        figures += plot_group(
            data,
            f=f,
            cmp_groups=cmp_groups,
            folder_name=folder_name,
        )

    return figures


def plot_together(
    data,
    folder_name=None,
    only=True,
    **kwargs
):
    folder_name = _make_folder(data, folder_name=folder_name)

    figures = plot_group(
        data,
        folder_name=folder_name,
        **kwargs
    )

    return figures
