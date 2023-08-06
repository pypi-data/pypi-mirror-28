#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ..plugin_interfaces.analysis import OnTheFlyAnalysis

class FitnessStore(OnTheFlyAnalysis):

    # Analysis interval.
    interval = 1

    # Only analyze in master process?
    master_only = True

    def setup(self, ng, engine):
        # Generation numbers.
        self.ngs = []

        # Best fitness in each generation.
        self.fitness_values = []

        # Best solution.
        self.solution = []

    def register_step(self, g, population, engine):
        # Collect data.
        best_indv = population.best_indv(engine.fitness)
        best_fit = engine.ori_fmax

        self.ngs.append(g)
        self.solution.append(best_indv.solution)
        self.fitness_values.append(best_fit)

    def finalize(self, population, engine):
        with open('best_fit.py', 'w', encoding='utf-8') as f:
            f.write('best_fit = [\n')
            for ng, x, y in zip(self.ngs, self.solution, self.fitness_values):
                f.write('    ({}, {}, {}),\n'.format(ng, x, y))
            f.write(']\n\n')

        self.logger.info('Best fitness values are written to best_fit.py')

