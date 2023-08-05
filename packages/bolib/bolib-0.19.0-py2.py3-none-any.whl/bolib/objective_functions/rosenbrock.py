# -*- coding: utf-8 -*-
#
#    Copyright 2018 Ibai Roman
#
#    This file is part of BOlib.
#
#    BOlib is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    BOlib is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with BOlib. If not, see <http://www.gnu.org/licenses/>.

import numpy as np
from .objective_function import ObjectiveFunction


class Rosenbrock(ObjectiveFunction):
    """

    """
    def __init__(self):
        """

        """
        super(Rosenbrock, self).__init__(
            d=2,
            gaussian_noise=0,
            f_bias=390.0,
            max_eval=400,
            lower=[-100, -100],
            upper=[100, 100],
            objective=[1.42478, 5.475],
            objective_val=390.0,
            params=['x', 'y'],
            types=[float, float]
        )

    def batch_evaluate(self, points):
        """
        CEC 2005 F6 Basic Multimodal Function

        :param points:
        :type points:
        :return:
        :rtype:
        """
        norm_points = points - np.array(self.objective) + 1.0

        result = 0.0
        for i in range(0, norm_points.shape[1]-1):
            result += 100 * np.square(
                    np.square(norm_points[:, i][:, None]) -
                    norm_points[:, i+1][:, None]
                ) + np.square(norm_points[:, i][:, None]-1.0)

        return result + self.f_bias
