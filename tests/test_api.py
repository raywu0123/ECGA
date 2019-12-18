from unittest import TestCase
import os

from dotenv import load_dotenv
load_dotenv('./.env')

from api_utils import APIConnector


class APITest(TestCase):

    def setUp(self):
        self.connector = APIConnector(
            api_url=os.environ.get('API_URL'),
            student_id=os.environ.get('STUDENT_ID'),
        )

    def test_get_population(self):
        population = self.connector.get_population(i_generation=0)
        self.assertTupleEqual(tuple(population.shape), (4000, 50))

    def test_get_info(self):
        self.connector.get_info()

    def test_post_mpm(self):
        r = self.connector.post_mpm('testing_mpm.txt', i_generation=0)
        self.assertSetEqual(set(r.keys()), {'max_fitness', 'best_chromosome'})
