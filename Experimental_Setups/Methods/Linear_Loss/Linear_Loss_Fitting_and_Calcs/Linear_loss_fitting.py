#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 2024-05-02. Formulas as given in G Tittelbach et al 1993 Pure Appl. Opt. 2 683

@author: Daniel Espinosa, Ozan Oner
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.optimize import curve_fit
from matplotlib.ticker import FormatStrFormatter

def Pout(beta, eta, R1, R2, a, L, Pinc):
    return (eta*(1-R1)*(1-R2)*np.exp(-a*L)*Pinc)/(1-2*np.sqrt(R1*R2)*np.exp(-a*L)*np.cos(2*beta*L)+R1*R2*np.exp(-2*a*L))

#########################################################
# Type the parameters of the waveguide
#
length = 5.33 # (mm) - Waveguide length in milimeters
datafile = 'NW-Ref3.lvm' # Place the data file in the same folder of this code. Write the file name here.
data = pd.read_csv(datafile,sep=' ')

alpha = 4.54 # (dB/cm) - Propagation loss coefficient in decidels per centimeters
neff = 4.02 # Effective index of the waveguide mode
eta = 0.14 # Coupling efficiency (this coefficient does not include the reflectivity of the waveguide)
Pinc = 540 # (uW) - Incident power in microwatts
Lambda = 1550 # (nm) - Central wavelength for the Fabry-Perot simulation in nanometers
#
#
#########################################################

#########################################################
# Some calculations and unit conversions
#
R1 = (neff - 1)**2 / (neff + 1)**2 # Facet 1 - Calculated Fresnell reflection coefficient
R2 = (neff - 1)**2 / (neff + 1)**2 # Facet 2 - Calculated Fresnell reflection coefficient
L = length*1e-3; # length in m
a = 100*alpha/(10 * np.log10(np.exp(1))) # alpha in m^-1
lambdam = Lambda*1e-9 # lambda in m
deltalambda = lambdam**2 / (2*L*neff) # period in m

liminf = lambdam-2.5*deltalambda
limsup = lambdam+2.5*deltalambda

x = np.linspace(liminf, limsup, 200)
beta = (2*np.pi*neff)/(x)
step = (limsup-liminf)/200 # step in nm for 200 acquisition points
#
#

#########################################################
# Calculation of output power
#
#
#Pout = eta*(1-R1)*(1-R2)*np.exp(-a*L)*Pinc

# Create sample data
y = Pout(beta, eta, R1, R2, a, L, Pinc)
plt.plot(x*1e9, y, label="Pout vs. Pinc")
#plt.annotate('Period = ',xy=((lambdam-2.5*deltalambda)*1e-9,1))
plt.xlabel('Wavelength (nm)')
plt.ticklabel_format(axis='x',useOffset=False)
#plt.gca().yaxis.set_major_formatter(StrMethodFormatter('{x:,.2f}'))
plt.ylabel('Output power (uW)')
plt.grid()
plt.show()
print('Period = ',format(deltalambda*1e9,".4f"),' nm, approximately')
print('Use the following parameters:')
print('Initial wavelength = ',format(liminf*1e9,".2f"),' nm')
print('Final wavelength = ',format(limsup*1e9,".2f"),' nm')
print('Step size = ',format(step*1e9,".4f"),' nm')



