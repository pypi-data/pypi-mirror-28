#!/usr/bin/env python
"""Resampling utils.

Following the API of ``imbalanced-learn`` estimators.
"""

from __future__ import division, absolute_import, print_function

import logging

from imblearn.base import BaseSampler
import numpy as np
from scipy.stats import rv_discrete


class FlatSampler(BaseSampler):
    """Class to sample equally from all flavors.
    """
    def __init__(self):
        super(BaseSampler, self).__init__()
        self.ratio = 'auto'     # whater that is
        self._sampling_type = 'clean-sampling'
        self.logger = logging.getLogger(__name__)

    def _sample(self, X, y):
        """Resample to have a flat distribution in y.

        Parameters
        ----------
        X : {array-like, sparse matrix}, shape (n_samples, n_features)
            Matrix containing the data which have to be sampled.

        y : array-like, shape (n_samples,)
            Corresponding label for each sample in X.

        Returns
        -------
        X_resampled : {ndarray, sparse matrix}, shape \
(n_samples_new, n_features)
            The array containing the resampled data.

        y_resampled : ndarray, shape (n_samples_new,)
            The corresponding label of `X_resampled`
        """
        wgt = reweight_flat(y)
        samp_idx = sample_weighted_idx(wgt)
        return X[samp_idx], y[samp_idx]


def bin_index(arr, bins):
    """Get the array index of an event's bin."""
    arr = np.atleast_1d(arr)
    ix = np.digitize(arr, bins)
    ix -= 1
    return ix


def reweight_flat(arr, binlims='auto'):
    """Reweight into flat histogram, for given bins."""
    arr = np.atleast_1d(arr)
    counts, bins = np.histogram(arr, binlims, density=True)
    assert not np.any(counts == 0), "Bins cannot be empty"
    idx = bin_index(arr, bins)
    wgt = 1 / counts[idx]
    wgt /= np.sum(wgt)
    return wgt, bins


def sample_weighted_idx(wgt, n_samp=None):
    if n_samp is None:
        n_samp = len(wgt)
    wgt /= np.sum(wgt)
    sup = np.arange(len(wgt))
    dist = rv_discrete(values=(sup, wgt))
    return dist.rvs(n_samp)
