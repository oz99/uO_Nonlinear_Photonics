import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# Function to generate and save plots for a given range of wavelengths
def generate_plots_for_wavelength_range(all_file_names, directory, start_wavelength, end_wavelength, step):
    wavelengths = [f"{w}.0nm" for w in range(start_wavelength, end_wavelength + 1, step)]
    saved_paths = {}

    for wavelength in wavelengths:
        filtered_files = [fn for fn in all_file_names if f"-{wavelength}-" in fn]

        plt.figure(figsize=(12, 8))

        for file_name in filtered_files:
            input_power = file_name.split('-')[-1].replace('.csv', '')
            data = pd.read_csv(file_name, delimiter='\t', header=None, names=['X', 'Y'])

            # Normalize the Y values to their maximum for each file
            max_y_value = data['Y'].max()
            normalized_y = data['Y'] / max_y_value if max_y_value != 0 else data['Y']

            plt.plot(data['X'], normalized_y, label=f'Power: {input_power}')

        plt.xlabel('Wavelength (nm)')
        plt.ylabel('Normalized Spectral Power (Relative to Max Power in File)')
        plt.title(f'Spectral Measurements at {wavelength}')
        plt.legend()

        device_folder = os.path.join(directory, device)
        if not os.path.exists(device_folder):
            os.makedirs(device_folder)

        save_path = os.path.join(device_folder, f'plot_{wavelength}.png')
        plt.savefig(save_path)
        plt.close()

        saved_paths[wavelength] = save_path

    return saved_paths


# Adjusted directory path for your environment
base_directory = 'c:\\Users\\Test\\Downloads\\OneDrive_2023-12-18\\NA_Straight_Waveguides'

# Loop over devices L0 to L10
for device in [f"L0{i}D0" if i < 11 else f"L0{i}D0" for i in range(11)]:
    # File pattern to match all CSV files for the current device in the directory
    file_pattern = os.path.join(base_directory, f"1-SPM-{device}-*.0nm-*.csv")

    # Fetch all matching file names
    all_file_names = glob.glob(file_pattern)

    # Generate and save plots for wavelengths from 1500 nm to 1560 nm
    saved_paths_for_range = generate_plots_for_wavelength_range(all_file_names, base_directory, 1500, 1560, 10)

    # Print the paths of the saved plots
    for wavelength, path in saved_paths_for_range.items():
        print(f'Device: {device}, Wavelength: {wavelength}, Saved Path: {path}')
