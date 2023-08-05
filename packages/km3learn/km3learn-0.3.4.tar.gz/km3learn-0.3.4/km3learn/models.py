#!/usr/bin/env python
"""Pre-built model pipelines.
"""

from sklearn.decomposition import PCA
from sklearn.ensemble import RandomForestClassifier, ExtraTreesClassifier
from sklearn.model_selection import GridSearchCV, RandomizedSearchCV    # noqa
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import RobustScaler


MYMODEL = None

rf = RandomForestClassifier(
    n_estimators=101,
    n_jobs=-1,
    class_weight='balanced',
    criterion='entropy',
    verbose=1,
)
rf_pipe = Pipeline([
    ('quantile_scaler', RobustScaler()),
    ('reduce_dim', PCA(svd_solver='auto')),
    ('forest', rf),
])
rf_param_grid = {
    'forest__n_estimators': [10, 30, 100],
    'forest__criterion': ['gini', 'entropy'],
}
rf_grid = GridSearchCV(rf_pipe, param_grid=rf_param_grid)

et = ExtraTreesClassifier(
    n_estimators=101,
    n_jobs=-1,
    class_weight='balanced',
    criterion='entropy',
    verbose=1,
)
et_pipe = Pipeline([
    ('quantile_scaler', RobustScaler()),
    ('reduce_dim', PCA(svd_solver='auto')),
    ('forest', et),
])
et_param_grid = {
    'forest__n_estimators': [10, 30, 100],
    'forest__criterion': ['gini', 'entropy'],
}
et_grid = GridSearchCV(et_pipe, param_grid=et_param_grid)
