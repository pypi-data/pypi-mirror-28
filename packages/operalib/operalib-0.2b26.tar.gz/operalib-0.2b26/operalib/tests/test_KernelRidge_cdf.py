"""OVK learning, unit tests.

The :mod:`sklearn.tests.test_ovkernelRidge` tests OVK ridge regression
estimator.
"""
from numpy import NaN, bool
from numpy.random import binomial

import operalib as ovk

from sklearn import __version__
from distutils.version import LooseVersion
if LooseVersion(__version__) < LooseVersion('0.18'):
    from sklearn.cross_validation import train_test_split
else:
    from sklearn.model_selection import train_test_split


def test_learn_cf():
    """Test ovk curl-free estimator fit."""
    X, y = ovk.toy_data_curl_free_field(n_samples=500)

    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=400)

    regr_1 = ovk.OVKRidge(ovkernel=ovk.RBFCurlFreeKernel(gamma=10.), lbda=0)
    regr_1.fit(Xtr, ytr)
    assert regr_1.score(Xte, yte) >= 0.8


def test_learn_df():
    """Test ovk curl-free estimator fit."""
    X, y = ovk.toy_data_div_free_field(n_samples=500)

    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=400)

    regr_1 = ovk.OVKRidge(ovkernel=ovk.RBFDivFreeKernel(gamma=10.), lbda=0)
    regr_1.fit(Xtr, ytr)
    assert regr_1.score(Xte, yte) >= 0.8


def test_learn_cf_semi():
    """Test ovk curl-free estimator fit on semi-supervised data."""
    X, y = ovk.toy_data_curl_free_field(n_samples=500)

    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=400)
    nan_mask = binomial(1, 0.1, ytr.shape[0]).astype(bool)
    ytr[nan_mask, :] = NaN

    regr_1 = ovk.OVKRidge(ovkernel=ovk.RBFCurlFreeKernel(gamma=10.), lbda=0)
    regr_1.fit(Xtr, ytr)
    assert regr_1.score(Xte, yte) >= 0.8


def test_learn_df_semi():
    """Test ovk curl-free estimator fit on semi-supervised data.."""
    X, y = ovk.toy_data_div_free_field(n_samples=500)

    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=400)
    nan_mask = binomial(1, 0.1, ytr.shape[0]).astype(bool)
    ytr[nan_mask, :] = NaN

    regr_1 = ovk.OVKRidge(ovkernel=ovk.RBFDivFreeKernel(gamma=10.), lbda=0)
    regr_1.fit(Xtr, ytr)
    assert regr_1.score(Xte, yte) >= 0.8
