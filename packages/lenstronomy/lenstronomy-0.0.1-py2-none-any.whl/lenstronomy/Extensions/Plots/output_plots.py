import copy

import lenstronomy.Util.util as util
import lenstronomy.Util.mask as util_maskl
import corner
import matplotlib.pyplot as plt
import numpy as np
import scipy.ndimage as ndimage
from lenstronomy.LensModel.Profiles.external_shear import ExternalShear
from mpl_toolkits.axes_grid1 import make_axes_locatable

from lenstronomy.LensModel.lens_model_extensions import LensModelExtensions
from lenstronomy.ImSim.image_model import ImageModel
from lenstronomy.Data.coord_transforms import Coordinates


def text_description(ax, d, text, color='w', backgroundcolor='k', flipped=False):
    if flipped:
        ax.text(d - d / 40., d - d / 15., text, color=color, fontsize=15, backgroundcolor=backgroundcolor)
    else:
        ax.text(d / 40., d - d / 15., text, color=color, fontsize=15, backgroundcolor=backgroundcolor)


def scale_bar(ax, d, dist=1., text='1"', color='w', flipped=False):
    if flipped:
        p0 = d - d / 15. - dist
        p1 = d / 15.
        ax.plot([p0, p0 + dist], [p1, p1], linewidth=2, color=color)
        ax.text(p0 + dist / 2., p1 + 0.01 * d, text, fontsize=15, color=color, ha='center')
    else:
        p0 = d / 15.
        ax.plot([p0, p0 + dist], [p0, p0], linewidth=2, color=color)
        ax.text(p0 + dist / 2., p0 + 0.01 * d, text, fontsize=15, color=color, ha='center')


def coordinate_arrows(ax, d, coords, color='w', arrow_size=0.05):
    d0 = d / 8.
    p0 = d / 15.
    pt = d / 9.
    deltaPix = coords.pixel_size
    ra0, dec0 = coords.map_pix2coord((d - d0) / deltaPix, d0 / deltaPix)
    xx_, yy_ = coords.map_coord2pix(ra0, dec0)
    xx_ra, yy_ra = coords.map_coord2pix(ra0 - p0, dec0)
    xx_dec, yy_dec = coords.map_coord2pix(ra0, dec0 + p0)
    xx_ra_t, yy_ra_t = coords.map_coord2pix(ra0 - pt, dec0)
    xx_dec_t, yy_dec_t = coords.map_coord2pix(ra0, dec0 + pt)

    ax.arrow(xx_ * deltaPix, yy_ * deltaPix, (xx_ra - xx_) * deltaPix, (yy_ra - yy_) * deltaPix,
             head_width=arrow_size * d, head_length=arrow_size * d, fc=color, ec=color, linewidth=1)
    ax.text(xx_ra_t * deltaPix, yy_ra_t * deltaPix, "E", color=color, fontsize=15, ha='center')
    ax.arrow(xx_ * deltaPix, yy_ * deltaPix, (xx_dec - xx_) * deltaPix, (yy_dec - yy_) * deltaPix,
             head_width=arrow_size * d, head_length=arrow_size * d, fc
             =color, ec=color, linewidth=1)
    ax.text(xx_dec_t * deltaPix, yy_dec_t * deltaPix, "N", color=color, fontsize=15, ha='center')


def plot_line_set(ax, coords, ra_caustic_list, dec_caustic_list, color='g'):
    """

    :param coords:
    :return:
    """
    deltaPix = coords.pixel_size
    for i in range(len(ra_caustic_list)):
        x_c, y_c = coords.map_coord2pix(ra_caustic_list[i], dec_caustic_list[i])
        ax.plot((x_c + 0.5) * (deltaPix), (y_c + 0.5) * (deltaPix), color=color)
    return ax


