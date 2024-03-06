from cProfile import label
import pandas as pd
import matplotlib.pyplot as plt
# from scipy.optimize import curve_fit
import numpy as np
import scipy

########### Load DataSet ############
file_name = 'InGaAsP_InP_NW_dispersion'
dataTE = pd.read_csv(file_name+'_TE.csv')
# dataTM = pd.read_csv(file_name+'_TM.txt')
c = scipy.constants.c

########### check if the data is properly imported
# print(dataTE)
# print(dataTE.lambda0r)
# print(dataTE.Effective_mode_index)

lamb = dataTE.lambda0r
freq = c/lamb
beta = dataTE.Propagation_constant

########### Interpolation ############
span = 300 # [nm]
step = 5 # [nm]
lamb_center = 1550 # [nm]
freq_center = c*1e9/lamb_center # [Hz]
fit_range = np.arange(-span/2, span/2+step, step)  # [nm].
center_ind = np.where(fit_range==0)[0][0]
lamb_interp = (lamb_center-fit_range)*1e-9  # [m], decreasing values
freq_interp = c/lamb_interp - freq_center # [Hz]
beta_interp = np.interp(freq_interp*2*np.pi, (np.flip(freq)-freq_center)*2*np.pi, np.flip(beta))
# vg_interp = np.interp(freq_interp*2*np.pi, (np.flip(dataTE.f)-freq_center)*2*np.pi, np.flip(dataTE.vg))
print(beta_interp[center_ind])
# print(vg_interp[center_ind])

# ########### Plot to check interpolation ############
# plt.plot((freq-freq_center)*2*np.pi, beta, 'o', label='sim')
# plt.plot(freq_interp*2*np.pi, beta_interp, '*', label='interp')
# plt.show()

########### Polynomial fit ############
fit = np.polynomial.polynomial.polyfit(freq_interp*2*np.pi, beta_interp, 5)

print("group velocity = " + str(1/fit[1]) + " m/s")
print("beta2 = " + str(2*fit[2]) + " s^2/m")
print("beta3 = " + str(6*fit[3]) + " s^3/m")
print("beta4 = " + str(24*fit[4]) + " s^4/m")

# ########### Plot to check the fit ############
# plt.plot((freq-freq_center)*2*np.pi, beta)
# plt.plot(freq_interp*2*np.pi, fit[0]+fit[1]*freq_interp*2*np.pi)

# plt.xlabel('Frequency (THz)')
# plt.ylabel('beta_real (1/m)')
# # plt.legend()
# # # plt.savefig('neff.pdf')
# plt.show()

# ########### Plot ############
# plt.plot(freq_interp*2*np.pi, beta_interp-fit[0]-fit[1]*freq_interp*2*np.pi)
# plt.plot(freq_interp*2*np.pi, fit[2]*(freq_interp*2*np.pi)**2+fit[3]*(freq_interp*2*np.pi)**3)
# # plt.plot((np.flip(dataTE.f)-freq_center)*2*np.pi, fit[0]+fit[1]*(np.flip(dataTE.f)-freq_center)*2*np.pi+fit[2]*np.square((np.flip(dataTE.f)-freq_center)*2*np.pi))
# plt.xlabel('Frequency (THz)')
# plt.ylabel('beta_real (1/m)')
# # plt.legend()
# # # plt.savefig('neff.pdf')
# plt.show()

########### Repeat the process changing the central wavelength ############
det = np.arange(10.0, 100, 2) # [nm]
lamb_s = 1550 # [nm]
lamb_p = lamb_s-det # [nm]
lamb_i = lamb_p*lamb_s/(2*lamb_s-lamb_p)
vgp = np.arange(0.0, len(det), 1)
beta2p = np.arange(0.0, len(det), 1)
beta3p = np.arange(0.0, len(det), 1)
beta4p = np.arange(0.0, len(det), 1)
vgi = np.arange(0.0, len(det), 1)
beta2i = np.arange(0.0, len(det), 1)
beta3i = np.arange(0.0, len(det), 1)
beta4i = np.arange(0.0, len(det), 1)

for ind, lamp in enumerate(lamb_p):
    ########### Interpolation ############
    span = 300 # [nm]
    step = 5 # [nm]
    lamb_center = lamp # [nm]
    freq_center = c*1e9/lamb_center # [Hz]
    fit_range = np.arange(-span/2, span/2+step, step)  # [nm].
    center_ind = np.where(fit_range==0)[0][0]
    lamb_interp = (lamb_center-fit_range)*1e-9  # [m], decreasing values
    freq_interp = c/lamb_interp - freq_center # [Hz]
    # print(np.diff(freq_interp))
    beta_interp = np.interp(freq_interp*2*np.pi, (np.flip(freq)-freq_center)*2*np.pi, np.flip(beta))
    # vg_interp = np.interp(freq_interp*2*np.pi, (np.flip(freq)-freq_center)*2*np.pi, np.flip(dataTE.vg))

    ########### Polynomial fit ############
    fit = np.polynomial.polynomial.polyfit(freq_interp*2*np.pi, beta_interp, 5)
    beta2p[ind] = 2*fit[2]
    beta3p[ind] = 6*fit[3]
    beta4p[ind] = 24*fit[4]
    vgp[ind] = 1/fit[1]
    # vgp[ind] = vg_interp[center_ind]

########### Plot dispersion ############
plt.plot(lamb_p, beta2p)

plt.xlabel('Wavelength (nm)')
plt.ylabel('beta_2 (s^2/m)')
# plt.legend()
# # plt.savefig('neff.pdf')
plt.show()
    
########### Repeat the process changing the idler's wavelength ############
# for ind, lami in enumerate(lamb_i):
#     ########### Interpolation ############
#     span = 300 # [nm]
#     step = 5 # [nm]
#     lamb_center = lami # [nm]
#     freq_center = c*1e9/lamb_center # [Hz]
#     fit_range = np.arange(-span/2, span/2+step, step)  # [nm].
#     center_ind = np.where(fit_range==0)[0][0]
#     lamb_interp = (lamb_center-fit_range)*1e-9  # [m], decreasing values
#     freq_interp = c/lamb_interp - freq_center # [Hz]
#     # print(np.diff(freq_interp))
#     beta_interp = np.interp(freq_interp*2*np.pi, (np.flip(dataTE.f)-freq_center)*2*np.pi, np.flip(dataTE.beta_real))
#     vg_interp = np.interp(freq_interp*2*np.pi, (np.flip(dataTE.f)-freq_center)*2*np.pi, np.flip(dataTE.vg))

#     ########### Polynomial fit ############
#     fit = np.polynomial.polynomial.polyfit(freq_interp*2*np.pi, beta_interp, 5)
#     beta2i[ind] = 2*fit[2]
#     beta3i[ind] = 6*fit[3]
#     beta4i[ind] = 24*fit[4]
#     vgi[ind] = 1/fit[1]
#     # vgi[ind] = vg_interp[center_ind]
# print(beta2i)
    
########### Save dispersion data ############
# beta_interp_p = np.interp(c*1e9/lamb_p, np.flip(freq), np.flip(beta))
# beta_interp_i = np.interp(c*1e9/lamb_i, np.flip(freq), np.flip(beta))
# # scipy.io.savemat('Disp5.mat', dict(detuning=det, groupVelocityPump=vgp, dispersionPump=beta2p, dispersionPump3=beta3p, dispersionPump4=beta4p, groupVelocityIdler=vgi, dispersionIdler=beta2i, dispersionIdler3=beta3i, dispersionIdler4=beta4i, betaPump=beta_interp_p, betaIdler=beta_interp_i))
