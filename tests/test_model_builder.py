from unittest import TestCase

import numpy as np

from model_builder import BB, ModelBuilder


class TestModelBuilder(TestCase):

    def setUp(self):
        self.population = np.array([
            [0, 0, 0, 1],
            [1, 1, 0, 0],
            [0, 0, 1, 1],
            [0, 1, 0, 1],
        ])
        self.model_builder = ModelBuilder(population=self.population)

    def test_learn_mpm(self):
        self.model_builder.learn_mpm()
        print(self.model_builder.registered_bbs)


class TestBB(TestCase):

    def test_bb_add(self):
        population = np.array([
            [0, 0, 0, 1],
            [1, 1, 0, 0],
            [0, 0, 1, 1],
            [0, 1, 0, 1],
        ])
        new_bb = BB(indices={0, 3}, population=population)
        self.assertEqual(new_bb.D_data, -4 * ((1/4) * np.log2(1/4) + (3/4) * np.log2(3/4)))
        self.assertEqual(new_bb.D_model, 2 ** (2 - 1) * np.log2(4))
