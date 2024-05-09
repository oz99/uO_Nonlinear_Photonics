import pandas as pd
import matplotlib.pyplot as plt
import glob
import os
import numpy as np  # for logarithm
import re

def mw_to_dbm(power_mw):
    return 10 * np.log10(power_mw)

def generate_offset_plots_for_wavelength_range(all_file_names, data_directory, save_directory ,start_wavelength, end_wavelength, step, offset_step):
    wavelengths = [f"{w}.0nm" for w in range(start_wavelength, end_wavelength + 1, step)]
    saved_paths = {}

    #print(all_file_names)

    for wavelength in wavelengths:
        filtered_files = [fn for fn in all_file_names if f"{wavelength}-" in fn]

        plt.figure(figsize=(12, 8))
        offset = 0  # Initialize offset for the highest power plot

        # Sort files in ascending order of power
        sorted_files = sorted(filtered_files, key=lambda fn: float(fn.split('-')[-2].replace('mW', '')))

        for file_name in sorted_files[::-1]:  # Reverse the list to start from the highest power
            input_power_mw = float(file_name.split('-')[-2].replace('mW', ''))
            input_power_dbm = mw_to_dbm(input_power_mw)
            data = pd.read_csv(file_name, delimiter='\t', header=None, names=['X', 'Y'])

            max_y_value = data['Y'].max()
            max_y_dbm = mw_to_dbm(max_y_value)  # Convert peak power to dBm
            normalized_y = (data['Y'] / max_y_value if max_y_value != 0 else data['Y']) + offset

            plt.plot(data['X'], normalized_y, label=f'P_in={input_power_dbm:.2f}dBm')
            
            #plt.plot(data['X'], normalized_y, label=f'Pin={input_power_dbm:.2f}dBm Pout={max_y_dbm:.2f}dBm')

            # Decrement the offset for the next plot so lower powers are below
            offset -= offset_step

        ## Each device has a specific length. I want to make a list for the lengths of each device and reutn the value to device_length
        if device == 'L00D0':
            device_length = 99999
        elif device == 'L01D0':
            device_length = 40 
        elif device == 'L02D0':
            device_length = 30
        elif device == 'L03D0':
            device_length = 20
        elif device == 'L04D0':
            device_length = 10


        plt.xlabel('Wavelength (nm)', fontsize=24)
        plt.ylabel('Normalized Spectral Power (a.u.)', fontsize=24)
        plt.xticks(fontsize=20)
        plt.yticks(fontsize=20)
        #plt.title(f'SPM at {wavelength} for Hugyens MetaWaveguide L={device_length}um',fontsize=24)
        plt.legend(loc='upper right',fontsize=16)
        s = wavelength
        number = int(re.search(r'\d+', s).group())
        plt.text(number-20, 0.8, f'Strip WG L={device_length}mm', fontsize=20)

        device_folder = os.path.join(data_directory, device)
        if not os.path.exists(device_folder):
            os.makedirs(device_folder)

        save_path = os.path.join(save_directory, f'Si Strip WG SPM L={device_length}mm at {wavelength}.png')
        plt.savefig(save_path)
        plt.close()

        saved_paths[wavelength] = save_path

    return saved_paths

# import pandas as pd
# import matplotlib.pyplot as plt
# import glob
# import os

# # Function to generate and save offset plots for a given range of wavelengths
# def generate_offset_plots_for_wavelength_range(all_file_names, directory, start_wavelength, end_wavelength, step, offset_step):
#     wavelengths = [f"{w}.0nm" for w in range(start_wavelength, end_wavelength + 1, step)]
#     saved_paths = {}

#     for wavelength in wavelengths:
#         filtered_files = [fn for fn in all_file_names if f"-{wavelength}-" in fn]

#         plt.figure(figsize=(12, 8))
#         offset = 0  # Initialize offset for the highest power plot

#         # Sort files in ascending order of power
#         sorted_files = sorted(filtered_files, key=lambda fn: float(fn.split('-')[-2].replace('mW', '')))

#         for file_name in sorted_files[::-1]:  # Reverse the list to start from the highest power
#             input_power = file_name.split('-')[-1].replace('.csv', '').replace('mW', '')
#             data = pd.read_csv(file_name, delimiter='\t', header=None, names=['X', 'Y'])

#             max_y_value = data['Y'].max()
#             normalized_y = (data['Y'] / max_y_value if max_y_value != 0 else data['Y']) + offset

#             plt.plot(data['X'], normalized_y, label=f'Power: {input_power}')

#             # Decrement the offset for the next plot so lower powers are below
#             offset -= offset_step

#         plt.xlabel('Wavelength (nm)')
#         plt.ylabel('Normalized Spectral Magnitude (a.u.)')
#         plt.title(f'Spectral Measurements at {wavelength}')
#         plt.legend(loc='upper right')

#         device_folder = os.path.join(directory, device)
#         if not os.path.exists(device_folder):
#             os.makedirs(device_folder)

#         save_path = os.path.join(device_folder, f'offset_plot_{wavelength}.png')
#         plt.savefig(save_path)
#         plt.close()

#         saved_paths[wavelength] = save_path

#     return saved_paths

# Adjust your directory path and loop over devices as needed
# Adjust the offset_step to match the separation you desire between lines
# ...



# Adjusted directory path for your environment
data_directory = 'c:\\Users\\Test\\Downloads\\Huygens_Data\\Strip-WG-Serp'

save_directory ='c:\\Users\\Test\\Downloads'

# Loop over devices L0 to L10
for device in [f"L0{i}D0" if i < 5 else f"L0{i}D0" for i in range(5)]:
    # File pattern to match all CSV files for the current device in the directory
    file_pattern = os.path.join(data_directory, f"*SPM-STRIP-SERP-{device}*.0nm-*-20dec23.csv") 
                                                #SPM-NA-WG-STRAIGHT-L03-D0-1500.0nm-0.23869mW-19dec23
    # Fetch all matching file names
    all_file_names = glob.glob(file_pattern)



    # Generate and save plots for wavelengths from 1500 nm to 1560 nm
    saved_paths_for_range = generate_offset_plots_for_wavelength_range(all_file_names, data_directory, save_directory,1500, 1560, 10,0.3) #figure out a way of doing 0.5nm. May or may not need to switch to Angstroms

    # Print the paths of the saved plots
    for wavelength, path in saved_paths_for_range.items():
        print(f'Device: {device}, Wavelength: {wavelength}, Saved Path: {path}')
