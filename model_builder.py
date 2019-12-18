from itertools import combinations
import heapq

import numpy as np


class ModelBuilder:

    def __init__(self):
        self.population = None

    def update_population(self, population: np.array):
        self.population = population
        self.gene_size = population.shape[-1]
        self.registered_bbs = set([
            BB({i}, population) for i in range(self.gene_size)
        ])
        self.candidate_bbs = self.init_candidate_bbs()

    def init_candidate_bbs(self):
        candidate_bbs = []
        for bb1, bb2 in combinations(self.registered_bbs, r=2):
            candidate_bbs.append(bb1 + bb2)
        heapq.heapify(candidate_bbs)
        return candidate_bbs

    def learn_mpm(self):
        while len(self.registered_bbs) > 1:
            best_candidate_bb = heapq.heappop(self.candidate_bbs)
            if best_candidate_bb.improvement < 0:
                break

            for component in best_candidate_bb.components:
                self.registered_bbs.remove(component)

            new_candidate_bbs = []
            for bb in self.candidate_bbs:
                if len(best_candidate_bb.indices & bb.indices) == 0:
                    new_candidate_bbs.append(bb)
            self.candidate_bbs = new_candidate_bbs

            for bb in self.registered_bbs:
                heapq.heappush(self.candidate_bbs, bb + best_candidate_bb)

            self.registered_bbs.add(best_candidate_bb)

    def save_mpm(self, path):
        with open(path, 'w') as f:
            f.write(f'{len(self.registered_bbs)}\n')
            for bb in self.registered_bbs:
                f.write(f'{len(bb.indices)} {" ".join([str(i) for i in bb.indices])}\n')


class BB:

    def __init__(self, indices: set, population: np.array, components: list = ()):
        self.indices = indices
        self.components = components
        self.population = population
        n = len(population)
        self.D_model = (2 ** (len(indices) - 1)) * np.log2(n)

        _, counts = np.unique(
            self.population[:, list(self.indices)],
            return_counts=True,
            axis=0,
        )
        ps = counts / n
        self.D_data = -n * np.sum(ps * np.log2(ps))
        self.D_total = self.D_data + self.D_model

        if len(self.components) == 2:
            self.improvement = self.components[0].D_total + self.components[1].D_total \
                - self.D_total
        else:
            self.improvement = None

    def __add__(self, other):
        return BB(
            indices=self.indices.union(other.indices),
            population=self.population,
            components=[self, other],
        )

    def __lt__(self, other):
        return self.improvement > other.improvement

    def __repr__(self):
        return str(self.indices)
