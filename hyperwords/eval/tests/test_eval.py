import unittest
from eval import _safe_pearson
from scipy.stats import pearsonr

class Test(unittest.TestCase):

    def test_pearson(self):
        assert pearsonr([0.1, 2.1, 1.3], [0.2, 0.3, 1.0])[0] < 1
        assert _safe_pearson([0.1, 2.1, 1.3], [0.2, 2.3, 1.0])[0] < 1
        assert _safe_pearson([0.1, None, 1.3, 4.5], [0.2, 2.3, 1.0, 5.2])[0] < 1