def image_position_plot(ax, coords, kwargs_else):
    """

    :param ax:
    :param coords:
    :param kwargs_else:
    :return:
    """
    deltaPix = coords.pixel_size
    if 'ra_pos' in kwargs_else:
        x_image, y_image = coords.map_coord2pix(kwargs_else['ra_pos'], kwargs_else['dec_pos'])
        abc_list = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
        for i in range(len(x_image)):
            x_ = (x_image[i] + 0.5) * deltaPix
            y_ = (y_image[i] + 0.5) * deltaPix
            ax.plot(x_, y_, 'or')
            ax.text(x_, y_, abc_list[i], fontsize=20, color='k')
    return ax


def source_position_plot(ax, coords, kwargs_source):
    """

    :param ax:
    :param coords:
    :param kwargs_source:
    :return:
    """
    deltaPix = coords.pixel_size
    x_source, y_source = coords.map_coord2pix(kwargs_source[0]['center_x'], kwargs_source[0]['center_y'])
    ax.plot((x_source + 0.5) * deltaPix, (y_source + 0.5) * deltaPix, '*', markersize=10)
    return ax


class LensModelPlot(object):
    """
    class that manages the summary plots of a lens model
    """
    def __init__(self, kwargs_options, kwargs_data, kwargs_psf, kwargs_lens, kwargs_source, kwargs_lens_light, kwargs_else, arrow_size=0.1, cmap_string="gist_heat", high_res=5):
        """

        :param kwargs_options:
        :param kwargs_data:
        :param arrow_size:
        :param cmap_string:
        """
        self._kwargs_data = kwargs_data
        cmap = plt.get_cmap(cmap_string)
        cmap.set_bad(color='k', alpha=1.)
        cmap.set_under('k')
        self._cmap = cmap
        self._arrow_size = arrow_size

        nx, ny = np.shape(kwargs_data['image_data'])
        Mpix2coord = kwargs_data['transform_pix2angle']
        self._Mpix2coord = Mpix2coord
        self._coords = Coordinates(Mpix2coord, ra_at_xy_0=kwargs_data['ra_at_xy_0'], dec_at_xy_0=kwargs_data['dec_at_xy_0'])
        self._deltaPix = self._coords.pixel_size
        self._frame_size = self._deltaPix * nx

        self._x_grid, self._y_grid = kwargs_data['x_coords'], kwargs_data['y_coords']

        self._imageModel = ImageModel(kwargs_options=kwargs_options, kwargs_data=kwargs_data, kwargs_psf=kwargs_psf)
        self._lensModel = LensModelExtensions(lens_model_list=kwargs_options['lens_model_list'], foreground_shear=kwargs_options.get("foreground_shear", False))
        self._ra_crit_list, self._dec_crit_list, self._ra_caustic_list, self._dec_caustic_list = self._lensModel.critical_curve_caustics(kwargs_lens, kwargs_else, compute_window=self._frame_size, grid_scale=0.01)

        model, error_map, cov_param, param = self._imageModel.image_linear_solve(kwargs_lens, kwargs_source,
                                                                      kwargs_lens_light, kwargs_else, inv_bool=True)
        self._kwargs_lens = kwargs_lens
        self._kwargs_source = kwargs_source
        self._kwargs_lens_light = kwargs_lens_light
        self._kwargs_else = kwargs_else
        self._model = model
        self._data = kwargs_data['image_data']
        self._cov_param = cov_param
        self._norm_residuals = self._imageModel.Data.reduced_residuals(model, error_map=error_map)
        self._reduced_x2 = self._imageModel.Data.reduced_chi2(model, error_map=error_map)
        self._v_min_default = max(np.min(np.log10(model)), -5)
        self._v_max_default = min(np.max(np.log10(model)), 10)
        print("reduced chi^^ = ", self._reduced_x2)

    def data_plot(self, ax, v_min=None, v_max=None):
        """

        :param ax:
        :return:
        """
        if v_min is None:
            v_min = self._v_min_default
        if v_max is None:
            v_max = self._v_max_default
        im = ax.matshow(np.log10(self._data), origin='lower',
                        extent=[0, self._frame_size, 0, self._frame_size], cmap=self._cmap, vmin=v_min, vmax=v_max)  # , vmin=0, vmax=2

        ax.get_xaxis().set_visible(False)
        ax.get_yaxis().set_visible(False)
        ax.autoscale(False)

        scale_bar(ax, self._frame_size, dist=1, text='1"')
        text_description(ax, self._frame_size, text="Observed", color="w", backgroundcolor='k')
        coordinate_arrows(ax, self._frame_size, self._coords, arrow_size=self._arrow_size)
        divider = make_axes_locatable(ax)
        cax = divider.append_axes("right", size="5%", pad=0.05)
        cb = plt.colorbar(im, cax=cax)
        cb.set_label(r'log$_{10}$ flux', fontsize=15)
        return ax

    def model_plot(self, ax, v_min=None, v_max=None):
        """

        :param ax:
        :param model:
        :param v_min:
        :param v_max:
        :return:
        """
        if v_min is None:
            v_min = self._v_min_default
        if v_max is None:
            v_max = self._v_max_default
        im = ax.matshow(np.log10(self._model), origin='lower', vmin=v_min, vmax=v_max,
                        extent=[0, self._frame_size, 0, self._frame_size], cmap=self._cmap)
        ax.get_xaxis().set_visible(False)
        ax.get_yaxis().set_visible(False)
        ax.autoscale(False)
        scale_bar(ax, self._frame_size, dist=1, text='1"')
        text_description(ax, self._frame_size, text="Reconstructed", color="w", backgroundcolor='k')
        coordinate_arrows(ax, self._frame_size, self._coords, arrow_size=self._arrow_size)
        divider = make_axes_locatable(ax)
        cax = divider.append_axes("right", size="5%", pad=0.05)
        cb = plt.colorbar(im, cax=cax)
        cb.set_label(r'log$_{10}$ flux', fontsize=15)

        plot_line_set(ax, self._coords, self._ra_caustic_list, self._dec_caustic_list, color='b')
        plot_line_set(ax, self._coords, self._ra_crit_list, self._dec_crit_list, color='r')
        image_position_plot(ax, self._coords, self._kwargs_else)
        source_position_plot(ax, self._coords, self._kwargs_source)

    def convergence_plot(self, ax, v_min=None, v_max=None):
        """

        :param x_grid:
        :param y_grid:
        :param kwargs_lens:
        :param kwargs_else:
        :return:
        """
        kappa_result = util.array2image(self._lensModel.kappa(self._x_grid, self._y_grid, self._kwargs_lens, self._kwargs_else))
        im = ax.matshow(np.log10(kappa_result), origin='lower',
                        extent=[0, self._frame_size, 0, self._frame_size], cmap=self._cmap, vmin=v_min, vmax=v_max)
        ax.get_xaxis().set_visible(False)
        ax.get_yaxis().set_visible(False)
        ax.autoscale(False)
        scale_bar(ax, self._frame_size, dist=1, text='1"', color='w')
        coordinate_arrows(ax, self._frame_size, self._coords, color='w', arrow_size=self._arrow_size)
        text_description(ax, self._frame_size, text="Convergence", color="w", backgroundcolor='k', flipped=False)
        divider = make_axes_locatable(ax)
        cax = divider.append_axes("right", size="5%", pad=0.05)
        cb = plt.colorbar(im, cax=cax)
        cb.set_label(r'log$_{10}$ $\kappa$', fontsize=15)
        return ax

    def normalized_residual_plot(self, ax, v_min=-6, v_max=6):
        """

        :param ax:
        :param residuals:
        :return:
        """
        im = ax.matshow(self._norm_residuals, vmin=v_min, vmax=v_max,
                        extent=[0, self._frame_size, 0, self._frame_size], cmap='bwr', origin='lower')
        ax.get_xaxis().set_visible(False)
        ax.get_yaxis().set_visible(False)
        ax.autoscale(False)
        scale_bar(ax, self._frame_size, dist=1, text='1"', color='k')
        text_description(ax, self._frame_size, text="Normalized Residuals", color="k", backgroundcolor='w')
        coordinate_arrows(ax, self._frame_size, self._coords, color='k', arrow_size=self._arrow_size)
        divider = make_axes_locatable(ax)
        cax = divider.append_axes("right", size="5%", pad=0.05)
        cb = plt.colorbar(im, cax=cax)
        cb.set_label(r'(f$_{model}$-f$_{data}$)/$\sigma$', fontsize=15)
        return ax

    def absolute_residual_plot(self, ax, v_min=-1, v_max=1):
        """

        :param ax:
        :param residuals:
        :return:
        """
        im = ax.matshow(self._model - self._data, vmin=v_min, vmax=v_max,
                        extent=[0, self._frame_size, 0, self._frame_size], cmap='bwr', origin='lower')
        ax.get_xaxis().set_visible(False)
        ax.get_yaxis().set_visible(False)
        ax.autoscale(False)
        scale_bar(ax, self._frame_size, dist=1, text='1"', color='k')
        text_description(ax, self._frame_size, text="Residuals", color="k", backgroundcolor='w')
        coordinate_arrows(ax, self._frame_size, self._coords, color='k', arrow_size=self._arrow_size)
        divider = make_axes_locatable(ax)
        cax = divider.append_axes("right", size="5%", pad=0.05)
        cb = plt.colorbar(im, cax=cax)
        cb.set_label(r'(f$_{model}$-f$_{data}$)', fontsize=15)
        return ax

    def source_plot(self, ax, numPix, deltaPix_source, source_sigma=0.001, convolution=False, v_min=None, v_max=None):
        """

        :param ax:
        :param coords_source:
        :param source:
        :return:
        """
        if v_min is None:
            v_min = self._v_min_default
        if v_max is None:
            v_max = self._v_max_default
        d_s = numPix * deltaPix_source
        x_grid_source, y_grid_source = util.make_grid_transformed(numPix,
                                                                  self._Mpix2coord * deltaPix_source / self._deltaPix)
        x_center = self._kwargs_source[0]['center_x']
        y_center = self._kwargs_source[0]['center_y']
        x_grid_source += x_center
        y_grid_source += y_center
        coords_source = Coordinates(self._Mpix2coord * deltaPix_source / self._deltaPix, ra_at_xy_0=x_grid_source[0],
                                    dec_at_xy_0=y_grid_source[0])

        source = self._imageModel.SourceModel.surface_brightness(x_grid_source, y_grid_source, self._kwargs_source)
        source = util.array2image(source)
        if convolution:
            source = ndimage.filters.gaussian_filter(source, sigma=source_sigma / deltaPix_source, mode='nearest',
                                                      truncate=20)

        im = ax.matshow(np.log10(source), origin='lower', extent=[0, d_s, 0, d_s],
                        cmap=self._cmap, vmin=v_min, vmax=v_max)  # source
        ax.get_xaxis().set_visible(False)
        ax.get_yaxis().set_visible(False)
        ax.autoscale(False)
        divider = make_axes_locatable(ax)
        cax = divider.append_axes("right", size="5%", pad=0.05)
        cb = plt.colorbar(im, cax=cax)
        cb.set_label(r'log$_{10}$ flux', fontsize=15)
        plot_line_set(ax, coords_source, self._ra_caustic_list, self._dec_caustic_list, color='b')
        scale_bar(ax, d_s, dist=0.1, text='0.1"', color='w', flipped=False)
        coordinate_arrows(ax, d_s, coords_source, arrow_size=self._arrow_size, color='w')
        text_description(ax, d_s, text="Reconstructed source", color="w", backgroundcolor='k', flipped=False)
        source_position_plot(ax, coords_source, self._kwargs_source)
        return ax

    def error_map_source_plot(self, ax, numPix, deltaPix_source, v_min=None, v_max=None):
        x_grid_source, y_grid_source = util.make_grid_transformed(numPix,
                                                                  self._Mpix2coord * deltaPix_source / self._deltaPix)
        x_center = self._kwargs_source[0]['center_x']
        y_center = self._kwargs_source[0]['center_y']
        x_grid_source += x_center
        y_grid_source += y_center
        coords_source = Coordinates(self._Mpix2coord * deltaPix_source / self._deltaPix, ra_at_xy_0=x_grid_source[0],
                                    dec_at_xy_0=y_grid_source[0])
        error_map_source = self._imageModel.error_map_source(self._kwargs_source, x_grid_source, y_grid_source, self._cov_param)
        error_map_source = util.array2image(error_map_source)
        d_s = numPix * deltaPix_source
        im = ax.matshow(error_map_source, origin='lower', extent=[0, d_s, 0, d_s],
                        cmap=self._cmap, vmin=v_min, vmax=v_max)  # source
        ax.get_xaxis().set_visible(False)
        ax.get_yaxis().set_visible(False)
        ax.autoscale(False)
        divider = make_axes_locatable(ax)
        cax = divider.append_axes("right", size="5%", pad=0.05)
        cb = plt.colorbar(im, cax=cax)
        cb.set_label(r'error variance', fontsize=15)
        plot_line_set(ax, coords_source, self._ra_caustic_list, self._dec_caustic_list, color='b')
        scale_bar(ax, d_s, dist=0.1, text='0.1"', color='w', flipped=False)
        coordinate_arrows(ax, d_s, coords_source, arrow_size=self._arrow_size, color='w')
        text_description(ax, d_s, text="Error map in source", color="w", backgroundcolor='k', flipped=False)
        source_position_plot(ax, coords_source, self._kwargs_source)
        return ax

    def magnification_plot(self, ax, v_min=-10, v_max=10):
        """

        :param ax:
        :return:
        """
        mag_result = util.array2image(self._lensModel.magnification(self._x_grid, self._y_grid, self._kwargs_lens, self._kwargs_else))
        im = ax.matshow(mag_result, origin='lower', extent=[0, self._frame_size, 0, self._frame_size],
                        vmin=v_min, vmax=v_max, cmap=self._cmap, alpha=0.5)
        ax.get_xaxis().set_visible(False)
        ax.get_yaxis().set_visible(False)
        ax.autoscale(False)
        scale_bar(ax, self._frame_size, dist=1, text='1"', color='k')
        coordinate_arrows(ax, self._frame_size, self._coords, color='k', arrow_size=self._arrow_size)
        text_description(ax, self._frame_size, text="Magnification model", color="k", backgroundcolor='w')
        divider = make_axes_locatable(ax)
        cax = divider.append_axes("right", size="5%", pad=0.05)
        cb = plt.colorbar(im, cax=cax)
        cb.set_label(r'det(A$^{-1}$)', fontsize=15)

        plot_line_set(ax, self._coords, self._ra_caustic_list, self._dec_caustic_list, color='b')
        plot_line_set(ax, self._coords, self._ra_crit_list, self._dec_crit_list, color='r')
        image_position_plot(ax, self._coords, self._kwargs_else)
        source_position_plot(ax, self._coords, self._kwargs_source)
        return ax

    def decomposition_plot(self, ax, text='Reconstructed', v_min=None, v_max=None, unconvolved=False, point_source_add=False, source_add=False, lens_light_add=False):

        model, _ = self._imageModel.image_with_params(self._kwargs_lens, self._kwargs_source, self._kwargs_lens_light,
                                                    self._kwargs_else, unconvolved=unconvolved, source_add=source_add,
                                                    lens_light_add=lens_light_add, point_source_add=point_source_add)
        if v_min is None:
            v_min = self._v_min_default
        if v_max is None:
            v_max = self._v_max_default
        im = ax.matshow(np.log10(model), origin='lower', vmin=v_min, vmax=v_max,
                        extent=[0, self._frame_size, 0, self._frame_size], cmap=self._cmap)
        ax.get_xaxis().set_visible(False)
        ax.get_yaxis().set_visible(False)
        ax.autoscale(False)
        scale_bar(ax, self._frame_size, dist=1, text='1"')
        text_description(ax, self._frame_size, text=text, color="w", backgroundcolor='k')
        coordinate_arrows(ax, self._frame_size, self._coords, arrow_size=self._arrow_size)
        divider = make_axes_locatable(ax)
        cax = divider.append_axes("right", size="5%", pad=0.05)
        cb = plt.colorbar(im, cax=cax)
        cb.set_label(r'log$_{10}$ flux', fontsize=15)
        return ax

    def subtract_from_data_plot(self, ax, text='Subtracted', v_min=None, v_max=None, point_source_add=False, source_add=False, lens_light_add=False):
        model, _ = self._imageModel.image_with_params(self._kwargs_lens, self._kwargs_source, self._kwargs_lens_light,
                                                    self._kwargs_else, unconvolved=False, source_add=source_add,
                                                    lens_light_add=lens_light_add, point_source_add=point_source_add)
        if v_min is None:
            v_min = self._v_min_default
        if v_max is None:
            v_max = self._v_max_default
        im = ax.matshow(np.log10(self._data - model), origin='lower', vmin=v_min, vmax=v_max,
                        extent=[0, self._frame_size, 0, self._frame_size], cmap=self._cmap)
        ax.get_xaxis().set_visible(False)
        ax.get_yaxis().set_visible(False)
        ax.autoscale(False)
        scale_bar(ax, self._frame_size, dist=1, text='1"')
        text_description(ax, self._frame_size, text=text, color="w", backgroundcolor='k')
        coordinate_arrows(ax, self._frame_size, self._coords, arrow_size=self._arrow_size)
        divider = make_axes_locatable(ax)
        cax = divider.append_axes("right", size="5%", pad=0.05)
        cb = plt.colorbar(im, cax=cax)
        cb.set_label(r'log$_{10}$ flux', fontsize=15)
        return ax


