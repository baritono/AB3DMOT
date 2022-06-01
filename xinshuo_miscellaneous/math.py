import copy

import numpy as np

from xinshuo_miscellaneous.type_check import isscalar, isnparray


def safe_angle(input_angle, radian=False, warning=True, debug=True):
    '''
    make ensure the rotation is in [-180, 180] in degree
    parameters:
        input_angle:	an angle which is supposed to be in degree
        radian:			if True, the unit is replaced to radian instead of degree
    outputs:
        angle:			an angle in degree within (-180, 180]
    '''
    angle = copy.copy(input_angle)
    if debug:
        assert isscalar(angle), 'the input angle should be a scalar'

    if isnparray(angle): angle = angle[0]		# single numpy scalar value
    if radian:
        while angle > np.pi: angle -= np.pi
        while angle <= -np.pi: angle += np.pi
    else:
        while angle > 180: angle -= 360
        while angle <= -180: angle += 360

    return angle
