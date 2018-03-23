"""
For now, assume everything is M200m.
"""
import numpy as np

#Default cosmology to do the inversion
cos = {"om":0.3,"ob":0.049,"ol":1.-0.3,"ok":0.0,"h":h,"s8":0.82,"ns":0.96,"w0":-1.0,"wa":0.0}

def convert_mass(M, inDelta, outDelta, indef, outdef):
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
    import pyccl as ccl
    cosmo = 0
    return np.log(dndM2/dndM1)/np.log(d)

def get_aemulus_beta(M, z):
    import aemHMF
    hmf = aemHMF.Aemulus_HMF()
    hmf.set_cosmology()
    d = 1.0001
    dndM1 = hmf.dndlM(M, z)/M
    dndM2 = hmf.dndlM(M*d, z)/(M*d)
    return -np.log(dndM2/dndM1)/np.log(d)
    
def get_cosmocalc_beta(M, z):
    a = 1./(1+z)
    import cosmocalc as cc
    MF = cc.tinker2008_mass_function
    cc.set_cosmology(cos)
    d = 1.00001
    dndM1 = MF(M, a, 200)
    dndM2 = MF(M*d, a, 200)
    return np.log(dndM2/dndM1)/np.log(d)
