import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# Function to generate and save offset plots for a given range of wavelengths
def generate_offset_plots_for_wavelength_range(all_file_names, directory, start_wavelength, end_wavelength, step, offset_step):
    wavelengths = [f"{w}.0nm" for w in range(start_wavelength, end_wavelength + 1, step)]
    saved_paths = {}

    for wavelength in wavelengths:
        filtered_files = [fn for fn in all_file_names if f"-{wavelength}-" in fn]

        plt.figure(figsize=(12, 8))
        offset = 0  # Initialize offset for the highest power plot

        # Sort files in ascending order of power
        sorted_files = sorted(filtered_files, key=lambda fn: float(fn.split('-')[-1].replace('.csv', '').replace('mW', '')))

        for file_name in sorted_files[::-1]:  # Reverse the list to start from the highest power
            input_power = file_name.split('-')[-1].replace('.csv', '').replace('mW', '')
            data = pd.read_csv(file_name, delimiter='\t', header=None, names=['X', 'Y'])

            max_y_value = data['Y'].max()
            normalized_y = (data['Y'] / max_y_value if max_y_value != 0 else data['Y']) + offset

            plt.plot(data['X'], normalized_y, label=f'Power: {input_power}')

            # Decrement the offset for the next plot so lower powers are below
            offset -= offset_step

        plt.xlabel('Wavelength (nm)')
        plt.ylabel('Normalized Spectral Magnitude (a.u.)')
        plt.title(f'Spectral Measurements at {wavelength}')
        plt.legend(loc='upper right')

        device_folder = os.path.join(directory, device)
        if not os.path.exists(device_folder):
            os.makedirs(device_folder)

        save_path = os.path.join(device_folder, f'offset_plot_{wavelength}.png')
        plt.savefig(save_path)
        plt.close()

        saved_paths[wavelength] = save_path

    return saved_paths

# Adjust your directory path and loop over devices as needed
# Adjust the offset_step to match the separation you desire between lines
# ...



# Adjusted directory path for your environment
base_directory = 'c:\\Users\\Test\\Downloads\\RefWG\\Reference_Serpentine_Waveguides'

# Loop over devices L0 to L10
for device in [f"L{i}" if i < 5 else f"L{i}D0" for i in range(5)]:
    # File pattern to match all CSV files for the current device in the directory
    file_pattern = os.path.join(base_directory, f"1-SPM-strip-WG-{device}-*.0nm-*.csv")

    # Fetch all matching file names
    all_file_names = glob.glob(file_pattern)

    # Generate and save plots for wavelengths from 1500 nm to 1560 nm
    saved_paths_for_range = generate_offset_plots_for_wavelength_range(all_file_names, base_directory, 1500, 1560, 10,0.15)

    # Print the paths of the saved plots
    for wavelength, path in saved_paths_for_range.items():
        print(f'Device: {device}, Wavelength: {wavelength}, Saved Path: {path}')
