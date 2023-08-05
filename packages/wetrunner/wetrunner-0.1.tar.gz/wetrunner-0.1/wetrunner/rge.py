"""Function to perform the RG evolution for Wilson coefficients of a given
sector."""


from wetrunner import evmat
from wetrunner.definitions import sectors
from collections import OrderedDict
import numpy as np


def run_sector(sector, C_in, Etas, Alphas, Alphaem, mb, mc, mtau, betas):
    args = Etas, Alphas, Alphaem, mb, mc, mtau, betas
    Cdictout = OrderedDict()
    for classname, C_lists in sectors[sector].items():
        for i, keylist in enumerate(C_lists):
            C_input = np.array([C_in.get(key, 0) for key in keylist])
            if np.count_nonzero(C_input) == 0 or classname == 'Vnu':
                # nothing to do for SM-like WCs or qqnunu operators
                C_result = C_input
            else:
                Us = getattr(evmat, 'Us' + classname)(*args)
                Ue = getattr(evmat, 'Ue' + classname)(*args)
                C_result = (Us + Ue) @ C_input
            for j in range(len(C_result)):
                Cdictout[keylist[j]] = C_result[j]
    return Cdictout
