#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 2024-05-02. Formulas as given in G Tittelbach et al 1993 Pure Appl. Opt. 2 683

@authors: Daniel Espinosa, Ozan Oner
	
"""

import matplotlib.pyplot as plt
import numpy as np

#########################################################
# Type the parameters for the calculation
#
length = 5.26 # (mm) - Waveguide length in milimeters.
Pref = 468 # (uW) - Reference power in microwatts.
Factor1 = 0.74 # Pinc = Factor1*Pref - This factor should be measured before or after the experiments
Factor2 = 0.89 # Pdet = Factor2*Pout - This factor should be measured before or after the experiments
Pdetmax = 29.6 # (uW) - Power of one of the Fabry-Perot peaks measured by the detector at the output.
Pdetmin = 16.7 # (uW) - Power of one of the Fabry-Perot valleys measured by the detector at the output.
Lambda1 = 1550.050 # (nm) - Wavelength of the first peak (or valley) of one full cycle.
Lambda2 = 1549.988 # (nm) - Wavelength of the second peak (or valley) of one full cycle.
#
#
#########################################################

#########################################################
# Some calculations and unit conversions
#
Pinc = Pref*Factor1*1e-6 # P incident in W
Pmax = (Pdetmax*1e-6)/Factor2 # P output max in W
Pmin = (Pdetmin*1e-6)/Factor2 # P output min in W
L = length*1e-3 # length in m
lambda1 = Lambda1*1e-9 # Lambda1 in m
lambda2 = Lambda2*1e-9 # Lambda2 in m
deltalambda = np.abs(lambda2 - lambda1) # Fabry-Perot oscillation period in m
lambdam = (lambda1 + lambda2)/2 # central wavelength in m
neff = lambdam**2 / (2*L*deltalambda) # Effective index
R = (neff - 1)**2 / (neff + 1)**2 # Facet 1 - Calculated Fresnell reflection coefficient
TL = -10*np.log10(((Pmax+Pmin)/2)/Pinc)
K = (Pmax - Pmin)/(Pmax + Pmin)
alphacm = -np.log((1-np.sqrt(1-K**2))/(R*K))/(100*L) # alpha in cm^-1
alphadB = alphacm*(10 * np.log10(np.exp(1))) # alpha in dB/cm
PL = alphadB*L*1e2 # Propagation loss in dB
RL = -10*np.log10(1-R) # Reflection loss per facet in dB
CL = TL - PL - 2*RL #+ 10*np.log10(1-R) # coupling loss in dB

#######################################################################
# Printed output
print('Period = ',format(deltalambda*1e12,".2f"),' pm')
print('Reflection coefficient per facet = ',format(R,".2f"))
print('-----------------------------------')
print('Total loss = ',format(TL,".2f"),' dB')
print('--Propagation loss = ',format(PL,".2f"),' dB')
print('--Reflection loss input facet = ',format(RL,".2f"),' dB')
print('--Reflection loss output facet = ',format(RL,".2f"),' dB')
print('--Coupling loss (input facet, excluding R) = ',format(CL,".2f"),' dB')
print('-----------------------------------')
print('Effective index = ',format(neff,".2f"))
print('Propagation loss coefficient) = ',format(alphadB,".2f"),' dB/cm')
print('Propagation loss coefficient) = ',format(alphacm,".2f"),' cm^-1')
