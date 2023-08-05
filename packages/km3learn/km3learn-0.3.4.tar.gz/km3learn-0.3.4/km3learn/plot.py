#!/usr/bin/env python
# vim: set ts=4 sts=4 sw=4 et:

from __future__ import division, absolute_import, print_function

from collections import defaultdict

import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.gridspec import GridSpec
import numpy as np          # noqa
import pandas as pd     # noqa
from sklearn.metrics import roc_curve, precision_recall_curve

from km3learn.metrics import fraction_pred_as


def get_ax(ax=None):
    if ax is None:
        ax = plt.gca()
    return ax


def plot_purity_efficiency(y_true, y_preds, names=None, ax=None, **kwds):
    y_preds = np.atleast_2d(y_preds)
    n_preds = len(y_preds)
    if not names:
        names = ['Model #{}'.format(k) for k in range(n_preds)]
    ax = get_ax(ax)
    for i, y_pred in enumerate(y_preds):
        prec, reca, thres = precision_recall_curve(
            y_true, y_pred, **kwds)
        name = names[i]
        lin = ax.plot(thres, reca[:-1], label='Efficiency {}'.format(name))
        c = lin[0].get_color()
        ax.plot(thres, prec[:-1], color=c, linestyle='--',
                label='Purity {}'.format(name))

    # plot 2 invisible points to prevent suppression of (0, 1) range
    # I don't want to `ax.set_xrange()` since the matplotlib style
    # should handle this (mpl>=2.0 adds nice padding to xyrange)
    ax.plot(0, 0, c='k', alpha=0, label=None)
    ax.plot(1, 1, c='k', alpha=0, label=None)
    ax.set_xlabel('Signalness Threshold')
    ax.legend()
    return ax


def plot_roc_curve(y_true, y_preds, names=None, ax=None, plot_luck=True, **kwds):
    y_preds = np.atleast_2d(y_preds)
    n_preds = len(y_preds)
    if not names:
        names = ['Model #{}'.format(k) for k in range(n_preds)]
    ax = get_ax(ax)
    if plot_luck:
        ax.plot([0, 1], [0, 1], linestyle='--', lw=2, color='k',
                label='ROC Luck')
    for i, y_pred in enumerate(y_preds):
        fpr, tpr, _ = roc_curve(y_true, y_pred, **kwds)
        ax.plot(fpr, tpr, label=names[i])
    ax.set_xlabel('True Positive Rate')
    ax.set_ylabel('False Positive Rate')
    ax.legend()
    return ax


def histratio(X, Y, bins='auto', **kwargs):
    """Plot Histogram on 2 arrays, and plot the binwise ratio below.

    Returns bincount_x, bincount_y, bcx/bcy, binlims
    """
    fig = plt.figure()      # noqa
    gs = GridSpec(2, 1, height_ratios=[4, 1])
    ax0 = plt.subplot(gs[0])
    ax1 = plt.subplot(gs[1], sharex=ax0)

    bc1, binlims, _ = ax0.hist(X, bins=bins, **kwargs)
    bc2, _, _ = ax0.hist(Y, bins=binlims, **kwargs)
    ratio = bc2 / bc1
    ax1.step(binlims[:-1], ratio)
    ax1.set_title('Ratio')
    return bc1, bc2, binlims, fig, ax0, ax1


def diag(ax=None, linecolor='0.0', linestyle='--', **kwargs):
    ax = get_ax(ax)
    xy_min = np.min((ax.get_xlim(), ax.get_ylim()))
    xy_max = np.max((ax.get_ylim(), ax.get_xlim()))
    return ax.plot([xy_min, xy_max], [xy_min, xy_max],
                   ls=linestyle, c=linecolor, **kwargs)


def corr(x, y, ax=None, cmap='Greys', logscale=False, **kwargs):
    ax = get_ax(ax)
    plt.set_cmap(cmap)
    if logscale:
        c_norm = mpl.colors.LogNorm()
    else:
        c_norm = None
    c, xe, ye, img = ax.hist2d(x, y, norm=c_norm, **kwargs)
    plt.colorbar(img, ax=ax)
    return ax


def automeshgrid(x, y, step=0.02, xstep=None, ystep=None, pad=0.5,
                 xpad=None, ypad=None):
    if xpad is None:
        xpad = pad
    if xstep is None:
        xstep = step
    if ypad is None:
        ypad = pad
    if ystep is None:
        ystep = step
    xmin = x.min() - xpad
    xmax = x.max() + xpad
    ymin = y.min() - ypad
    ymax = y.max() + ypad
    return meshgrid(xmin, xmax, step, ymin, ymax, ystep)


def meshgrid(x_min, x_max, x_step, y_min=None, y_max=None, y_step=None):
    if y_min is None:
        y_min = x_min
    if y_max is None:
        y_max = x_max
    if y_step is None:
        y_step = x_step
    xx, yy = np.meshgrid(np.arange(x_min, x_max, x_step),
                         np.arange(y_min, y_max, y_step))
    return xx, yy


def plot_clf(clf, x, y, lab, **mgargs):
    print(x.shape)
    print(y.shape)
    print(lab.shape)
    xx, yy = automeshgrid(x, y, **mgargs)
    Z = clf.predict(np.c_[xx.ravel(), yy.ravel()])
    Z = Z.reshape(xx.shape)
    plt.contourf(xx, yy, Z, cmap=plt.cm.coolwarm, alpha=.8)
    plt.scatter(x[lab == 0], y[lab == 0])
    plt.scatter(x[lab == 1], y[lab == 1])


def corrplot_facet(dataframe, x, y, by='target'):
    n_groups = len(dataframe[by].unique())
    fig, axes = plt.subplots(ncols=2, figsize=(n_groups * 10, 6))

    for i, (lab, df) in enumerate(dataframe.groupby('target')):
        ax = axes[i]
        ax.hexbin(df[x], df[y])
        ax.set_title(lab)
        ax.set_xlabel(x)
        ax.set_ylabel(y)


class LoIPlot(object):
    def __init__(self, df, categories, weight_col=None,
                 flavor_col='flavor', ebin_col='ebin'):
        self.categories = categories
        self.weight_col = weight_col
        self.grouped = df.groupby([flavor_col, ebin_col])

    def _facet_by_col(self, pred_col='pred_name'):
        out = {cat: defaultdict(dict) for cat in self.categories}
        for cat in self.categories:
            for (flavor, ene_idx), j in self.grouped:
                if flavor == 'mu+':
                    continue
            p = j[pred_col]
            if self.weight_col is not None:
                wgt = j[self.weight_col]
            else:
                wgt = None
            frac = fraction_pred_as(p, lab=cat, weights=wgt)
            out[cat][flavor][ene_idx] = frac
        self.out = {key: pd.DataFrame(val)
                    for key, val in out.items()}

    def show(self, **kwargs):
        df = self._facet_by_col(**kwargs)
        n_cats = len(self.categories)
        fig, axes = plt.subplots(ncols=n_cats, figsize=(6 * n_cats, 4))
        plt.suptitle('Efficiency by Flavor/Energy')
        for i, ax in enumerate(axes):
            cat = self.categories[i]
            df[cat].plot(drawstyle='steps', ax=ax)
            ax.set_ylabel('Fraction Predicted as "{}"'.format(cat))
            ax.set_xlabel('Energy / GeV')
            ax.plot(1, 1, alpha=0)
            ax.plot(0, 0, alpha=0)
            ax.set_title(cat)
            ax.legend()
