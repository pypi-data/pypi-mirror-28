__author__ = 'sibirrer'

import numpy.testing as npt
import numpy as np
import pytest
from lenstronomy.LensModel.lens_model_extensions import LensModelExtensions


class TestLensModelExtensions(object):
    """
    tests the source model routines
    """
    def setup(self):
        pass

    def test_critical_curves(self):
        lens_model_list = ['SPEP']
        kwargs_lens = [{'theta_E': 1., 'gamma': 2., 'q': 0.8, 'phi_G': 1., 'center_x': 0, 'center_y': 0}]
        lensModel = LensModelExtensions(lens_model_list)
        ra_crit_list, dec_crit_list, ra_caustic_list, dec_caustic_list = lensModel.critical_curve_caustics(kwargs_lens,
                                                                                                 kwargs_else={}, compute_window=5, grid_scale=0.005)
        print(ra_caustic_list)
        npt.assert_almost_equal(ra_caustic_list[0][3], -0.25629009803139047, decimal=5)
        npt.assert_almost_equal(dec_caustic_list[0][3], -0.39153358367275115, decimal=5)
        npt.assert_almost_equal(ra_crit_list[0][3], -0.53249999999999997, decimal=5)
        npt.assert_almost_equal(dec_crit_list[0][3], -1.2536936868024853, decimal=5)

        """
        import matplotlib.pyplot as plt
        lensModel = LensModel(lens_model_list)
        x_grid_high_res, y_grid_high_res = util.make_subgrid(x_grid, y_grid, 10)
        mag_high_res = util.array2image(
            lensModel.magnification(x_grid_high_res, y_grid_high_res, kwargs_lens, kwargs_else={}))

        cs = plt.contour(util.array2image(x_grid_high_res), util.array2image(y_grid_high_res), mag_high_res, [0],
                         alpha=0.0)
        paths = cs.collections[0].get_paths()
        for i, p in enumerate(paths):
            v = p.vertices
            ra_points = v[:, 0]
            dec_points = v[:, 1]
            print(ra_points, ra_crit_list[i])
            npt.assert_almost_equal(ra_points[0], ra_crit_list[i][0], 5)
            npt.assert_almost_equal(dec_points[0], dec_crit_list[i][0], 5)
        """

    def test_get_magnification_model(self):
        self.kwargs_options = { 'lens_model_list': ['GAUSSIAN'], 'source_light_model_list': ['GAUSSIAN'],
                               'lens_light_model_list': ['SERSIC']
            , 'subgrid_res': 10, 'numPix': 200, 'psf_type': 'gaussian', 'x2_simple': True}
        kwargs_lens = [{'amp': 1, 'sigma_x': 2, 'sigma_y': 2, 'center_x': 0, 'center_y': 0}]

        x_pos = np.array([1., 1., 2.])
        y_pos = np.array([-1., 0., 0.])
        lens_model = LensModelExtensions(lens_model_list=['GAUSSIAN'])
        mag = lens_model.magnification_finite(x_pos, y_pos, kwargs_lens, kwargs_else=None, source_sigma=0.003, window_size=0.1, grid_number=100)
        npt.assert_almost_equal(mag[0], 0.98848384784633392, decimal=5)

    def test_profile_slope(self):
        lens_model = LensModelExtensions(lens_model_list=['SPP'])
        gamma_in = 2.
        kwargs_lens = [{'theta_E': 1., 'gamma': gamma_in, 'center_x': 0, 'center_y': 0}]
        gamma_out = lens_model.profile_slope(kwargs_lens, kwargs_else={})
        npt.assert_array_almost_equal(gamma_out, gamma_in, decimal=3)
        gamma_in = 1.7
        kwargs_lens = [{'theta_E': 1., 'gamma': gamma_in, 'center_x': 0, 'center_y': 0}]
        gamma_out = lens_model.profile_slope(kwargs_lens, kwargs_else={})
        npt.assert_array_almost_equal(gamma_out, gamma_in, decimal=3)

        gamma_in = 2.5
        kwargs_lens = [{'theta_E': 1., 'gamma': gamma_in, 'center_x': 0, 'center_y': 0}]
        gamma_out = lens_model.profile_slope(kwargs_lens, kwargs_else={})
        npt.assert_array_almost_equal(gamma_out, gamma_in, decimal=3)

        lens_model = LensModelExtensions(lens_model_list=['SPEP'])
        gamma_in = 2.
        kwargs_lens = [{'theta_E': 1.4516812130749424, 'q': 0.89760957136967312, 'center_x': -0.04507598845306314,
         'center_y': 0.054491803177414651, 'phi_G': 0.34403343049704888, 'gamma': gamma_in}]
        gamma_out = lens_model.profile_slope(kwargs_lens, kwargs_else={})
        npt.assert_array_almost_equal(gamma_out, gamma_in, decimal=3)


if __name__ == '__main__':
    pytest.main("-k TestLensModel")



