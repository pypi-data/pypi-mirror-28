__author__ = 'sibirrer'

import numpy.testing as npt
import pytest
import numpy as np
from lenstronomy.SimulationAPI.simulations import Simulation
from lenstronomy.ImSim.psf_fitting import PSF_fitting


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

        kwargs_data = self.SimAPI.data_configure(numPix, deltaPix, exp_time, sigma_bkg)
        kwargs_psf = self.SimAPI.psf_configure(psf_type='gaussian', fwhm=fwhm, kernelsize=31, deltaPix=deltaPix, truncate=3,
                                          kernel=None)
        kwargs_psf = self.SimAPI.psf_configure(psf_type=psf_type, fwhm=fwhm, kernelsize=31, deltaPix=deltaPix,
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

        image_sim = self.SimAPI.im_sim(self.kwargs_options, kwargs_data, kwargs_psf, self.kwargs_lens, self.kwargs_source,
                                  self.kwargs_lens_light, self.kwargs_else)
        kwargs_data['image_data'] = image_sim
        self.kwargs_data = kwargs_data
        self.kwargs_psf = kwargs_psf
        self.psf_fitting = PSF_fitting()

    def test_update_psf(self):
        fwhm = 0.3
        kwargs_psf = self.SimAPI.psf_configure(psf_type='gaussian', fwhm=fwhm, kernelsize=31, deltaPix=0.05, truncate=3,
                                          kernel=None)
        kwargs_psf = self.SimAPI.psf_configure(psf_type='pixel', fwhm=fwhm, kernelsize=31, deltaPix=0.05,
                                               truncate=6,
                                               kernel=kwargs_psf['kernel_point_source'])

        kwargs_psf_return, improved_bool = self.psf_fitting.update_psf(self.kwargs_data, kwargs_psf, self.kwargs_options, self.kwargs_lens, self.kwargs_source, self.kwargs_lens_light,
                   self.kwargs_else, factor=0.1, symmetry=1)
        assert improved_bool
        kernel_new = kwargs_psf_return['kernel_point_source']
        kernel_true = self.kwargs_psf['kernel_point_source']
        kernel_old = kwargs_psf['kernel_point_source']
        diff_old = np.sum((kernel_old - kernel_true)**2)
        diff_new = np.sum((kernel_new - kernel_true) ** 2)
        assert diff_old > diff_new

    def test_update_iterative(self):
        fwhm = 0.3
        kwargs_psf = self.SimAPI.psf_configure(psf_type='gaussian', fwhm=fwhm, kernelsize=31, deltaPix=0.05, truncate=3,
                                          kernel=None)
        kwargs_psf = self.SimAPI.psf_configure(psf_type='pixel', fwhm=fwhm, kernelsize=31, deltaPix=0.05,
                                               truncate=6,
                                               kernel=kwargs_psf['kernel_point_source'])
        kwargs_psf_new = self.psf_fitting.update_iterative(self.kwargs_data, kwargs_psf, self.kwargs_options, self.kwargs_lens, self.kwargs_source, self.kwargs_lens_light,
                   self.kwargs_else, factor=0.2, num_iter=10, symmetry=1)
        kernel_new = kwargs_psf_new['kernel_point_source']
        kernel_true = self.kwargs_psf['kernel_point_source']
        kernel_old = kwargs_psf['kernel_point_source']
        diff_old = np.sum((kernel_old - kernel_true)**2)
        diff_new = np.sum((kernel_new - kernel_true) ** 2)
        assert diff_old > diff_new
        assert diff_new < 0.001


if __name__ == '__main__':
    pytest.main()


