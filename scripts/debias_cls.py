import os,sys
import numpy as np
import healpy as hp
import pandas as pd
import Extension4BINGO as cs
import matplotlib
from   matplotlib import rc
import matplotlib.pyplot as plt
import time
import argparse, json
rc('text', usetex=True)
font = {'weight' : 'bold',
        'size'   : 22}
matplotlib.rc('font', **font)


###################################################################
# Check the python version and import configparser
###################################################################

if sys.version_info[0]==2:
	import ConfigParser
	config = ConfigParser.RawConfigParser()
elif sys.version_info[0]==3:
	import configparser
	config = configparser.ConfigParser()

###################################################################
# This part is for extracting information from parameters_clplot.ini file
###################################################################
INI         = "parameters_clplot.ini"
config.read(os.path.join(os.getcwd(),INI))

#General variables
#Paths
pathcls       = config.get("Paths","pathcls")
dir_hi        = config.get("Paths","dir_hi")
dir_fg        = config.get("Paths","dir_fg")
dir_prior     = config.get("Paths","dir_prior")
dir_noise     = config.get("Paths","dir_noise")
dir_pure      = config.get("Paths","dir_pure")
dir_projprior = config.get("Paths","dir_projprior")
dir_projnoise = config.get("Paths","dir_projnoise")
dir_projpure  = config.get("Paths","dir_projpure")	

#Variable of the Realisation
seed_used  = config.getint("Realisation","seed_used")
#Variable of the plots
debias_model  = config.get("Plots","debias_model")
###############################################################################
# You can modify any options in the parameters.ini file by the command terminal
###############################################################################

parser = argparse.ArgumentParser(description='Modify by the command terminal parameters in parameters_clplot.ini file')

parser.add_argument('--seed_used', action = 'store', dest = 'seed_used', default =seed_used , help = 'Realisation used.')
parser.add_argument('--pathcls', action = 'store', dest = 'pathcls', default =pathcls , help = '')
parser.add_argument('--dir_hi', action = 'store', dest = 'dir_hi', default =dir_hi , help = 'Path of the clshi directory')
parser.add_argument('--dir_fg', action = 'store', dest = 'dir_fg', default =dir_fg , help = 'Path of the clsfg directory')
parser.add_argument('--dir_prior', action = 'store', dest = 'dir_prior', default =dir_prior , help = 'Path of the clsprior directory')
parser.add_argument('--dir_noise', action = 'store', dest = 'dir_noise', default =dir_noise , help = 'Path of the clsnoise directory')
parser.add_argument('--dir_pure', action = 'store', dest = 'dir_pure', default =dir_pure , help = 'Path of the clspure directory')
parser.add_argument('--dir_projprior', action = 'store', dest = 'dir_projprior', default =dir_projprior , help = '')
parser.add_argument('--dir_projnoise', action = 'store', dest = 'dir_projnoise', default =dir_projnoise , help = '')
parser.add_argument('--dir_projpure', action = 'store', dest = 'dir_projpure', default =dir_projpure , help = '')
parser.add_argument('--debias_model', action = 'store', dest = 'debias_model', default =debias_model, help = '')

arguments = parser.parse_args()
###############################################################################
# Variables
###############################################################################
seed_used    = int(arguments.seed_used)
pathcls      = str(arguments.pathcls)
dir_hi       = str(arguments.dir_hi)
dir_fg       = str(arguments.dir_fg)
dir_pure     = str(arguments.dir_pure)
dir_prior    = str(arguments.dir_prior)
dir_noise    = str(arguments.dir_noise)
dir_projpure  = str(arguments.dir_projpure)
dir_projprior = str(arguments.dir_projprior)
dir_projnoise = str(arguments.dir_projnoise)
debias_model  = str(arguments.debias_model)

####################################################################################################################################################################
#####################################################################################################################################################################
#####################################################################################################################################################################

Cls = cs.loadcls(pathcls,dirs=[dir_hi,dir_fg,dir_prior,dir_noise,dir_pure])  
cls = cs.noisedebiasing(Cls_=Cls, seed_used=seed_used, dir_hi = dir_hi, dir_prior=dir_prior, dir_noise = dir_noise, type_=debias_model)
Cls_ndb   = cls["Cls_debias"]
#S         = cls["S"]
#Cls_noise = cls["Cls_noise"]
####################################################################################################################################################################
#####################################################################################################################################################################
#####################################################################################################################################################################

Cls = cs.loadcls(pathcls,dirs=[dir_hi,dir_fg,dir_prior,dir_noise,dir_pure])
fig      = plt.figure()

