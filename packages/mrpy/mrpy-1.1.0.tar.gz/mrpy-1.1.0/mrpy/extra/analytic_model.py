"""
A module defining the likelihoods and related quantities involved when
the data is purely ideal and analytic.

See appendix of Murray, Power and Robotham for more details.

It is intended to provide a fast way to estimate the strength of fits using
different parameters (such as the scaling).
"""
import numpy as np
from . import likelihoods as lk
import mrpy.base.special as sp
from mrpy.base import core
from cached_property import cached_property as _cached

ln10 = np.log(10)


class IdealAnalytic(lk.SampleLike):

    def __init__(self, logHsd=None, alphad=None, betad=None, lnAd=None, **kwargs):
        """
        Subclass of :class:`~mrpy.extra.likelihoods.SampleLike`, defining the expected likelihood and covariance for a sample
        of variates drawn directly from an MRP distribution.

        See Murray, Robotham, Power (2016) for details.

        In this class, no vector of masses is passed, but rather mmin is used everywhere. To do this, it
        automatically creates a length-1 vector of masses, equalling mmin, to use the methods of its
        superclass. To invoke methods for general vectors of m, do not use this class.

        Parameters
        ----------
        logHsd, alphad, betad : float, optional
            Values of the MRP parameters for the *data*. If not given, they are set to the
            corresponding values of the variable parameters (i.e. the solution).

        Other Parameters
        ----------------
        args :
            Other parameters are passed directly to :class:`PerObjLike`
        """
        if "log_mmin" not in kwargs:
            raise ValueError("log_mmin needs to be specified in this class")
        else:
            log_mmin = kwargs.pop("log_mmin")

        super(IdealAnalytic, self).__init__(logm=np.array([log_mmin]), log_mmin=log_mmin, **kwargs)

        # Set data parameters
        self.logHsd = logHsd or self.logHs
        self.alphad = alphad or self.alpha
        self.betad = betad or self.beta
        self.lnAd = self.lnA if lnAd is None else lnAd

        self._shape = [getattr(getattr(self, q), "__len__", None) for q in ["mmin", "logHs", "alpha", "beta"]]
        while None in self._shape:
            self._shape.remove(None)

    @_cached
    def Hsd(self):
        return 10 ** self.logHsd

    @_cached
    def Ad(self):
        return np.exp(self.lnAd)

    # ===========================================================================
    # Basic Unit Quantities
    # ===========================================================================
    @_cached
    def _yd(self):
        return self.mmin / self.Hsd

    @_cached
    def _xd(self):
        return self._yd ** self.betad

    @_cached
    def _zd(self):
        return (self.alphad + 1) / self.betad

    # ===========================================================================
    # Cached special functions (data counterparts)
    # ===========================================================================
    @_cached
    def _gammazd(self):
        return sp.gamma(self._zd)

    @_cached
    def gammainc_zxd(self):
        return sp.gammainc(self._zd, self._xd)

    @_cached
    def gammainc_z1x(self):
        return sp.gammainc(self._z + 1, self._x)

    @_cached
    def gammainc_z1xd(self):
        return sp.gammainc(self._zd + self.beta / self.betad, self._xd)

    @_cached
    def G1d(self):
        return self.Ad * self.Hsd * sp.G1(self._zd, self._xd)

    @_cached
    def G1d_p1(self):
        return self.Ad * self.Hsd * sp.G1(self._zd + self.beta / self.betad, self._xd)

    @_cached
    def G2d(self):
        return self.Ad * self.Hsd * sp.G2(self._zd, self._xd)

    @_cached
    def G2d_p1(self):
        return self.Ad * self.Hsd * sp.G2(self._zd + self.beta / self.betad, self._xd)

    @_cached
    def _Gbard(self):
        return self.G1d * np.log(self._xd) + 2 * self.G2d

    @_cached
    def _Gbard_p1(self):
        return self.G1d_p1 * np.log(self._xd) + 2 * self.G2d_p1

    @_cached
    def _phid(self):
        return self.mmin * self._gd

    # ===========================================================================
    # Basic MRP quantities
    # ===========================================================================
    @_cached
    def _gd(self):
        """
        The shape of the MRP, completely unnormalised (ie. A=1) (truncation mass)
        """
        return core.dndm(self.mmin, self.logHsd, self.alphad, self.betad, norm=self.Ad)

    @_cached
    def _qd(self):
        """
        The normalisation of the MRP (ie. integral of g) (truncation masses)
        """
        return sp.gammainc(self._zd, self._xd) * self.Hsd * self.Ad

    #
    # @_cached
    # def _qd_nos(self):
    #     """
    #     q for the data parameters, without scaling.
    #     """
    #     return sp.gammainc((self.alphad+1)/self.betad, self._xd)*self.Hsd

    @_cached
    def _lngd(self):
        """
        Better log of g than log(g) (truncation mass)
        """
        return core.ln_mrp_shape(self.mmin, self.logHsd, self.alphad, self.betad, log=True, norm=self.lnAd)

    # ===========================================================================
    # Basic likelihood
    # ===========================================================================
    @_cached
    def _t(self):
        a = self.alpha
        ad = self.alphad
        zd = self._zd
        pg = sp.polygamma(0, zd)
        return np.exp(self.lnAd) * (a * self.Hsd / self.betad) * self._gammazd * (self._yd ** (ad + 1) * self._gammazd *
                                                                                  sp.hyperReg_2F2(zd, self._xd) +
                                                                                  pg - self.betad * np.log(self._yd))

    @_cached
    def _u(self):
        a = (self.Hsd / self.Hs) ** self.beta
        b = self.Ad * self.Hsd * self.gammainc_z1xd
        c = self._xd ** (self.beta / self.betad) * self._qd
        return a * (b - c)

    @_cached
    def _F(self):
        return np.squeeze(-self._q + self._qd * self._lng + self._t - self._u)

    @_cached
    def lnL(self):
        return self._F

    # ===========================================================================
    # Simple Derivatives
    # ===========================================================================
    # ---------------u'() --------------------------------------------
    @_cached
    def _u_A(self):
        return 0

    @_cached
    def _u_A_A(self):
        return 0

    @_cached
    def _u_h_A(self):
        return 0

    @_cached
    def _u_a_A(self):
        return 0

    @_cached
    def _u_b_A(self):
        return 0

    @_cached
    def _u_a(self):
        return 0

    @_cached
    def _u_a_a(self):
        return 0

    @_cached
    def _u_h_a(self):
        return 0

    @_cached
    def _u_a_b(self):
        return 0

    @_cached
    def _u_h(self):
        return -self.beta * self._u * ln10

    @_cached
    def _u_h_h(self):
        return -ln10 * self.beta * self._u_h

    @_cached
    def _u_b(self):
        a = self._u * (np.log(self.Hsd / self.Hs) + np.log(self._xd) / self.betad)
        b = (self.Hsd / self.Hs) ** self.beta * self.G1d_p1 / self.betad
        return a + b
        # a = np.log(self.Hsd / self.Hs) * self._u
        # b = (self.Hsd / self.Hs) ** self.beta
        # c = self._u * np.log(self._xd)/b
        # d = np.exp(self.lnAd) * self.Hsd * self.gammainc_z1xd * self.G1d_p1
        # return a + b * ((1.0 / self.betad) * (c + d))

    @_cached
    def _u_h_b(self):
        return -ln10 * (self._u + self.beta * self._u_b)

    @_cached
    def _u_b_b(self):
        hf = self.Hsd / self.Hs
        hfb = hf ** self.beta

        # a = self._u_b*(np.log(hf) + np.log(self._xd)/self.betad)
        # b = np.log(hf) * hfb * self.G1d_p1/self.betad
        # c =
        a = np.log(hf) + np.log(self._xd) / self.betad
        b = self._u_b + hfb * self.G1d_p1 / self.betad
        c = 2 * hfb * self.G2d_p1 / self.betad ** 2
        return a * b + c
        # a = 1/self.betad
        # b = self._u_b*(self.betad*np.log(hfrac) + np.log(self._xd))
        # c = np.log(hfrac) * self.Hsd * self.G1d_p1 * self.gammainc_z1xd * hfrac**self.beta
        # d = self.Hsd * hfrac**self.beta * self.gammainc_z1xd * self._Gbard_p1/self.betad
        #
        # return a*(b+c+d)

    # ---------------t'() --------------------------------------------
    @_cached
    def _t_A(self):
        return 0

    @_cached
    def _t_A_A(self):
        return 0

    @_cached
    def _t_h_A(self):
        return 0

    @_cached
    def _t_a_A(self):
        return 0

    @_cached
    def _t_b_A(self):
        return 0

    @_cached
    def _t_a(self):
        return self._t / self.alpha

    @_cached
    def _t_a_a(self):
        return 0

    @_cached
    def _t_h_a(self):
        return 0

    @_cached
    def _t_a_b(self):
        return 0

    @_cached
    def _t_h(self):
        return 0

    @_cached
    def _t_h_h(self):
        return 0

    @_cached
    def _t_b(self):
        return 0

    @_cached
    def _t_h_b(self):
        return 0

    @_cached
    def _t_b_b(self):
        return 0

    # ===========================================================================
    # Jacobians and Hessians
    # ===========================================================================
    # -----------------F'() ---------------------------------------------
    def _F_x(self, x):
        """
        Derivatives of Q w.r.t x
        """
        gx = getattr(self, "_lng_%s" % x)
        qx = getattr(self, "_q_%s" % x)
        ux = getattr(self, "_u_%s" % x)
        tx = getattr(self, "_t_%s" % x)

        return self._qd * gx + tx - ux - qx

    def _F_x_y(self, x, y):
        """
        Double derivatives of F w.r.t x then y
        """
        if y == "h" or (y == "a" and x == "b"):
            x, y = y, x

        lngxy = getattr(self, "_lng_%s_%s" % (x, y))
        qxy = getattr(self, "_q_%s_%s" % (x, y))
        uxy = getattr(self, "_u_%s_%s" % (x, y))

        return self._qd * lngxy - uxy - qxy

    @_cached
    def jacobian(self):
        h = self._F_x("h")
        a = self._F_x("a")
        b = self._F_x("b")
        A = self._F_x("A")

        if self._shape:
            x = np.array([np.array([h[i], a[i], b[i], A[i]]
                                   ) for i in range(len(h))]).T
        else:
            x = np.array([h, a, b, A])
        return np.squeeze(x)

    @_cached
    def hessian(self):
        hh = self._F_x_y("h", "h")
        ha = self._F_x_y("h", "a")
        hb = self._F_x_y("h", "b")
        aa = self._F_x_y("a", "a")
        ab = self._F_x_y("a", "b")
        bb = self._F_x_y("b", "b")
        hA = self._F_x_y("h", "A")
        aA = self._F_x_y("a", "A")
        bA = self._F_x_y("b", "A")
        AA = self._F_x_y("A", "A")

        if self._shape:
            x = np.array([np.array([[hh[i], ha[i], hb[i], hA[i]],
                                    [ha[i], aa[i], ab[i], aA[i]],
                                    [hb[i], ab[i], bb[i], bA[i]],
                                    [hA[i], aA[i], bA[i], AA[i]]]) for i in range(len(hh))]).T
        else:
            x = np.array([[hh, ha, hb, hA],
                          [ha, aa, ab, aA],
                          [hb, ab, bb, bA],
                          [hA, aA, bA, AA]])
        return np.squeeze(x)

    @_cached
    def cov(self):
        """
        The covariance matrix of the current "solution".
        """
        if self._shape:
            return np.array([np.linalg.inv(-h) for h in self.hessian])
        else:
            return np.linalg.inv(-self.hessian)

    @_cached
    def corr(self):
        """
        The correlation matrix of the current "solution".
        """
        if self._shape:
            s = [np.sqrt(np.diag(c)) for c in self.cov]
            return np.array([self.cov[i] / np.outer(ss, ss) for i, ss in enumerate(s)])
        else:
            s = np.sqrt(np.diag(self.cov))
            return self.cov / np.outer(s, s)
