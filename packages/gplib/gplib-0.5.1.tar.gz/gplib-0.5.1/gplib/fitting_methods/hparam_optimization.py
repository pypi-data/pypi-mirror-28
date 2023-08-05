# -*- coding: utf-8 -*-
#
#    Copyright 2018 Ibai Roman
#
#    This file is part of GPlib.
#
#    GPlib is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    GPlib is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with GPlib. If not, see <http://www.gnu.org/licenses/>.

import time

import numpy as np
import scipy.optimize as spo

from .fitting_method import FittingMethod


class HparamOptimization(FittingMethod):
    """

    """

    def __init__(self, maxfuncall=1000, maxlsiter=100, ls_method='L-BFGS-B'):

        self.ls_method = ls_method
        if self.ls_method in ["Newton-CG", "dogleg", "trust-ncg"]:
            raise NotImplementedError("Hessian not implemented for {}".format(
                self.ls_method))
        self.grad_needed = self.ls_method in [
            "CG", "BFGS", "Newton-CG", "L-BFGS-B",
            "TNC", "SLSQP", "dogleg", "trust-ncg"
        ]
        self.bounded_search = self.ls_method in [
            "L-BFGS-B", "TNC", "SLSQP"
        ]
        self.maxfuncall = maxfuncall
        self.maxlsiter = maxlsiter
        self.log = {
            'best_params': [],
            'best_estimator': None,
            'funcalls': 0,
            'improvement_count': 0,
            'last_improvement': {
                'restart': 0,
                'funcall': 0
            },
            'time': 0.0
        }
        super(HparamOptimization, self).__init__()

    def get_log(self):
        """

        :return:
        :rtype:
        """
        return self.log

    def fit(self, data):
        """
        optimize hyperparams

        :param data:
        :type data:
        :return:
        :rtype:
        """
        # Get estimator wrappers ready
        bounds = None
        if self.bounded_search:
            bounds = self.gp.get_param_bounds(trans=True)
        estimator_opt_wrapper = self.get_estimator_wrapper(
            data, grad_needed=self.grad_needed)

        # Main loop
        self.log['funcalls'] = 0
        self.log['current_params'] = None
        self.log['current_estimator'] = np.inf
        self.log['best_params'] = None
        self.log['best_estimator'] = np.inf
        self.log['improvement_count'] = 0
        self.log['restart_count'] = 0
        self.log['last_improvement'] = {
            'restart': 0,
            'funcall': 0
        }
        start = time.time()
        while self.log['funcalls'] < self.maxfuncall:
            # run optimization
            self.log['current_estimator'] = np.inf
            x_0 = self.gp.get_param_values(trans=True)
            try:
                spo.minimize(
                    estimator_opt_wrapper,
                    x_0, method=self.ls_method,
                    jac=self.grad_needed, bounds=bounds,
                    options={
                        'disp': False,
                        'maxiter': self.maxlsiter
                    }
                )
            except (AssertionError, np.linalg.linalg.LinAlgError):
                pass

            self.log['restart_count'] += 1
            if self.log['current_estimator'] < self.log['best_estimator']:
                self.log['best_estimator'] = self.log['current_estimator']
                self.log['best_params'] = self.log['current_params']
                self.log['improvement_count'] += 1
                self.log['last_improvement']['restart'] = \
                    self.log['restart_count']
                self.log['last_improvement']['funcall'] = self.log['funcalls']
            self.gp.set_params_at_random(trans=True)

        end = time.time()
        self.log['time'] = end - start
        del self.log['current_estimator']
        del self.log['current_params']

        if self.log['best_params'] is None:
            raise Exception("No params were found")

        self.gp.set_param_values(self.log['best_params'], trans=False)

        # TODO create a test
        # last_estimator = -float(
        #     self.gp.likelihood_function.get_log_likelihood(
        #         data, gradient_needed=False
        #     )
        # )
        #
        # assert last_estimator == self.log['best_estimator'],\
        #     "best_params and best_estimator are not consistent"

    def get_estimator_wrapper(self, data, grad_needed=False):
        """

        :param data:
        :type data:
        :param grad_needed:
        :type grad_needed:
        :return:
        :rtype:
        """

        def estimator_wrapper(mod_params):
            """
            estimator wrapper to optimize hyperparameters
            :param mod_params:
            :return:
            """
            assert self.log['funcalls'] < self.maxfuncall,\
                "Funcall limit reached"
            self.log['funcalls'] += 1

            likelihood = np.Inf
            grad_likelihood = np.random.uniform(-1, 1, len(mod_params))

            try:
                self.gp.set_param_values(mod_params, trans=True)
                likelihood = self.gp.likelihood_function.get_log_likelihood(
                    data, gradient_needed=grad_needed
                )
                if grad_needed:
                    likelihood, grad_likelihood = likelihood
                    grad_likelihood = -np.array(grad_likelihood)
                likelihood = -float(likelihood)
            except np.linalg.linalg.LinAlgError as ex:
                raise(ex)
            except AssertionError:
                pass

            if likelihood < self.log['current_estimator']:
                self.log['current_estimator'] = likelihood
                self.log['current_params'] = self.gp.get_param_values()

            if grad_needed:
                return likelihood, grad_likelihood

            return likelihood

        return estimator_wrapper
