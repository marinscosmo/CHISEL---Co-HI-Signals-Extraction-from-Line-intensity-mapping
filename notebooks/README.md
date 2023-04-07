
This code is a extension for the BINGO Telescope from 
 - GMCA (from Jean Luc Starck, Jerome Bobin and Isabella Carucci 's code ) 
 - (fast)ICA (with scikit-learn code) methods
 
It's a public code, but if you will use it I would like you to quote us:
 - Generalised Morphological Component Analysis applied to HI signals from Intensity Mapping - A. Marins et al (in preparation)
 - Different Component Separation Methods for BINGO Telescope - A. Marins et al (in preparation)
 
It was create by 
 - Alessandro Marins (USP)
 - Filipe Abdalla (UCL, USP, INPE and RU)

USP  = Universidade de Sao Paulo (Brazil)
INPE = Instituto Nacional de Pesquisas Espaciais (Brazil)
UCL  = University College London (UK)
RU   = Rhodes University (South Africa)
 
I'd like to thank Isabella Carucci and Jerome Bobin for send us your GMCA code used on MeerKAT analysis

Necessary non-native python3 packages:
 - numpy >= 1.19.4
 - pandas >= 0.25.3
 - scikit-learn >= 0.22.2.post1
 - pys2let >= 2.2.1
 - healpy >= 1.13.0
 - astropy >= 4.1
 - gmca4im_lib2 (https://github.com/isab3lla/gmca4im)
 - PyWavelets >= 1.1.1
 - progressbar2 >=3.53.1
 - mtneedlet >=0.0.5
 
At the moment, this code contain:
 - (1) Wavelet Transform:
     - (1.1) Identity Wavelet Transform
     - (1.2) Starlet on the Sphere (Isotropic Undecimated Wavelet Transform by Jean-Luc Starck)
     - (1.3) Axisymmetric Wavelet Transform on the Sphere (by Jason McEwen)
     - (1.4) PyWavelets = Python Package for Redundant Wavelet Transforms
     - (1.5) Needlets from MTNeedlet package (https://javicarron.github.io/mtneedlet/index.html)
 - (2) Component Separation Method:
     - (2.1) Generalized Morphological Component Analysis (GMCA) by Jerome Bobin and Isabella Carucci
     - (2.2) Fast Independent Component Analysis (FastICA) by Scikit-Learn python package
     
Last update: July/21/2021
If you have any questions about that, please contact us:
 - alessandro.marins@usp.br

