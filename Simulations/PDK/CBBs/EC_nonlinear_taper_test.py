import numpy as np 
import os

import importlib.util
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

layer = 1
material = "Au (Gold) - CRC"
zmin = 0 
zmax = 220e-9

n = fdtd.gdsimport("C:\\Users\ooner083\\EC_Nonlinear_Taper.gds", "EC_nonlinear_taper", layer, material, zmin, zmax)


fdtd.save("EC_Nonlinear_Taper.fsp")

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