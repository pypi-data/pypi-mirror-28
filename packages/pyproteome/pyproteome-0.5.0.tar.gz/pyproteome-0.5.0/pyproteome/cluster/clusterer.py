
from scipy.stats import zscore

import numpy as np
import pandas as pd
import sklearn
from scipy.stats import pearsonr
import sklearn.decomposition
import sklearn.cluster


def get_data(ds, dropna=True, groups=None):
    ds = ds.copy()

    if groups is None:
        groups = list(ds.groups.keys())

    if dropna:
        ds = ds.dropna(how="any", groups=groups)

    names = [
        chan
        for group in groups
        for chan in ds.groups[group]
        if chan in ds.channels
    ]
    chans = [ds.channels[chan] for chan in names]
    data = ds.data[chans]

    c = np.corrcoef(data.as_matrix())
    z = zscore(data, axis=1)

    classes = np.array([
        [
            groups.index(i)
            for i in groups
            if col in ds.groups[i]
        ][0]
        for col in names
    ])

    return {
        "ds": ds,
        "data": data,
        "z": z,
        "c": c,
        "names": names,
        "labels": groups,
        "classes": classes,
    }


def cluster(data, fn=None, kwargs=None, n_clusters=20):
    z = data["z"]
    ds = data["ds"]

    if fn is None:
        fn = sklearn.cluster.AgglomerativeClustering

    if kwargs is None:
        kwargs = {
            "n_clusters": n_clusters,
        }

    clr = fn(
        **kwargs
    )

    y_pred_spec = clr.fit_predict(z)

    y_pred = pd.Series(y_pred_spec, index=ds.psms.index)

    return clr, y_pred


def cluster_clusters(
    data, y_pred,
    p_cutoff=1,
    corr_cutoff=.7,
    iterations=3,
):
    y_pred = y_pred.copy()

    for _ in range(iterations):
        ss = sorted(set(y_pred), key=lambda i: -(y_pred == i).sum())

        for ind, i in enumerate(ss):
            corrs = [
                (
                    o,
                    np.correlate(
                        data["z"][y_pred == i].mean(axis=0),
                        data["z"][y_pred == o].mean(axis=0),
                    )[0],
                )
                for o in sorted(set(y_pred))
                if o < i
            ]
            if not corrs:
                continue

            o, (rho) = max(corrs, key=lambda x: x[1])

            # if rho > corr_cutoff:
            #     y_pred[y_pred == i] = o
            if (
                # p < p_cutoff and
                rho > 0 and rho > corr_cutoff
            ):
                y_pred[y_pred == i] = o

    y_pred_old = y_pred.copy()

    for ind, i in enumerate(sorted(set(y_pred))):
        y_pred[y_pred_old == i] = ind

    return y_pred
