import os
import unittest
import numpy as np
import numpy.typing as npt
from tictac import __main__


class TestMainFunction(unittest.TestCase):

    def test_main_simple(self):

        img_dir = os.path.join('test', 'data', '8_3V')
        roi_path = os.path.join('test', 'data', '8_3V_seg',
                                'Segmentation.nrrd')
        out_path = os.path.join('test', 'tac.txt')

        __main__.main([img_dir, roi_path, out_path])

        # reassemble outfile into dict:
        with open(out_path) as f:
            header = f.readline()
        header_cols = header.split()
        header_cols = header_cols[1:]

        # Load data (excluding header)
        data = np.loadtxt(out_path)

        # Put data into a dict object with correct labels
        data_dict: dict[str, npt.NDArray[np.float64]] = {}
        for i in range(len(header_cols)):
            data_dict[header_cols[i]] = data[:, i]

        tacq = data_dict['tacq']
        tacq_exp = np.array([0, 3.0, 6.3, 9.5, 12.8, 16.0, 19.3, 22.5, 25.8])
        self.assertFalse(np.any(tacq - tacq_exp))

        r1 = data_dict['1']
        r1_exp = np.array([0.0, 0.767681, 1229.61, 12019.3,
                           12058.9, 1277.01, 13.4822, 0.748028, 0.0])
        self.assertTrue(np.all((r1 - r1_exp) < 0.1))

        r2 = data_dict['2']
        r2_exp = np.array([31.3157, 3501.54, 33128.1, 38544.1,
                           9529.26, 642.525, 2.57748, 0.345963, 0.0727437])
        self.assertTrue(np.all((r2 - r2_exp) < 0.1))

    def test_main_labels(self):
        img_dir = os.path.join('test', 'data', '8_3V')
        roi_path = os.path.join('test', 'data', '8_3V_seg',
                                'Segmentation.nrrd')
        out_path = os.path.join('test', 'tac.txt')

        __main__.main([img_dir, roi_path, out_path,
                       "--labels", "1,stuff", "2,stoff"])

        # reassemble outfile into dict:
        with open(out_path) as f:
            header = f.readline()
        header_cols = header.split()
        header_cols = header_cols[1:]

        # Load data (excluding header)
        data = np.loadtxt(out_path)

        # Put data into a dict object with correct labels
        data_dict: dict[str, npt.NDArray[np.float64]] = {}
        for i in range(len(header_cols)):
            data_dict[header_cols[i]] = data[:, i]

        r1 = data_dict['stuff']
        r1_exp = np.array([0.0, 0.767681, 1229.61, 12019.3,
                           12058.9, 1277.01, 13.4822, 0.748028, 0.0])
        self.assertTrue(np.all((r1 - r1_exp) < 0.1))

        r2 = data_dict['stoff']
        r2_exp = np.array([31.3157, 3501.54, 33128.1, 38544.1,
                           9529.26, 642.525, 2.57748, 0.345963, 0.0727437])
        self.assertTrue(np.all((r2 - r2_exp) < 0.1))

    def test_main_ignore(self):
        img_dir = os.path.join('test', 'data', '8_3V')
        roi_path = os.path.join('test', 'data', '8_3V_seg',
                                'Segmentation.nrrd')
        out_path = os.path.join('test', 'tac.txt')

        __main__.main([img_dir, roi_path, out_path,
                       "--ignore", "1", "2"])

        # reassemble outfile into dict:
        with open(out_path) as f:
            header = f.readline()
        header_cols = header.split()
        header_cols = header_cols[1:]

        # Load data (excluding header)
        data = np.loadtxt(out_path)

        # Put data into a dict object with correct labels
        data_dict: dict[str, npt.NDArray[np.float64]] = {}
        for i in range(len(header_cols)):
            data_dict[header_cols[i]] = data[:, i]

        self.assertTrue("0" in data_dict)
        self.assertFalse("1" in data_dict)
        self.assertFalse("2" in data_dict)

    def test_main_resample_roi(self):

        img_dir = os.path.join('test', 'data', '8_3V')
        roi_path = os.path.join('test', 'data', '8_3V_seg',
                                'Segmentation_2.nrrd')
        out_path = os.path.join('test', 'tac.txt')

        __main__.main([img_dir, roi_path, out_path,
                       "--resample", "roi"])

        # reassemble outfile into dict:
        with open(out_path) as f:
            header = f.readline()
        header_cols = header.split()
        header_cols = header_cols[1:]

        # Load data (excluding header)
        data = np.loadtxt(out_path)

        # Put data into a dict object with correct labels
        data_dict: dict[str, npt.NDArray[np.float64]] = {}
        for i in range(len(header_cols)):
            data_dict[header_cols[i]] = data[:, i]

        r1 = data_dict['1']
        r2 = data_dict['2']

        self.assertAlmostEqual(float(r1[3]), 13473.5, places=1)
        self.assertAlmostEqual(float(r2[3]), 17120.9, places=1)

    def test_main_resample_img(self):

        img_dir = os.path.join('test', 'data', '8_3V')
        roi_path = os.path.join('test', 'data', '8_3V_seg',
                                'Segmentation_2.nrrd')
        out_path = os.path.join('test', 'tac.txt')

        __main__.main([img_dir, roi_path, out_path,
                       "--resample", "img"])

        # reassemble outfile into dict:
        with open(out_path) as f:
            header = f.readline()
        header_cols = header.split()
        header_cols = header_cols[1:]

        # Load data (excluding header)
        data = np.loadtxt(out_path)

        # Put data into a dict object with correct labels
        data_dict: dict[str, npt.NDArray[np.float64]] = {}
        for i in range(len(header_cols)):
            data_dict[header_cols[i]] = data[:, i]

        r1 = data_dict['1']
        r2 = data_dict['2']

        self.assertAlmostEqual(float(r1[3]), 11405.7, places=1)
        self.assertAlmostEqual(float(r2[3]), 15053.1, places=1)

    def test_main_scale(self):

        img_dir = os.path.join('test', 'data', '8_3V')
        roi_path = os.path.join('test', 'data', '8_3V_seg',
                                'Segmentation.nrrd')
        out_path = os.path.join('test', 'tac.txt')

        __main__.main([img_dir, roi_path, out_path,
                       "--scale", "1", "1a", "2.0",
                       "--scale", "2", "2a", "0.5"])

        # reassemble outfile into dict:
        with open(out_path) as f:
            header = f.readline()
        header_cols = header.split()
        header_cols = header_cols[1:]

        # Load data (excluding header)
        data = np.loadtxt(out_path)

        # Put data into a dict object with correct labels
        data_dict: dict[str, npt.NDArray[np.float64]] = {}
        for i in range(len(header_cols)):
            data_dict[header_cols[i]] = data[:, i]

        r1 = data_dict['1a']
        r1_exp = 2.0*np.array([0.0, 0.767681, 1229.61, 12019.3,
                               12058.9, 1277.01, 13.4822, 0.748028, 0.0])
        self.assertTrue(np.all((r1 - r1_exp) < 0.1))

        r2 = data_dict['2a']
        r2_exp = 0.5*np.array([31.3157, 3501.54, 33128.1, 38544.1,
                               9529.26, 642.525, 2.57748, 0.345963,
                               0.0727437])
        self.assertTrue(np.all((r2 - r2_exp) < 0.1))

    def tearDown(self):
        if os.path.exists(os.path.join('test', 'tac.txt')):
            os.remove(os.path.join('test', 'tac.txt'))
