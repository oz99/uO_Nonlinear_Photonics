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
import csv
import datetime


## This code is used to obtain the Pref vs Pinc relation for optical measurements.


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
    # osa_address = 'GPIB0::1::INSTR'
    # osa = AQ6315B(osa_address)
    pm_address = 'USB0::0x104D::0xCEC7::NI-VISA-10002::RAW'
    pm =  Newport2936R(pm_address)
    index_number = 1
    kdc =  KDC101(index_number)
    
    # Parameters for OSA (Optical Spectrum Analyzer)
    # start_wavelength = 1530  # Start wavelength for the scan (in nm)
    # stop_wavelength = 1570  # Stop wavelength for the scan (in nm)
    # resolution = 1.0  # Spectral resolution (in nm)
    # points = 100  # Number of data points in the scan
    # avg = 3  # Number of averages to take per scan
    # ref_level = 30.0  # Reference level (in dBm)
    # sensitivity = 'SHI1'  # Sensitivity setting
    
    # Define power levels at which to take OSA sweeps (in mW)
    power_levels = range(10, 120, 10) #Change to 60

    try:
        # Initialize KDC101 stage with its model
        model = 'PRMTZ8'
        kdc.SetStageModel(model)
        
        #kdc.SendHome()
        #kdc.SetPosition(110)  # Initial position set to 160 (arbitrary units)
        #time.sleep(1)

        
        time.sleep(1)
            
        power_measurements = np.array([['CH1_Power', 'CH2_Power']], dtype=object)
# #Attempt 3 - Dynamic Power Tuning for more accurate measurements. It works!!!
           
        for level in power_levels:
            iteration_count = 0
            max_iterations = 100  # Set a limit to avoid infinite loop
            
            print(f"Setting power to {level} mW...")
            
            print(pm.GetPowerCH1())
            print(level*10**-6)
            
            # while abs(pm.GetPowerCH1() - level*10**-6)/(level*10**-6) > 0.25:  # Adjust to your required precision #Should be > 
            #     if iteration_count >= max_iterations:
            #         print("Maximum iterations reached. Breaking the loop.")
            #         break
                
            #     increment = 10000
        
            #     if pm.GetPowerCH1() < level*10**-6:
            #         print("Stepping forward...")
            #         kdc.StepFwd(increment)
            #         # kdc.SetPosition(200)
            #     else:
            #         print("Stepping backward...")
            #         kdc.StepBwd(increment)
            #         # kdc.SetPosition(100)
                    
            #     iteration_count += 1
            #     time.sleep(0.5)  # Time to allow the power to stabilize
                
            while abs(pm.GetPowerCH1() - level*10**-6)/(level*10**-6) > 0.10:  # Adjust to your required precision #Should be > 
                if iteration_count >= max_iterations:
                    print("Maximum iterations reached. Breaking the loop.")
                    break
                
                increment = 2000
        
                if pm.GetPowerCH1() < level*10**-6:
                    print("Stepping forward...")
                    kdc.StepFwd(increment)
                    # kdc.SetPosition(200)
                else:
                    print("Stepping backward...")
                    kdc.StepBwd(increment)
                    # kdc.SetPosition(100)
                    
                iteration_count += 1
                time.sleep(0.5)  # Time to allow the power to stabilize
                
            while abs(pm.GetPowerCH1() - level*10**-6)/(level*10**-6) > 0.025:  # Adjust to your required precision #Should be > 
                if iteration_count >= max_iterations:
                    print("Maximum iterations reached. Breaking the loop.")
                    break
                
                increment = 250 # Step which the KDC Cube will take X amount is ~ X degrees
        
                if pm.GetPowerCH1() < level*10**-6:
                    print("Stepping forward...")
                    kdc.StepFineFwd(increment)
                    # kdc.SetPosition(200)
                else:
                    print("Stepping backward...")
                    kdc.StepFineBwd(increment)
                    # kdc.SetPosition(100)
                    
                iteration_count += 1
                time.sleep(0.5)  # Time to allow the power to stabilize
        
 ## Turned off plotting for troubleshooting
            column1 = pm.GetPowerCH1()
            column2 = pm.GetPowerCH2() 
            new_row = np.array([[column1, column2]], dtype=object)
            power_measurements = np.vstack([power_measurements, new_row])

        with open('power_readingsA2.csv', 'w', newline='') as csvfile:
            # Create a CSV writer object
            csvwriter = csv.writer(csvfile)

            # Write the header row

            csvwriter.writerows(power_measurements)
            
            csvfile.close()
        print(power_measurements)

        # # Move the HWP to below 5mW to avoid burning a sample 
        # if pm.GetPowerCH1() < 5*10**-6:
        #     print("Stepping forward...")
        #     kdc.StepFwd(increment)
        #     # kdc.SetPosition(200)
        # else:
        #     print("Stepping backward...")
        #     kdc.StepBwd(increment)
        #     # kdc.SetPosition(100)
        
    except Exception as e:
        # Log any exceptions that occur
        logging.error(f"Error: {e}")
        
    finally:
        # Close all instrument connections
        pm.close()
        # osa.close()
        kdc.obj.close()
        
if __name__ == "__main__":
    main()
