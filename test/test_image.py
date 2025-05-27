import os.path
import unittest
import tictac.image
import numpy as np
import SimpleITK as sitk


class TestLoadDynamicSeries(unittest.TestCase):

    def test_load_dynamic_series_8_3V(self):
        dcm_path = os.path.join('test', 'data', '8_3V')
        dyn = tictac.image.load_dynamic_series(dcm_path)
        img = dyn['img']
        acq = dyn['acq']
        self.assertEqual(len(img), 9)
        self.assertEqual(img[0].GetSize(), (128, 128, 64))
        self.assertEqual(img[0].GetSpacing(), (4.92, 4.92, 4.92))
        self.assertEqual(img[0].GetDimension(), 3)
        self.assertEqual(img[1].GetSize(), (128, 128, 64))
        self.assertEqual(img[1].GetSpacing(), (4.92, 4.92, 4.92))
        self.assertEqual(img[1].GetDimension(), 3)
        self.assertEqual(img[2].GetSize(), (128, 128, 64))
        self.assertEqual(img[2].GetSpacing(), (4.92, 4.92, 4.92))
        self.assertEqual(img[2].GetDimension(), 3)
        self.assertEqual(img[3].GetSize(), (128, 128, 64))
        self.assertEqual(img[3].GetSpacing(), (4.92, 4.92, 4.92))
        self.assertEqual(img[3].GetDimension(), 3)
        self.assertEqual(img[4].GetSize(), (128, 128, 64))
        self.assertEqual(img[4].GetSpacing(), (4.92, 4.92, 4.92))
        self.assertEqual(img[4].GetDimension(), 3)
        self.assertEqual(img[5].GetSize(), (128, 128, 64))
        self.assertEqual(img[5].GetSpacing(), (4.92, 4.92, 4.92))
        self.assertEqual(img[5].GetDimension(), 3)
        self.assertEqual(img[6].GetSize(), (128, 128, 64))
        self.assertEqual(img[6].GetSpacing(), (4.92, 4.92, 4.92))
        self.assertEqual(img[6].GetDimension(), 3)
        self.assertEqual(img[7].GetSize(), (128, 128, 64))
        self.assertEqual(img[7].GetSpacing(), (4.92, 4.92, 4.92))
        self.assertEqual(img[7].GetDimension(), 3)
        self.assertEqual(img[8].GetSize(), (128, 128, 64))
        self.assertEqual(img[8].GetSpacing(), (4.92, 4.92, 4.92))
        self.assertEqual(img[8].GetDimension(), 3)
        self.assertEqual(acq,
                         [0, 3.0, 6.3, 9.5, 12.8, 16.0, 19.3, 22.5, 25.8])


class TestResampleSeriesToReference(unittest.TestCase):

    def test_resample_series_to_reference_8_3V(self):
        dcm_path = os.path.join('test', 'data', '8_3V')
        dyn = tictac.image.load_dynamic_series(dcm_path)

        ref_img = sitk.ReadImage(os.path.join(
            'test', 'data', '8_3V_seg', 'Segmentation_2.nrrd'))

        img = tictac.image.resample_series_to_reference(dyn['img'], ref_img)
        self.assertEqual(img[0].GetSize(), (512, 512, 132))
        self.assertAlmostEqual(img[0].GetSpacing()[0], 1.269531, places=5)
        self.assertAlmostEqual(img[0].GetSpacing()[1], 1.269531, places=5)
        self.assertAlmostEqual(img[0].GetSpacing()[2], 2.5, places=5)
        self.assertEqual(img[0].GetDimension(), 3)
        self.assertEqual(img[1].GetSize(), (512, 512, 132))
        self.assertAlmostEqual(img[1].GetSpacing()[0], 1.269531, places=5)
        self.assertAlmostEqual(img[1].GetSpacing()[1], 1.269531, places=5)
        self.assertAlmostEqual(img[1].GetSpacing()[2], 2.5, places=5)
        self.assertEqual(img[1].GetDimension(), 3)
        self.assertEqual(img[2].GetSize(), (512, 512, 132))
        self.assertAlmostEqual(img[2].GetSpacing()[0], 1.269531, places=5)
        self.assertAlmostEqual(img[2].GetSpacing()[1], 1.269531, places=5)
        self.assertAlmostEqual(img[2].GetSpacing()[2], 2.5, places=5)
        self.assertEqual(img[2].GetDimension(), 3)
        self.assertEqual(img[3].GetSize(), (512, 512, 132))
        self.assertAlmostEqual(img[3].GetSpacing()[0], 1.269531, places=5)
        self.assertAlmostEqual(img[3].GetSpacing()[1], 1.269531, places=5)
        self.assertAlmostEqual(img[3].GetSpacing()[2], 2.5, places=5)
        self.assertEqual(img[3].GetDimension(), 3)
        self.assertEqual(img[4].GetSize(), (512, 512, 132))
        self.assertAlmostEqual(img[4].GetSpacing()[0], 1.269531, places=5)
        self.assertAlmostEqual(img[4].GetSpacing()[1], 1.269531, places=5)
        self.assertAlmostEqual(img[4].GetSpacing()[2], 2.5, places=5)
        self.assertEqual(img[4].GetDimension(), 3)
        self.assertEqual(img[5].GetSize(), (512, 512, 132))
        self.assertAlmostEqual(img[5].GetSpacing()[0], 1.269531, places=5)
        self.assertAlmostEqual(img[5].GetSpacing()[1], 1.269531, places=5)
        self.assertAlmostEqual(img[5].GetSpacing()[2], 2.5, places=5)
        self.assertEqual(img[5].GetDimension(), 3)
        self.assertEqual(img[6].GetSize(), (512, 512, 132))
        self.assertAlmostEqual(img[6].GetSpacing()[0], 1.269531, places=5)
        self.assertAlmostEqual(img[6].GetSpacing()[1], 1.269531, places=5)
        self.assertAlmostEqual(img[6].GetSpacing()[2], 2.5, places=5)
        self.assertEqual(img[6].GetDimension(), 3)
        self.assertEqual(img[7].GetSize(), (512, 512, 132))
        self.assertAlmostEqual(img[7].GetSpacing()[0], 1.269531, places=5)
        self.assertAlmostEqual(img[7].GetSpacing()[1], 1.269531, places=5)
        self.assertAlmostEqual(img[7].GetSpacing()[2], 2.5, places=5)
        self.assertEqual(img[7].GetDimension(), 3)
        self.assertEqual(img[8].GetSize(), (512, 512, 132))
        self.assertAlmostEqual(img[8].GetSpacing()[0], 1.269531, places=5)
        self.assertAlmostEqual(img[8].GetSpacing()[1], 1.269531, places=5)
        self.assertAlmostEqual(img[8].GetSpacing()[2], 2.5, places=5)
        self.assertEqual(img[8].GetDimension(), 3)


