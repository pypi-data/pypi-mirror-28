#!/usr/bin/env python
"""Data loading helpers.
"""

import pandas as pd

from km3pipe.io.pandas import H5Chain, merge_event_ids
from km3pipe.mc import get_flavor
from km3learn.features import remove_constant_features
from km3learn.label import (label_tracklike_energy_dependent,
                            label_pdg_only, target_to_name)


DEFAULT_BAD_FEATURES = [
    'dusj_cos_zenith',
]


def remove_bad_features(rec, bad_cols=None):
    if bad_cols is None:
        bad_cols = DEFAULT_BAD_FEATURES
    return rec.drop(columns=bad_cols)


def load_reco(fnames):
    with H5Chain(fnames) as h5:
        mc = h5['/truth']
        gandalf = h5['/reco/gandalf']
        gandalf_ext = h5['/reco/gandalf_extra']
        recolns = h5['/reco/recolns']
        recolns_ext = h5['/reco/recolns_extra']
        dusj = h5['/reco/dusj']
        dusj_ext = h5['/reco/dusj_extra']
        diff = h5['/reco/diff']
    assert mc.shape[0] == gandalf.shape[0] == recolns.shape[0] == \
        dusj.shape[0] == gandalf_ext.shape[0] == recolns_ext.shape[0] == \
        dusj_ext.shape[0] == diff.shape[0]
    reco = pd.concat([
        gandalf, gandalf_ext,
        recolns, recolns_ext,
        dusj, dusj_ext,
        diff,
    ], axis=1)
    reco = merge_event_ids(reco, drop_duplicates=False)
    return reco, mc


def add_labels(mc):
    mc['flavor'] = get_flavor(mc.type)
    mc['label_pdg'] = label_pdg_only(mc.type, mc.is_cc)
    mc['name_pdg'] = target_to_name(mc.label_pdg)
    mc['label_ene_bjy'] = label_tracklike_energy_dependent(mc.type, mc.is_cc,
                                                           mc.energy,
                                                           mc.bjorkeny)
    mc['name_ene_bjy'] = target_to_name(mc.label_ene_bjy)
    return mc


def clean_features(reco):
    reco = remove_bad_features(reco)
    reco, _ = remove_constant_features(reco)
    return reco
