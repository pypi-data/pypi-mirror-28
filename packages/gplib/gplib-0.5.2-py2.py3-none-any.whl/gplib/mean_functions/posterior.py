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

import numpy as np

from .mean_function import MeanFunction


class Posterior(MeanFunction):
    """

    """

    def mean(self, x):
        """
        Marginalize posterior mean

        :param x:
        :return:
        """

        assert self.gp.prior, "There is no prior data"

        # Use marginal cache if data and hyperparameters are the same
        if self.gp.prior['marginal'] and \
                hash(tuple(self.gp.prior['gp'].get_param_values())) == \
                    self.gp.prior['marginal']['param_hash']:
            marginal = self.gp.prior['marginal']
        else:
            marginal = self.gp.prior['gp'].inference_method.marginalize_gp(
                self.gp.prior['data']
            )
            self.gp.prior['marginal'] = marginal

        ka_matrix = self.gp.prior['gp'].\
            covariance_function.marginalize_covariance(
                self.gp.prior['data']['X'], x)
        test_mean = self.gp.prior['gp'].mean_function.marginalize_mean(x)

        f_mean = np.dot(
            ka_matrix.T, marginal['alpha']) + \
                 test_mean

        y_mean = \
            self.gp.prior['gp'].likelihood_function.get_predictive_mean(
                f_mean
            )

        return y_mean

    def dmu_dx(self, x):
        """

        :param x:
        :type x:
        :return:
        :rtype:
        """

        raise NotImplementedError("Not Implemented. This is an interface.")

    def dmu_dtheta(self, x):
        """

        :param x:
        :type x:
        :return:
        :rtype:
        """

        raise NotImplementedError("Not Implemented. This is an interface.")
