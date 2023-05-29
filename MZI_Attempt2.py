#This document attempted to use a TSL-710 tunable laser and an ANDO AQ6317B Optical 
# Spectrum Analyzer to measure the transmission spectrum of a MZI.
# The implementation was unsuccesful as we used a super continuum source for ease of use
# This document was included within the library to help with automation of laboratory equipment

import numpy as np
import pyvisa

class OSAController:

    def __init__(self):
        self.initialize_instruments()

    def initialize_instruments(self):
        from globalsFile import *
        from __santecTSL1__ import *
        from SantecTSL710 import SantecTSL710

        # Initialize the VISA resource manager
        rm = pyvisa.ResourceManager()

        # Open the laser and OSA resources
        self.laser = SantecTSL710('GPIB0::0::INSTR')
        self.ANDO = rm.open_resource('GPIB0::1::INSTR')

    def get_trace(self, trace):
        wl = self.ANDO.query('WDAT'+trace).strip().split(',')[1:]
        intensity = self.ANDO.query('LDAT'+trace).strip().split(',')[1:]
        wl = np.asarray(wl,'f').T
        intensity = np.asarray(intensity,'f').T
        return wl, intensity

    def save_trace(self, wl, intensity, filename):
        wl = np.asarray(wl,'str')
        intensity = np.asarray(intensity,'str')
        data = np.column_stack((wl, intensity))
        
        with open(filename+'.txt', "w") as txt_file:
            for line in data:
                txt_file.write(" ".join(line) + "\n")
        return

    def change_range(self, start, stop):
        self.ANDO.query('STAWL'+start+'.00')
        self.ANDO.query('STPWL'+stop+'.00')

    def set_laser_wavelength(self, wavelength):
        self.laser.setWavelength(wavelength)

    def increment_wavelength(self, increment=1):
        start_wl = float(self.ANDO.query('STAWL?'))
        stop_wl = float(self.ANDO.query('STPWL?'))
        laser_wl = self.laser.getWavelength()

        self.change_range(str(start_wl + increment), str(stop_wl + increment))
        self.set_laser_wavelength(laser_wl + increment)

    def perform_measurement_and_save_trace(self, trace, filename_prefix):
        wl, intensity = self.get_trace(trace)
        self.save_trace(wl, intensity, f"{filename_prefix}_{wl[0]}_to_{wl[-1]}")

    def combine_traces(self, filenames, output_filename):
        combined_data = []

        for filename in filenames:
            with open(filename + '.txt', 'r') as file:
                data = [line.strip().split() for line in file.readlines()]
                combined_data.extend(data)

        with open(output_filename + '.txt', 'w') as output_file:
            for line in combined_data:
                output_file.write(" ".join(line) + "\n")
    
    def close_instruments(self):
        self.laser.close()
        self.ANDO.close()

#%%
# Create an instance of the OSAController class
osa_controller = OSAController()

# Set the initial wavelength range, perform measurements, save traces, and combine them
# (same as the previous example)
osa_controller.change_range("1500", "1501")
osa_controller.set_laser_wavelength(1500)
osa_controller.perform_measurement_and_save_trace('A', 'filename')
filenames = ['filename_1500.0_to_1600.0']

for _ in range(5):  # Change the number of iterations as needed
    osa_controller.increment_wavelength()
    osa_controller.perform_measurement_and_save_trace('A', 'filename')
    start_wl = float(osa_controller.ANDO.query('STAWL?'))
    stop_wl = float(osa_controller.ANDO.query('STPWL?'))
    filenames.append(f"filename_{start_wl}_to_{stop_wl}")

osa_controller.combine_traces(filenames, 'combined_traces')

# Close the laser and OSA connections
osa_controller.close_instruments()


#%%