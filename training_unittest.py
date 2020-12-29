import unittest
import training

import numpy as np
import sklearn


class TrainingTests(unittest.TestCase):
    def test_prepare_sensors(self):
        sensors = {
            'head_direction': [False, True, False, False],
            'distance_to_apple': 1.718253158075502,
            'apple_direction': [False, False, True, False]
        }
        result = training.prepare_sensors(sensors)
        expected_result = [False, True, False, False, 1.718253158075502, False, False, True, False]
        self.assertEqual(result, expected_result)

    # def test_init_coefs(self):
    #     hidden_layers = (2, 3, 4)
    #     input_nb = 3
    #     result = training.init_coefs(hidden_layers, input_nb)
    #     expected_result = [
    #         np.array([[1.62434536, -0.61175641], [-0.52817175, -1.07296862], [0.86540763, -2.3015387]]),
    #         np.array([[1.74481176, -0.7612069, 0.3190391], [-0.24937038, 1.46210794, -2.06014071]]), 
    #         np.array([[-0.3224172 , -0.38405435, 1.13376944, -1.09989127], [-0.17242821, -0.87785842, 0.04221375, 0.58281521], [-1.10061918, 1.14472371, 0.90159072, 0.50249434]]), 
    #         np.array([[0.90085595, -0.68372786, -0.12289023, -0.93576943], [-0.26788808, 0.53035547, -0.69166075, -0.39675353], [-0.6871727, -0.84520564, -0.67124613, -0.0126646], [-1.11731035, 0.2344157, 1.65980218, 0.74204416]])
    #     ]
    #     for i in range(len(expected_result)):
    #         self.assertEqual(result[i].shape, expected_result[i].shape)
    #         print(result[i])
    #         print(expected_result[i])
    #         self.assertTrue(np.allclose(result[i], expected_result[i]))

    def test_coefs_to_list(self):
        coefs_arr = [
            np.array([[1.62434536, -0.61175641], [-0.52817175, -1.07296862], [0.86540763, -2.3015387]]),
            np.array([[1.74481176, -0.7612069, 0.3190391], [-0.24937038, 1.46210794, -2.06014071]]), 
            np.array([[-0.3224172 , -0.38405435, 1.13376944, -1.09989127], [-0.17242821, -0.87785842, 0.04221375, 0.58281521], [-1.10061918, 1.14472371, 0.90159072, 0.50249434]]), 
            np.array([[0.90085595, -0.68372786, -0.12289023, -0.93576943], [-0.26788808, 0.53035547, -0.69166075, -0.39675353], [-0.6871727, -0.84520564, -0.67124613, -0.0126646], [-1.11731035, 0.2344157, 1.65980218, 0.74204416]])
        ]
        result = training.coefs_to_list(coefs_arr)
        expected_result = np.array([1.62434536, -0.61175641, -0.52817175, -1.07296862, 0.86540763, -2.3015387, 1.74481176, -0.7612069, 0.3190391, -0.24937038, 1.46210794, -2.06014071, -0.3224172, -0.38405435, 1.13376944, -1.09989127, -0.17242821, -0.87785842, 0.04221375, 0.58281521, -1.10061918, 1.14472371, 0.90159072, 0.50249434, 0.90085595, -0.68372786, -0.12289023, -0.93576943, -0.26788808, 0.53035547, -0.69166075, -0.39675353, -0.6871727, -0.84520564, -0.67124613, -0.0126646, -1.11731035, 0.2344157, 1.65980218, 0.74204416])
        self.assertTrue((result == expected_result).all())

    def test_generate_model(self):
        hidden_layers = (6,)
        result = training.generate_model(hidden_layers=hidden_layers)
        self.assertIsInstance(result[0], sklearn.neural_network._multilayer_perceptron.MLPClassifier)
        self.assertEqual(result[1][0].shape, (78,))
        self.assertEqual(result[1][1].shape, (10,))

if __name__ == '__main__':
    np.random.seed(1)
    unittest.main()