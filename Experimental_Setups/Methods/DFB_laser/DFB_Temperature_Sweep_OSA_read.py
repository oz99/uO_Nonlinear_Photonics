# -*- coding: utf-8 -*-
"""
Created on Fri Oct 06 14:49:12 2023

@author: Lisa Fischer, lfisc035@uottawa.ca
        Ozan Oner, ooner083@uottawa.ca
"""

import pyvisa as visa
import numpy as np
import matplotlib.pyplot as plt
import time
import logging

# Importing custom libraries for the optical instruments
from OSA import AQ6315B
from TC300_COMMAND_LIB import TC300
#from Newport2936R import Newport2936R
#from KDC101 import KDC101
import csv
import datetime


# Initialize logging
logging.basicConfig(filename='lab_log.log', level=logging.INFO)

def CheckDeviceStatus(output):
    if (output & 2**2)>>2 == 1:
            print('Normal operation.')
    elif (output & 2**3)>>3 == 1:
        if (output & 2**4)>>4 == 1:
            print('There is a warning and an error!')
            #warning = self.instrument.query('WARN?')
            #error = self.instrument.query('ERR?')
            #print(warning)
            #print(error)
        else:
            print('There is a warning for the TC300')
            #warning = self.instrument.query('WARN?')
            #print(warning)
        
    else:
        print('There is an error for the TC300!')
        #error = self.instrument.query('ERR?')
        #print(error)
        
    return


# Main function
def main():
    # Initialize instruments with their addresses
    osa_address = 'GPIB0::1::INSTR'
    tc_adress = '' # to be defined
    tc = TC300()
    try:
        devs = TC300.list_devices()
        print(devs)
        if len(devs) <= 0:
            print('There is no devices connected')
            exit()
        device_info = devs[0]
        sn = device_info[0]
        print("connect ", sn)
        hdl = tc.open(sn, 115200, 3)
        if hdl < 0:
            print("open ", sn, " failed")
            exit()
        if tc.is_open(sn) == 0:
            print("TC300IsOpen failed")
            tc.close()
            exit()
        osa = AQ6315B(osa_address)
        #pm_address = 'USB0::0x104D::0xCEC7::NI-VISA-40005::RAW'
        #pm =  Newport2936R(pm_address)
        
        # Parameters for OSA (Optical Spectrum Analyzer)
        time.sleep(15)
        # Insert Write channel selection
        # Insert 
        start_wavelength = 1250  # Start wavelength for the scan (in nm)
        stop_wavelength = 1265  # Stop wavelength for the scan (in nm)
        resolution = 0.1  # Spectral resolution (in nm)
        points =  1000 # Number of data points in the scan. Typically 300 when we are using 1530nm-1570nm range. Ensure time sleep is 45
        avg = 3  # Number of averages to take per point
        #!!!!!!!ref_level = -30.0  # Reference level (in dBm)
        sensitivity = 1  # Sensitivity setting either 1,2,3
        # Insert scale params log or linear
        
        # Define power levels at which to take OSA sweeps (in mW)
        #temperature_levels = range(20, 51, 1) #Change to 60
        temperature_levels = range(31, 52,1)

    
        # # Initialize KDC101 stage with its model
        
        
        # Configure OSA settings
        osa.SetMeasurementMode('CW')
        # # #osa.SetPulseMeasurement('LPF')
        osa.SetStartWavelength(start_wavelength)
        osa.SetStopWavelength(stop_wavelength)
        osa.SetResolution(resolution)
        osa.SetPoints(points)
        osa.SetAverage(avg)
        
        # ## Fix the following
        # #!!!!!!!!osa.SetReference(ref_level) # This is currently commented out of the OSA driver.
        # #osa.SetSensitivity(sensitivity) 
        status = tc.get_status([0b11111111])
        CheckDeviceStatus(status[0])
        #print(tc.get_warning_message([0b11111111])[0])
        print('Status: ',status)
        tc.set_brightness(35)
        channel = 2
        tc.set_mode(channel,0)
        tc.set_min_temperature(channel, 10)
        tc.set_max_temperature(channel,70)
        tc.set_max_current(channel, 2)
        tc.set_max_voltage(channel, 5)
        #tc.set_target_temperature(1,20)
        tc.enable_channel(channel,1)
        tc.set_autoPID_ctrl(1, 1)
        time.sleep(1)
            
            
        
        for level in temperature_levels:
            
            tc.set_target_temperature(channel, level)
            print(f"Setting temperature to {level} °C...")
            
                    
                
            while abs(level - tc.get_actual_temperature(channel, [level])[0] ) >= 0.1:  # Adjust to your required precision 
                time.sleep(1)
                print(tc.get_actual_temperature(channel, [level])[0])
                
            
            time.sleep(2)
            print("Taking an OSA sweep...")
            time.sleep(1)  # Time to allow the power to stabilize
            osa.SingleScan()
            osa.WaitForSweepFinish()
            #time.sleep(15)  # Time for the scan to complete Depends on number of points and averag use 15s for p=100 avg =3
            # x = datetime.datetime.now()   # Attempt to insert datetime labeling to each lab file 
            # print(x)
            osa.ExportScan(f"S8_{level}_deg_C.csv")
                
    except Exception as e:
        # Log any exceptions that occur
        logging.error(f"Error: {e}")
        
    finally:
        # Close all instrument connections
        #pm.close()
        osa.close()
        tc.close()
        
if __name__ == "__main__":
    main()



