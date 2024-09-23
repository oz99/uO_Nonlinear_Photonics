# -*- coding: utf-8 -*-
"""
Created on Wed Mar  6 11:38:50 2024

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

def main():


    # Initialize instruments
    tc_address = 'ASRL3::INSTR'
    tc = TC300()
    
    PM_address = 'USB0::0x104D::0xCEC7::NI-VISA-30011::RAW'
    PM = Newport2936R(PM_address)
    
    keith_address = 'USB0::0x05E6::0x2450::04577394::INSTR'
    sourcemeter = Keithley2450(keith_address)

    # Number of measurements to average for each current step
    num_measurements = 2 # This can be tuned as needed
    #15 seems to provide best results to d
    
    # Prepare CSV file for storing results
    csv_filename = 'PIV_measurements_new_chip_wateroff_1_num2_120_6.csv'
    with open(csv_filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Current (mA)', 'Voltage (V)', 'Average Power (W)'])

    time.sleep(120)

    currents = np.linspace(0, 120, 120)  # mA
    powers = []
    voltages = []
    


    try:

    

        sourcemeter.apply_current()                # Sets up to source current
        sourcemeter.source_current_range = 150e-3   # Sets the source current range to 10 mA
        sourcemeter.compliance_voltage = 5        # Sets the compliance voltage to 10 V
        sourcemeter.source_current = 0             # Sets the source current to 0 mA
        sourcemeter.enable_source()                # Enables the source output

        sourcemeter.measure_voltage()              # Sets up to measure voltage

        # # sourcemeter.ramp_to_current(80e-3)          # Ramps the current to 5 mA
        print(sourcemeter.voltage)
        print(PM.GetPowerCH1())                 # Prints the voltage in Volts

        power_measurements = []
        power = PM.GetPowerCH1()
        # power_measurements.append(power)
        # print(power_measurements[-1])
        
        # time.sleep(60) enable this incase you need to leave the room. Air flux from opening the door will cause fiber to move. 


        for current in currents:
            sourcemeter.ramp_to_current((current*1e-3 )) # Convert mA to A
 
            time.sleep(5)  # Stabilization time


            for _ in range(num_measurements):

                power = PM.GetPowerCH1()  # Assuming this method returns the power in W
                
                if power > 1:
                    print('correction1')
                    time.sleep(5)
                    power = PM.GetPowerCH1()  # Assuming this method returns the power in W
                    print(power)
                    
                if power > 1:
                    print('correction2')
                    time.sleep(5)
                    power = PM.GetPowerCH1()  # Assuming this method returns the power in W
                    print(power)
                    

                        
                # if 0.6*power_measurements[-1] > power > 1.4*power_measurements[-1]:
                #     print('correction1')
                #     time.sleep(5)
                #     power = PM.GetPowerCH1()  # Assuming this method returns the power in W
                #     print(power)
                    
                # if 0.6*power_measurements[-1] > power > 1.4*power_measurements[-1]:
                #     print('correction2')
                #     time.sleep(5)
                #     power = PM.GetPowerCH1()  # Assuming this method returns the power in W
                #     print(power)
                    
                # if 0.6*power_measurements[-1] > power > 1.4*power_measurements[-1]:
                #     print('correction3')
                #     time.sleep(5)
                #     power = PM.GetPowerCH1()  # Assuming this method returns the power in W
                #     print(power)
                            
  
                power_measurements.append(power)
                time.sleep(1)  # Delay between measurements for stability

            # Calculate average power
            average_power = sum(power_measurements) / num_measurements
            
            #print(power)
            print(average_power)
            # powers.append(average_power)
            powers.append(power)
            voltage = sourcemeter.voltage
            voltages.append(voltage)

            with open(csv_filename, mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([current, voltage, average_power])


    finally:
        sourcemeter.shutdown()
        PM.close()
        tc.close()
        
        
        # Plotting the graph
       
        plt.figure()
        plt.plot(currents, powers, '-o')
        plt.xlabel('Current (mA)')
        plt.ylabel('Power (W)')
        plt.title('Current vs Power (Averaged over {} measurements)'.format(num_measurements))
        plt.grid(True)
        plt.savefig('current_vs_power_averaged.png')
        plt.show()
        
        # Plotting the graph
        plt.figure()
        plt.plot(currents, voltages, '-o')
        plt.xlabel('Current (mA)')
        plt.ylabel('Voltage (V)')
        plt.title('Current vs Voltage (Averaged over {} measurements)'.format(num_measurements))
        plt.grid(True)
        plt.savefig('current_vs_voltage.png')
        plt.show()

if __name__ == "__main__":
    main()