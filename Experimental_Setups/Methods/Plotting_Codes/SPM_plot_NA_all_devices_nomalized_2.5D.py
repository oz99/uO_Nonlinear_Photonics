import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import glob
import os
import numpy as np  # for logarithm
import re


def mw_to_dbm(power_mw):
    return 10 * np.log10(power_mw)

def generate_offset_plots_for_wavelength_range(all_file_names, data_directory, save_directory ,start_wavelength, end_wavelength, step, offset_step):
    wavelengths = [f"{w}.0nm" for w in range(start_wavelength, end_wavelength + 1, step)]
    saved_paths = {}

    for wavelength in wavelengths:
        filtered_files = [fn for fn in all_file_names if f"-{wavelength}-" in fn]

        plt.figure(figsize=(12, 10))
        offset = 0  # Initialize offset for the highest power plot

        # Sort files in ascending order of power
        sorted_files = sorted(filtered_files, key=lambda fn: float(fn.split('-')[-2].replace('mW', '')))

        # Create a colormap
        cmap = cm.plasma
        num_lines = len(sorted_files)
        colors = cmap(np.linspace(0.1, 0.9, num_lines))

        # Loop through files and plot
        for counter, file_name in enumerate(sorted_files[::-1]):  # Reverse the list to start from the highest power
            input_power_mw = float(file_name.split('-')[-2].replace('mW', ''))
            input_power_dbm = mw_to_dbm(input_power_mw)
            data = pd.read_csv(file_name, delimiter='\t', header=None, names=['X', 'Y'])

            max_y_value = data['Y'].max()
            max_y_dbm = mw_to_dbm(max_y_value)  # Convert peak power to dBm
            normalized_y = (data['Y'] / max_y_value if max_y_value != 0 else data['Y']) + offset

            # Plot the data with color from the gist_heat colormap
            plt.plot(data['X'], normalized_y, label=f'{input_power_dbm:.2f}', color=colors[counter],linewidth=2)

            mpl.rcParams['axes.linewidth'] = 1
            plt.tick_params(width=2)
            plt.xlim(min(data['X']), max(data['X'])-4)
            plt.ylim(-2.7, 1.1)
            plt.gca().set_yticks([])
            plt.gca().set_yticklabels([])
            # Decrement the offset for the next plot so lower powers are below
            offset -= offset_step

        # for file_name in sorted_files[::-1]:  # Reverse the list to start from the highest power
        #     input_power_mw = float(file_name.split('-')[-2].replace('mW', ''))
        #     input_power_dbm = mw_to_dbm(input_power_mw)
        #     data = pd.read_csv(file_name, delimiter='\t', header=None, names=['X', 'Y'])

        #     max_y_value = data['Y'].max()
        #     max_y_dbm = mw_to_dbm(max_y_value)  # Convert peak power to dBm
        #     normalized_y = (data['Y'] / max_y_value if max_y_value != 0 else data['Y']) + offset


        #     cmap = cm.gist_heat
        #     num_lines = len(sorted_files)
        #     colors = cmap(np.linspace(0, 1, num_lines))
        #     counter = 1

        #     plt.plot(data['X'], normalized_y, label=f'{input_power_dbm:.2f}dBm', color=colors[counter])
        #     plt.gca().set_yticklabels([])
        #     counter += 1
        #     # plt.set(ylabel=None)  # remove the y-axis label
            
        #     #plt.plot(data['X'], normalized_y, label=f'Pin={input_power_dbm:.2f}dBm Pout={max_y_dbm:.2f}dBm')

        #     # Decrement the offset for the next plot so lower powers are below
        #     offset -= offset_step

        ## Each device has a specific length. I want to make a list for the lengths of each device and reutn the value to device_length
        if device == 'L00-D0':
            device_length = 2.5
        elif device == 'L01-D0':
            device_length = 7740
        elif device == 'L02-D0':
            device_length = 6020
        elif device == 'L03-D0':
            device_length = 4300
        elif device == 'L04-D0':
            device_length = 2580
        elif device == 'L05-D0':
            device_length = 860
        elif device == 'L06-D0':
            device_length = 430
        elif device == 'L07-D0':
            device_length = 215
        elif device == 'L08-D0':
            device_length = 150.5
        elif device == 'L09-D0':
            device_length = 86
        elif device == 'L010-D0':
            device_length = 21.5

        plt.xlabel('Wavelength (nm)', fontsize=24)
        plt.ylabel('Normalized Spectral Power (a.u.)', fontsize=24)
        plt.xticks(fontsize=20)
        plt.yticks(fontsize=20)
        #plt.title(f'SPM at {wavelength} for Hugyens MetaWaveguide L={device_length}um',fontsize=24)
        plt.legend(title='$\mathregular{P_{in-avg}}$ (dBm)', title_fontsize = 20, loc='lower left',
                    fontsize=20,handleheight=2.22, bbox_to_anchor=(0, 0.0075), framealpha=1,
                    edgecolor='black', frameon = True, fancybox=True ) #loc='upper right' loc='lower left',
        
        #plt.subplots_adjust(bottom=-0.05)
        s = wavelength
        number = int(re.search(r'\d+', s).group())
        plt.text(number-19.5, 0.8, f'Huygens L={device_length}um', fontsize=24)

        device_folder = os.path.join(data_directory, device)
        if not os.path.exists(device_folder):
            os.makedirs(device_folder)

        save_path = os.path.join(save_directory, f'Huygens SPM L={device_length}um at {wavelength}.png')
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
data_directory = 'c:\\Users\\Test\\Downloads\\Huygens_Data\\NA-WG-Straight\\18-19_dec_strong_but_scattered'

save_directory ='c:\\Users\\Test\\Downloads'

# Loop over devices L0 to L10
for device in [f"L0{i}-D0" if i < 11 else f"L0{i}-D0" for i in range(11)]:
    # File pattern to match all CSV files for the current device in the directory
    file_pattern = os.path.join(data_directory, f"SPM-NA-WG-STRAIGHT-{device}-*.0nm-*.csv") 
                                                #SPM-NA-WG-STRAIGHT-L03-D0-1500.0nm-0.23869mW-19dec23
    # Fetch all matching file names
    all_file_names = glob.glob(file_pattern)



    # Generate and save plots for wavelengths from 1500 nm to 1560 nm
    saved_paths_for_range = generate_offset_plots_for_wavelength_range(all_file_names, data_directory, save_directory,1500, 1560, 10,0.3) #figure out a way of doing 0.5nm. May or may not need to switch to Angstroms

    # Print the paths of the saved plots
    for wavelength, path in saved_paths_for_range.items():
        print(f'Device: {device}, Wavelength: {wavelength}, Saved Path: {path}')
