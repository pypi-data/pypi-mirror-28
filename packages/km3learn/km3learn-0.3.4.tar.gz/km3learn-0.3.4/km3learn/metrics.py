#!/usr/bin/env python

from __future__ import division, absolute_import, print_function

import numpy as np


def fraction_pred_as(y_pred, lab, weights=None):
    """assumes y_true is the same for all."""
    if weights is None:
        weights = np.ones_like(y_pred)
    n_evts = np.sum(weights)
    pred_as_label = y_pred == lab
    n_pred_as_lab = np.sum(weights[pred_as_label])
    return n_pred_as_lab / n_evts
