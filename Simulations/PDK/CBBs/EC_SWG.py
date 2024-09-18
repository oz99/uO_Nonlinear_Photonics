import numpy as np 
import os
import sys
import importlib.machinery
import importlib.util
import subprocess


######### Setup geometry paramters

h = 200e-9 # height of the structure

## Note that the following variables go into the GDS structure and are in um
## Note that the following variables go into the GDS structure and are in um

num_gratings = 110 # Number of grating elements

initial_period = 0.4 # Initial period of the grating (e.g., 700 nm)
final_period = 0.267 # Final period of the grating (e.g., 300 nm)
initial_width = 0.2 # Initial width of the grating element (e.g., 350 nm)
final_width = 0.17 # Final width of the grating element (e.g., 150 nm)
initial_duty_cycle = 0.5 # Initial duty cycle (50% of the period)
final_duty_cycle = 0.6 # Final duty cycle (80% of the period)
tapering_length = 35 # Length over which tapering occurs (e.g., 10 microns)
initial_y_span = 0.2 # Initial height of the grating element (e.g., 450 nm)
final_y_span = 0.45 # Final height of the grating element (e.g., 250 nm)
output_WG_length = 10 
min_feature_size = 0.04 # Minimum feature size, generally 40nm for our e-beam

WL_Start = 1500e-6
WL_Stop = 1600e-6



# Define the Python file you want to run and the arguments to pass

file_to_run = 'C:\\Git_Dump\\uO_Nonlinear_Photonics\\Fabrication\\PDK\\CBBs\\EC_SWG.py'
arguments = [

    '--num_gratings', str(num_gratings),  # Replace with your desired value
    '--min_feature_size', str(min_feature_size),  # Replace with your desired value
    '--initial_period', str(initial_period),  # Replace with your desired value
    '--final_period', str(final_period),  # Replace with your desired value
    '--initial_width', str(initial_width),  # Replace with your desired value
    '--final_width', str(final_width),  # Replace with your desired value
    '--initial_duty_cycle', str(initial_duty_cycle),  # Replace with your desired value
    '--final_duty_cycle', str(final_duty_cycle),  # Replace with your desired value
    '--tapering_length', str(tapering_length),  # Replace with your desired value
    '--initial_y_span', str(initial_y_span),  # Replace with your desired value
    '--final_y_span', str(final_y_span),  # Replace with your desired value
    '--output_WG_length', str(output_WG_length),  # Replace with your desired value
]


# Run the Python file with arguments
subprocess.run(['python', file_to_run] + arguments)
#default path for current release 
#xpos = os.environ.get(xpos)

os.add_dll_directory( 'C:\\Program Files\\Lumerical\\v241\\api\\python')
spec_win = importlib.util.spec_from_file_location('lumapi', 'C:\\Program Files\\Lumerical\\v241\\api\\python\\lumapi.py')
#Functions that perform the actual loading
lumapi = importlib.util.module_from_spec(spec_win) #windows
spec_win.loader.exec_module(lumapi)

# remoteArgs = { "hostname": "10.132.193.235",
#                "port": 8989 }
# fdtd = lumapi.FDTD(hide=True, remoteArgs=remoteArgs)

fdtd = lumapi.FDTD()

fdtd.newproject()

layer = 1
material = "Si (Silicon) - Palik"
zmin = 0 
zmax = 200e-9

n = fdtd.gdsimport("C:\\Users\\ooner083\\EC_SWG.gds", "EC_SWG", layer, material, zmin, zmax)




counter = 0 

for i in range(int(num_gratings - (num_gratings * 0.1))):


        xpos = i * initial_period   # Positioning each grating element based on the initial period

        # Calculate the taper ratio based on the manual tapering length

        #taper_ratio = xpos / tapering_length;  # Ratio within the tapering length

        # Calculate the taper ratio based on the position
        taper_ratio = i / (num_gratings-1)
        
        # Taper the period
        current_period = initial_period * (1 - taper_ratio) + final_period * taper_ratio
        
        # Taper the duty cycle
        current_duty_cycle = initial_duty_cycle * (1 - taper_ratio) + final_duty_cycle * taper_ratio
        
        # Calculate the width of the current grating element
        current_width = current_duty_cycle * current_period

        # Taper the grating width independently of the duty cycle
        actual_width = initial_width * (1 - taper_ratio) + final_width * taper_ratio
        
        # Taper the y span (height)
        current_y_span = initial_y_span * (1 - taper_ratio) + final_y_span * taper_ratio
    
        # Calculate the gap between this segment and the next
        current_gap = current_period - current_width
        
        
        print([i])        
  

        name = counter
        
        counter += 1
