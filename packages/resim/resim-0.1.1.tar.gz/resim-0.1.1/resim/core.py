"""ReSim: chemoREsistance SIMulator

ReSim (chemoREsistance SIMulator) simulates cancer chemoresistance dynamics
based on a stochastic model. The model describes the interaction between
chemotherapeutics and various cancer cell subpopulations (including sensitive,
primary resistant, acquired resistant and quiescent cancer cells).

Examples:
    minimal setup using default parameters:
        >>>  import resim
        >>>  model = resim.Simulator()
        >>>  res = model.simulate()

    set your own params:
        >>>  model = resim.Simulator(gr=[0.02, 0.1, 0.1])
    or
        >>>  model = resim.Simulator()
        >>>  model.set_param_gr([0.02, 0.1, 0.1])
    or
        >>>  model = resim.Simulator()
        >>>  model.gr_s = 0.02
        >>>  model.gr_pr = 0.1
    Please set t using set_param_t instead of assign directly to model.t.

Attribute:
    sig (int): calibrated diffusion constant for the set of stochastic differential equations.
    ccmax (float): tumor carrying capacity (10^8).

Todo:
    1. Add class methods for conventional first-line/second-line chemos in HCC,
    PC.
    2. Add tool for converting tumor's diameter/volume to number of cells.
    3. Add tool for converting doubling time to growth rate.
    4. Add tool for converting half-life to k.
    5. Integrate parallel programming sde solver module (nsim) to speed up the
    computation.

"""

#import warnings; warnings.simplefilter('ignore')
import numpy as np
import pandas as pd
import sdeint

sig = 0.01
ccmax = 500

