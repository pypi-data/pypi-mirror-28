__author__ = 'sibirrer'


from lenstronomy.LensModel.Profiles.p_jaffe import PJaffe

import numpy as np
import pytest

class TestP_JAFFW(object):
    """
    tests the Gaussian methods
    """
    def setup(self):
        self.profile = PJaffe()

    def test_function(self):
        x = np.array([1])
        y = np.array([2])
        sigma0 = 1.
        Ra, Rs = 0.5, 0.8
        values = self.profile.function(x, y, sigma0, Ra, Rs)
        assert values[0] == 0.87301557036070054
        x = np.array([0])
        y = np.array([0])
        sigma0 = 1.
        Ra, Rs = 0.5, 0.8
        values = self.profile.function(x, y, sigma0, Ra, Rs)
        assert values[0] == 0.20267440905756931

        x = np.array([2, 3, 4])
        y = np.array([1, 1, 1])
        values = self.profile.function( x, y, sigma0, Ra, Rs)
        assert values[0] == 0.87301557036070054
        assert values[1] == 1.0842781309377669
        assert values[2] == 1.2588604178849985

    def test_derivatives(self):
        x = np.array([1])
        y = np.array([2])
        sigma0 = 1.
        Ra, Rs = 0.5, 0.8
        f_x, f_y = self.profile.derivatives( x, y, sigma0, Ra, Rs)
        assert f_x[0] == 0.11542369603751264
        assert f_y[0] == 0.23084739207502528
        x = np.array([0])
        y = np.array([0])
        f_x, f_y = self.profile.derivatives( x, y, sigma0, Ra, Rs)
        assert f_x[0] == 0
        assert f_y[0] == 0

        x = np.array([1,3,4])
        y = np.array([2,1,1])
        values = self.profile.derivatives(x, y, sigma0, Ra, Rs)
        assert values[0][0] == 0.11542369603751264
        assert values[1][0] == 0.23084739207502528
        assert values[0][1] == 0.19172866612512479
        assert values[1][1] == 0.063909555375041588

    def test_hessian(self):
        x = np.array([1])
        y = np.array([2])
        sigma0 = 1.
        Ra, Rs = 0.5, 0.8
        f_xx, f_yy,f_xy = self.profile.hessian(x, y, sigma0, Ra, Rs)
        assert f_xx[0] == 0.077446121589827679
        assert f_yy[0] == -0.036486601753227141
        assert f_xy[0] == -0.075955148895369876
        x = np.array([1,3,4])
        y = np.array([2,1,1])
        values = self.profile.hessian(x, y, sigma0, Ra, Rs)
        assert values[0][0] == 0.077446121589827679
        assert values[1][0] == -0.036486601753227141
        assert values[2][0] == -0.075955148895369876
        assert values[0][1] == -0.037260794616683197
        assert values[1][1] == 0.052668405375961035
        assert values[2][1] == -0.033723449997241584


if __name__ == '__main__':
    pytest.main()