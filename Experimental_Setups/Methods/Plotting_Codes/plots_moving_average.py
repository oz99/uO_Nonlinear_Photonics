# -*- coding: utf-8 -*-
"""
Created on Wed Apr  3 10:56:51 2024

@author: ooner083
"""
import pandas as pd
import matplotlib.pyplot as plt

def plot_power_spectrum(csv_file):
    # Load the CSV file
    df = pd.read_csv(csv_file, sep=',', header=None)
    
    # Assuming the first column is current, the second is voltage, and the third is power,
    # naming the columns accordingly
    df.columns = ['Current', 'Voltage', 'Power']
    
    # Calculating the moving average of the 'Current' column with a specified window size
    # The window size can be adjusted as needed; here it is set to 10 for demonstration
    df['Current_MA'] = df['Current'].rolling(150).mean()
    
    # Plotting the data using the moving average of 'Current' against the original 'Power'
    plt.figure(figsize=(12, 7))
    plt.plot(df['Current_MA'], df['Power'], label='Power vs. Averaged Current', color='blue')
    
    plt.xlabel('Averaged Current (mA)', fontsize=14)
    plt.ylabel('Power (mW)', fontsize=14)
    plt.title('Power at Room Temperature (Smoothed Current)', fontsize=16)
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# Replace 'power_measurements.csv' with the path to your actual CSV file
plot_power_spectrum('power_measurements.csv')
