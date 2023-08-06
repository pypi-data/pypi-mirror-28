import copy
import numpy as np
import lenstronomy.Util.util as util
import lenstronomy.Util.analysis_util as analysis_util
from lenstronomy.LensModel.Profiles.gaussian import Gaussian
import lenstronomy.Util.multi_gauss_expansion as mge

from lenstronomy.LightModel.light_model import LensLightModel, SourceModel
from lenstronomy.LensModel.lens_model_extensions import LensModelExtensions
from lenstronomy.LensModel.numeric_lens_differentials import NumericLens


class LensAnalysis(object):
    """
    class to compute flux ratio anomalies, inherited from standard MakeImage
    """
    def __init__(self, kwargs_options, kwargs_data):
        self.LensLightModel = LensLightModel(kwargs_options.get('lens_light_model_list', ['NONE']))
        self.SourceModel = SourceModel(kwargs_options.get('source_light_model_list', ['NONE']))
        self.LensModel = LensModelExtensions(lens_model_list=kwargs_options['lens_model_list'], foreground_shear=kwargs_options.get("foreground_shear", False))
        #self.kwargs_data = kwargs_data
        self.kwargs_options = kwargs_options
        self.NumLensModel = NumericLens(lens_model_list=kwargs_options['lens_model_list'], foreground_shear=kwargs_options.get("foreground_shear", False))
        self.gaussian = Gaussian()

    def half_light_radius(self, kwargs_lens_light, deltaPix=None, numPix=None):
        """
        computes numerically the half-light-radius of the deflector light and the total photon flux

        :param kwargs_lens_light:
        :return:
        """
        if numPix is None:
            numPix = 1000
        if deltaPix is None:
            deltaPix = 0.05
        x_grid, y_grid = util.make_grid(numPix=numPix, deltapix=deltaPix)
        lens_light = self._lens_light_internal(x_grid, y_grid, kwargs_lens_light)
        R_h = analysis_util.half_light_radius(lens_light, x_grid, y_grid)
        return R_h

    def _lens_light_internal(self, x_grid, y_grid, kwargs_lens_light):
        """

        :param x_grid:
        :param y_grid:
        :param kwargs_lens_light:
        :return:
        """
        kwargs_lens_light_copy = copy.deepcopy(kwargs_lens_light)
        lens_light_model_internal_bool = self.kwargs_options.get('lens_light_model_internal_bool', [True] * len(kwargs_lens_light))
        lens_light = np.zeros_like(x_grid)
        for i, bool in enumerate(lens_light_model_internal_bool):
            if bool is True:
                kwargs_lens_light_copy[i]['center_x'] = 0
                kwargs_lens_light_copy[i]['center_y'] = 0
                lens_light_i = self.LensLightModel.surface_brightness(x_grid, y_grid, kwargs_lens_light_copy, k=i)
                lens_light += lens_light_i
        return lens_light

    def multi_gaussian_lens_light(self, kwargs_lens_light, n_comp=20):
        """
        multi-gaussian decomposition of the lens light profile (in 1-dimension)

        :param kwargs_lens_light:
        :param n_comp:
        :return:
        """
        r_h = self.half_light_radius(kwargs_lens_light)
        r_array = np.logspace(-2, 1, 50) * r_h
        flux_r = self._lens_light_internal(r_array, np.zeros_like(r_array), kwargs_lens_light)
        amplitudes, sigmas, norm = mge.mge_1d(r_array, flux_r, N=n_comp)
        return amplitudes, sigmas

    def multi_gaussian_lens(self, kwargs_lens, kwargs_else, n_comp=20):
        """
        multi-gaussian lens model in convergence space

        :param kwargs_lens:
        :param n_comp:
        :return:
        """
        kwargs_lens_copy = copy.deepcopy(kwargs_lens)
        if 'center_x' in kwargs_lens_copy[0]:
            center_x = kwargs_lens_copy[0]['center_x']
            center_y = kwargs_lens_copy[0]['center_y']
        else:
            raise ValueError('no keyword center_x defined!')
        theta_E = self.LensModel.effective_einstein_radius(kwargs_lens, kwargs_else)
        r_array = np.logspace(-2, 1, 50) * theta_E
        lens_model_internal_bool = self.kwargs_options.get('lens_model_internal_bool', [True] * len(kwargs_lens))
        kappa_s = np.zeros_like(r_array)
        for i in range(len(kwargs_lens_copy)):
            if lens_model_internal_bool[i]:
                if 'center_x' in kwargs_lens_copy[0]:
                    kwargs_lens_copy[i]['center_x'] -= center_x
                    kwargs_lens_copy[i]['center_y'] -= center_y
                kappa_s += self.LensModel.kappa(r_array, np.zeros_like(r_array), kwargs_lens_copy, kwargs_else, k=i)
        amplitudes, sigmas, norm = mge.mge_1d(r_array, kappa_s, N=n_comp)
        return amplitudes, sigmas, center_x, center_y

    def flux_components(self, kwargs_light, n_grid=400, delta_grid=0.01, type="lens"):
        """
        computes the total flux in each component of the model

        :param kwargs_light:
        :param n_grid:
        :param delta_grid:
        :return:
        """
        flux_list = []
        R_h_list = []
        x_grid, y_grid = util.make_grid(numPix=n_grid, deltapix=delta_grid)
        kwargs_copy = copy.deepcopy(kwargs_light)
        for k, kwargs in enumerate(kwargs_light):
            kwargs_copy[k]['center_x'] = 0
            kwargs_copy[k]['center_y'] = 0
            if type == 'lens':
                light = self.LensLightModel.surface_brightness(x_grid, y_grid, kwargs_copy, k=k)
            elif type == 'source':
                light = self.SourceModel.surface_brightness(x_grid, y_grid, kwargs_copy, k=k)
            else:
                raise ValueError("type %s not supported!" % type)
            flux = np.sum(light)*delta_grid**2
            R_h = analysis_util.half_light_radius(light, x_grid, y_grid)
            flux_list.append(flux)
            R_h_list.append(R_h)
        return flux_list, R_h_list

    def buldge_disk_ratio(self, kwargs_buldge_disk):
        """
        computes the buldge-to-disk ratio of the luminosity
        :param kwargs_buldge_disk: kwargs of the buldge2disk function
        :return:
        """
        kwargs_bd = copy.deepcopy(kwargs_buldge_disk)
        kwargs_bd['center_x'] = 0
        kwargs_bd['center_y'] = 0
        deltaPix = 0.05
        numPix = 200
        x_grid, y_grid = util.make_grid(numPix, deltaPix)
        from lenstronomy.LightModel.Profiles.sersic import BuldgeDisk
        bd_class = BuldgeDisk()
        light_grid = bd_class.function(x_grid, y_grid, **kwargs_bd)
        light_tot = np.sum(light_grid)
        kwargs_bd['I0_d'] = 0
        light_grid = bd_class.function(x_grid, y_grid, **kwargs_bd)
        light_buldge = np.sum(light_grid)
        return light_tot, light_buldge

    def external_lensing_effect(self, kwargs_lens, kwargs_else):
        """
        computes deflection, shear and convergence at (0,0) for those part of the lens model not included in the main deflector

        :param kwargs_lens:
        :return:
        """
        alpha0_x, alpha0_y = 0, 0
        kappa_ext = 0
        shear1, shear2 = 0, 0
        lens_model_internal_bool = self.kwargs_options.get('lens_model_internal_bool', [True] * len(kwargs_lens))
        for i, kwargs in enumerate(kwargs_lens):
            if not lens_model_internal_bool[i]:
                f_x, f_y = self.LensModel.alpha(0, 0, kwargs_lens, kwargs_else, k=i)
                f_xx, f_yy, f_xy = self.LensModel.hessian(0, 0, kwargs_lens, kwargs_else, k=i)
                alpha0_x += f_x
                alpha0_y += f_y
                kappa_ext += (f_xx + f_yy)/2.
                shear1 += 1./2 * (f_xx - f_yy)
                shear2 += f_xy
        return alpha0_x, alpha0_y, kappa_ext, shear1, shear2
