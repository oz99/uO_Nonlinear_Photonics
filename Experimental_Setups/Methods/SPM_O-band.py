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

# Main function
def main():
    # Initialize instruments with their addresses
    osa_address = 'GPIB0::1::INSTR'
    osa = AQ6315B(osa_address)
    pm_address = 'USB0::0x104D::0xCEC7::NI-VISA-40005::RAW'
    pm =  Newport2936R(pm_address)
    index_number = 0
    kdc =  KDC101(index_number)
    
    # Parameters for OSA (Optical Spectrum Analyzer)
    start_wavelength = 1308  # Start wavelength for the scan (in nm)
    stop_wavelength = 1315  # Stop wavelength for the scan (in nm)
    resolution = 2.0  # Spectral resolution (in nm)
    points = 100  # Number of data points in the scan
    avg = 10  # Number of averages to take per scan
    ref_level = -60  # Reference level (in dBm)
    sensitivity = 'SHI1'  # Sensitivity setting
    
    # Define power levels at which to take OSA sweeps (in mW)
    power_levels = range(10, 61, 10)
    
    try:
        # Initialize KDC101 stage with its model
        model = 'PRMTZ8'
        kdc.SetStageModel(model)
        
        kdc.SendHome()
        #kdc.SetPosition(110)  # Initial position set to 160 (arbitrary units)
        #time.sleep(1)
        
        # Configure OSA settings
        osa.SetStartWavelength(start_wavelength)
        osa.SetStopWavelength(stop_wavelength)
        osa.SetResolution(resolution)
        osa.SetPoints(points)
        osa.SetAverage(avg)
        #osa.SetReference(ref_level) # This is currently commented out of the OSA driver.
        #osa.SetSensitivity(sensitivity) #This isn't currently within the OSA driver
        
        time.sleep(1)
            
# #Attempt 2 at portion above            
        for level in power_levels:
            iteration_count = 0
            max_iterations = 100  # Set a limit to avoid infinite loop
            
            print(f"Setting power to {level} mW...")
            
            while abs(pm.GetPowerCH1() - level) > 0.000001:  # Adjust to your required precision #Should be > 
                if iteration_count >= max_iterations:
                    print("Maximum iterations reached. Breaking the loop.")
                    break
        
                if pm.GetPowerCH1() < level:
                    print("Stepping forward...")
                    kdc.StepFwd()
                    # kdc.SetPosition(200)
                else:
                    print("Stepping backward...")
                    kdc.StepBwd()
                    # kdc.SetPosition(100)
                    
                iteration_count += 1
                time.sleep(0.5)  # Time to allow the power to stabilize
        
            print("Taking an OSA sweep...")
            osa.SingleScan()
            time.sleep(20)  # Time for the scan to complete
            osa.ExportScan(f"{level}mW test_potatoes")


    except Exception as e:
        # Log any exceptions that occur
        logging.error(f"Error: {e}")
        
    finally:
        # Close all instrument connections
        pm.close()
        osa.close()
        kdc.obj.close()
        
if __name__ == "__main__":
    main()
