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
kagome_b.move([0, -2*a])



square_area = c2 << gf.components.rectangle(size=(a*(row_length-1), 24*a), layer=(1, 0))
square_area.move([hole_radius,-13*a])
 
c = gf.Component("Kagome_negative")
final_t = c << gf.boolean(square_area, c1, "A-B",layer=(1,0))
# final_b = c << gf.boolean(square_area, kagome_b, "A-B",layer=(1,0))




# row2.show()
c.show()
# 



