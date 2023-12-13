import gdsfactory as gf
from scipy.interpolate import CubicSpline
import numpy as np

def create_contour_component_with_ports():
    # Length of the shape and widths at specific points
    L = 2.5
    w0, w1, w2, w3, w4, w5 = [0.3, 0.6, 0.9, 0.8, 0.75, 0.7]
    breakpoints = np.linspace(0, L, 6)
    
    # Heights for the upper and lower halves
    heights_upper = [w0, w1, w2, w3, w4, w5]
    heights_lower = [-w for w in heights_upper]

    # Cubic Spline interpolation
    cs_upper = CubicSpline(breakpoints, heights_upper, bc_type='natural')
    cs_lower = CubicSpline(breakpoints, heights_lower, bc_type='natural')
    x_dense = np.linspace(0, L, 1000)
    y_upper = cs_upper(x_dense)
    y_lower = cs_lower(x_dense)

    # Create the polygon
    polygon_points = list(zip(x_dense, y_upper)) + list(zip(x_dense[::-1], y_lower[::-1]))

    # Create a new component
    c = gf.Component("contour_shape_with_ports")

    # Add the main contour shape
    c.add_polygon(polygon_points, layer=(1, 0))

    # Add a rectangle for the input port at the center on the left
    input_port_width = 0.6  # Width of the input port
    input_port_length = 2.0  # Length of the input port (extending leftwards)
    c.add_polygon([(-input_port_length, -input_port_width / 2), (0, -input_port_width / 2), 
                   (0, input_port_width / 2), (-input_port_length, input_port_width / 2)], layer=(1, 0))

    # Output ports at a specified distance from w5
    
    output_port_distance = 0.05  # Distance from w5, can be adjusted as needed
    output_port_y = w5 / 2 + output_port_distance
    port_output1 = c.add_port(name="output1", center=(L, output_port_y), orientation=0, width=w5)
    port_output2 = c.add_port(name="output2", center=(L, -output_port_y), orientation=0, width=w5)

    # Add rectangles (600nm x 2um) aligned with the output ports
    rect_width = 0.6
    rect_length = 2.0
    c.add_polygon([(port_output1.x, port_output1.y - rect_width / 2), 
                   (port_output1.x + rect_length, port_output1.y - rect_width / 2), 
                   (port_output1.x + rect_length, port_output1.y + rect_width / 2), 
                   (port_output1.x, port_output1.y + rect_width / 2)], layer=(1, 0))
    c.add_polygon([(port_output2.x, port_output2.y - rect_width / 2), 
                   (port_output2.x + rect_length, port_output2.y - rect_width / 2), 
                   (port_output2.x + rect_length, port_output2.y + rect_width / 2), 
                   (port_output2.x, port_output2.y + rect_width / 2)], layer=(1, 0))

    # Write to a GDS file and show
    c.write_gds("contour_shape_with_ports.gds")
    c.show()
    
    return c

# Example usage of the function with a specific output port distance
contour_component_with_ports = create_contour_component_with_ports()



######## This next portion of code was just to create  the contour shape with ports, but I wanted to keep it for reference. ########

# import gdsfactory as gf
# from scipy.interpolate import CubicSpline
# import numpy as np

# def create_contour_component_with_ports(output_port_distance):
#     # Length of the shape and widths at specific points
#     L = 2.5
#     w0, w1, w2, w3, w4, w5 = [0.3, 0.6, 0.9, 0.8, 0.75, 0.7]
#     breakpoints = np.linspace(0, L, 6)
    
#     # Heights for the upper and lower halves
#     heights_upper = [w0, w1, w2, w3, w4, w5]
#     heights_lower = [-w for w in heights_upper]

#     # Cubic Spline interpolation
#     cs_upper = CubicSpline(breakpoints, heights_upper, bc_type='natural')
#     cs_lower = CubicSpline(breakpoints, heights_lower, bc_type='natural')
#     x_dense = np.linspace(0, L, 1000)
#     y_upper = cs_upper(x_dense)
#     y_lower = cs_lower(x_dense)

#     # Create the polygon
#     polygon_points = list(zip(x_dense, y_upper)) + list(zip(x_dense[::-1], y_lower[::-1]))

#     # Create a new component
#     c = gf.Component("contour_shape_with_ports")

#     # Add the main contour shape
#     c.add_polygon(polygon_points, layer=(1, 0))

#     # Define the input port
#     input_port_y = 0  # Centered vertically
#     c.add_port(name="input", center=(0, input_port_y), width=w0, orientation=180)

#     # Define the output ports
#     output_port_y_upper = w5 / 2 + output_port_distance
#     output_port_y_lower = -w5 / 2 - output_port_distance
#     c.add_port(name="output1", center=(L, output_port_y_upper), width=w5, orientation=0)
#     c.add_port(name="output2", center=(L, output_port_y_lower), width=w5, orientation=0)

#     # Write to a GDS file and show
#     c.write_gds("contour_shape_with_ports.gds")
#     c.show()
    
#     return c

# # Example usage of the function with a specific output port distance
# output_port_distance = 0.05  # Distance from w5, can be adjusted as needed
# contour_component_with_ports = create_contour_component_with_ports(output_port_distance)
