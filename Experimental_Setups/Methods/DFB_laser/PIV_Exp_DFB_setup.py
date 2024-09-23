# -*- coding: utf-8 -*-
"""
Created on Fri Feb 23 09:06:02 2024

@author: ooner083
"""
import os
os.chdir('C:/Users/ooner083/.spyder-py3')
import os
import pyvisa as visa
import matplotlib.pyplot as plt
import time
import logging
from TC300_COMMAND_LIB import TC300
from Newport2936R import Newport2936R
import csv
from pymeasure.instruments.keithley import Keithley2450

# Initialize logging
logging.basicConfig(filename='lab_log.log', level=logging.INFO)

def main():
    # Change working directory to where the .csv file will be saved
    os.chdir('C:/Users/ooner083/.spyder-py3')

    # Initialize instruments
    tc_address = 'ASRL3::INSTR'
    tc = TC300()
    
    PM_address = 'USB0::0x104D::0xCEC7::NI-VISA-30011::RAW'
    PM = Newport2936R(PM_address)
    
    keith_address = 'USB0::0x05E6::0x2450::04577394::INSTR'
    sourcemeter = Keithley2450(keith_address)

    # Prepare CSV file for storing results
    csv_filename = 'power_measurements.csv' #Ensure to name this accordignly
    with open(csv_filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Current (mA)', 'Voltage (V)', 'Power (W)'])

    currents = range(1, 121)  # mA
    powers = []

    try:
        sourcemeter.source_mode = 'current'
        sourcemeter.compliance_voltage = 5 # In Volts

        for current in currents:
            sourcemeter.source_current = current * 1e-3  # Convert mA to A
            sourcemeter.enable_source()
            time.sleep(0.1)  # Stabilization time
            
            voltage = sourcemeter.measure_voltage()
            
     
            power1 = PM.GetPowerCH1()  # Assuming this method returns the power in W+
            time.sleep(0.1)
            power2 = PM.GetPowerCH1()
            time.sleep(0.1)
            power3 = PM.GetPowerCH1()
            
            power = (power1 + power2 + power3)/3
            
            powers.append(power)

            with open(csv_filename, mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([current, voltage, power])

            sourcemeter.disable_source()

    finally:
        PM.close()
        tc.close()

    # Plotting the graph
    plt.figure()
    plt.plot(currents, powers, '-o')
    plt.xlabel('Current (mA)')
    plt.ylabel('Power (W)')
    plt.title('Current vs Power')
    plt.grid(True)
    plt.savefig('current_vs_power.png')
    plt.show()

if __name__ == "__main__":
    main()