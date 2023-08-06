from lenstronomy.ImSim.psf_fitting import PSF_fitting
from lenstronomy.Workflow.fitting import Fitting
from lenstronomy.MCMC.alignment_matching import AlignmentFitting

class FittingSequence(object):
    """
    class to define a sequence of fitting applied, inherite the Fitting class
    """
    def __init__(self, kwargs_data, kwargs_psf, kwargs_options, kwargs_init, kwargs_sigma, kwargs_fixed, kwargs_lower, kwargs_upper):
        self.kwargs_data = kwargs_data
        self.kwargs_psf = kwargs_psf
        self.kwargs_options = kwargs_options
        self._lens_init, self._source_init, self._lens_light_init, self._else_init = kwargs_init
        self._lens_sigma, self._source_sigma, self._lens_light_sigma, self._else_sigma = kwargs_sigma
        self._lens_fixed, self._source_fixed, self._lens_light_fixed, self._else_fixed = kwargs_fixed

        self.fitting = Fitting(kwargs_data=kwargs_data, kwargs_psf=kwargs_psf, kwargs_fixed=kwargs_fixed, kwargs_lower=kwargs_lower, kwargs_upper=kwargs_upper)
        self.psf_iter = PSF_fitting()

    def fit_sequence(self, fitting_kwargs_list):
        """

        :param fitting_kwargs_list: list of kwargs specify the fitting routine to be executed
        :return:
        """
        chain_list = []
        param_list = []
        samples_mcmc, param_mcmc, dist_mcmc = [], [], []
        lens_temp, source_temp, lens_light_temp, else_temp = self._init_kwargs()
        for fitting_kwargs in fitting_kwargs_list:
            if fitting_kwargs['fitting_routine'] in ['MCMC', 'MCMC_source']:
                samples_mcmc, param_mcmc, dist_mcmc = self.mcmc(fitting_kwargs, lens_temp, source_temp, lens_light_temp, else_temp)
            else:
                lens_temp, source_temp, lens_light_temp, else_temp, chain, param = self.fit_single(fitting_kwargs,
                    lens_temp, source_temp, lens_light_temp, else_temp)
                chain_list.append(chain)
                param_list.append(param)
        return lens_temp, source_temp, lens_light_temp, else_temp, chain_list, param_list, samples_mcmc, param_mcmc, dist_mcmc

    def mcmc(self, fitting_kwargs, lens_input, source_input, lens_light_input, else_input):
        """

        :param fitting_kwargs:
        :param lens_input:
        :param source_input:
        :param lens_light_input:
        :param else_input:
        :return:
        """
        n_burn = fitting_kwargs['n_burn']
        n_run = fitting_kwargs['n_run']
        walkerRatio = fitting_kwargs['walkerRatio']
        mpi = fitting_kwargs.get('mpi', False)
        sigma_scale = fitting_kwargs['sigma_scale']
        lens_sigma, source_sigma, lens_light_sigma, else_sigma = self._sigma_kwargs()
        if fitting_kwargs['fitting_routine'] == 'MCMC':
            samples, param, dist = self.fitting.mcmc_run(self.kwargs_options,
                                  lens_input, source_input, lens_light_input, else_input,
                                  lens_sigma, source_sigma, lens_light_sigma, else_sigma,
                                  n_burn, n_run, walkerRatio, threadCount=1, mpi=mpi, init_samples=None, sigma_factor=sigma_scale)
        elif fitting_kwargs['fitting_routine'] == 'MCMC_source':
            samples, param, dist = self.fitting.mcmc_source(self.kwargs_options,
                                  lens_input, source_input, lens_light_input, else_input,
                                  lens_sigma, source_sigma, lens_light_sigma, else_sigma,
                                  n_burn, n_run, walkerRatio, threadCount=1, mpi=mpi, init_samples=None, sigma_factor=sigma_scale)
        else:
            raise ValueError("%s is not supported as a mcmc routine" % fitting_kwargs['fitting_routine'])
        return samples, param, dist

    def fit_single(self, fitting_kwargs, lens_input, source_input, lens_light_input, else_input):
        """

        :param fitting_kwargs:
        :param lens_input:
        :param source_input:
        :param lens_light_input:
        :param else_input:
        :return:
        """
        fitting_routine = fitting_kwargs['fitting_routine']
        mpi = fitting_kwargs.get('mpi', False)
        sigma_scale = fitting_kwargs.get('sigma_scale', 1)
        n_particles = fitting_kwargs.get('n_particles', 10)
        n_iterations = fitting_kwargs.get('n_iterations', 10)
        compute_bool = fitting_kwargs.get('compute_bands', [True]*len(self.kwargs_data))
        lens_sigma, source_sigma, lens_light_sigma, else_sigma = self._sigma_kwargs()

        if fitting_routine == 'lens_only':
            lens_result, source_result, lens_light_result, else_result, chain, param_list, _ = self.fitting.find_lens_only(
                self.kwargs_options, lens_input, source_input, lens_light_input, else_input,
                lens_sigma, source_sigma, lens_light_sigma, else_sigma,
                n_particles, n_iterations, mpi=mpi, sigma_factor=sigma_scale, compute_bool=compute_bool)
        elif fitting_routine == 'source_only':
            lens_result, source_result, lens_light_result, else_result, chain, param_list, _ = self.fitting.find_source_only(
                self.kwargs_options, lens_input, source_input, lens_light_input, else_input,
                lens_sigma, source_sigma, lens_light_sigma, else_sigma,
                n_particles, n_iterations, mpi=mpi, sigma_factor=sigma_scale, compute_bool=compute_bool)
        elif fitting_routine == 'lens_light_only':
            lens_result, source_result, lens_light_result, else_result, chain, param_list, _ = self.fitting.find_lens_light_only(
                self.kwargs_options, lens_input, source_input, lens_light_input, else_input,
                lens_sigma, source_sigma, lens_light_sigma, else_sigma,
                n_particles, n_iterations, mpi=mpi, sigma_factor=sigma_scale, compute_bool=compute_bool)
        elif fitting_routine == 'lens_fixed':
            lens_result, source_result, lens_light_result, else_result, chain, param_list, _ = self.fitting.find_fixed_lens(
                self.kwargs_options, lens_input, source_input, lens_light_input, else_input,
                lens_sigma, source_sigma, lens_light_sigma, else_sigma,
                n_particles, n_iterations, mpi=mpi, sigma_factor=sigma_scale, compute_bool=compute_bool)
        elif fitting_routine == 'lens_combined_gamma_fixed':
            lens_result, source_result, lens_light_result, else_result, chain, param_list, _ = self.fitting.find_lens_combined(
                self.kwargs_options, lens_input, source_input, lens_light_input, else_input,
                lens_sigma, source_sigma, lens_light_sigma, else_sigma,
                n_particles, n_iterations, mpi=mpi, sigma_factor=sigma_scale, gamma_fixed=True, compute_bool=compute_bool)
        elif fitting_routine == 'lens_combined':
            lens_result, source_result, lens_light_result, else_result, chain, param_list, _ = self.fitting.find_lens_combined(
                self.kwargs_options, lens_input, source_input, lens_light_input, else_input,
                lens_sigma, source_sigma, lens_light_sigma, else_sigma,
                n_particles, n_iterations, mpi=mpi, sigma_factor=sigma_scale, compute_bool=compute_bool)
        elif fitting_routine == 'psf_iteration':
            print('PSF fitting...')
            psf_iter_factor = fitting_kwargs['psf_iter_factor']
            psf_iter_num = fitting_kwargs['psf_iter_num']
            for i in range(len(self.kwargs_psf)):
                if compute_bool[i]:
                    psf_symmetry = self.kwargs_psf[i].get('psf_symmetry', 1)
                    self.kwargs_psf[i] = self.psf_iter.update_iterative(self.kwargs_data[i], self.kwargs_psf[i], self.kwargs_options, lens_input, source_input,
                                                                    lens_light_input, else_input, factor=psf_iter_factor, num_iter=psf_iter_num,
                                                   symmetry=psf_symmetry, verbose=False)
            lens_result, source_result, lens_light_result, else_result = lens_input, source_input, lens_light_input, else_input
            chain, param_list = [], []
            print('PSF fitting completed')
        elif fitting_routine == 'align_images':
            print('Align images...')
            lens_result, source_result, lens_light_result, else_result = lens_input, source_input, lens_light_input, else_input
            param_list = []
            alignmentFitting = AlignmentFitting(self.kwargs_data, self.kwargs_psf, self.kwargs_options, lens_input, source_input,
                                                                    lens_light_input, else_input, compute_bool=compute_bool)
            lowerLimit = fitting_kwargs.get('lower_limit_shift', -0.1)
            upperLimit = fitting_kwargs.get('upper_limit_shift', 0.1)
            self.kwargs_data, chain = alignmentFitting.pso(n_particles, n_iterations, lowerLimit, upperLimit, threadCount=1, mpi=mpi, print_key='Alignment fitting')
            self.fitting.kwargs_data = self.kwargs_data

        else:
            raise ValueError("%s is not a valid fitting routine" %fitting_routine)
        return lens_result, source_result, lens_light_result, else_result, chain, param_list

    def _init_kwargs(self):
        """

        :return: initial kwargs
        """
        return self._lens_init, self._source_init, self._lens_light_init, self._else_init

    def _sigma_kwargs(self):
        return self._lens_sigma, self._source_sigma, self._lens_light_sigma, self._else_sigma

    def _fixed_kwargs(self):
        return self._lens_fixed, self._source_fixed, self._lens_light_fixed, self._else_fixed