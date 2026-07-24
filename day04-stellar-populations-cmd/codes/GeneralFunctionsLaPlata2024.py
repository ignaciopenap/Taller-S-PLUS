import numpy as np
import h5py
from astropy.table import Table
import pickle
import matplotlib.pyplot as plt


# matplotlib shit - just to make plots prettier
# plt.style.use('seaborn-bright')
# Change the style for this one if using matplotlib version 3.6 and up
plt.style.use('seaborn-v0_8-bright')
plt.rcParams['font.family'] = 'serif'
plt.rcParams['mathtext.fontset'] = 'stix'
plt.rcParams['axes.labelsize'] = 14
plt.rcParams['axes.linewidth'] = 1.5
plt.rcParams['xtick.labelsize'] = 14
plt.rcParams['ytick.labelsize'] = 14
plt.rcParams['legend.fontsize'] = 14
plt.rcParams['figure.figsize'] = (8, 5)
plt.rcParams['lines.linewidth'] = 2


# -----------------------------------------------------------------------------
def read_base_hdf5(baseFile):
    '''
    Read an hdf5-base file produced by me w/ISYA_ascii2hdf5_4StarlightBases.
    Convert the astropy table shit to arrays & store things the way I like.
    OBS: tUpp__j will be filled with nan's for bases of pure SSPs.
         It only makes sense for "square-bursts" (where SFR = conts between t__j & tUpp__j)
    Cid@Lagoa - 29/Nov/2022
    '''
    print('(read_base_hdf5) reading ', baseFile, '...')
    base = Table.read(baseFile,path='BASE')

    t__j      = base['age_base'].data
    tUpp__j   = base['age_base_upp'].data
    Z__j      = base['Z_base'].data
    Mstars__j = base['Mstars'].data
    l__l      = base['base_wl'][0]
    spec__lj  = (base['base_spec'].T).data

    return t__j, tUpp__j, Z__j, Mstars__j, l__l, spec__lj
# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
def read_filters_dict(shortVersion=True, masterFiltDicFile='Data/SPLUSFilters_ExtendedByErik.pkl'):
    '''
    shortVersion reads (& rename!) only FUV, NUV & ugriz.
    '''

    with open(masterFiltDicFile, 'rb') as f:
        filters = pickle.load(f)
        filters['GALEX_FUV']['curve']['transm'] /= 100   # GALEX curves are in %...
        filters['GALEX_NUV']['curve']['transm'] /= 100

    if shortVersion:
        # _l = ['GALEX_FUV', 'GALEX_NUV', 'splus_uJAVA', 'splus_gSDSS', 'splus_rSDSS', 'splus_iSDSS', 'splus_zSDSS', '2MASS_J', '2MASS_H', '2MASS_Ks']
        # _l = ['GALEX_FUV', 'GALEX_NUV', 'splus_uJAVA', 'splus_gSDSS', 'splus_rSDSS', 'splus_iSDSS', 'splus_zSDSS']
        # _d = dict()
        # for i in _l:
        #     _d[i] = filters[i]
        # filters = _d

        _d = dict()
        _d['FUV'] = filters['GALEX_FUV']
        _d['NUV'] = filters['GALEX_NUV']
        _d['u'] = filters['splus_uJAVA']
        _d['g'] = filters['splus_gSDSS']
        _d['r'] = filters['splus_rSDSS']
        _d['i'] = filters['splus_iSDSS']
        _d['z'] = filters['splus_zSDSS']
        filters = _d

    return filters
# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
def _calcSynPhot(wv__l, flux__l, filtersDic):
    '''
    For a filters dictionary filtersDic and an input spectrum flux__l(wv__l),
    returns the pivot wavelengths (pivot__b) and synthetic photo-fluxes (synFlux__b)
    in all the bands in filtersDic.
    '''
    pivot__b, synFlux__b = np.zeros(len(filtersDic)), np.zeros(len(filtersDic))
    for ib, i in enumerate(filtersDic.keys()):
        transm__l = np.interp(wv__l, filtersDic[i]['curve']['wl'], filtersDic[i]['curve']['transm'], left=0, right=0)
        r__l = transm__l * wv__l
        _den = np.trapz(r__l, x=wv__l)
        synFlux__b[ib] = np.trapz(flux__l * r__l, x=wv__l) / _den
        pivot__b[ib] = np.sqrt( 1 / ( np.trapz( (1 / wv__l**2) * r__l, x=wv__l) / _den ) )
    return pivot__b, synFlux__b
# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
def SimpleGaussSmooth(l__o, f__o, v0, sig, l__s=None, n_sig=6, n_u=51):
    '''
    Smooth an input spectrum f__o(l__o) with a Gaussian centered at velocity
    v = v0 and with sig as velocity dispersion. The output is f__s(l__s).
    The convolution is done with a BRUTE FORCE integration of n_u points
    from u = -n_sig to u = +n_sig, where u = (v - v0) / sig.

    OBS: Assumes original spectrum f__o(l__o) is EQUALLY SPACED in lambda!!
          Units of v0 & sig = km/s

    Borrowed from the good-old Starlight's SUBROUTINE GaussSmooth!
    Cid@UFSC - 05/Jul/2023
    '''

    # Def l__s if not given
    if l__s is None:
        l__s = l__o
    f__s = np.zeros_like( l__s )

    # u-grid params
    u_low, u_upp = -n_sig, n_sig
    u__u = np.linspace(u_low,u_upp,n_u)
    du = u__u[1] - u__u[0]

    # compute the convolution integral for each output l__s
    for i_s in range(len(l__s)):
        vv__u = v0 + np.abs(sig) * u__u
        ll__u = l__s[i_s] / (1. + vv__u/299792.5)
        ff__u = np.interp(ll__u,l__o, f__o)
        sum_fg = (ff__u * np.exp(-(u__u**2/2.))). sum()
        f__s[i_s] = sum_fg * du / np.sqrt(2. * np.pi)

    return f__s
# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
def _calcSpecFor2Bursts(mY, tY, tO, t__j, spec__lj, Mtot=1):
    '''
    This function looks up the t__j SSP age array and find the models closest
    to the input ages tY & tO. Their spectra are then added after scaling the tY
    spectrum my mY/100 and the tO by its complement percentage (100 - mY)/100.
        - mY = fraction of (initial) MASS in the tY SSP
        - tY, tO = ages of the Y ("Young") and O ("Old") SSPs
        - Mtot (default to 1=Msun) is the total mass.
        - t__j & spec__lj = the age and spectral arrays
    Returns the spectral of the Y and O components, as well as their sum.

    OBS: This works if spec__lj are in units of per (initial) Msun (e.g.,
         Lsun/A/Msun, as they are in these notebooks).
    '''
    indY = np.abs(t__j - tY).argmin()
    indO = np.abs(t__j - tO).argmin()
    fY__l =  Mtot * (mY/100) * spec__lj[:,indY]
    fO__l =  Mtot * (100 - mY)/100 * spec__lj[:,indO]
    tot__l = fY__l + fO__l
    return fY__l, fO__l, tot__l
# -----------------------------------------------------------------------------


#------------------------------------------------------------------------------
def DefSFR__t(t,t0,tau,law='linexp'):
    '''
    Define SFR(t) function & scale it to produce 1 solar mass (hence this SFR is
    also a sSFR!). Besides 'exp', 'linexp', & 'square', law can be an array of
    SFR(t) values, which are then just scaled to produce 1 Msun.
    Cid@Lagoa - 25/Feb/2018
    '''

    if type(law) == str:
        if law == 'linexp':
            x = (t0 - t) / tau
            y = np.where(t < t0, x * np.exp(-x) , 0)
        elif law == 'exp':
            x = (t0 - t) / tau
            y = np.where(t < t0, np.exp(-x) , 0)
        elif law == 'square':
            y = np.where( (t < t0) * (t > t0 - tau), 1 , 0)
            # Q&D fix - sometimes the interval does not contain a t__jj!
            if y.sum() == 0:
                y[np.argmin(np.abs(t - t0))] = 1

        else:
            print('[@DefSFR__t] oops ...')
            sys.exit()

    elif len(law) == len(t):
        y = law

    dt = DefIntervals(t)
    y = y / (y * dt).sum()

    return y
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
def DefIntervals(x):
    '''
    Given an array x[] define the intervals dx represented by each x[j]
    as distance from the half-way points between x[j-1] --> x[j] and
    x[j] --> x[j+1]. Borders (@ x[0] & x[-1]) have halved dx's

	Example: x = np.array([0, 1, 4, 10, 20])
			 dx = ([0.5, 2. , 4.5, 8. , 5.])

    Cid@Lagoa - 21 Dec 2022
    '''
    dx = np.zeros(len(x))
    dx[0]    = (x[1] - x[0]) / 2.
    dx[-1]   = (x[-1] - x[-2]) / 2.
    dx[1:-1] = (x[2:] - x[:-2]) / 2.
    return dx
