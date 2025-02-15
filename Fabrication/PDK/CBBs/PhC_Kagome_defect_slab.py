import kfactory as kf
import numpy as np
"""
This script demonstrates the use of the `kfactory` and `gdsfactory` libraries to create and manipulate GDSII layout cells.
The script performs the following steps:
1. Creates a main cell `c` with a specified name "ToFill".
2. Adds an elliptical shape to layer (1, 0) and a triangular shape to layer (10, 0) in the main cell.
3. Creates a fill cell `fc` and adds two rectangular shapes to layers (2, 0) and (3, 0).
4. Uses the `fill_tiled` function to fill the main cell `c` with instances of the fill cell `fc`, while excluding certain layers and specifying spacing between instances.
5. Writes the resulting layout to a GDSII file named "mzi_fill.gds".
6. Imports the GDSII file using `gdsfactory` and displays the cell named "ToFill".
Dependencies:
- kfactory
- gdsfactory
Usage:
- Ensure the required libraries are installed.
- Run the script to generate and visualize the GDSII layout.
"""
from kfactory.utils.fill import fill_tiled


import gdsfactory as gf
import numpy as np
import argparse
import re
from scipy.interpolate import CubicSpline
import json   

row_length = 50
a = 283800/1000000 # lattice constant in microns. Note that GDSfactory uses floats so division needed to avoid decimals


hole_radius = 82302/1000000
circle = gf.components.circle(radius=hole_radius)

kagome_top = gf.Component("Kagome_top")


row1 = kagome_top.add_ref(circle, columns=row_length, rows=5, column_pitch = a, row_pitch=2*a)
row1.move([hole_radius, 0])
row2 = kagome_top.add_ref(circle, columns=row_length/2, rows=5, column_pitch = 2*a, row_pitch=2*a)
row2.move([hole_radius+(a/2),a])



c2 = gf.Component("Kagome_positive")

c1 = gf.Component("Kagome_pos_all")
kagome_t = c1.add_ref(kagome_top)
kagome_b = c1 << kagome_top

kagome_b.dmirror_y()

# This is where we determine the defect width (y-coordinate) and the offset between the top and bottom PhC (x-coordinate)
kagome_b.move([0, -((2*(a+hole_radius)))])# Ty[ically the width of the defect slab is 2 x lattice cst



square_area = c2 << gf.components.rectangle(size=(a*(row_length-1), 24*a), layer=(1, 0))
square_area.move([hole_radius,-(13*a)-hole_radius])
 
c = gf.Component("Kagome_defect_PhC_{}_rows_a={}um".format(row_length,a))

final_geo = c << gf.boolean(square_area, c1, "A-B",layer=(1,0))
final_geo.move(destination=[0, 0], origin=[hole_radius, -(a+hole_radius)]) 
# final_b = c << gf.boolean(square_area, kagome_b, "A-B",layer=(1,0))


# Creates ports for the W1 PhC
c.add_port(
    name="opt1",
    center=(0, 0),     # (x, y) position in microns
    width=2*a,         # waveguide width in microns
    orientation=180,   # facing left (west)
    layer=(1, 0),      # GDS layer/datatype, optional if cross_section sets layer
    port_type="optical" # can be "optical", "electrical", etc.
)

# Add another port at (x=50, y=0), facing east (orientation=0 degrees)
c.add_port(
    name="opt2",
    center=(a*(row_length-1), 0),
    width=2*a,
    orientation=0,     # facing right (east)
    layer=(1, 0),
    port_type="optical"
)

# Becomes compatible with SiEPIC-Tools for PIC design 
c_with_pins = gf.add_pins.add_pins_siepic_optical(c)

c_with_pins.write_gds("Kagome_defect_PhC_{}_rows_a={}um.gds".format(row_length,a))

c_with_pins.show()
# 


