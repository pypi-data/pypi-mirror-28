#!/usr/bin/env python
# vim:set ts=4 sts=4 sw=4 et:
"""Generate classification labels.

"""
from __future__ import division, absolute_import, print_function

import numpy as np

from km3pipe.mc import is_neutrino, name2pdg


NUM2LAB = {
    0: 'shower',
    1: 'track',
    2: 'muon',
    3: 'noise',
}
LAB2NUM = {v: k for k, v in NUM2LAB.items()}


def target_to_name(nums):
    return [NUM2LAB[num] for num in nums]


def name_to_target(labs):
    return [LAB2NUM[lab] for lab in labs]


def label_tracklike_energy_dependent(mc_type, is_cc, energy, bjy):
    """Energy/Bjy dependent Track definition. (Assumes Neutrinos).

    Taken from Jannik + Steffen.
    """
    mc_type = np.atleast_1d(mc_type)
    is_cc = np.atleast_1d(is_cc)
    energy = np.atleast_1d(energy)
    bjy = np.atleast_1d(bjy)

    assert mc_type.shape[0] == is_cc.shape[0] == energy.shape[0] == bjy.shape[0]

    n_evts = mc_type.shape[0]
    out = np.full(n_evts, LAB2NUM['muon'], dtype=int)

    is_nu = np.array(is_neutrino(mc_type))
    is_numu = np.abs(mc_type) == name2pdg('nu_mu')
    is_track = np.logical_and(np.logical_and(is_nu, is_cc), is_numu)
    e_muon = energy * bjy
    he_sel = e_muon > np.sqrt(
        np.power(2., 2.) + np.power(0.1 * energy, 0.2)
    )
    he_track = np.logical_and(is_track, he_sel)
    is_shower = np.logical_and(np.logical_not(he_track), is_nu)

    out[he_track] = LAB2NUM['track']

    out[is_shower] = LAB2NUM['shower']
    return out


def label_pdg_only(mc_type, is_cc):
    """Flavor == class label. Except NC events, of course."""
    is_cc = np.atleast_1d(is_cc)
    mc_type = np.atleast_1d(mc_type)
    assert mc_type.shape[0] == is_cc.shape[0]

    n_evts = mc_type.shape[0]
    out = np.full(n_evts, LAB2NUM['muon'], dtype=int)

    is_nu = np.array(is_neutrino(mc_type))

    is_numu = np.abs(mc_type) == 14
    is_track = np.logical_and(is_cc, is_numu)
    out[is_track] = LAB2NUM['track']

    is_shower = np.logical_and(is_nu, np.logical_not(is_track))
    out[is_shower] = LAB2NUM['shower']
    return out