#------------------------------------------------------------------------------


# -----------------------------------------------------------------------------
def calc_Dn4000(wavelength, flux):
    '''
    Dn4000 index cf Balogh et al 1999 , ApJ, 527,54
    ATT: No flag or negative flux corrections!
    Cid@ISYA 25/Jul/2023
    '''
    lBlue_low, lBlue_upp = 3850., 3950.
    lRed_low,   lRed_upp = 4000., 4100.

    maskBlue__l = (wavelength >= lBlue_low) & (wavelength <= lBlue_upp)
    maskRed__l  = (wavelength >= lRed_low)  & (wavelength <= lRed_upp)
    _l, _f = wavelength[maskBlue__l], flux[maskBlue__l]
    F_Blue = np.trapz((_f * _l**2), x=_l)
    _l, _f = wavelength[maskRed__l], flux[maskRed__l]
    F_Red = np.trapz((_f * _l**2), x=_l)
    Dn4000  = F_Red / F_Blue

    return Dn4000
# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
def calc_EW(wavelength, flux, ll_low,ll_upp,lf_low,lf_upp,lr_low,lr_upp):
    '''
    Compute the equivalent width of some line in a flux(wavelength) spectrum
    for the input side & feature bands.
        ll_* = left (blue) side-band lambda lower & upper limits
        lf_* = feature band lambda lower & upper limits
        lr_* = right (blue) side-band lambda lower & upper limits

    ATT: No flag or negative flux corrections!
    Cid@ISYA 25/Jul/2023
    '''

# define masks for left, feature & right bands
    maskLeft    = (wavelength >= ll_low) & (wavelength <= ll_upp)
    maskRight   = (wavelength >= lr_low) & (wavelength <= lr_upp)
    maskFeature = (wavelength >= lf_low) & (wavelength <= lf_upp)

# Compute mean continuum fluxes in left & right bands
    F_Left  = flux[maskLeft].mean()
    F_Right = flux[maskRight].mean()

# Interpolating coeficients (A & B) for a straight-line continuum spectrum
    ll_mid = (ll_low + ll_upp) / 2.
    lr_mid = (lr_low + lr_upp) / 2.
    A = (F_Right - F_Left) / (lr_mid - ll_mid)
    B = F_Right - A * lr_mid

# (Pseudo) Continuum spectrum
    cont = A * wavelength + B

# Compute equivalent width
    _l, _f, _c = wavelength[maskFeature], flux[maskFeature], cont[maskFeature]
    W = np.trapz((_f - _c) / _c, x=_l)

# Return both the eq width and stuff nedded for a plot
    return W, cont, ll_mid, lr_mid, F_Left, F_Right
# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
def MedidorDeCosas(l__l, spec__l, filters=None):
    '''
    Measure things for an input spectrum spec__l[l__l] and return them on a
    dictionary D! If a filters dic is given then D will also include synthetic
    photometry.
    Crude, but useful both for models and data.
    Cid@INAOE - 2/Jul/2023
    '''
    D = dict()

    # --------------------------------------------------------------------------
    # Dn4000, HdA, Mgb, W_Ha, cont_Ha
    Dn4000 = calc_Dn4000(l__l, spec__l)
    D['Dn4000'] = Dn4000

    # Hd_A (cf Worthey & Ottaviani 1997, ApJS, 111,377)
    ll_low, ll_upp, lf_low, lf_upp, lr_low, lr_upp = 4041.60, 4079.75, 4083.50, 4122.25, 4128.50, 4161.00
    W, cont__l, ll_mid, lr_mid, F_Left, F_Right = calc_EW(l__l, spec__l, ll_low,ll_upp,lf_low,lf_upp,lr_low,lr_upp)
    D['HdA'] = W

    # Lick index Mg_b
    ll_low, ll_upp, lf_low, lf_upp, lr_low, lr_upp = 5142.625, 5161.375, 5160.125, 5192.625,5191.375, 5206.375
    W, cont__l, ll_mid, lr_mid, F_Left, F_Right = calc_EW(l__l, spec__l, ll_low,ll_upp,lf_low,lf_upp,lr_low,lr_upp)
    D['Mgb'] = W

    # Quick & Dirty definition of Ha bands! Should check!
    ll_low, ll_upp, lf_low, lf_upp, lr_low, lr_upp = 6520., 6535., 6555., 6571., 6597., 6612.
    W, cont__l, ll_mid, lr_mid, F_Left, F_Right = calc_EW(l__l, spec__l, ll_low,ll_upp,lf_low,lf_upp,lr_low,lr_upp)
    D['W_Ha'] = W

    i_Ha = np.argmin(np.abs(l__l - 6563))
    cont_Ha = cont__l[i_Ha]
    D['cont_Ha'] = cont_Ha
    # --------------------------------------------------------------------------


    # --------------------------------------------------------------------------
    # calc QH in ionizing photons/s (assuming input spec__l is in Lsun/A!)
    h_Planck = 6.62607015e-27            # erg s
    L_Sun = 3.826e33                     # erg / s
    c_light_inAngs = 2.99792458e18       # Angs / s
    m__l = (l__l <= 912)

    if (m__l.sum() > 10):
        _integrand__l = spec__l[m__l] * l__l[m__l] * L_Sun / (h_Planck * c_light_inAngs)
        _x__l = l__l[m__l]
        QH = np.trapz(_integrand__l, x=_x__l)
        D['QH'] = QH
    # --------------------------------------------------------------------------


    if filters is not None:
        # --------------------------------------------------------------------------
        #           Synthetic photometry @ filters = [FUV,NUV,u,g,r,i,z]
        # --------------------------------------------------------------------------
        # Resample filter ib curve to l__l to facilitate the integrals ==> transm__lb
        # Then compute the photo-flux spec__b & the pivot wavelength l__b
        # OBS: spec__b is in units of spec__l (= Lsun/A/Msun in the case of models)
        n_b, n_l = len(filters), len(l__l)
        l__b, spec__b, transm__lb = np.zeros(n_b), np.zeros(n_b), np.zeros( (n_l,n_b) )
        for ib, i in enumerate(filters.keys()):
            transm__lb[:,ib] = np.interp(l__l, filters[i]['curve']['wl'], filters[i]['curve']['transm'], left=0, right=0)
            r__l = transm__lb[:,ib] * l__l
            _den = np.trapz(r__l, x=l__l)
            spec__b[ib] = np.trapz(spec__l * r__l, x=l__l) / _den
            l__b[ib] = np.sqrt( 1 / ( np.trapz( (1 / l__l**2) * r__l, x=l__l) / _den ) )

        # Convert Lsun/A to a flux at 10pc in units of erg/s/cm2/A  (all per Msun!)
        # and compute the corresponding magnitute at 10 pc (ie, the absolute mag) for each band b.
        l2f_at_10pc = 3.826e33 / (4 * np.pi * (10 * 3.086e18)**2)
        Mag__b = -2.5 * np.log10(l__b**2 * spec__b * l2f_at_10pc) - 2.41

        D['spec__b'] = spec__b
        D['Mag__b'] = Mag__b
        D['l__b'] = l__b
        # --------------------------------------------------------------------------

    return D
# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
def calcParametricModel_spec(law, Mtot, t0, tau, t__j, spec__lj):
    '''
    Compute SFR & MAH (SFR__j, cumulM__j) & the current (t = 0) spectrum (spec__l)
    for a law [= exp, lin-exp or square] parametric model.
    '''
    dt__j  = DefIntervals(t__j)
    SFR__j = Mtot * DefSFR__t(t__j, t0, tau, law=law)
    dM__j  = SFR__j * dt__j
    dL__lj = spec__lj * dM__j
    cumulM__j  = np.cumsum(dM__j[::-1])[::-1]
    cumulL__lj = np.cumsum(dL__lj[:,::-1],axis=1)[:,::-1]
    spec__l    = cumulL__lj[:,0]
    return SFR__j, cumulM__j, spec__l
# -----------------------------------------------------------------------------
