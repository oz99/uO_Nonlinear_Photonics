import gdsfactory as gf


############################################ For a simple row of squares ###########################################################
# def create_periodic_squares_route():
#     # Create a new component
#     c = gf.Component("periodic_squares_route")

#     # Define the size of the squares and the spacing between them
#     square_size = 10
#     spacing = 5
#     num_squares = 10

#     # Create the squares and add them to the component
#     for i in range(num_squares):
#         square = gf.components.rectangle(size=(square_size, square_size))
#         c.add_ref(square).move((i * (square_size + spacing), 0))

#     return c

# # Create the route of periodic squares
# component = create_periodic_squares_route()

# # Save the component to a GDS file
# component.write_gds("periodic_squares_route.gds")

# # Display the component in KLayout
# gf.show(component)

#################################### Routing using this #################################################################################

def create_perpendicular_squares_route():
    # Create a new component
    c = gf.Component("perpendicular_squares_route")

    # Define the size of the squares and the spacing between them
    square_size = 10
    spacing = 5
    num_squares = 10

    # Create the squares and add them to the component
    for i in range(num_squares):
        square = gf.components.rectangle(size=(square_size, square_size))
        ref = c.add_ref(square)
        ref.move((i * (square_size + spacing), 0))
        ref.rotate(90)  # Rotate the square to make it perpendicular to the route

    return c

# Create the route of perpendicular squares
component = create_perpendicular_squares_route()

# Save the component to a GDS file
component.write_gds("perpendicular_squares_route.gds")

# Display the component in KLayout
gf.show(component)

# def create_periodic_squares_route_with_coordinates(coordinates):
#     # Create a new component
#     c = gf.Component("periodic_squares_route_with_coordinates")

#     # Define the size of the squares
#     square_size = 10

#     # Create the squares at the specified coordinates and add them to the component
#     for coord in coordinates:
#         square = gf.components.rectangle(size=(square_size, square_size))
#         c.add_ref(square).move(coord)

#     return c

# # Define the coordinates for the squares
# coordinates = [(0, 0), (20, 10), (40, 20), (60, 30), (80, 40)]

# # Create the route of periodic squares with coordinates
# component = create_periodic_squares_route_with_coordinates(coordinates)

# # Save the component to a GDS file
# component.write_gds("periodic_squares_route_with_coordinates.gds")

# # Display the component in KLayout
# gf.show(component)