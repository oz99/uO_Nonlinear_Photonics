#test

import gdsfactory as gf

# c = gf.Component()
# top = c << gf.components.nxn(north=8, south=0, east=0, west=0)
# bot = c << gf.components.nxn(north=2, south=2, east=2, west=2, xsize=10, ysize=10)
# top.dmovey(100)

# routes = gf.routing.route_bundle(
#     c,
#     ports1=bot.ports,
#     ports2=top.ports,
#     radius=5,
#     sort_ports=True,
# )

c = gf.Component()
c.add_polygon([(-8, -6), (6, 8), (7, 17), (9, 5)], layer=(1, 0))

c.show()