# -*- coding: utf-8 -*-
"""
Created on Fri Oct  6 15:42:07 2023

@author: Ozan W. Oner
"""

import pyvisa as visa
import numpy as np
import matplotlib.pyplot as plt
import time
import logging

# Importing custom libraries for the optical instruments
from OSA import AQ6315B
from Newport2936R import Newport2936R
from KDC101 import KDC101
import csv
import datetime



# Constants for power adjustment loop
MAX_ITERATIONS = 100  # Max iterations for reaching the target power level
TOLERANCE = 1e-6  # Tolerance for difference between actual and target power level

# Initialize logging
logging.basicConfig(filename='lab_log.log', level=logging.INFO)

# Function to adjust the power level to the desired value
def adjust_power_level(target, pm, kdc):
    iteration = 0
    while abs(pm.GetPowerCH1() - target) > TOLERANCE:
        if iteration >= MAX_ITERATIONS:
            logging.warning("Max iterations reached for power adjustment. Exiting.")
            return False
        if pm.GetPowerCH1() < target:
            kdc.StepFwd()  # Increase power
        else:
            kdc.StepBwd()  # Decrease power
        iteration += 1
    return True

def calibration(x,m,b):
    return m*x+b


# Main function
def main():
    # Initialize instruments with their addresses
    osa_address = 'GPIB2::1::INSTR'
    osa = AQ6315B(osa_address)
    #pm_address = 'USB0::0x104D::0xCEC7::NI-VISA-40005::RAW'
    #pm =  Newport2936R(pm_address)
    #index_number = 1
   # kdc =  KDC101(index_number)
    
    # Parameters for OSA (Optical Spectrum Analyzer)
    
    # Insert Write channel selection
    # Insert 
    center = 1550
    # start_wavelength = center -20  # Start wavelength for the scan (in nm)
    # stop_wavelength = center +15  # Stop wavelength for the scan (in nm)
    start_wavelength = center # Start wavelength for the scan (in nm)
    stop_wavelength =  center +0.1 #Stop wavelength for the scan (in nm)
    resolution = 1  # Spectral resolution (in nm)
    points = 500 # Number of data points in the scan. Typically 300 when we are using 1530nm-1570nm range. Ensure time sleep is 45
    avg = 1  # Number of averages to take per point
    #!!!!!!!ref_level = -30.0  # Reference level (in dBm)
    sensitivity = 1  # Sensitivity setting either 1,2,3
    measurement_mode = "CW"
    # Insert scale params log or linear
    
    # Define power levels at which to take OSA sweeps (in mW)
    #power_levels = range(10, 31, 10) #Change to 60

    try:
        # Initialize KDC101 stage with its model
        #model = 'PRMTZ8'sition set to 160 (arbitrary units)
        #time.sleep(1)
        
        #Configure OSA settings
        time.sleep(1)
        print('done')
        osa.SetMeasurementMode(measurement_mode)
        print('done')
        time.sleep(1.5)
        #osa.SetPULSEModes("LPF")
        osa.SetStartWavelength(start_wavelength)
        print('done')
        time.sleep(1.5)
        osa.SetStopWavelength(stop_wavelength)
        time.sleep(0.5)
        osa.SetResolution(resolution)
        time.sleep(0.5)
        osa.SetPoints(points)
        time.sleep(0.5)
        osa.SetAverage(avg)
       # osa.SetSensNorm()
        # scale = 'LOG'
        scale = 'LIN'
        osa.SetScale(scale, 10.0)
        
        ## Fix the following
        #!!!!!!!!osa.SetReference(ref_level) # This is currently commented out of the OSA driver.
        
        osa.SetSensitivity(sensitivity) #This isn't currently within the OSA driver

        
        time.sleep(1)
        # osa.SingleScan()
        osa.RepeatScan()
        # osa.StopScan()
        osa.WaitForSweepFinish()
        osa.ExportScan(f"L07D0-160uW-1500nm-1.csv")

    except Exception as e:
        # Log any exceptions that occur
        logging.error(f"Error: {e}")
        
        
    finally:
        # Close all instrument connections
       # pm.close()
        osa.close()
       ## kdc.obj.close()
        
if __name__ == "__main__":
    main()
