import os
import unittest
from tictac import bard_pvc
import pandas as pd

class TestBardPVC(unittest.TestCase):

    def test_unit_ratio(self):
        tab_path = os.path.join(
            'test', 'data', 'bard_test.txt')
        tab = pd.read_csv(tab_path)
        r = bard_pvc(5.0, 5.0, 16, tab)
        self.assertEqual(r, 1.0)

    def test_ltunit_ratio(self):
        tab_path = os.path.join(
            'test', 'data', 'bard_test.txt')
        tab = pd.read_csv(tab_path)
        r = bard_pvc(3.0, 5.0, 16, tab)
        self.assertEqual(r, 1.0)

    def test_on_grid(self):
        tab_path = os.path.join(
            'test', 'data', 'bard_test.txt')
        tab = pd.read_csv(tab_path)
        r = bard_pvc(30.0, 3.0, 20, tab)
        self.assertEqual(r, 60.0)