class Simulator:
    """ReSim Simulator Class"""
    def __init__(self,
            gr = [0.015, 0.015, 0.015],
            k = [1e-6, 1e-4, 5e-4, 1e-6, 5e-4, 1e-6, 5e-4, 5e-4, 5e-4, 5e-4],
            d = [10, 10, 240, 0.9, 0.7],
            init = [0.42, 0.05, 0, 0.03, 0],
            t = 365, n = 50):

        """set Simulator attributes.

        Args:
            gr (list of floats) : growth rate of cancer cells (gr_s, gr_pr,
                gr_ar).
            k (list of floats) : kinetic constants (ks_pr, ks_ar, ks_q, kpr_s,
                kpr_q, kar_s, kar_q, kq_s, kq_pr, kq_ar).
            d (list of floats) : drug related constants (ki, qf, dose, dsmax,
                ke).
            init (list of floats) : initial states (s, pr, ar, q, d)
            t (int) : simulation time frame in days e.g. 365d = 1y.
            n (int) : number of iterations, repeat simulation n times.

        """

        self._set_param(gr, k, d, init, t, n)

    def _set_param(self, gr, k, d, init, t, n):
        """Private Simulator attributes setter"""
        self.set_param_gr(gr)
        self.set_param_k(k)
        self.set_param_d(d)
        self.set_param_t(t)
        self.init = np.array(init)
        self.n = n
        self._ccmax = ccmax
        self._sig = sig

    def set_param_gr(self, gr):
        """Set growth rates

        Args:
            gr (list of floats) : growth rate of cancer cells (gr_s, gr_pr,
                gr_ar).

        Raises:
            ValueError: if gr length not equal to 3.
            ValueError: if any elements in gr smaller than 0.
        """
        if len(gr) != 3:
            raise ValueError('gr list must have 3 elements.')
        for x in gr:
            if x < 0:
                raise ValueError('gr must be larger than 0.')
        self.grs = gr[0]
        self.grpr = gr[1]
        self.grar = gr[2]

    def set_param_k(self, k):
        """Set k

        Args:
            k (list of floats) : kinetic constants (ks_pr, ks_ar, ks_q, kpr_s,
                kpr_q, kar_s, kar_q, kq_s, kq_pr, kq_ar).

        Raises:
            ValueError: if k length not equal to 10.
            ValueError: if any elements in k smaller than 0.
        """
        if len(k) != 10:
            raise ValueError('k list must have 10 elements.')
        for x in k:
            if x < 0:
                raise ValueError('k must be larger than 0.')
        self.kspr = k[0]
        self.ksar = k[1]
        self.ksq = k[2]
        self.kprs = k[3]
        self.kprq = k[4]
        self.kars = k[5]
        self.karq = k[6]
        self.kqs = k[7]
        self.kqpr = k[8]
        self.kqar = k[9]

    def set_param_d(self, d):
        """Set drug related parameters

        Args:
            d (list of floats) : drug related constants (ki, qf, dose, dsmax,
                ke).

        Raises:
            ValueError: if d length not equal to 5.
            ValueError: if any elements in d smaller than 0.
        """
        if len(d) != 5:
            raise ValueError('d list must have 5 elements.')
        for x in d:
            if x < 0:
                raise ValueError('d must be larger than 0.')
        self.ki = d[0]
        self.qf = d[1]
        self.dose = d[2]
        self.dsmax = d[3]
        self.ke = d[4]

    def set_param_t(self, t):
        """Set t

        set self.t (int) and self._tspan (numpy array).

        Args:
            t (int) : simulation time frame in days e.g. 365d = 1y.

        Raises:
            ValueError: if t is smaller than 0.
        """
        if t < 0:
            raise ValueError('t must be larger than 0.')
        self.t = t
        self._tspan = np.linspace(0, t, t+1)

    def _simulate(self):
        """Private, simulate sde

        Returns:
            dict of pandas data frame with key 'cells', 'drugs', 'fht'.
        """
        def f(x, t):
            if x[0] < 1e-8: x[0] = 0
            if x[1] < 1e-8: x[1] = 0
            if x[2] < 1e-8: x[2] = 0
            if x[3] < 1e-8: x[3] = 0
            if x[4] < 0: x[4] = 0

            if self._dose == 0:
                cs_dt = lambda x, t: (self._growth(self.grs, x) - self._quiescere_s(self.ksq, x[4]) - self._transit(self.kspr)) * x[0] + self._transit(self.kprs) * x[1] + self._transit(self.kqs) * x[3]
                cpr_dt = lambda x, t: (self._growth(self.grpr, x) - self._quiescere_r(self.kprq) - self._transit(self.kprs)) * x[1] + self._transit(self.kspr) * x[0] + self._transit(self.kqpr) * x[3]
                car_dt = lambda x, t: 0
                cq_dt = lambda x, t: -(self._transit(self.kqs) + self._transit(self.kqpr)) * x[3] + self._quiescere_s(self.ksq, x[4]) * x[0] + self._quiescere_r(self.kprq) * x[1]
                d_dt = lambda x, t: 0
            else:
                cs_dt = lambda x, t: (self._growth(self.grs, x) - self._quiescere_s(self.ksq, x[4]) - self._transit(self.ksar) - self._death(x[4])) * x[0] + self._transit(self.kprs) * x[1] + self._transit(self.kars) * x[2] + self._transit(self.kqs) * x[3]
                cpr_dt = lambda x, t: (self._growth(self.grpr, x) - self._quiescere_r(self.kprq) - self._transit(self.kprs)) * x[1]
                car_dt = lambda x, t: (self._growth(self.grar, x) - self._quiescere_r(self.karq) - self._transit(self.kars)) * x[2] + self._transit(self.ksar) * x[0] + self._transit(self.kqar) * x[3]
                cq_dt = lambda x, t: -(self._transit(self.kqs) + self._transit(self.kqar)) * x[3] + self._quiescere_s(self.ksq, x[4]) * x[0] + self._quiescere_r(self.kprq) * x[1] + self._quiescere_r(self.karq) * x[2]
                d_dt = lambda x, t: self._dose - self.ke * x[4]
            a = np.array([cs_dt(x,t), cpr_dt(x,t), car_dt(x,t), cq_dt(x,t), d_dt(x,t)])
            return a

        def g(x, t):
            difu = np.diag(np.repeat(self._sig, len(self.init)))
            return difu * x

        cth = self._get_cth()
        dfcell = pd.DataFrame()
        dfdrug = pd.DataFrame()
        fht = []

        for i in range(self.n):
            itg = sdeint.itoint(f, g, self.init, self._tspan)
            tdf = pd.DataFrame(itg)
            tdf = tdf.drop(tdf.index[len(tdf)-1])
            tdfdrug = pd.DataFrame(tdf.iloc[:,-1])
            tdfdrug[len(tdfdrug.columns)] = i
            tdfdrug[len(tdfdrug.columns)] = pd.Series(self._tspan)
            dfdrug = dfdrug.append(tdfdrug)
            tdfcell = tdf.iloc[:,0:4]
            tdfcell[len(tdfcell.columns)] = tdfcell.sum(axis=1)
            tdfcell[len(tdfcell.columns)] = i
            tdfcell[len(tdfcell.columns)] = pd.Series(self._tspan)
            dfcell = dfcell.append(tdfcell)
            tdfcellsum = tdfcell.iloc[:,4]
            if tdfcellsum.iloc[-1] < cth:
                tfht = np.nan
            else:
                tfht = [n for n, j in enumerate(tdfcell[4]) if j > cth][0]
            fht.append(tfht)

        dfcell.columns = ['sensitive', 'primary resistant', 'acquired resistant', 'quiescent', 'total', 'n', 'days']
        dfdrug.columns = ['drug conc', 'n', 'days']
        dfs = {'cells':dfcell, 'drugs':dfdrug, 'fht':fht}
        return dfs

    def simulate(self):
        """Simulate based on Simulator attributes

        Returns:
            dict: dict of dictionaries with keys 'control' and 'case'. Both 'control' and 'case' holds a dictionary of pandas data frame with keys 'cells', 'drugs' and 'fht'.

        """
        self._dose = 0
        ctrlres = self._simulate()
        self._dose = self.dose
        res = self._simulate()

        d = {'control': ctrlres, 'case':res}
        return d

    def _get_cth(self):
        """Private, Get threshold for first hitting time (progress free time)"""
        return self.init[0:-1].sum() * 3.5

    def _death(self, d):
        ds = self.dsmax * d / (self.ki + d)
        return ds

    def _transit(self, k):
        khat = k
        return khat

    def _quiescere_s(self, k, d):
        if d > 0:
            khat = k * self.qf * d / (self.ki + d)
        else:
            khat = k
        return khat

    def _quiescere_r(self, k):
        khat = k
        return khat

    def _growth(self, gr, x):
        ghat = gr * (1 - sum(x[0:4]) / self._ccmax)
        return ghat

    #@classmethod
    #def hcc_sorafenib(cls):
    #    return cls()
