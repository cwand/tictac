import os
import unittest
from tictac import bard_pvc
import pandas as pd
import numpy as np


class TestBardPVC(unittest.TestCase):

    def test_on_grid(self):
        tab_path = os.path.join(
            'test', 'data', 'bard_test.txt')
        tab = pd.read_csv(tab_path)
        aorta = np.array([800.0, 130.0, 120.0, 68.0, 50.0, 0.0])
        bkg = np.array([10.0, 20.0, 30.0, 40.0, 50.0, 60.0])
        diameter = 20
        exp = np.array([1000.0, 200.0, 150.0, 80.0, 50.0, 0.0])
        act = bard_pvc(aorta=aorta,
                       bkg=bkg,
                       diameter=diameter,
                       table=tab)
        self.assertTrue(np.all(abs(exp - act) < 0.00001))

    def test_interpolate_ratio(self):
        tab_path = os.path.join(
            'test', 'data', 'bard_test.txt')
        tab = pd.read_csv(tab_path)
        aorta = np.array([1.4, 11.3])
        bkg = np.array([1.0, 2.0])
        diameter = 30
        exp = np.array([1.5, 15.0])
        act = bard_pvc(aorta=aorta,
                       bkg=bkg,
                       diameter=diameter,
                       table=tab)
        self.assertTrue(np.all(abs(exp - act) < 0.00001))

    def test_interpolate_diameter(self):
        tab_path = os.path.join(
            'test', 'data', 'bard_test.txt')
        tab = pd.read_csv(tab_path)
        aorta = np.array([1.425, 6.25, 136.125])
        bkg = np.array([1.0, 2.0, 3.0])
        diameter = 35
        exp = np.array([1.5, 7.0, 165.0])
        act = bard_pvc(aorta=aorta,
                       bkg=bkg,
                       diameter=diameter,
                       table=tab)
        self.assertTrue(np.all(abs(exp - act) < 0.00001))

    def test_ltunit_ratio(self):
        tab_path = os.path.join(
            'test', 'data', 'bard_test.txt')
        tab = pd.read_csv(tab_path)
        aorta = np.array([0.5, 1.3, 0.2])
        bkg = np.array([1.0, 2.0, 3.0])
        diameter = 35
        exp = np.array([0.5, 1.3, 0.2])
        act = bard_pvc(aorta=aorta,
                       bkg=bkg,
                       diameter=diameter,
                       table=tab)
        self.assertTrue(np.all(abs(exp - act) < 0.00001))
