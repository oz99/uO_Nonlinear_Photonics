# -*- coding: utf-8 -*-
"""
Created on Tue Sep 12 09:12:56 2023

@author: Ozan W. Oner, ooner083@uottawa.ca
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
from OPO import OPO

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
    
    pm_address = 'USB0::0x104D::0xCEC7::NI-VISA-10002::RAW'    
    pm =  Newport2936R(pm_address)
    
    index_number = 1
    kdc =  KDC101(index_number)
    
    serial_port = "COM21"
    baud_rate = 9600
    opo = OPO(serial_port, baud_rate)
    
    # Parameters for OSA (Optical Spectrum Analyzer)
    
    # Insert Write channel selection
    # Insert 
    resolution = 1  # Spectral resolution (in nm)
    points =  500 # Number of data points in the scan. Typically 300 when we are using 1530nm-1570nm range. Ensure time sleep is 45
    avg = 1  # Number of averages to take per point
    #!!!!!!!ref_level = -30.0  # Reference level (in dBm)
    sensitivity = 1 # Sensitivity setting either 1,2,3
    measurement_mode = "CW"
    # Insert scale params log or linear
    
    # Define power levels at which to take OSA sweeps (in mW)
    # power_levels = range(14,15,1) #[50, 60] # range(50, 51, 1) #Change to 60
    
    m = 0.45059
    b = -476.216*(10**-7) #

    try:
        # Initialize KDC101 stage with its model
        model = 'PRMTZ8'
        kdc.SetStageModel(model)
        opo.connect()
        
        #kdc.SendHome()
        #kdc.SetPosition(110)  # Initial position set to 160 (arbitrary units)
        #time.sleep(1)
        
        # Configure OSA settings
        # osa.SetMeasurementMode(measurement_mode)
        #osa.SetPULSEModes("LPF")
        # osa.SetResolution(resolution)
        # osa.SetPoints(points)
        # osa.SetAverage(avg)
        #osa.SetSensNorm()
        
        # ## Fix the following
        # #!!!!!!!!osa.SetReference(ref_level) # This is currently commented out of the OSA driver.
        # osa.SetSensitivity(sensitivity) #This isn't currently within the OSA driver

        
        time.sleep(1)
        
        #scale = 'LOG'
        # scale = 'LIN'
        # osa.SetScale(scale, 10.0)
        # time.sleep(1)
        
        # power_measurements = np.array([['P_in in W', 'P_out in W']], dtype = object)
        # merda = calibration(pm.GetPowerCH1()*1000,m,b)/0.001
        # print("Power is {:.2f}mW".format(merda))

        hwp_position = np.arange(204, 213, 1) #Change to 60
        # kdc.SetPosition(330)  # Initial position set to 160 (arbitrary units)
        #time.sleep(1)
        average_number = range(1, 4, 1)
        
        wavelengths = range(15000, 15601, 100) #wavelengths in angstroms
# #Attempt 3 - Dynamic Power Tuning for more accurate measurements. It works!!!
         
  
        for wavelength in wavelengths:
            opo.SetWavelength(wavelength)
            time.sleep(1)
            center = wavelength*0.1
            start_wavelength = center -20  # Start wavelength for the scan (in nm)
            stop_wavelength = center +15  # Stop wavelength for the scan (in nm)
            # wavelength = 15500 # wavelength in angstrons
            osa.SetStartWavelength(start_wavelength)
            time.sleep(1)
            
            osa.SetStopWavelength(stop_wavelength)
            time.sleep(1) 
            
            for position in hwp_position:
                
                time.sleep(1)
                print('shit here')
                kdc.SetPosition(position)
                 
                time.sleep(1)
            
                power = calibration(pm.GetPowerCH1()*1000,m,b)/0.001
               
                print("Taking an OSA sweep...")
               
                time.sleep(1)  # Time to allow the power to stabilize
               
                osa.SingleScan()
                osa.WaitForSweepFinish()
               
                osa.ExportScan("SPM-NA-WG-SERP-L1-D0-{}nm-{:.5f}mW-18dec23.csv".format(center,power))
               
            kdc.SetPosition(204)
        

        
    except Exception as e:
        # Log any exceptions that occur
        logging.error(f"Error: {e}")
        
    finally:
        # Close all instrument connections
        pm.close()
        osa.close()
        kdc.obj.close()
        opo.close()
        
if __name__ == "__main__":
    main()
