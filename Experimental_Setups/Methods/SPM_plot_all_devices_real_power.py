import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# Function to generate and save plots for a given range of wavelengths
def generate_plots_for_wavelength_range(all_file_names, directory, start_wavelength, end_wavelength, step):
    # Generate wavelengths in the specified range
    wavelengths = [f"{w}.0nm" for w in range(start_wavelength, end_wavelength + 1, step)]

    # Dictionary to store the saved file paths for each wavelength
    saved_paths = {}

    # Generate and save plots for each wavelength in the range
    for wavelength in wavelengths:
        # Filter file names for the specific wavelength
        filtered_files = [fn for fn in all_file_names if f"-{wavelength}-" in fn]

        # Load data and create a plot for the specific wavelength
        plt.figure(figsize=(12, 8))
        for file_name in filtered_files:
            # Extracting the input power from the file name
            input_power = file_name.split('-')[-1].replace('.csv', '')

            data = pd.read_csv(file_name, delimiter='\t', header=None, names=['X', 'Y'])
            plt.plot(data['X'], data['Y'], label=f'Power: {input_power}')

        # Adding labels, title, and legend
        plt.xlabel('Wavelength (nm)')
        plt.ylabel('Spectral Power W/nm')
        plt.title(f'Spectral Measurements at {wavelength}')
        plt.legend()

        # Create a folder for the current device if it doesn't exist
        device_folder = os.path.join(directory, device)
        if not os.path.exists(device_folder):
            os.makedirs(device_folder)

        # Save the plot in the device folder
        save_path = os.path.join(device_folder, f'plot_{wavelength}.png')
        plt.savefig(save_path)
        plt.close()  # Close the plot to avoid display in notebook

        # Store the path in the dictionary
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
