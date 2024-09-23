# -*- coding: utf-8 -*-
"""
Created on Fri Sep 20 13:42:10 2024

@author: ooner083
"""


import os

os.chdir('C:/Users/ooner083/.spyder-py3')
import pyvisa as visa
import matplotlib.pyplot as plt
import time
import logging
from TC300_COMMAND_LIB import TC300
import csv
from pymeasure.instruments.keithley import Keithley2450
import numpy as np


# Importing custom libraries for the optical instruments
from OSA import AQ6315B
#from Newport2936R import Newport2936R
#from KDC101 import KDC101
import datetime
import pandas as pd


# Initialize logging
logging.basicConfig(filename='lab_log.log', level=logging.INFO)

time.sleep(120)

# Number of experiment runs
num_runs = 1  # Modify this number based on how many times you want the experiment to run

def main(run_index):
    

    keith_address = 'USB0::0x05E6::0x2450::04577394::INSTR'
    sourcemeter = Keithley2450(keith_address)
    
    # Initialize instruments with their addresses
    osa_address = 'GPIB0::1::INSTR'
    osa = AQ6315B(osa_address)
    #osa.reset_inst()
   # osa.GetInfo()
    
    #osa.GetResolution()
    #osa.StopScan()
  
    # Parameters for OSA (Optical Spectrum Analyzer)
    
    # Insert Write channel selection
    # Insert 
    start_wavelength = 1260 # Start wavelength for the scan (in nm)
    stop_wavelength =  1290 # Stop wavelength for the scan (in nm)
    resolution = 0.2  # Spectral resolution (in nm)
    points =  5000 # Number of data points in the scan. Typically 300 when we are using 1530nm-1570nm range. Ensure time sleep is 45
    avg = 1  # Number of averages to take per point
    #!!!!!!!ref_level = -30.0  # Reference level (in dBm)
    scale = 'LOG' #'LIN' or 'LOG'
    sensitivity = 1  # Sensitivity setting either 1,2,3
    measurement_mode = "CW"
    osa.StopScan()



    # Prepare CSV file for storing results, unique filename for each run
    csv_filename = f'PIV_OSA_1EB12_wateroff_MAX200mW_run{run_index}.csv'
    with open(csv_filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Current (mA)', 'Voltage (V)'])



    ascending = np.linspace(0, 200, 200)  # Adjust range and number of points as needed
    descending = np.linspace(200, 0, 200)  # Adjust range and number of points as needed
    currents = np.append(ascending,descending)
    
    voltages = []

    try:
        # Sourcemeter setup
        sourcemeter.apply_current()
        sourcemeter.source_current_range = 200e-3
        sourcemeter.compliance_voltage = 5
        sourcemeter.source_current = 0
        sourcemeter.enable_source()
        sourcemeter.measure_voltage()



        for current in currents:
            sourcemeter.ramp_to_current((current*1e-3))
            time.sleep(5)  # Stabilization time




            voltage = sourcemeter.voltage
            voltages.append(voltage)
            
            # Configure OSA settings
            osa.SetMeasurementMode(measurement_mode)
            #osa.SetPULSEModes("LPF")
            osa.SetStartWavelength(start_wavelength)
            time.sleep(1)
            osa.SetStopWavelength(stop_wavelength)
            osa.SetResolution(resolution)
            osa.SetPoints(points)
            osa.SetAverage(avg)
            

            osa.SetScale(scale, 10.0)
            
            ## Fix the following
            #!!!!!!!!osa.SetReference(ref_level) # This is currently commented out of the OSA driver.
            # osa.SetSensitivity(sensitivity) #This isn't currently within the OSA driver

            
            time.sleep(1)
            
            osa.SingleScan()
           # osa.StopScan()
            # osa.RepeatScan()
            
            #osa.StopScan()
            osa.WaitForSweepFinish()
            
            file_name = 'LOG_OSA_sweep_1EB12_1275nm_at_{}mW_room_temp.csv'.format(current)
            
            osa.ExportScan(file_name)
            

            df = pd.read_csv(file_name, sep='\t', header=None)
            
            # Assuming the first column is wavelength and the second is power, naming the columns accordingly
            df.columns = ['Wavelength', 'Power']
            
            # Plotting the data
            plt.figure(figsize=(12, 7))
            plt.plot(df['Wavelength'], df['Power'], label='Power vs. Wavelength', color='blue')
            plt.xlabel('Wavelength (nm)', fontsize=14)
            plt.ylabel('Power (dBm)', fontsize=14)
            plt.title('Power Spectrum at {}mW'.format(current), fontsize=16) 
            plt.legend()
            plt.grid(True)
            plt.tight_layout()
            plt.savefig(f'OSA_PIV_sweep_no_temp{run_index}.png')
            plt.show()


            with open(csv_filename, mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([current, voltage])

    finally:
        # Clean up and plot
        sourcemeter.shutdown()
        osa.close()
        
        plt.figure()
        plt.plot(currents, voltages, '-o')
        plt.xlabel('Current (mA)')
        plt.ylabel('Voltage (V)')
        plt.title('Current vs Voltage')
        plt.grid(True)
        plt.savefig(f'current_vs_voltage_run{run_index}.png')
        plt.show()

if __name__ == "__main__":
    for i in range(1, num_runs + 1):
        main(i)
