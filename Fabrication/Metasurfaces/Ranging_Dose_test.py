import gdsfactory as gf
from gdsfactory.generic_tech import get_generic_pdk
import math

import L_shape_YAML_proximity_correction

PDK = get_generic_pdk()
PDK.activate()

### L shape with proximity correction
### Run the code in L_shape_YAML_proximity_correction.py with 10 varying argument sets
### The arguments are width, length1, length2, layer, overdose, underdose
### The arguments are in nm

args = [
    [80, 170, 160, (1, 0), 10, 10],
    [80, 170, 160, (1, 0), 20, 20],
    [80, 170, 160, (1, 0), 30, 30],
    [80, 170, 160, (1, 0), 40, 40],
    [80, 170, 160, (1, 0), 50, 50],
    [80, 170, 160, (1, 0), 60, 60],
    [80, 170, 160, (1, 0), 70, 70],
    [80, 170, 160, (1, 0), 80, 80],
    [80, 170, 160, (1, 0), 90, 90],
    [80, 170, 160, (1, 0), 100, 100]
]

for arg in args:
    L_shape_YAML_proximity_correction.main(arg)
    ## Move each component to x nm away from eachother
    ## x = 1000
    x += 1000
    c.move([x,0])
    c.show()


# c = gf.Component()
# c = gf.components.L(width=80, size=(170, 160), layer=(1, 0))
# gdspath = c.write_gds(precision=1e-9, unit=1e-9)

# gf.show()