def plot_chain(chain, param_list):
    X2_list, pos_list, vel_list, _ = chain

    f, axes = plt.subplots(1, 3, figsize=(18, 6), sharex=False, sharey=False)
    ax = axes[0]
    ax.plot(np.log10(-np.array(X2_list)))
    ax.set_title('-logL')

    ax = axes[1]
    pos = np.array(pos_list)
    vel = np.array(vel_list)
    n_iter = len(pos)
    plt.figure()
    for i in range(0,len(pos[0])):
        ax.plot((pos[:,i]-pos[n_iter-1,i]),label=param_list[i])
    ax.set_title('particle position')
    ax.legend()

    ax = axes[2]
    for i in range(0,len(vel[0])):
        ax.plot(vel[:,i], label=param_list[i])
    ax.set_title('param velocity')
    ax.legend()
    plt.show()
    return f, axes


def ext_shear_direction(kwargs_data, kwargs_options, kwargs_lens,
                        kwargs_else, strength_multiply=10):
    """

    :param kwargs_data:
    :param kwargs_psf:
    :param kwargs_options:
    :param lens_result:
    :param source_result:
    :param lens_light_result:
    :param else_result:
    :return:
    """
    foreground_shear = kwargs_options.get('foreground_shear', False)
    x_grid, y_grid = kwargs_data['x_coords'], kwargs_data['y_coords']
    shear = ExternalShear()

    if not 'EXTERNAL_SHEAR' in kwargs_options['lens_model_list']:
        f_x_shear, f_y_shear = 0, 0
    else:
        for i, lens_model in enumerate(kwargs_options['lens_model_list']):
            if lens_model == 'EXTERNAL_SHEAR':
                kwargs = kwargs_lens[i]
                f_x_shear, f_y_shear = shear.derivatives(x_grid, y_grid, e1=kwargs['e1'] * strength_multiply,
                                                         e2=kwargs['e2'] * strength_multiply)
    x_shear = x_grid - f_x_shear
    y_shear = y_grid - f_y_shear

    if foreground_shear:
        f_x_shear1, f_y_shear1 = shear.derivatives(x_grid, y_grid, e1=kwargs_else['gamma1_foreground']*strength_multiply, e2=kwargs_else['gamma2_foreground']*strength_multiply)
    else:
        f_x_shear1, f_y_shear1 = 0, 0
    x_foreground = x_grid - f_x_shear1
    y_foreground = y_grid - f_y_shear1

    center_x = np.mean(x_grid)
    center_y = np.mean(y_grid)
    radius = (np.max(x_grid) - np.min(x_grid))/4
    circle_shear = util_maskl.mask_sphere(x_shear, y_shear, center_x, center_y, radius)
    circle_foreground = util_maskl.mask_sphere(x_foreground, y_foreground, center_x, center_y, radius)
    f, ax = plt.subplots(1, 1, figsize=(16, 8), sharex=False, sharey=False)
    im = ax.matshow(util.array2image(np.log10(kwargs_data['image_data'])), origin='lower', alpha=0.5)
    im = ax.matshow(util.array2image(circle_shear), origin='lower', alpha=0.5, cmap="jet")
    im = ax.matshow(util.array2image(circle_foreground), origin='lower', alpha=0.5)
    #f.show()
    return f, ax


