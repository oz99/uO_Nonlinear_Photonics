# -*- coding: utf-8 -*-
"""
Created on Wed Nov 22 16:15:01 2023

@authors: Gabriel Flizikowski
            Ozan W. Oner

Power out / power in
Half-wave plate moving and Power meter 

"""
import pyvisa as visa
import matplotlib.pyplot as plt
import numpy as np
import logging
import time
import csv
import datetime

from Newport2936R import Newport2936R
from KDC101 import KDC101
from OPO import OPO

def calibration(x,m,b):
    return m*x+b

# Main function
def main():
    # Initialize instruments with their addresses
    pm_address = 'USB0::0x104D::0xCEC7::NI-VISA-10002::RAW'
    pm = Newport2936R(pm_address)
    
    index_number = 1
    kdc =  KDC101(index_number)
    
    serial_port = "COM21"
    baud_rate = 9600
    opo = OPO(serial_port, baud_rate)
    
    m = 0.45059
    b = -476.216*(10**-7) #
    
    # Define power levels at which to take OSA sweeps (in mW)
    # power_levels = range(1, 21, 1) #Change to 60

    try:
        # Initialize KDC101 stage with its model
        model = 'PRMTZ8'
        kdc.SetStageModel(model)
        opo.connect()
        #kdc.SendHome()
        
        ### 330 is low power ~1 uW in the PM screen
        ### 290 is ~170  in the PM screen
        # hwp_position = range(204, 209, 0.5) #Change to 60
        hwp_position = np.arange(204, 213, 1) #Change to 60
        # kdc.SetPosition(330)  # Initial position set to 160 (arbitrary units)
        #time.sleep(1)
        average_number = range(1, 4, 1)
        
        wavelengths = range(15000, 15601, 100) #wavelengths in angstroms
        
        time.sleep(1)
        
        # print(pm.GetPowerBoth())   
        
        
        # stop the measurement if the saturation point is reached
        # if counter >=6 and np.max(power_measurements[-5:,1]) - np.min(power_measurements[-5:,1]) <= 5*1e-9:
        #     print("Saturation point reached")
        #     break
        #power_measurements = np.array([['P_in in W', 'P_out in W']], dtype = object)
    
        # increment = 1000
        # kdc.StepFwd(increment)
        # kdc.StepBwd(increment)
        
        # kdc.GetPosition()
        
        for wavelength in wavelengths:
            opo.SetWavelength(wavelength)
            time.sleep(1)
            
            for num in average_number:
                
                power_measurements = np.array([['P_in in W', 'P_out in W']], dtype = object)
            
                for position in hwp_position:
                
                    kdc.SetPosition(position)
                
                    time.sleep(1)
                    
                    power_in = calibration(pm.GetPowerCH1()*1000,m,b)
                    power_out = pm.GetPowerCH2()
                    new_row = np.array([[power_in, power_out]], dtype=object)
                    power_measurements = np.vstack([power_measurements, new_row])
                
                time.sleep(1)
                
                kdc.SetPosition(204)
                
                with open('1-Dec-13-NLA-L05D0-{}nm-{}.csv'.format(wavelength, num), 'w', newline='') as csvfile:
                # Create a CSV writer object
                    csvwriter = csv.writer(csvfile)
        
                # Write the header row
        
                    csvwriter.writerows(power_measurements)
                
                    csvfile.close()
                    print(power_measurements)
        
    # except Exception as e:
    #     # Log any exceptions that occur
    #     logging.error(f"Error: {e}")
       
        # kdc.SetPosition(20)
        
    finally:
        # Close all instrument connections
        pm.close()
        kdc.obj.close()
        
if __name__ == "__main__":
    main()