import unittest
import genetic_algo

import numpy as np


class GeneticAlgoTests(unittest.TestCase):
    def test_init_pop(self):
        nb = 3
        result = genetic_algo.init_pop()



if __name__ == '__main__':
    np.random.seed(1)
    unittest.main()