def psf_iteration_compare(kwargs_psf):
    """

    :param kwargs_psf:
    :return:
    """
    psf_out = kwargs_psf['kernel_point_source']
    psf_in = kwargs_psf['kernel_point_source_init']
    n_kernel = len(psf_in)
    delta_x = n_kernel/20.
    delta_y = n_kernel/10.
    cmap_kernel = 'seismic'

    f, axes = plt.subplots(1, 3, figsize=(15, 5), sharex=False, sharey=False)
    ax = axes[0]
    im = ax.matshow(np.log10(psf_in), origin='lower', cmap=cmap_kernel)
    v_min, v_max = im.get_clim()
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="5%", pad=0.05)
    plt.colorbar(im, cax=cax)
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)
    ax.text(delta_x, n_kernel-delta_y, "stacked stars", color="k", fontsize=20, backgroundcolor='w')

    ax = axes[1]
    im = ax.matshow(np.log10(psf_out), origin='lower', vmin=v_min, vmax=v_max, cmap=cmap_kernel)
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="5%", pad=0.05)
    plt.colorbar(im, cax=cax)
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)
    ax.text(delta_x, n_kernel-delta_y, "iterative reconstruction", color="k", fontsize=20, backgroundcolor='w')

    ax = axes[2]
    im = ax.matshow(psf_out-psf_in, origin='lower', vmin=-10**-3, vmax=10**-3, cmap=cmap_kernel)
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="5%", pad=0.05)
    plt.colorbar(im, cax=cax)
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)
    ax.text(delta_x, n_kernel-delta_y, "difference", color="k", fontsize=20, backgroundcolor='w')
    f.tight_layout()
    return f, axes


def mcmc_output(samples_mcmc, param_mcmc, fitting_kwargs_list, truths=None):
    """

    :param samples_mcmc:
    :param param_mcmc:
    :param kwargs_fitting_mcmc:
    :return:
    """
    plot = corner.corner(samples_mcmc, labels=param_mcmc, truths=truths)

    fitting_kwargs_mcmc = fitting_kwargs_list[-1]
    n_run = fitting_kwargs_mcmc['n_run']
    walkerRatio = fitting_kwargs_mcmc['walkerRatio']
    numParam = len(param_mcmc)
    numWalkers = numParam*walkerRatio
    x_axis = np.linspace(1,n_run, n_run)
    means = np.zeros((n_run, numParam))
    for i in range(0, n_run):
        means[i] = np.mean(samples_mcmc[:][numWalkers*i:numWalkers*(i+1)], axis=0)
    f, axes = plt.subplots(1, 1, figsize=(8, 8), sharex=False, sharey=False)
    ax = axes
    for i in range(0,numParam):
        ax.plot(x_axis, means.T[i]/means.T[i][-1], label=param_mcmc[i])
    ax.legend()
    return plot, f
