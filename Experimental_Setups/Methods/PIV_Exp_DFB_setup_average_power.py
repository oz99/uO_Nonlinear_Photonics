# -*- coding: utf-8 -*-
"""
Created on Fri Feb 23 09:06:02 2024

@author: ooner083
"""
import os
os.chdir('C:/Users/ooner083/.spyder-py3')

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


    # Initialize instruments
    tc_address = 'ASRL3::INSTR'
    tc = TC300()
    
    PM_address = 'USB0::0x104D::0xCEC7::NI-VISA-30011::RAW'
    PM = Newport2936R(PM_address)
    
    keith_address = 'USB0::0x05E6::0x2450::04577394::INSTR'
    sourcemeter = Keithley2450(keith_address)

    # Number of measurements to average for each current step
    num_measurements = 1  # This can be tuned as needed

    # Prepare CSV file for storing results
    csv_filename = 'power_measurements.csv'
    with open(csv_filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Current (mA)', 'Voltage (V)', 'Average Power (W)'])


    currents = range(81, 86)  # mA
    powers = []
    
    try:  
        

        sourcemeter.apply_current()                # Sets up to source current
        sourcemeter.source_current_range = 120e-3   # Sets the source current range to 10 mA
        sourcemeter.compliance_voltage = 5        # Sets the compliance voltage to 10 V
        sourcemeter.source_current = 0             # Sets the source current to 0 mA
        sourcemeter.enable_source()                # Enables the source output

        sourcemeter.measure_voltage()              # Sets up to measure voltage

        sourcemeter.ramp_to_current(80e-3)          # Ramps the current to 5 mA
        # print(sourcemeter.voltage)                 # Prints the voltage in Volts




        for current in currents:
            # sourcemeter.enable_source()
            sourcemeter.ramp_to_current(current*1e-3 ) # Convert mA to A
            sourcemeter.enable_source()
            time.sleep(1)  # Stabilization time

            # Initialize variables for averaging
            power_measurements = []

            for _ in range(num_measurements):
                voltage = sourcemeter.measure_voltage()
                power = PM.GetPowerCH1()  # Assuming this method returns the power in W
                power_measurements.append(power)
                time.sleep(0.1)  # Delay between measurements for stability

            # Calculate average power
            average_power = sum(power_measurements) / num_measurements
            powers.append(average_power)

            with open(csv_filename, mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([current, voltage, average_power])

            sourcemeter.disable_source()

    finally:
        # sourcemeter.shutdown()
        PM.close()
        tc.close()

    # Plotting the graph
    # plt.figure()
    # plt.plot(currents, powers, '-o')
    # plt.xlabel('Current (mA)')
    # plt.ylabel('Power (W)')
    # plt.title('Current vs Power (Averaged over {} measurements)'.format(num_measurements))
    # plt.grid(True)
    # plt.savefig('current_vs_power_averaged.png')
    # plt.show()

if __name__ == "__main__":
    main()