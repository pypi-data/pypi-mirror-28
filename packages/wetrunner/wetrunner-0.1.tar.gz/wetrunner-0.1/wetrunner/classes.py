"""Defines the `WET` class that provides the main interface to the wetrunner
package."""


import wcxf
from wcxf.util import qcd
from wetrunner import rge, definitions
from wetrunner.parameters import p as default_parameters
from collections import OrderedDict


class WETrunner(object):
    """Class representing a point in Wilson coefficient space.

    Methods:

    - run: Evolve the Wilson coefficients to a different scale
    """

    def __init__(self, wc, parameters=None):
        """Initialize the instance.

        Parameters:

        - wc: instance of `wcxf.WC` representing Wilson coefficient values
          at a given (input) scale. The EFT must be one of `WET`, `WET-4`,
          or `WET-3`; the basis must be `Bern`.
        - parameters: optional. If provided, must be a dictionary containing
          values for the input parameters as defined in `wetrunner.parameters`.
          Default values are used for all parameters not provided.
        """
        assert isinstance(wc, wcxf.WC)
        assert wc.basis == 'Bern', \
            "Wilson coefficients must be given in the 'Bern' basis"
        self.eft = wc.eft
        # number of quark flavours
        if self.eft == 'WET':
            self.f = 5
        elif self.eft == 'WET-4':
            self.f = 4
        elif self.eft == 'WET-3':
            self.f = 3
        self.scale_in = wc.scale
        self.C_in = wc.dict
        self.parameters = default_parameters
        if parameters is not None:
            self.parameters.update(parameters)

    @staticmethod
    def _betas(f):
        """QCD beta function for `f` dynamical quark flavours."""
        return (11*3 - 2*f)/3

    def _get_running_parameters(self, scale, f):
        """Get the running parameters (e.g. quark masses and the strong
        coupling at a given scale."""
        p = {}
        p['alpha_s'] = qcd.alpha_s(scale, self.f, self.parameters['alpha_s'])
        p['m_b'] = qcd.m_b(self.parameters['m_b'], scale, self.f, self.parameters['alpha_s'])
        p['m_c'] = qcd.m_c(self.parameters['m_c'], scale, self.f, self.parameters['alpha_s'])
        # running ignored for alpha_e and lepton mass
        p['alpha_e'] = self.parameters['alpha_e']
        p['m_tau'] = self.parameters['m_tau']
        return p

    def run(self, scale_out, sectors='all'):
        """Evolve the Wilson coefficients to the scale `scale_out`.

        Parameters:

        - scale_out: output scale
        - sectors: optional. If provided, must be a tuple of strings
          corresponding to WCxf sector names. Only Wilson coefficients
          belonging to these sectors will be present in the output.

        Returns an instance of `wcxf.WC`.
        """
        p_i = self._get_running_parameters(self.scale_in, self.f)
        p_o = self._get_running_parameters(scale_out, self.f)
        betas = self._betas(self.f)
        Etas = (p_i['alpha_s'] / p_o['alpha_s'])
        if self.f != 5:  # for WET-4 and WET-3
            # to account for the fact that beta0 is hardcoded for f=5 in the
            # evolution matrices
            Etas = Etas**(self._betas(5) / self._betas(self.f))
            p_i['alpha_e'] = 0  # because QED evolution is not consistent yet
        if scale_out > self.scale_in:
            p_i['alpha_e'] = 0  # because QED evolution is not consistent yet
        C_out = OrderedDict()
        for sector in wcxf.EFT[self.eft].sectors:
            if sector in definitions.sectors:
                if sectors == 'all' or sector in sectors:
                    C_out.update(rge.run_sector(sector, self.C_in,
                                 Etas, p_i['alpha_s'], p_i['alpha_e'],
                                 p_i['m_b'], p_i['m_c'], p_i['m_tau'],
                                 betas))
        C_out = {k: v for k, v in C_out.items() if v != 0}
        return wcxf.WC(eft=self.eft, basis='Bern',
                       scale=scale_out,
                       values=wcxf.WC.dict2values(C_out))
