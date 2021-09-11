import numpy as np
import astropy.stats as stat
import pandas as pd
import Extension4BINGO as cs

########################
#                      #
# Building the dataset #
#                      #
########################
def output_debias(Cls = None, model = None, output = "Cls_debias", dir_hi=None, dir_prior=None, dir_noise=None):
    for i,Li in enumerate(list(Cls["21cm"].keys())):
        iseed = int(Li.split("L")[1])
        cls = cs.noisedebiasing(Cls_=Cls, seed_used=iseed, dir_hi = dir_hi, dir_prior=dir_prior, dir_noise = dir_noise, type_ = model)[output]
        if i==0:
            Cls_all     = {Li:cls}
        else:
            Cls_all[Li] = cls
    return pd.Series(Cls_all)        

def data_binned(Cls = None):
    nbins, nl = Cls[list(Cls.keys())[0]].shape
    for ibin in range(nbins):
        for j,key in enumerate(Cls.keys()):
            if j==0:
                bin_ = Cls[key][ibin,:]
            else:
                bin_ = np.vstack((bin_, Cls[key][ibin,:]))
        if ibin==0:
            Cls_binned = {str(ibin):bin_}
        else:
            Cls_binned[str(ibin)] = bin_
    return pd.Series(Cls_binned)

####################
#                  #
# Jacknnife method #
#                  #
####################
def jacknnife_stat(cls_binned_=None, stat_func=np.std):
    test_statistic = lambda x: (stat_func(x))
    for i,ibin in enumerate(cls_binned_.keys()):
        data       = cls_binned_[ibin]
        nrealis,nl = data.shape
        jack_ = []
        for l in range(nl):
            jack_.append(stat.jackknife_stats(data[:,l], test_statistic, 0.95)[0])
        if i==0:
            jacknnife_ = {ibin:np.asarray(jack_)}
        else:
            jacknnife_[ibin]=np.asarray(jack_)
    return jacknnife_

####################
#                  #
# Bootstrap method #
#                  #
####################
def bootstrap_stat(cls_binned_=None, n_samples=1e6, stat_func=np.std):
    for i,ibin in enumerate(cls_binned_.keys()):
        data       = cls_binned_[ibin]
        nrealis,nl = data.shape
        boot_l = []
        for l in range(nl):
            boot  = np.random.choice(data[:,l],size=(data[:,l].size,int(n_samples)),replace=True)
            Bmean = stat_func(boot,axis=0)
            Bmean = np.sum(Bmean)/(Bmean.size -1)
            boot_l.append(Bmean)
        if i==0:
            bootstrap_ = {ibin:np.asarray(boot_l)}
        else:
            bootstrap_[ibin]=np.asarray(boot_l)
    return bootstrap_