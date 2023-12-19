import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# Function to generate and save offset plots for a given center wavelength
def generate_offset_plots_for_center_wavelength(all_file_names, directory, start_wavelength, end_wavelength, step, offset_step):
    saved_paths = {}
    
    for center_wavelength in range(start_wavelength, end_wavelength + 1, step):
        plt.figure(figsize=(12, 8))
        
        # Filter files for the specific center wavelength
        filtered_files = [fn for fn in all_file_names if f"-{center_wavelength}.0nm-" in fn]
        
        # Sort files in ascending order of power
        sorted_files = sorted(filtered_files, key=lambda fn: float(fn.split('-')[-1].replace('.csv', '').replace('mW', '')))

        offset = 0  # Initialize offset for the highest power plot

        for file_name in sorted_files[::-1]:  # Reverse the list to start from the highest power
            input_power = file_name.split('-')[-1].replace('.csv', '').replace('mW', '')
            data = pd.read_csv(file_name, delimiter='\t', header=None, names=['X', 'Y'])

            # Calculate the change in wavelength relative to the center
            data['X'] = data['X'] - center_wavelength

            max_y_value = data['Y'].max()
            normalized_y = (data['Y'] / max_y_value if max_y_value != 0 else data['Y']) + offset

            plt.plot(data['X'], normalized_y, label=f'Power: {input_power}')

            # Decrement the offset for the next plot so lower powers are below
            offset -= offset_step

        plt.xlabel('Change in Wavelength (nm)')
        plt.ylabel('Normalized Spectral Magnitude (a.u.)')
        plt.title(f'Spectral Measurements at {center_wavelength} nm')
        plt.legend(loc='upper right')

        # Save the plot for the center wavelength
        device_folder = os.path.join(directory, device)
        if not os.path.exists(device_folder):
            os.makedirs(device_folder)

        save_path = os.path.join(device_folder, f'offset_plot_{center_wavelength}nm.png')
        plt.savefig(save_path)
        plt.close()


        # # Create a folder for the current wavelength if it doesn't exist
        # wavelength_folder = os.path.join(directory, f"{center_wavelength}nm")
        # if not os.path.exists(wavelength_folder):

        #     os.makedirs(wavelength_folder)

        # # Save the plot in the wavelength folder
        # save_path = os.path.join(wavelength_folder, f'offset_plot_{center_wavelength}nm.png')
        # plt.savefig(save_path)
        # plt.close()

        # Store the path in the dictionary
        saved_paths[center_wavelength] = save_path

    return saved_paths



# Example usage:
# saved_paths = generate_offset_plots_for_center_wavelength(all_file_names, directory, start_wavelength, end_wavelength, step, offset_step)




# Adjusted directory path for your environment
base_directory = 'c:\\Users\\Test\\Downloads\\OneDrive_2023-12-18\\NA_Straight_Waveguides'

# Loop over devices L0 to L10
for device in [f"L0{i}D0" if i < 11 else f"L0{i}D0" for i in range(11)]:
    # File pattern to match all CSV files for the current device in the directory
    file_pattern = os.path.join(base_directory, f"1-SPM-{device}-*.0nm-*.csv")

    # Fetch all matching file names
    all_file_names = glob.glob(file_pattern)

    # Generate and save plots for wavelengths from 1500 nm to 1560 nm
    saved_paths_for_range = generate_offset_plots_for_center_wavelength(all_file_names, base_directory, 1500, 1560, 10,0.15)

    # Print the paths of the saved plots
    for wavelength, path in saved_paths_for_range.items():
        print(f'Device: {device}, Wavelength: {wavelength}, Saved Path: {path}')
