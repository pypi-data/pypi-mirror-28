__author__ = 'sibirrer'

import numpy as np
from lenstronomy.LensModel.lens_model import LensModel
from lenstronomy.LensModel.Solver.lens_equation_solver import LensEquationSolver
from lenstronomy.LensModel.Solver.solver2point import Solver2Point
from lenstronomy.LensModel.Solver.solver4point import Solver4Point
from lenstronomy.Workflow.else_param import ElseParam
from lenstronomy.Workflow.lens_param import LensParam
from lenstronomy.Workflow.light_param import LightParam


class Param(object):
    """
    this class contains routines to deal with the number of parameters given certain options in a config file

    rule: first come the lens parameters, than the source parameters, psf parameters and at the end (if needed) some more

    list of parameters
    Gaussian: amp, sigma_x, sigma_y (center_x, center_y as options)
    NFW: to do
    SIS:  phi_E, (center_x, center_y as options)
    SPEMD: to do
    SPEP:  phi_E,gamma,q,phi_G, (center_x, center_y as options)
    """

    def __init__(self, kwargs_options, kwargs_fixed_lens, kwargs_fixed_source, kwargs_fixed_lens_light, kwargs_fixed_else):
        """

        :return:
        """
        self.kwargs_fixed_lens = kwargs_fixed_lens
        self.kwargs_fixed_source = kwargs_fixed_source
        self.kwargs_fixed_lens_light = kwargs_fixed_lens_light
        self.kwargs_fixed_else = kwargs_fixed_else
        self.kwargs_options = kwargs_options
        self.lensModel = LensModel(lens_model_list=kwargs_options['lens_model_list'])
        self.ImagePosition = LensEquationSolver(lensModel=self.lensModel)

        if 'FOREGROUND_SHEAR' in kwargs_options['lens_model_list']:
            decoupling = False
        else:
            decoupling = True
        self._num_images = kwargs_options.get('num_point_sources', 0)

        self._fix_mass2light = kwargs_options.get('mass2light_fixed', False)
        self._fix_magnification = kwargs_options.get('fix_magnification', False)
        self._additional_images = kwargs_options.get('additional_images', False)
        if kwargs_options.get('solver', False):
            self.solver_type = kwargs_options.get('solver_type', 'NONE')
            if self._num_images == 4:
                self.solver4points = Solver4Point(self.lensModel, decoupling=decoupling)
            elif self. _num_images == 2:
                self.solver2points = Solver2Point(self.lensModel, decoupling=decoupling, solver_type=self.solver_type)
            else:
                raise ValueError("%s number of images is not valid. Use 2 or 4!" % self._num_images)
        else:
            self.solver_type = "NONE"
        self.lensParams = LensParam(kwargs_options, kwargs_fixed_lens)
        self.souceParams = LightParam(kwargs_options, kwargs_fixed_source, type='source_light')
        self.lensLightParams = LightParam(kwargs_options, kwargs_fixed_lens_light, type='lens_light')
        self.elseParams = ElseParam(kwargs_options, kwargs_fixed_else)

    def getParams(self, args):
        """

        :param args: tuple of parameter values (float, strings, ...(
        :return: keyword arguments sorted
        """
        i = 0
        kwargs_lens, i = self.lensParams.getParams(args, i)
        kwargs_source, i = self.souceParams.getParams(args, i)
        kwargs_lens_light, i = self.lensLightParams.getParams(args, i)
        kwargs_else, i = self.elseParams.getParams(args, i)
        return kwargs_lens, kwargs_source, kwargs_lens_light, kwargs_else

    def setParams(self, kwargs_lens, kwargs_source, kwargs_lens_light, kwargs_else, bounds=None):
        """
        inverse of getParam function
        :param kwargs_lens: keyword arguments depending on model options
        :param kwargs_source: keyword arguments depending on model options
        :return: tuple of parameters
        """
        args = self.lensParams.setParams(kwargs_lens, bounds=bounds)
        args += self.souceParams.setParams(kwargs_source, bounds=bounds)
        args += self.lensLightParams.setParams(kwargs_lens_light, bounds=bounds)
        args += self.elseParams.setParams(kwargs_else)
        return args

    def param_init(self, kwarg_mean_lens, kwarg_mean_source, kwarg_mean_lens_light, kwarg_mean_else):
        """
        returns upper and lower bounds on the parameters used in the X2_chain function for MCMC/PSO starting
        bounds are defined relative to the catalogue level image called in the class Data
        might be migrated to the param class
        """
        #inizialize mean and sigma limit arrays
        mean, sigma = self.lensParams.param_init(kwarg_mean_lens)
        _mean, _sigma = self.souceParams.param_init(kwarg_mean_source)
        mean += _mean
        sigma += _sigma
        _mean, _sigma = self.lensLightParams.param_init(kwarg_mean_lens_light)
        mean += _mean
        sigma += _sigma
        _mean, _sigma = self.elseParams.param_init(kwarg_mean_else)
        mean += _mean
        sigma += _sigma
        return mean, sigma

    def num_param(self):
        """

        :return: number of parameters involved (int)
        """
        num, list = self.lensParams.num_param()
        _num, _list = self.souceParams.num_param()
        num += _num
        list += _list
        _num, _list = self.lensLightParams.num_param()
        num += _num
        list += _list
        _num, _list = self.elseParams.num_param()
        num += _num
        list += _list
        return num, list

    def _update_mass2ligth(self, kwargs_lens, kwargs_else):
        """
        updates the lens models with an additional multiplicative factor to convert light profiles into mass profiles
        ATTENTION: this makes only sense when the original parameters of the LENS model were derived from a LIGHTMODEL
        :param kwargs_lens:
        :param mass2light:
        :return:
        """
        if not self._fix_mass2light:
            return kwargs_lens
        mass2light = kwargs_else['mass2light']
        lens_model_list = self.kwargs_options['lens_model_list']
        for i, lens_model in enumerate(lens_model_list):
            if lens_model in ['HERNQUIST', 'PJAFFE', 'PJAFFE_ELLIPSE', 'HERNQUIST_ELLIPSE']:
                if 'sigma0' in self.kwargs_fixed_lens[i]:
                    kwargs_lens[i]['sigma0'] = self.kwargs_fixed_lens[i]['sigma0'] * mass2light
            elif lens_model in ['SIS', 'SIE', 'SPEP', 'SPEMD', 'SPEMD_SMOOTH']:
                if 'theta_E' in self.kwargs_fixed_lens[i]:
                    kwargs_lens[i]['theta_E'] = self.kwargs_fixed_lens[i]['theta_E'] * mass2light
        return kwargs_lens

    def _update_magnification(self, kwargs_lens, kwargs_else):
        """
        updates point source amplitude to relative magnifications
        :param kwargs_lens:
        :param kwargs_else:
        :return:
        """
        mag = self.lensModel.magnification(kwargs_else['ra_pos'], kwargs_else['dec_pos'], kwargs_lens)
        kwargs_else['point_amp'] = np.abs(mag)
        return kwargs_else

    def get_all_params(self, args):
        kwargs_lens, kwargs_source, kwargs_lens_light, kwargs_else = self.getParams(args)
        if self._fix_mass2light:
            kwargs_lens = self._update_mass2ligth(kwargs_lens, kwargs_else)
        kwargs_lens, kwargs_source, kwargs_lens_light, kwargs_else = self.update_kwargs(kwargs_lens, kwargs_source, kwargs_lens_light, kwargs_else)
        if self._additional_images:
            kwargs_else = self.update_image_positions(kwargs_lens, kwargs_source, kwargs_else)
        if self._fix_magnification:
            kwargs_else = self._update_magnification(kwargs_lens, kwargs_else)
        return kwargs_lens, kwargs_source, kwargs_lens_light, kwargs_else

    def update_image_positions(self, kwargs_lens, kwargs_source, kwargs_else):
        """

        :param kwargs_else:
        :return:
        """
        if 'center_x' in kwargs_source[0]:
            sourcePos_x = kwargs_source[0]['center_x']
            sourcePos_y = kwargs_source[0]['center_y']
            min_distance = 0.05
            search_window = 10
            x_pos, y_pos = self.ImagePosition.image_position_from_source(sourcePos_x, sourcePos_y, kwargs_lens, min_distance=min_distance, search_window=search_window)
            kwargs_else['ra_pos'] = x_pos
            kwargs_else['dec_pos'] = y_pos
        else:
            raise ValueError('To compute the image positions, the kwargs_source requires positional information!')
        return kwargs_else

    def update_kwargs(self, kwargs_lens_list, kwargs_source_list, kwargs_lens_light, kwargs_else):
        if self.kwargs_options.get('solver', False):
            x_, y_ = kwargs_else['ra_pos'], kwargs_else['dec_pos']
            if self._num_images == 4:
                kwargs_lens_list = self.solver4points.constraint_lensmodel(x_, y_, kwargs_lens_list)
            elif self._num_images == 2:
                kwargs_lens_list = self.solver2points.constraint_lensmodel(x_, y_, kwargs_lens_list)
            else:
                raise ValueError("%s number of images is not valid. Use 2 or 4!" % self._num_images)

        if self.kwargs_options.get('image_plane_source', False):
            x_mapped, y_mapped = self.lensModel.ray_shooting(kwargs_else['ra_pos'], kwargs_else['dec_pos'], kwargs_lens_list)
            for i, kwargs_source in enumerate(kwargs_source_list):
                kwargs_source_list[i]['center_x'] = x_mapped[i]
                kwargs_source_list[i]['center_y'] = y_mapped[i]
        if self.kwargs_options.get('solver', False):
            x_mapped, y_mapped = self.lensModel.ray_shooting(kwargs_else['ra_pos'], kwargs_else['dec_pos'], kwargs_lens_list)
            if 'center_x' in kwargs_source_list[0]:
                kwargs_source_list[0]['center_x'] = np.mean(x_mapped)
                kwargs_source_list[0]['center_y'] = np.mean(y_mapped)
        if self.kwargs_options.get('joint_center_source'):
            for i in range(1, len(kwargs_source_list)):
                kwargs_source_list[i]['center_x'] = kwargs_source_list[0]['center_x']
                kwargs_source_list[i]['center_y'] = kwargs_source_list[0]['center_y']

        return kwargs_lens_list, kwargs_source_list, kwargs_lens_light, kwargs_else
