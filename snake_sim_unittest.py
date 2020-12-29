import unittest
import snake_sim

import random


class SnakeSimTests(unittest.TestCase):
    def test_overbody_true(self):
        snake = [[5, 3], [4, 3], [4, 4], [4, 5], [5, 5], [5, 4], [5, 3]]
        result = snake_sim.overbody(snake)
        self.assertTrue(result)

    def test_overbody_false(self):
        snake = [[6, 3], [5, 3], [4, 3], [4, 4], [4, 5], [5, 5], [5, 4]]
        result = snake_sim.overbody(snake)
        self.assertFalse(result)

    def test_newapple_lotofspace(self):
        snake = [[6, 3], [5, 3], [4, 3], [4, 4], [4, 5], [5, 5], [5, 4]]
        tile_nb = 10
        result = snake_sim.newapple(snake, tile_nb)
        self.assertEqual(result, (2, 9))

    def test_newapple_one_remaining_spot(self):
        snake = [[0, 0], [0, 1], [0, 2], [1, 2], [1, 1], [1, 0], [2, 0], [2, 1]]
        tile_nb = 3
        result = snake_sim.newapple(snake, tile_nb)
        self.assertEqual(result, (2, 2))

    # def test_simulate_game(self):
        # need a model



if __name__ == '__main__':
    random.seed(1)
    unittest.main()