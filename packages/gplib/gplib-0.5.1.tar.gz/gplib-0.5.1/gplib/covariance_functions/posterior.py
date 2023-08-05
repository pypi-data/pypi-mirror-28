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

import scipy.linalg
import numpy as np

from .covariance_function import CovarianceFunction


class Posterior(CovarianceFunction):
    """

    """

    def covariance(self, mat_a, mat_b=None, only_diagonal=False):
        """
        Measures the distance matrix between solutions of A and B, and
        applies the kernel function element-wise to the distance matrix.

        :param mat_a: List of solutions in lines and dimensions in columns.
        :type mat_a:
        :param mat_b: List of solutions in lines and dimensions in columns.
        :type mat_b:
        :param only_diagonal:
        :type only_diagonal:
        :return: Result matrix with kernel function applied element-wise.
        :rtype:
        """
        assert self.gp.prior, "There is no prior data"

        # Use marginal cache if data and hyperparameters are the same
        if self.gp.prior['marginal'] and \
                hash(tuple(self.gp.prior['gp'].get_param_values())) == \
                self.gp.prior['marginal']['param_hash']:
            marginal = self.gp.prior['marginal']
        else:
            marginal = self.gp.prior['gp'].inference_method.\
                mkb_matrixarginalize_gp(self.gp.prior['data'])
            self.gp.prior['marginal'] = marginal

        kxa_matrix = self.gp.prior['gp'].\
            covariance_function.marginalize_covariance(
                self.gp.prior['data']['X'], mat_a) * marginal['noise_precision']

        beta_a = scipy.linalg.solve_triangular(
            marginal['l_matrix'],
            kxa_matrix,
            lower=True,
            check_finite=False)

        if mat_b is None:
            if only_diagonal:
                kaa_diag = \
                    self.gp.prior['gp'].covariance_function.\
                        marginalize_covariance(mat_a, only_diagonal=True)
                f_covariance = kaa_diag - \
                    np.sum(np.power(beta_a, 2), axis=0).reshape(-1, 1)
                f_covariance = f_covariance.clip(min=0.0)
            else:
                kaa_matrix = self.gp.prior['gp']. \
                    covariance_function.marginalize_covariance(
                    mat_a)
                f_covariance = kaa_matrix - np.dot(beta_a.T, beta_a)

            y_covariance = \
                self.gp.prior['gp'].likelihood_function.get_predictive_variance(
                    f_covariance
                )
        else:
            kxb_matrix = self.gp.prior['gp'].\
                covariance_function.marginalize_covariance(
                    self.gp.prior['data']['X'], mat_b) * \
                         marginal['noise_precision']
            kab_matrix = self.gp.prior['gp'].\
                covariance_function.marginalize_covariance(
                    mat_a, mat_b)

            beta_b = scipy.linalg.solve_triangular(
                marginal['l_matrix'],
                kxb_matrix,
                lower=True,
                check_finite=False)

            f_covariance = kab_matrix - np.dot(beta_a.T, beta_b)

            y_covariance = f_covariance

        return y_covariance

    def dk_dx(self, mat_a, mat_b=None):
        """
        Measures gradient of the distance between solutions of A and B in X.

        :param mat_a: List of solutions in lines and dimensions in columns.
        :param mat_b: List of solutions in lines and dimensions in columns.
        :return: 3D array with the gradient in every dimension of X.
        """

        raise NotImplementedError("Not Implemented. This is an interface.")

    def dk_dtheta(self, mat_a, mat_b=None):
        """
        Measures gradient of the distance between solutions of A and B in the
        hyper-parameter space.

        :param mat_a: List of solutions in lines and dimensions in columns.
        :param mat_b: List of solutions in lines and dimensions in columns.
        :return: 3D array with the gradient in every
         dimension the length-scale hyper-parameter space.
        """

        raise NotImplementedError("Not Implemented. This is an interface.")
