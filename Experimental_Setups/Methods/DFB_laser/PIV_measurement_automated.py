# -*- coding: utf-8 -*-
"""
Created on Mon Apr 29 17:17:52 2024

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
import numpy as np

# Initialize logging
logging.basicConfig(filename='lab_log.log', level=logging.INFO)

time.sleep(120)

# Number of experiment runs
num_runs = 50  # Modify this number based on how many times you want the experiment to run

def main(run_index):
    

    # Initialize instruments
    tc_address = 'ASRL3::INSTR'
    tc = TC300()
    
    PM_address = 'USB0::0x104D::0xCEC7::NI-VISA-30011::RAW'
    PM = Newport2936R(PM_address)
    
    keith_address = 'USB0::0x05E6::0x2450::04577394::INSTR'
    sourcemeter = Keithley2450(keith_address)

    # Number of measurements to average for each current step
    num_measurements = 2

    # Prepare CSV file for storing results, unique filename for each run
    csv_filename = f'PIV_new_chip_wateroff_2avg_MAX140mW_run{run_index}.csv'
    with open(csv_filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Current (mA)', 'Voltage (V)', 'Average Power (W)'])



    currents = np.linspace(0, 200, 200)  # Adjust range and number of points as needed
    powers = []
    voltages = []

    try:
        # Sourcemeter setup
        sourcemeter.apply_current()
        sourcemeter.source_current_range = 150e-3
        sourcemeter.compliance_voltage = 5
        sourcemeter.source_current = 0
        sourcemeter.enable_source()
        sourcemeter.measure_voltage()

        print(sourcemeter.voltage)
        print(PM.GetPowerCH1())

        power_measurements = []

        for current in currents:
            sourcemeter.ramp_to_current((current*1e-3))
            time.sleep(5)  # Stabilization time

            for _ in range(num_measurements):
                power = PM.GetPowerCH1()
                # Correction steps
                if power > 1:
                    time.sleep(5)
                    power = PM.GetPowerCH1()
                power_measurements.append(power)

            average_power = sum(power_measurements) / num_measurements
            print(average_power)
            powers.append(average_power)
            voltage = sourcemeter.voltage
            voltages.append(voltage)

            with open(csv_filename, mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([current, voltage, average_power])

    finally:
        # Clean up and plot
        sourcemeter.shutdown()
        PM.close()
        tc.close()

        plt.figure()
        plt.plot(currents, powers, '-o')
        plt.xlabel('Current (mA)')
        plt.ylabel('Power (W)')
        plt.title('Current vs Power (Averaged over {} measurements)'.format(num_measurements))
        plt.grid(True)
        plt.savefig(f'current_vs_power_averaged_run{run_index}.png')
        plt.show()

        plt.figure()
        plt.plot(currents, voltages, '-o')
        plt.xlabel('Current (mA)')
        plt.ylabel('Voltage (V)')
        plt.title('Current vs Voltage (Averaged over {} measurements)'.format(num_measurements))
        plt.grid(True)
        plt.savefig(f'current_vs_voltage_run{run_index}.png')
        plt.show()

if __name__ == "__main__":
    for i in range(1, num_runs + 1):
        main(i)
