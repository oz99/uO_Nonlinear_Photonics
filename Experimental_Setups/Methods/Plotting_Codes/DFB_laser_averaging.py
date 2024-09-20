import glob
import matplotlib.pyplot as plt
import pandas as pd

# Define the file pattern for all runs
file_pattern = 'c:/UO/Characterization/W112_5CB12_PIV_DFB_roomtemp/All_Runs_data/PIV_new_chip_wateroff_2avg_MAX140mW_run*.csv'
files = glob.glob(file_pattern)

# Initialize an empty list to store data from all files
all_data = []

# Loop through each file and append the data to the list
for file in files:
    df = pd.read_csv(file)
    all_data.append(df)

# Concatenate all data and group by 'Current (mA)' to calculate the mean of 'Average Power (W)'
combined_df = pd.concat(all_data)
averaged_df = combined_df.groupby('Current (mA)').mean().reset_index()

# Save the averaged data to a new CSV file
output_file = 'c:/UO/Characterization/W112_5CB12_PIV_DFB_roomtemp/averaged_power_values.csv'
averaged_df.to_csv(output_file, index=False)

# Plot the results
plt.figure()
plt.plot(averaged_df['Current (mA)'], averaged_df['Average Power (W)'], marker='o')
plt.xlabel('Current (mA)')
plt.ylabel('Average Power (W)')
plt.title('Average Power vs Current')
plt.grid(True)
plt.show()

# Provide the output CSV file path
output_file