############## Simulation parameters #############################
Xsize = (xpos + 3*output_WG_length / 2)*10**-6 #FDTD mesh sizes
Ysize = 10e-6
Zsize = 4e-6

#mesh size usually 10-20nm is sufficient precision. More is better but expensive
dx = 20e-9
dy = 20e-9
dz = 20e-9

fdtd.addfdtd()
fdtd.set("x", ((xpos +output_WG_length)/2)*10**-6)
fdtd.set("x span", Xsize)
fdtd.set("y", 0.0)
fdtd.set("y span", Ysize)
fdtd.set("z",h/2)
fdtd.set("z span", Zsize)

fdtd.set("dimension","3D")
fdtd.set("simulation time", 500e-15)

fdtd.set("mesh type","uniform")
fdtd.set("dx", dx)
fdtd.set("dy", dy)
fdtd.set("dz", dz)

fdtd.set("background material","SiO2 (Glass) - Palik")

fdtd.setglobalsource("wavelength start",WL_Start)
fdtd.setglobalsource("wavelength stop",WL_Stop)


fdtd.addport() # add port
fdtd.set("name", "Input_port")
fdtd.set("x", 0)  # Set port position
fdtd.set("y", 0)
fdtd.set("y span", 5e-6)
fdtd.set("z", h/2)
fdtd.set("z span", 4e-6)
fdtd.set("direction", "forward")  # Direction of the input
fdtd.set("mode selection", "fundamental TE mode")



fdtd.addport() # add port
fdtd.set("name", "Output_port")
fdtd.set("x", (xpos + output_WG_length / 2)*10**-6)  # need to fix according to geometry structure
fdtd.set("y", 0)
fdtd.set("y span", 5e-6)
fdtd.set("z", h/2)
fdtd.set("z span", 4e-6)
fdtd.set("direction", "forward")  # Direction of the input

fdtd.save("EC_SWG.fsp")

fdtd.run()




############## Add an override region mesh?########################
# fdtd.addmesh
# set("name","mesh_y_splitter")
# # set dimension
# set("x",0);
# set("x span",2e-6);
# set("y",0);
# set("y span",5e-6);
# set("z",0);
# set("z span",10e-6);
# # enable in X direction and disable in Y,Z directions
# set("override x mesh",1);
# set("override y mesh",0);
# set("override z mesh",0);
# # restrict mesh by defining maximum step size
# set("set maximum mesh step",1);
# set("dx",5e-9);

























# Xsize = 240e-9
# Ysize = 240e-9
# Zsize = 240e-9

# R = 50e-9

# WL_Start = 200e-9
# WL_Stop = 1000e-9

# fdtd.addfdtd()
# fdtd.set("x",0.0)
# fdtd.set("x span",Xsize)
# fdtd.set("y",0.0)
# fdtd.set("y span",Ysize)
# fdtd.set("z",0.0)
# fdtd.set("z span",Zsize)

# fdtd.set("dimension","3D")
# fdtd.set("simulation time", 500e-15)

# fdtd.set("mesh type","uniform")
# fdtd.set("dx", 2.5e-9)
# fdtd.set("dy", 2.5e-9)
# fdtd.set("dz", 2.5e-9)

# ############################## Source Implementation ###############################
# fdtd.addtfsf()
# fdtd.set("x",0.0)
# fdtd.set("x span",Xsize - 40e-9)
# fdtd.set("y",0.0)
# fdtd.set("y span",Ysize - 40e-9)
# fdtd.set("z",0.0)
# fdtd.set("z span",Zsize - 40e-9)

# fdtd.set("injection axis","x")
# fdtd.set("wavelength start", WL_Start)
# fdtd.set("wavelength stop", WL_Stop)

# fdtd.addmovie()
# fdtd.set("x",0.0)
# fdtd.set("x span",Xsize)
# fdtd.set("y",0.0)
# fdtd.set("y span",Ysize)
# fdtd.set("z",0.0)

# fdtd.addsphere()
# fdtd.set("radius", R)

# fdtd.save("GoldSPhere.fsp")

# fdtd.run()