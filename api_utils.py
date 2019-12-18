from urllib.parse import urljoin
import posixpath

import requests
import numpy as np


class APIConnector:

    def __init__(self, api_url, student_id):
        self.api_url = api_url
        self.student_id = student_id

    def get_info(self):
        r = requests.get(
            url=urljoin(
                self.api_url,
                posixpath.join('api', self.student_id),
            ),
            params={"content-type": "application/json; charset=utf-8"},
        )
        return r.json()

    def get_population(self, i_generation: int):
        url = urljoin(
            self.api_url,
            posixpath.join(
                'population',
                self.student_id,
                f'popu{i_generation:03d}.txt',
            ),
        )
        r = requests.get(url)
        arr = np.asarray([
            [c - 48 for c in chr]
            for chr in r.content.splitlines()
        ], dtype=bool)
        return arr

    def post_mpm(self, filename, i_generation):
        with open(filename, 'rb') as f:
            r = requests.post(
                urljoin(
                    self.api_url,
                    posixpath.join('api', self.student_id)
                ),
                data={'gen': i_generation},
                files={'file': f},
            )
        j = r.json()['fitness'].split()
        max_fitness = float(j[1].split(':')[-1].split('/')[0])
        best_chromosome = j[-1].split(':')[-1]
        return {
            'max_fitness': max_fitness,
            'best_chromosome': best_chromosome,
        }
