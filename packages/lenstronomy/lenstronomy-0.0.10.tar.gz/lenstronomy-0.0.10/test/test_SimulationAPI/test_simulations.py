# import main simulation class of lenstronomy
from lenstronomy.SimulationAPI.simulations import Simulation
from lenstronomy.Data.imaging_data import Data
import numpy.testing as npt
import numpy as np
import copy
import pytest


class TestSimulation(object):
    def setup(self):
        self.SimAPI = Simulation()

        # data specifics
        sigma_bkg = 1.  # background noise per pixel
        exp_time = 10  # exposure time (arbitrary units, flux per pixel is in units #photons/exp_time unit)
        numPix = 100  # cutout pixel size
        deltaPix = 0.05  # pixel size in arcsec (area per pixel = deltaPix**2)
        fwhm = 0.5  # full width half max of PSF
        psf_type = 'pixel'  # 'gaussian', 'pixel', 'NONE'

        # PSF specification

        self.kwargs_data = self.SimAPI.data_configure(numPix, deltaPix, exp_time, sigma_bkg)
        kwargs_psf = self.SimAPI.psf_configure(psf_type='gaussian', fwhm=fwhm, kernelsize=31, deltaPix=deltaPix, truncate=3,
                                          kernel=None)
        self.kwargs_psf = self.SimAPI.psf_configure(psf_type='pixel', fwhm=fwhm, kernelsize=31, deltaPix=deltaPix,
                                               truncate=3,
                                               kernel=kwargs_psf['kernel_point_source'])

    def test_im_sim(self):
        # model specifics

        # list of lens models, supports:

        # 'EXERNAL_SHEAR': external shear
        kwargs_shear = {'e1': 0.01, 'e2': 0.01}  # gamma_ext: shear strength, psi_ext: shear angel (in radian)
        kwargs_spemd = {'theta_E': 1., 'gamma': 1.8, 'center_x': 0, 'center_y': 0, 'q': 0.8, 'phi_G': 0.2}

        lens_model_list = ['SPEP', 'SHEAR']
        kwargs_lens_list = [kwargs_spemd, kwargs_shear]

        # list of light profiles (for lens and source)
        # 'SERSIC': spherical Sersic profile
        kwargs_sersic = {'I0_sersic': 1., 'R_sersic': 0.1, 'n_sersic': 2, 'center_x': 0, 'center_y': 0}
        # 'SERSIC_ELLIPSE': elliptical Sersic profile
        kwargs_sersic_ellipse = {'I0_sersic': 1., 'R_sersic': .6, 'n_sersic': 7, 'center_x': 0, 'center_y': 0,
                                 'phi_G': 0.2, 'q': 0.9}


        lens_light_model_list = ['SERSIC']
        kwargs_lens_light_list = [kwargs_sersic]
        source_model_list = ['SERSIC_ELLIPSE']
        kwargs_source_list = [kwargs_sersic_ellipse]

        kwargs_else = {'sourcePos_x': 0.0, 'sourcePos_y': 0.0,
                       'quasar_amp': 1.}  # quasar point source position in the source plane and intrinsic brightness

        kwargs_options = {'lens_model_list': lens_model_list,
                          'lens_light_model_list': lens_light_model_list,
                          'source_light_model_list': source_model_list,
                          'psf_type': 'pixel',
                          'point_source': True
                          # if True, simulates point source at source position of 'sourcePos_xy' in kwargs_else
                          }

        image_sim = self.SimAPI.im_sim(kwargs_options, self.kwargs_data, self.kwargs_psf, kwargs_lens_list, kwargs_source_list,
                                  kwargs_lens_light_list, kwargs_else)

        assert len(image_sim) == 100
        npt.assert_almost_equal(np.sum(image_sim), 24476.280571230454, decimal=-3)

    def test_normalize_flux(self):
        kwargs_shear = {'e1': 0.01, 'e2': 0.01}  # gamma_ext: shear strength, psi_ext: shear angel (in radian)
        kwargs_spemd = {'theta_E': 1., 'gamma': 1.8, 'center_x': 0, 'center_y': 0, 'q': 0.8, 'phi_G': 0.2}

        lens_model_list = ['SPEP', 'SHEAR']
        kwargs_lens_list = [kwargs_spemd, kwargs_shear]

        # list of light profiles (for lens and source)
        # 'SERSIC': spherical Sersic profile
        kwargs_sersic = {'I0_sersic': 1., 'R_sersic': 0.1, 'n_sersic': 2, 'center_x': 0, 'center_y': 0}
        # 'SERSIC_ELLIPSE': elliptical Sersic profile
        kwargs_sersic_ellipse = {'I0_sersic': 1., 'R_sersic': .6, 'n_sersic': 7, 'center_x': 0, 'center_y': 0,
                                 'phi_G': 0.2, 'q': 0.9}
        lens_light_model_list = ['SERSIC']
        kwargs_lens_light_list = [kwargs_sersic]
        source_model_list = ['SERSIC_ELLIPSE']
        kwargs_source_list = [kwargs_sersic_ellipse]

        kwargs_else = {'sourcePos_x': 0.0, 'sourcePos_y': 0.0,
                       'quasar_amp': 1.}  # quasar point source position in the source plane and intrinsic brightness

        kwargs_options = {'lens_model_list': lens_model_list,
                          'lens_light_model_list': lens_light_model_list,
                          'source_light_model_list': source_model_list,
                          'psf_type': 'pixel',
                          'point_source': True
                          # if True, simulates point source at source position of 'sourcePos_xy' in kwargs_else
                          }
        image_sim = self.SimAPI.im_sim(kwargs_options, self.kwargs_data, self.kwargs_psf, kwargs_lens_list, kwargs_source_list,
                                  kwargs_lens_light_list, kwargs_else)
        kwargs_source_updated, kwargs_lens_light_updated, kwargs_else_updated = self.SimAPI.normalize_flux(kwargs_options, kwargs_source_list, kwargs_lens_light_list, kwargs_else, norm_factor_source=3, norm_factor_lens_light=2, norm_factor_point_source=0.)
        assert kwargs_else_updated['point_amp'][0] == 0

    def test_normalize_flux_source(self):
        # 'EXERNAL_SHEAR': external shear
        kwargs_shear = {'e1': 0.01, 'e2': 0.01}  # gamma_ext: shear strength, psi_ext: shear angel (in radian)
        kwargs_spemd = {'theta_E': 1., 'gamma': 1.8, 'center_x': 0, 'center_y': 0, 'q': 0.8, 'phi_G': 0.2}

        lens_model_list = ['SPEP', 'SHEAR']
        kwargs_lens_list = [kwargs_spemd, kwargs_shear]

        # list of light profiles (for lens and source)
        # 'SERSIC': spherical Sersic profile
        kwargs_sersic = {'I0_sersic': 1., 'R_sersic': 0.1, 'n_sersic': 2, 'center_x': 0, 'center_y': 0}
        # 'SERSIC_ELLIPSE': elliptical Sersic profile
        kwargs_sersic_ellipse = {'I0_sersic': 1., 'R_sersic': .6, 'n_sersic': 7, 'center_x': 0, 'center_y': 0,
                                 'phi_G': 0.2, 'q': 0.9}


        lens_light_model_list = ['SERSIC']
        kwargs_lens_light_list = [kwargs_sersic]
        source_model_list = ['SERSIC_ELLIPSE']
        kwargs_source_list = [kwargs_sersic_ellipse]
        kwargs_options = {'lens_model_list': lens_model_list,
                          'lens_light_model_list': lens_light_model_list,
                          'source_light_model_list': source_model_list,
                          'psf_type': 'pixel',
                          'point_source': True
                          # if True, simulates point source at source position of 'sourcePos_xy' in kwargs_else
                          }
        kwargs_source_updated = self.SimAPI.normalize_flux_source(kwargs_options, kwargs_source_list, norm_factor_source=10)
        assert kwargs_source_updated[0]['I0_sersic'] == kwargs_source_list[0]['I0_sersic'] * 10

    def test_source_plane(self):
        numPix = 10
        deltaPix = 0.1
        kwargs_sersic_ellipse = {'I0_sersic': 1., 'R_sersic': .6, 'n_sersic': 7, 'center_x': 0, 'center_y': 0,
                                 'phi_G': 0.2, 'q': 0.9}


        lens_light_model_list = ['SERSIC']
        source_model_list = ['SERSIC_ELLIPSE']
        kwargs_source = [kwargs_sersic_ellipse]
        kwargs_options = {
                          'lens_light_model_list': lens_light_model_list,
                          'source_light_model_list': source_model_list,
                          'psf_type': 'pixel',
                          'point_source': True
                          # if True, simulates point source at source position of 'sourcePos_xy' in kwargs_else
                          }
        source = self.SimAPI.source_plane(kwargs_options, kwargs_source, numPix, deltaPix)
        assert len(source) == numPix

    def test_fermat_potential(self):
        kwargs_shear = {'e1': 0.01, 'e2': 0.01}  # gamma_ext: shear strength, psi_ext: shear angel (in radian)
        kwargs_spemd = {'theta_E': 1., 'gamma': 1.8, 'center_x': 0, 'center_y': 0, 'q': 0.8, 'phi_G': 0.2}

        lens_model_list = ['SPEP', 'SHEAR']
        kwargs_lens_list = [kwargs_spemd, kwargs_shear]

        # list of light profiles (for lens and source)
        # 'SERSIC': spherical Sersic profile
        kwargs_sersic = {'I0_sersic': 1., 'R_sersic': 0.1, 'n_sersic': 2, 'center_x': 0, 'center_y': 0}
        # 'SERSIC_ELLIPSE': elliptical Sersic profile
        kwargs_sersic_ellipse = {'I0_sersic': 1., 'R_sersic': .6, 'n_sersic': 7, 'center_x': 0, 'center_y': 0,
                                 'phi_G': 0.2, 'q': 0.9}


        lens_light_model_list = ['SERSIC']
        kwargs_lens_light_list = [kwargs_sersic]
        source_model_list = ['SERSIC_ELLIPSE']
        kwargs_source_list = [kwargs_sersic_ellipse]

        kwargs_else = {'sourcePos_x': 0.0, 'sourcePos_y': 0.0,
                       'quasar_amp': 1.}  # quasar point source position in the source plane and intrinsic brightness

        kwargs_options = {'lens_model_list': lens_model_list,
                          'lens_light_model_list': lens_light_model_list,
                          'source_light_model_list': source_model_list,
                          'psf_type': 'pixel',
                          'point_source': True
                          # if True, simulates point source at source position of 'sourcePos_xy' in kwargs_else
                          }

        image_sim = self.SimAPI.im_sim(kwargs_options, self.kwargs_data, self.kwargs_psf, kwargs_lens_list, kwargs_source_list,
                                  kwargs_lens_light_list, kwargs_else)
        _ = self.SimAPI.fermat_potential(kwargs_options, kwargs_lens_list, kwargs_else)
        fermat_pot = self.SimAPI.fermat_potential(kwargs_options, kwargs_lens_list, kwargs_else)
        assert fermat_pot[0] == -0.27197369737141391
        assert len(fermat_pot) == 4

    def test_shift_coordinate_grid(self):
        x_shift = 0.05
        y_shift = 0
        kwargs_data_shifted = self.SimAPI.shift_coordinate_grid(self.kwargs_data, x_shift, y_shift, pixel_units=False)
        kwargs_data_new = copy.deepcopy(self.kwargs_data)
        kwargs_data_new['ra_shift'] = x_shift
        kwargs_data_new['dec_shift'] = y_shift
        data = Data(kwargs_data=kwargs_data_shifted)
        data_new = Data(kwargs_data=kwargs_data_new)
        ra, dec = 0, 0
        x, y = data.map_coord2pix(ra, dec)
        x_new, y_new = data_new.map_coord2pix(ra, dec)
        npt.assert_almost_equal(x, x_new, decimal=10)
        npt.assert_almost_equal(y, y_new, decimal=10)

        ra, dec = data.map_pix2coord(x, y)
        ra_new, dec_new = data_new.map_pix2coord(x, y)
        npt.assert_almost_equal(ra, ra_new, decimal=10)
        npt.assert_almost_equal(dec, dec_new, decimal=10)

        x_coords, y_coords = data.coordinates
        x_coords_new, y_coords_new = data_new.coordinates
        npt.assert_almost_equal(x_coords[0], x_coords_new[0], decimal=10)
        npt.assert_almost_equal(y_coords[0], y_coords_new[0], decimal=10)


if __name__ == '__main__':
    pytest.main()