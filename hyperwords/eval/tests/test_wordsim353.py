'''
Created on Jan 19, 2015

@author: Minh Ngoc Le
'''
import unittest
from eval.wordsim353 import read_data

class Test(unittest.TestCase):

    def test_simple(self):
        read_data('set1')

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test_sim_lemma']
    unittest.main()