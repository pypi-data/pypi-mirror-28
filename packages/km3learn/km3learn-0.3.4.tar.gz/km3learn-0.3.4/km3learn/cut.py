#!/usr/bin/env python
from __future__ import division, absolute_import, print_function

import numpy as np


def cut_most_votes(probas):
    probas = np.array(probas)
    return np.argmax(probas, axis=1)


def track_mincut(probas, min_cut=0.5, cscd_lab=1, track_lab=2, bkg_lab=0):
    probas = np.array(probas)
    pred = np.full(len(probas), cscd_lab)
    is_atmu = np.argmax(probas, axis=1) == bkg_lab
    pred[is_atmu] = bkg_lab
    is_track = probas[:, track_lab] >= min_cut
    pred[is_track] = track_lab
    return pred


def cascade_mincut(probas, min_cut=0.5, cscd_lab=1, track_lab=2, bkg_lab=0):
    probas = np.array(probas)
    pred = np.full(len(probas), track_lab)
    is_atmu = np.argmax(probas, axis=1) == bkg_lab
    pred[is_atmu] = bkg_lab
    is_cascade = probas[:, cscd_lab] >= min_cut
    pred[is_cascade] = cscd_lab
    return pred


def cut_df(df, strategy='vote',
           classtrans={0: 'background', 1: 'cascade', 2: 'track', },
           **cutargs):
    if strategy == 'vote':
        pred = cut_most_votes(df)
    elif strategy == 'min_cscd':
        pred = cascade_mincut(df, **cutargs)
    elif strategy == 'min_track':
        pred = cascade_mincut(df, **cutargs)
    else:
        raise ValueError('Unknown strategy {}'.format(strategy))
    df['pred'] = pred
    df['pred_name'] = df['pred'].apply(lambda c: classtrans[c])
    return df