class TestSeriesRoiMeans(unittest.TestCase):

    def test_series_roi_means_8_3V_no_resample(self):
        dcm_path = os.path.join('test', 'data', '8_3V')
        roi_path = os.path.join(
            'test', 'data', '8_3V_seg', 'Segmentation.nrrd')
        roi_list = [[roi_path, '1', '1', 'none'],
                    [roi_path, '2', '2', 'none']]
        dyn = tictac.image.series_roi_means(dcm_path, roi_list)

        tacq_exp = np.array([0, 3.0, 6.3, 9.5, 12.8, 16.0, 19.3, 22.5, 25.8])
        self.assertFalse(np.any(dyn['tacq'] - tacq_exp))

        r1 = dyn['1']
        r1_exp = np.array([0.0, 0.767681, 1229.61, 12019.3,
                           12058.9, 1277.01, 13.4822, 0.748028, 0.0])
        self.assertTrue(np.all((r1 - r1_exp) < 0.1))

        r2 = dyn['2']
        r2_exp = np.array([31.3157, 3501.54, 33128.1, 38544.1,
                           9529.26, 642.525, 2.57748, 0.345963, 0.0727437])
        self.assertTrue(np.all((r2 - r2_exp) < 0.1))

    def test_series_roi_means_8_3V_resample_roi(self):
        dcm_path = os.path.join('test', 'data', '8_3V')
        roi_path = os.path.join(
            'test', 'data', '8_3V_seg', 'Segmentation_2.nrrd')
        roi_list = [[roi_path, '1', '1', 'roi'],
                    [roi_path, '2', '2', 'roi']]
        dyn = tictac.image.series_roi_means(dcm_path, roi_list)

        r1 = dyn['1']
        r2 = dyn['2']

        self.assertAlmostEqual(float(r1[3]), 13473.5, places=1)
        self.assertAlmostEqual(float(r2[3]), 17120.9, places=1)

    def test_series_roi_means_8_3V_resample_img(self):
        dcm_path = os.path.join('test', 'data', '8_3V')
        roi_path = os.path.join(
            'test', 'data', '8_3V_seg', 'Segmentation_2.nrrd')
        roi_list = [[roi_path, '1', '1', 'img'],
                    [roi_path, '2', '2', 'img']]
        dyn = tictac.series_roi_means(dcm_path, roi_list)

        r1 = dyn['1']
        r2 = dyn['2']

        self.assertAlmostEqual(float(r1[3]), 11405.7, places=1)
        self.assertAlmostEqual(float(r2[3]), 15053.1, places=1)

    def test_custom_labels(self):
        dcm_path = os.path.join('test', 'data', '8_3V')
        roi_path = os.path.join(
            'test', 'data', '8_3V_seg', 'Segmentation.nrrd')
        roi_list = [[roi_path, '2', 'a', 'none']]
        dyn = tictac.image.series_roi_means(dcm_path, roi_list)

        tacq_exp = np.array([0, 3.0, 6.3, 9.5, 12.8, 16.0, 19.3, 22.5, 25.8])
        self.assertFalse(np.any(dyn['tacq'] - tacq_exp))

        r2 = dyn['a']
        r2_exp = np.array([31.3157, 3501.54, 33128.1, 38544.1,
                           9529.26, 642.525, 2.57748, 0.345963, 0.0727437])
        self.assertTrue(np.all((r2 - r2_exp) < 0.1))
