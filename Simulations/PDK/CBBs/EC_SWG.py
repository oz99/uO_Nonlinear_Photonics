import numpy as np 
import os
import sys
import importlib.machinery
import importlib.util
import subprocess


######### Setup geometry paramters

h = 200e-9 # height of the structure

## Note that the following variables go into the GDS structure and are in um
length = 5 # Length of the y-spliter
w0 = 0.6 # Width at point 0, and for the In/Out Waveguides
w1 = 1.2 # Width at point 1
w2 = 2.4 # Width at point 2
w3 = 4 # Width at point 3
w4 = 3 # Width at point 4
s = 0.2 #'Width of the split between the output splitter arms
#w5 = '(2*w0)+s' # Width at point 5 
w5 = 1.4
straightlength = 2 # Length of the Straight In/Out Waveguides (default: 5 um)
radius = 10 # Radius of the Bend Section (default: 2 um)

### Do I add a substrate?


WL_Start = 1500e-9
WL_Stop = 1600e-9

# Define the Python file you want to run and the arguments to pass

file_to_run = 'C:\\Git_Dump\\uO_Nonlinear_Photonics\\Fabrication\\PDK\\CBBs\\y_splitter_curved.py'
arguments = [
    '--length', str(length),  # Replace with your desired length value
    '--w0', str(w0),   # Replace with your desired width value
    '--w1', str(w1),    # Replace with your desired height value
    '--w2', str(w2),    # Replace with your desired height value
    '--w3', str(w3),    # Replace with your desired height value
    '--w4', str(w4),   # Replace with your desired height value
    '--w5', str(w5),    # Replace with your desired height value
    '--s', str(s),    # Replace with your desired height value
    '--straightlength', str(straightlength),    # Replace with your desired height value
    '--radius', str(radius),   # Replace with your desired height value
]

# Run the Python file with arguments
subprocess.run(['python', file_to_run] + arguments)
#default path for current release 

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

n = fdtd.gdsimport("C:\\Users\\ooner083\\Ysplitter_test.gds", "YSplitter", layer, material, zmin, zmax)

############## Simulation parameters #############################
Xsize = 12e-6 #FDTD mesh sizes
Ysize = 10e-6
Zsize = 4e-6

#mesh size usually 10-20nm is sufficient precision. More is better but expensive
dx = 20e-9
dy = 20e-9
dz = 20e-9

fdtd.addfdtd()
fdtd.set("x", 5e-6)
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
fdtd.set("x", straightlength*10**-6)  # Set port position
fdtd.set("y", 0)
fdtd.set("y span", 5e-6)
fdtd.set("z", h/2)
fdtd.set("z span", 4e-6)
fdtd.set("direction", "forward")  # Direction of the input
fdtd.set("mode selection", "fundamental TE mode")

fdtd.addport() # add port
fdtd.set("name", "Output_port_top")
fdtd.set("x", (length+straightlength*2+0.5)*10**-6)  # Set port position
fdtd.set("y", ((w0+s)/2)*10**-6)
fdtd.set("y span", w0*10**-6)
fdtd.set("z", h/2)
fdtd.set("z span", 4e-6)
fdtd.set("direction", "forward")  # Direction of the input

fdtd.addport() # add port
fdtd.set("name", "Output_port_bottom")
fdtd.set("x", (length+straightlength*2+0.5)*10**-6)  # Set port position
fdtd.set("y", -((w0+s)/2)*10**-6)
fdtd.set("y span", w0*10**-6)
fdtd.set("z", h/2)
fdtd.set("z span", 4e-6)
fdtd.set("direction", "forward")  # Direction of the input

fdtd.save("Ysplitter.fsp")

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