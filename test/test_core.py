import os
import unittest
from datetime import datetime
import numpy as np
import numpy.typing as npt
import tictac


class TestGetAcqDateTime(unittest.TestCase):

    def test_acq_datetime_8_3V_1(self):
        dcm_path = os.path.join(
            'test', 'data', '8_3V',
            'Patient_test_Study_10_Scan_10_Bed_1_Dyn_1.dcm')
        dt = tictac.get_acq_datetime(dcm_path)
        self.assertEqual(dt, datetime(2023, 12, 1, 13, 30, 28, 0))

    def test_acq_datetime_8_3V_5(self):
        dcm_path = os.path.join(
            'test', 'data', '8_3V',
            'Patient_test_Study_10_Scan_10_Bed_1_Dyn_5.dcm')
        dt = tictac.get_acq_datetime(dcm_path)
        self.assertEqual(dt, datetime(2023, 12, 1, 13, 30, 40, 800000))


class TestSaveDict(unittest.TestCase):

    def test_save_table(self):
        tac: dict[str, npt.NDArray[np.float64]] = \
            {'1': np.array([1.0, 2.0, 3.0]),
             '2': np.array([0.5, 0.1, 3.0]),
             'tacq': np.array([0.0, 1.2, 5.4])
             }
        tictac.save_table(tac, os.path.join('test', 'tac.txt'))

        # reassemble file into dict:
        with open(os.path.join('test', 'tac.txt')) as f:
            header = f.readline()
        header_cols = header.split()
        header_cols = header_cols[1:]

        # Load data (excluding header)
        data = np.loadtxt(os.path.join('test', 'tac.txt'))

        # Put data into a dict object with correct labels
        data_dict: dict[str, npt.NDArray[np.float64]] = {}
        for i in range(len(header_cols)):
            data_dict[header_cols[i]] = data[:, i]

        self.assertFalse(np.any(data_dict['1'] - np.array([1.0, 2.0, 3.0])))
        self.assertFalse(np.any(data_dict['2'] - np.array([0.5, 0.1, 3.0])))
        self.assertFalse(np.any(data_dict['tacq'] - np.array([0.0, 1.2, 5.4])))

    def tearDown(self):
        if os.path.exists(os.path.join('test', 'tac.txt')):
            os.remove(os.path.join('test', 'tac.txt'))
