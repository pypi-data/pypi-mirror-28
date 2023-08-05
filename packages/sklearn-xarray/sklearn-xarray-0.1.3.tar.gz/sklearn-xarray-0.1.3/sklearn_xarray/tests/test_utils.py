import numpy as np
import xarray as xr

import numpy.testing as npt

from sklearn_xarray.utils import (
    is_dataarray, is_dataset, is_target, convert_to_ndarray,  get_group_indices)

from sklearn_xarray import Target


def test_is_dataarray():

    X_da = xr.DataArray(np.random.random((100, 10)))

    assert is_dataarray(X_da)

    X_not_a_da = np.random.random((100, 10))

    assert not is_dataarray(X_not_a_da)


def test_is_dataset():

    X_ds = xr.Dataset({'var_1': 1})

    assert is_dataset(X_ds)

    X_not_a_ds = np.random.random((100, 10))

    assert not is_dataarray(X_not_a_ds)


def test_is_target():

    target = Target()

    assert is_target(target)

    not_a_target = 1

    assert not is_target(not_a_target)


def test_convert_to_ndarray():

    from collections import OrderedDict

    X_ds = xr.Dataset(
        OrderedDict([
            ('var_1', (['sample', 'feature'], np.random.random((100, 10)))),
            ('var_2', (['sample', 'feature'], np.random.random((100, 10))))]),
        coords={'sample': range(100), 'feature': range(10)}
    )

    X_arr = convert_to_ndarray(X_ds)

    npt.assert_equal(X_arr, np.dstack((X_ds.var_1, X_ds.var_2)))


def test_get_group_indices():

    import itertools

    coord_1 = ['a']*50 + ['b']*50
    coord_2 = np.tile(list(range(10))*10, (10, 1)).T

    X_da = xr.DataArray(
        np.random.random((100, 10)),
        coords={'sample': range(100), 'feature': range(10),
                'coord_1': (['sample'], coord_1),
                'coord_2': (['sample', 'feature'], coord_2)},
        dims=['sample', 'feature']
    )

    g1 = get_group_indices(X_da, 'coord_1')
    for i, gg in enumerate(g1):
        idx = np.array(coord_1) == np.unique(coord_1)[i]
        npt.assert_equal(gg, idx)

    g2 = get_group_indices(X_da, ['coord_1', 'coord_2'], group_dim='sample')
    combinations = list(
        itertools.product(np.unique(coord_1), np.unique(coord_2)))
    for i, gg in enumerate(g2):
        idx = (np.array(coord_1) == combinations[i][0]) \
            & (np.array(coord_2)[:, 0] == combinations[i][1])
        npt.assert_equal(gg, idx)
