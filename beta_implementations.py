"""
For now, assume everything is M200m.

'beta' is the logarithmic derivative of the mass function.
"""
import numpy as np

#Default cosmology to do the inversion
h = 0.7
cos = {"om":0.3,"ob":0.049,"ol":1.-0.3,"ok":0.0,"h":h,"s8":0.82,"ns":0.96,"w0":-1.0,"wa":0.0}

def convert_mass(M, inDelta, outDelta, indef, outdef):
    """A wrapper around the colossus tool for converting mass definitions.

    Note: the NFW profile is assumed for performing the conversion in colossus.

    Args:
        M (float): Mass in Msun/h.
        inDelta (float): Overdensity of input mass.
        outDelta (float): Overdensity of output mass.
        indef (string): Mass definition; either "m", "c", or "vir".
        outdef (string): Mass definition; either "m", "c", or "vir".

    Returns:
        float: Mass of the ouput definition.

    """
    if indef not in ['m', 'c'] and outdef not in ['m', 'c']:
        raise Exception("Mass definition must be either 'm' or 'c'.")
    from colossus.halo.mass_defs import changeMassDefinition
    from colossus.cosmology.cosmology import setCosmology
    from colossus.halo.concentration import concentration
    params = {'flat':True, 'H0':cos['h']*100, 'Om0':cos['om'], 'Ob0':cos['ob'], 'sigma8':cos['s8'], 'ns':cos['ns']}
    cosmo = setCosmology('default', params)
    #Parse indef and outdef and use
    return M

def get_CCL_beta(M,z):
    a = 1./(1+z)
    d = 1.0001
    import pyccl as ccl
    params = ccl.Parameters(Omega_c = cos['om']-cos['ob'], Omega_b=cos['ob'], h=cos['h'], sigma8=cos['s8'], n_s=cos['ns'])
    cosmo = ccl.Cosmology(params)
    dndM1 = ccl.massfunc(cosmo, M, a)/M
    dndM2 = ccl.massfunc(cosmo, M*d, a)/(M*d)
    return np.log(dndM2/dndM1)/np.log(d)

def get_aemulus_beta(M, z):
    import aemHMF
    hmf = aemHMF.Aemulus_HMF()
    hmf.set_cosmology()
    d = 1.0001
    dndM1 = hmf.dndlM(M, z)/M
    dndM2 = hmf.dndlM(M*d, z)/(M*d)
    return np.log(dndM2/dndM1)/np.log(d)
    
def get_cosmocalc_beta(M, z):
    a = 1./(1+z)
    import cosmocalc as cc
    MF = cc.tinker2008_mass_function
    cc.set_cosmology(cos)
    d = 1.00001
    dndM1 = MF(M, a, 200)
    dndM2 = MF(M*d, a, 200)
    return np.log(dndM2/dndM1)/np.log(d)

if __name__ == "__main__":
    M = 1e14
    z = 0
    b1 = get_CCL_beta(M, z)
    b2 = get_aemulus_beta(M, z)
    b3 = get_cosmocalc_beta(M, z)
    print b1, b2, b3
