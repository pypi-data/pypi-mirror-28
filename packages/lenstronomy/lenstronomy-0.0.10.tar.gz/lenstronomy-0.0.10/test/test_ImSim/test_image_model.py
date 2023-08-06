__author__ = 'sibirrer'

import numpy.testing as npt
import numpy as np
import pytest

from lenstronomy.ImSim.image_model import ImageModel
from lenstronomy.SimulationAPI.simulations import Simulation


class TestImageModel(object):
    """
    tests the source model routines
    """
    def setup(self):
        self.SimAPI = Simulation()

        # data specifics
        sigma_bkg = .05  # background noise per pixel
        exp_time = 100  # exposure time (arbitrary units, flux per pixel is in units #photons/exp_time unit)
        numPix = 100  # cutout pixel size
        deltaPix = 0.05  # pixel size in arcsec (area per pixel = deltaPix**2)
        fwhm = 0.5  # full width half max of PSF
        psf_type = 'pixel'  # 'gaussian', 'pixel', 'NONE'

        # PSF specification

        self.kwargs_data = self.SimAPI.data_configure(numPix, deltaPix, exp_time, sigma_bkg)
        kwargs_psf = self.SimAPI.psf_configure(psf_type='gaussian', fwhm=fwhm, kernelsize=31, deltaPix=deltaPix, truncate=3,
                                          kernel=None)
        self.kwargs_psf = self.SimAPI.psf_configure(psf_type=psf_type, fwhm=fwhm, kernelsize=31, deltaPix=deltaPix,
                                               truncate=6,
                                               kernel=kwargs_psf['kernel_point_source'])


        # 'EXERNAL_SHEAR': external shear
        kwargs_shear = {'e1': 0.01, 'e2': 0.01}  # gamma_ext: shear strength, psi_ext: shear angel (in radian)
        kwargs_spemd = {'theta_E': 1., 'gamma': 1.8, 'center_x': 0, 'center_y': 0, 'q': 0.8, 'phi_G': 0.2}

        lens_model_list = ['SPEP', 'SHEAR']
        self.kwargs_lens = [kwargs_spemd, kwargs_shear]

        # list of light profiles (for lens and source)
        # 'SERSIC': spherical Sersic profile
        kwargs_sersic = {'I0_sersic': 1., 'R_sersic': 0.1, 'n_sersic': 2, 'center_x': 0, 'center_y': 0}
        # 'SERSIC_ELLIPSE': elliptical Sersic profile
        kwargs_sersic_ellipse = {'I0_sersic': 1., 'R_sersic': .6, 'n_sersic': 7, 'center_x': 0, 'center_y': 0,
                                 'phi_G': 0.2, 'q': 0.9}


        lens_light_model_list = ['SERSIC']
        self.kwargs_lens_light = [kwargs_sersic]
        source_model_list = ['SERSIC_ELLIPSE']
        self.kwargs_source = [kwargs_sersic_ellipse]

        self.kwargs_else = {'sourcePos_x': 0.0, 'sourcePos_y': 0.0,
                       'quasar_amp': 1.}  # quasar point source position in the source plane and intrinsic brightness

        self.kwargs_options = {'lens_model_list': lens_model_list,
                          'lens_light_model_list': lens_light_model_list,
                          'source_light_model_list': source_model_list,
                          'psf_type': 'pixel',
                          'point_source': True
                          # if True, simulates point source at source position of 'sourcePos_xy' in kwargs_else
                          }

        image_sim = self.SimAPI.im_sim(self.kwargs_options, self.kwargs_data, self.kwargs_psf, self.kwargs_lens, self.kwargs_source,
                                  self.kwargs_lens_light, self.kwargs_else)
        self.kwargs_data['image_data'] = image_sim
        self.imageModel = ImageModel(self.kwargs_options, self.kwargs_data, self.kwargs_psf)

    def test_source_surface_brightness(self):
        source_model = self.imageModel.source_surface_brightness(self.kwargs_source, self.kwargs_lens, unconvolved=False, de_lensed=False)
        assert len(source_model) == 100
        npt.assert_almost_equal(source_model[10, 10], 0.13646500032614567, decimal=8)

        source_model = self.imageModel.source_surface_brightness(self.kwargs_source, self.kwargs_lens, unconvolved=True, de_lensed=False)
        assert len(source_model) == 100
        npt.assert_almost_equal(source_model[10, 10], 0.13162651658058167, decimal=8)

    def test_lens_surface_brightness(self):
        lens_flux = self.imageModel.lens_surface_brightness(self.kwargs_lens_light, unconvolved=False)
        npt.assert_almost_equal(lens_flux[50, 50], 0.41694042298079464, decimal=8)

        lens_flux = self.imageModel.lens_surface_brightness(self.kwargs_lens_light, unconvolved=True)
        npt.assert_almost_equal(lens_flux[50, 50], 4.4297004326559657, decimal=8)

    def test_image_linear_solve(self):
        model, error_map, cov_param, param = self.imageModel.image_linear_solve(self.kwargs_lens, self.kwargs_source, self.kwargs_lens_light, self.kwargs_else, inv_bool=False)
        chi2_reduced = self.imageModel.Data.reduced_chi2(model, error_map)
        npt.assert_almost_equal(chi2_reduced, 1, decimal=1)

    def test_image_with_params(self):
        model, error_map = self.imageModel.image_with_params(self.kwargs_lens, self.kwargs_source, self.kwargs_lens_light, self.kwargs_else, unconvolved=False, source_add=True, lens_light_add=True, point_source_add=True)
        chi2_reduced = self.imageModel.Data.reduced_chi2(model, error_map)
        npt.assert_almost_equal(chi2_reduced, 1, decimal=1)

    def test_point_sources_list(self):
        point_source_list = self.imageModel.point_sources_list(self.kwargs_else)
        assert len(point_source_list) == 4

    def test_image_positions(self):
        x_im, y_im = self.imageModel.image_positions(self.kwargs_lens, self.kwargs_else['sourcePos_x'], self.kwargs_else['sourcePos_y'])
        npt.assert_almost_equal(x_im[0], self.kwargs_else['ra_pos'][0], decimal=4)
        npt.assert_almost_equal(x_im[1], self.kwargs_else['ra_pos'][1], decimal=4)
        npt.assert_almost_equal(x_im[2], self.kwargs_else['ra_pos'][2], decimal=4)
        npt.assert_almost_equal(x_im[3], self.kwargs_else['ra_pos'][3], decimal=4)

    def test_likelihood_data_given_model(self):
        logL = self.imageModel.likelihood_data_given_model(self.kwargs_lens, self.kwargs_source, self.kwargs_lens_light, self.kwargs_else, source_marg=False)
        npt.assert_almost_equal(logL, -5000, decimal=-3)

        logLmarg = self.imageModel.likelihood_data_given_model(self.kwargs_lens, self.kwargs_source, self.kwargs_lens_light,
                                                           self.kwargs_else, source_marg=True)
        npt.assert_almost_equal(logL - logLmarg, 0, decimal=-3)

    def test_reduced_residuals(self):
        model = self.SimAPI.im_sim(self.kwargs_options, self.kwargs_data, self.kwargs_psf, self.kwargs_lens, self.kwargs_source,
                                  self.kwargs_lens_light, self.kwargs_else, no_noise=True)
        residuals = self.imageModel.reduced_residuals(model, error_map=0)
        npt.assert_almost_equal(np.std(residuals), 1.01, decimal=1)

        chi2 = self.imageModel.reduced_chi2(model, error_map=0)
        npt.assert_almost_equal(chi2, 1, decimal=1)

    def test_numData_evaluate(self):
        numData = self.imageModel.numData_evaluate
        assert numData == 10000

    def test_fermat_potential(self):
        phi_fermat = self.imageModel.fermat_potential(self.kwargs_lens, self.kwargs_else)
        print(phi_fermat)
        npt.assert_almost_equal(phi_fermat[0], -0.2719737, decimal=3)
        npt.assert_almost_equal(phi_fermat[1], -0.2719737, decimal=3)
        npt.assert_almost_equal(phi_fermat[2], -0.51082354, decimal=3)
        npt.assert_almost_equal(phi_fermat[3], -0.51082354, decimal=3)

    def test_add_mask(self):
        mask = np.array([[0, 1],[1, 0]])
        A = np.ones((10, 4))
        A_masked = self.imageModel._add_mask(A, mask)
        assert A[0, 1] == A_masked[0, 1]
        assert A_masked[0, 3] == 0

    def test_point_source_rendering(self):
        # initialize data
        from lenstronomy.SimulationAPI.simulations import Simulation
        SimAPI = Simulation()
        numPix = 100
        deltaPix = 0.05
        kwargs_data = SimAPI.data_configure(numPix, deltaPix, exposure_time=1, sigma_bkg=1)
        kwargs_options = {'lens_model_list': ['SPEP'], 'point_source': True, 'subgrid_res': 2}
        kernel = np.zeros((5, 5))
        kernel[2, 2] = 1
        kwargs_psf = {'kernel_point_source': kernel, 'kernel_pixel': kernel, 'psf_type': 'pixel'}
        makeImage = ImageModel(kwargs_options, kwargs_data, kwargs_psf=kwargs_psf)
        # chose point source positions
        x_pix = np.array([10, 5, 10, 90])
        y_pix = np.array([40, 50, 60, 50])
        ra_pos, dec_pos = makeImage.Data.map_pix2coord(x_pix, y_pix)
        kwargs_lens_init = [{'theta_E': 1, 'gamma': 2, 'q': 0.8, 'phi_G': 0, 'center_x': 0, 'center_y': 0}]
        kwargs_else = {'ra_pos': ra_pos, 'dec_pos': dec_pos, 'point_amp': np.ones_like(ra_pos)}
        model, _ = makeImage.image_with_params(kwargs_lens_init, kwargs_source={}, kwargs_lens_light={}, kwargs_else=kwargs_else)
        image = makeImage.Data.array2image(model)
        for i in range(len(x_pix)):
            assert image[y_pix[i], x_pix[i]] == 1

        x_pix = np.array([10.5, 5.5, 10.5, 90.5])
        y_pix = np.array([40, 50, 60, 50])
        ra_pos, dec_pos = makeImage.Data.map_pix2coord(x_pix, y_pix)
        kwargs_lens_init = [{'theta_E': 1, 'gamma': 2, 'q': 0.8, 'phi_G': 0, 'center_x': 0, 'center_y': 0}]
        kwargs_else = {'ra_pos': ra_pos, 'dec_pos': dec_pos, 'point_amp': np.ones_like(ra_pos)}
        model, _ = makeImage.image_with_params(kwargs_lens_init, kwargs_source={}, kwargs_lens_light={}, kwargs_else=kwargs_else)
        image = makeImage.Data.array2image(model)
        for i in range(len(x_pix)):
            print(int(y_pix[i]), int(x_pix[i]+0.5))
            assert image[int(y_pix[i]), int(x_pix[i])] == 0.5
            assert image[int(y_pix[i]), int(x_pix[i]+0.5)] == 0.5


if __name__ == '__main__':
    pytest.main()


