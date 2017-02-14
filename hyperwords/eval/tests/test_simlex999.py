'''
Created on Jan 19, 2015

@author: Minh Ngoc Le
'''
import unittest
from eval.simlex999 import _init

class Test(unittest.TestCase):

    def test_init(self):
        _init()

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test_sim_lemma']
    unittest.main()