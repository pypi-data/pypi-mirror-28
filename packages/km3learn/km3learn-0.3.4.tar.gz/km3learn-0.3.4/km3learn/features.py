#!/usr/bin/env python

from __future__ import division, absolute_import, print_function

from six import string_types

import numpy as np
import pandas as pd

from sklearn.ensemble import (ExtraTreesClassifier, RandomForestClassifier,
                              ExtraTreesRegressor, RandomForestRegressor)
from sklearn.feature_selection import (
    f_classif, f_regression,           # noqa
    mutual_info_classif, mutual_info_regression         # noqa
)      # noqa
from sklearn.model_selection import StratifiedKFold, KFold
from sklearn.preprocessing import LabelEncoder, RobustScaler


def remove_constant_features(df, return_names=True):
    constant_feats = df.loc[:, df.var() == 0].columns.sort_values()
    df = df.copy().loc[:, df.var() != 0]
    if return_names:
        return df, constant_feats
    return df


def tree_importance(X, y, n_trees=100, forest='et', task='classification',
                    cv=None, **tree_args):
    """Feature Importances from a Randomized Tree Ensemble."""
    if cv is None:
        if task == 'classification':
            cv = StratifiedKFold(n_splits=3, shuffle=True)
        if task == 'regression':
            cv = KFold(n_splits=3, shuffle=True)
    if isinstance(forest, string_types):
        if task == 'classification':
            if forest == 'rf':
                forest = RandomForestClassifier(n_estimators=n_trees, **tree_args)
            elif forest == 'et':
                forest = ExtraTreesClassifier(n_estimators=n_trees, **tree_args)
        if task == 'regression':
            if forest == 'rf':
                forest = RandomForestRegressor(n_estimators=n_trees, **tree_args)
            elif forest == 'et':
                forest = ExtraTreesRegressor(n_estimators=n_trees, **tree_args)
    fis = []
    stds = []
    for train, test in cv.split(X, y):
        forest.fit(X[train], y[train])
        fis.append(forest.feature_importances_)
        stds.append(np.std([tree.feature_importances_
                            for tree in forest.estimators_], axis=0))
    fi = np.mean(fis, axis=0)
    cv_err = np.std(fis, axis=0)
    inter_err = np.mean(stds, axis=0)
    return fi, cv_err, inter_err


def ftest_importance(X, y, task='classification'):
    X = np.nan_to_num(RobustScaler().fit_transform(X).astype(np.float32))
    if task == 'classification':
        return f_classif(X, y)[0]
    if task == 'regression':
        return f_regression(X, y)[0]


def mutual_info_importance(X, y, task='classification'):
    X = np.nan_to_num(RobustScaler().fit_transform(X).astype(np.float32))
    if task == 'classification':
        return mutual_info_classif(X, y)
    if task == 'regression':
        return mutual_info_regression(X, y)


def importances(X, y, normalize=True, task='classification', forest='et',
                **tree_args):
    """Compute Multiple Importance Measures & collect into DataFrame.

    Parameters
    ----------
    X: np.ndarray/pd.DataFrame
        2D Features to rank.
    y: np.ndarray/pd.Series
        Class labels.
    normalize: bool, default=True
        Normalize each columns, so that most important
        feature has importance 1.
    forest: 'et', 'rf'
        Which kind of forest to use.
    """
    cols = X.columns
    y = LabelEncoder().fit_transform(y)
    X.fillna(0, inplace=True)
    X = X.as_matrix().astype(np.float32)
    X = np.nan_to_num(X)
    assert not np.any(np.isnan(X))
    assert not np.any(np.isinf(X))
    t_imps, t_cv_err, t_inter_err = tree_importance(X, y, task=task,
                                                    forest=forest, n_jobs=-1,
                                                    **tree_args)
    f_imps = ftest_importance(X, y, task=task)
    m_imps = mutual_info_importance(X, y)
    imps = pd.DataFrame.from_records(
        list(zip(cols, f_imps, m_imps, t_imps, t_cv_err, t_inter_err)),
        columns=['feature', 'f_score', 'mutual_info', 'tree_importance',
                 'tree_cv_err', 'tree_inter_err']
    )
    imps.set_index('feature', inplace=True)
    if normalize:
        imps['f_score'] /= imps['f_score'].max()
        imps['mutual_info'] /= imps['mutual_info'].max()
        for col in ('tree_importance', 'tree_cv_err', 'tree_inter_err'):
            max = imps['tree_importance'].max()
            imps[col] /= max
    return imps
