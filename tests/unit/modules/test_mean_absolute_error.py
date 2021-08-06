import unittest

import pytest
import xarray as xr
import pandas as pd
from pywatts.core.exceptions.input_not_available import InputNotAvailable

from pywatts.modules.mean_absolute_error import MaeCalculator
import numpy as np


class TestMaeCalculator(unittest.TestCase):

    def setUp(self) -> None:
        self.mae_calculator = MaeCalculator()

    def tearDown(self) -> None:
        self.mae_calculator = None

    def test_get_params(self):
        self.assertEqual(self.mae_calculator.get_params(),
                         {'offset': 0, 'rolling': False, 'window': 24})

    def test_set_params(self):
        self.mae_calculator.set_params(offset=24, rolling=True, window=2)
        self.assertEqual(self.mae_calculator.get_params(),
                         {'offset': 24, 'rolling': True, 'window': 2})

    def test_transform_rolling(self):
        self.mae_calculator.set_params(rolling=True, window=2)
        time = pd.to_datetime(['2015-06-03 00:00:00', '2015-06-03 01:00:00',
                               '2015-06-03 02:00:00', '2015-06-03 03:00:00',
                               '2015-06-03 04:00:00'])

        test_data = xr.Dataset({"testCol": ("time", xr.DataArray([-2, -1, 0, 1, 2]).data),
                                "predictCol1": ("time", xr.DataArray([2, -3, 3, 1, -2]).data),
                                "predictCol2": ("time", xr.DataArray([4, 4, 3, -2, 1]).data), "time": time})

        test_result = self.mae_calculator.transform(y=test_data['testCol'], gt=test_data['testCol'],
                                                    pred1=test_data['predictCol1'],
                                                    pred2=test_data['predictCol2'])
        expected_result = xr.DataArray(np.array([[np.nan, np.nan, np.nan],
                                                 [0.0, 3, 5.5],
                                                 [0.0, 2.5, 4],
                                                 [0.0, 1.5, 3],
                                                 [0.0, 2, 2]]),
                                       coords={"time": time, "predictions": ["gt", "pred1", "pred2"]},
                                       dims=["time", "predictions"])

        xr.testing.assert_allclose(test_result, expected_result)

    def test_transform(self):
        self.mae_calculator.set_params()

        time = pd.to_datetime(['2015-06-03 00:00:00', '2015-06-03 01:00:00',
                               '2015-06-03 02:00:00', '2015-06-03 03:00:00',
                               '2015-06-03 04:00:00'])

        result_time = pd.to_datetime(['2015-06-03 04:00:00'])

        test_data = xr.Dataset({"testCol": ("time", xr.DataArray([-2, -1, 0, 1, 2]).data),
                                "predictCol1": ("time", xr.DataArray([2, -3, 3, 1, -2]).data),
                                "predictCol2": ("time", xr.DataArray([4, 4, 3, -2, 1]).data), "time": time})

        test_result = self.mae_calculator.transform(y=test_data['testCol'], gt=test_data['testCol'],
                                                    pred1=test_data['predictCol1'],
                                                    pred2=test_data['predictCol2'])

        expected_result = xr.DataArray(np.array([[0.0, 2.6, 3.6]]),
                                       coords={"time": result_time, "predictions": ["gt", "pred1", "pred2"]},
                                       dims=["time", "predictions"])

        xr.testing.assert_equal(test_result, expected_result)

    def test_transform_without_predictions(self):
        self.mae_calculator.set_params()

        time = pd.to_datetime(['2015-06-03 00:00:00', '2015-06-03 01:00:00',
                               '2015-06-03 02:00:00', '2015-06-03 03:00:00',
                               '2015-06-03 04:00:00'])

        test_data = xr.Dataset({"testCol": ("time", xr.DataArray([-2, -1, 0, 1, 2]).data),
                                "predictCol1": ("time", xr.DataArray([2, -3, 3, 1, -2]).data),
                                "predictCol2": ("time", xr.DataArray([4, 4, 3, -2, 1]).data), "time": time})

        with pytest.raises(InputNotAvailable) as e_info:
            self.mae_calculator.transform(y=test_data['testCol'])

        self.assertEqual(e_info.value.message,
                         "No predictions are provided as input for the MAE Calculator. You should add the predictions "
                         "by a separate key word arguments if you add the MaeCalculator to the pipeline.")