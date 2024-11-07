import gdsfactory as gf
from gdsfactory.cross_section import ComponentAlongPath

# Create the path
# p = gf.path.straight()
# p += gf.path.arc(10)
# p += gf.path.straight()

P = gf.Path()


# Create the basic Path components
left_turn = gf.path.euler(radius=4, angle=90)
right_turn = gf.path.euler(radius=4, angle=-90)
straight = gf.path.straight(length=10)


# Assemble a complex path by making list of Paths and passing it to `append()`
P.append(
    [
        straight,
        left_turn,
        straight,
        right_turn,
        straight,
        straight,
        right_turn,
        left_turn,
        straight,
        left_turn,


    ]
)

# Combine the path with the cross-section
c = gf.path.extrude(P, layer=(1,0), width=0.5)
c.show()


