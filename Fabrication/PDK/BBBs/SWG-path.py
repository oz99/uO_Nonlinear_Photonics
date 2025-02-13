import gdsfactory as gf
from gdsfactory.cross_section import ComponentAlongPath

import gplugins.path_length_analysis.path_length_analysis_from_gds as pl

# Create the path
# p = gf.path.straight()
# p += gf.path.arc(10)
# p += gf.path.straight()

P = gf.Path()


# Create the basic Path components
left_turn = gf.path.arc(radius=5, angle=180)
right_turn = gf.path.arc(radius=5, angle=-180)
straight_120 = gf.path.straight(length=120)
straight_110 = gf.path.straight(length=110)


# Assemble a complex path by making list of Paths and passing it to `append()`
P.append(
    [
        straight_110,
        right_turn,
        straight_120,
        left_turn,
        straight_120,
        right_turn,
        straight_120,
        left_turn,
        straight_120,
        right_turn,
        straight_110,


    ]
)

# f = P.plot()

# Define a cross-section with a via
grating = ComponentAlongPath(
    component=gf.c.rectangle(size=(0.14, 0.5), centered=True), spacing=0.2, padding=1
)


s = gf.Section(width=0.01, offset=0, layer=(2, 0), port_names=("o1", "o2"))
x = gf.CrossSection(sections=[s], components_along_path=[grating])

# Combine the path with the cross-section
c = gf.path.extrude(P, cross_section=x)

path_dict, ev_path_dict = pl.extract_paths(c, plot=True, under_sampling=1)
r_and_l_dict = pl.get_min_radius_and_length_path_dict(path_dict)
for ports, (min_radius, length) in r_and_l_dict.items():
    print(f"Ports: {ports}")
    print(f"Minimum radius of curvature: {min_radius:.2f}")
    print(f"Length: {length:.2f}")
    pl.plot_curvature(path_dict[ports])
print(c.info)


c.show()


