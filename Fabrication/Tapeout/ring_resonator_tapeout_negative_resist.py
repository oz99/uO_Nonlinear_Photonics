from functools import partial

import gdsfactory as gf
from gdsfactory.cell import cell
from gdsfactory.component import Component
from gdsfactory.port import Port


import gdsfactory as gf


c = gf.Component("Sample_Cascase_Rings")
ring1 = c << gf.components.ring_single(gap=0.2, radius=10.0, length_x=4.0, length_y=0.6, pass_cross_section_to_bend=True)
ring2 = c << gf.components.ring_single(gap=0.2, radius=10.0, length_x=4.0, length_y=0.6, pass_cross_section_to_bend=True)
ring2.move((100, 100))
route = gf.routing.get_route(ring1.ports["o2"], ring2.ports["o1"], radius=10, width=0.5)
c.add(route.references)

#c = gf.components.ring_section_based(gap=0.055, radius=25.0, add_drop=False, cross_sections_sequence='AB', start_angle=10.0, ang_res=0.1)
c.show()

## how do I determine the port location?
# c = gf.Component("sample_connect")
# mmi1 = c << gf.components.mmi1x2()
# mmi2 = c << gf.components.mmi1x2()
# mmi2.move((100, 100))
# route = gf.routing.get_route(mmi1.ports["o2"], mmi2.ports["o1"], radius=10, width=0.5)

# mmi1 = c << gf.components.ring_single(gap=0.2, radius=10.0, length_x=4.0, length_y=0.6, pass_cross_section_to_bend=True)
#c.show()