numplots = 3
grid     = plt.GridSpec(4,2*numplots,top=4.5,right=3*numplots)
nu,nl = Cls_ndb.shape
l     = np.arange(nl)
fact  = l*(l+1)/(2*np.pi)
L0    = "L{}".format(seed_used)

for col,i in enumerate(np.random.randint(nu,size=numplots)):
    ax = plt.subplot(grid[0,col])
    #print("bin: {}".format(i))
    l_bin, cls_bin = cs.clsbinned(Cls_ndb[i],del_l=4,l0=0)
    fact_bin       = l_bin*(l_bin+1)/(2*np.pi)
    plt.title("bin {}".format(i), fontsize=20)
    plt.plot(   l,fact*Cls["pure"][L0][i] , color="red"  , label="L0"           , linewidth =1)
    plt.scatter(l,fact*Cls_ndb[i]         , color="blue" , label="21cm - Debias", s=40)
    plt.scatter(l_bin,fact_bin*cls_bin    , color="orange", label="Binned"      , s=30)
    plt.xscale("log")
    plt.yscale("log")
    ax.tick_params(axis='both', which='major', labelsize = 20)
    plt.ylabel(r"$\ell(\ell+1)$C$_{\ell}/2\pi$ $(\textrm{mK}^2$)", fontsize=20)
    #plt.xlabel(r"$\ell$", fontsize=20)
    plt.legend(fontsize=15)

    ax = plt.subplot(grid[1,col])
    #print("bin: {}".format(i))
    #plt.title("bin {}".format(i), fontsize=20)
    plt.plot(l,fact*Cls["pure"][L0][i] , color="red"   , label="L0"           , linewidth =1)
    plt.scatter(l,fact*Cls_ndb[i]      , color="blue"  , label="21cm - Debias", s=40)
    plt.plot(l_bin,fact_bin*cls_bin    , color="orange", label="Binned"      , marker="+", markersize=20)
    #plt.scatter(l,fact*Cls_noise[i]    , color="green", label="Debiasing", linewidth =1)
    plt.xscale("log")
    #plt.yscale("log")
    ax.tick_params(axis='both', which='major', labelsize = 20)
    plt.ylabel(r"$\ell(\ell+1)$C$_{\ell}/2\pi$ $(\textrm{mK}^2$)", fontsize=20)
    #plt.xlabel(r"$\ell$", fontsize=20)
    plt.legend(fontsize=15)    
    
    ax = plt.subplot(grid[2,col])
    inds = cs.index_cls_binned(l,l_bin)
    plt.plot(l      ,(Cls["pure"][L0][i]       - Cls_ndb[i]), color="blue"  , label="error", marker="o", markersize=10,linewidth =3)
    plt.plot(l[inds],(Cls["pure"][L0][i][inds] - cls_bin)   , color="orange", label="error - binned", marker="o", markersize=10)
    plt.axhline(y=0, linestyle="dashed", color="black")
    plt.xscale("log")
    #plt.yscale("log")
    ax.tick_params(axis='both', which='major', labelsize = 20)
    plt.xlabel(r"$\ell$", fontsize=20)
    plt.ylabel(r"$\textrm{C}^{21\textrm{cm}}_{\ell} - \textrm{C}^{\textrm{debias}}_{\ell}$", fontsize=20)
    #plt.xlim(0,300)
    plt.ylim(-4e-7,4e-7)
    plt.legend(fontsize=15)
    
    ax = plt.subplot(grid[3,col])
    inds = cs.index_cls_binned(l,l_bin)
    plt.plot(l      ,fact*(Cls["pure"][L0][i]       - Cls_ndb[i]), color="blue"  , label="error", marker="o", markersize=10,linewidth =3)
    plt.plot(l[inds],fact_bin*(Cls["pure"][L0][i][inds] - cls_bin)   , color="orange", label="error - binned", marker="o", markersize=10)
    plt.axhline(y=0, linestyle="dashed", color="black")
    plt.xscale("log")
    #plt.yscale("log")
    ax.tick_params(axis='both', which='major', labelsize = 20)
    plt.xlabel(r"$\ell$", fontsize=20)
    plt.ylabel(r"$(\ell(\ell+1)/2\pi)(\textrm{C}^{21\textrm{cm}}_{\ell} - \textrm{C}^{\textrm{debias}}_{\ell})$", fontsize=20)
    #plt.xlim(0,300)
    #plt.ylim(-1e-7,4e-7)
    plt.legend(fontsize=15);    
plt.savefig("test.jpg", dpi=300, bbox_inches='tight')
plt.show()
