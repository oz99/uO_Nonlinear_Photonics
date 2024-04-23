from functools import partial

import gdsfactory as gf
from gdsfactory.cell import cell
from gdsfactory.component import Component
from gdsfactory.port import Port

c = gf.Component("sample_connect")
# mmi1 = c << gf.components.mmi1x2()
# mmi2 = c << gf.components.mmi1x2()
#mmi2.move((100, 50))
# route = gf.routing.get_route(mmi1.ports["o2"], mmi2.ports["o1"], radius=10, width=0.5)
# c.add(route.references)




mmi1 = c << gf.components.ring_single(gap=0.2, radius=10.0, length_x=4.0, length_y=0.6, pass_cross_section_to_bend=True)
c.show()
