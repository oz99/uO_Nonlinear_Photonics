import numpy as np
import gdspy
import os

curr_path = os.path.dirname(os.path.abspath(__file__))

if __name__ == "__main__":
    
    fname = "lines_with_labels"  # Change the file name
    lib = gdspy.GdsLibrary(unit=1e-9, precision=1e-9)
    chip_h = 25e6
    chip_w = 5e6

    # Cell for the chip size and chip facets
    chip = lib.new_cell("NChip")

    # Function to create a line
    def create_line(start_point, end_point, line_thickness, nlayer):
        polygons = []

        # Calculate half-thickness
        half_thickness = line_thickness / 2

        # Create the line
        line = gdspy.Rectangle((start_point[0] - half_thickness, start_point[1]),
                               (end_point[0] + half_thickness, end_point[1]), layer=nlayer)
        polygons.append(line)

        return polygons

    # Function to create text with the same thickness as the lines
    def create_text(text, position, line_thickness, text_layer, text_height):
        text_width = len(text) * text_height / 2  # Rough estimation of text width
        text_position = (position[0] - text_width / 2, position[1] - text_height / 2)
        text_label = gdspy.Text(text, text_height, text_position, layer=text_layer)
        return text_label

    # Create the lines with specified parameters
    start_point1 = (0, 0)
    end_point1 = (0, 9)
    start_point2 = (5, 0)
    end_point2 = (5, 9)
    line_thickness = 0.1  # 0.05mm in nanometers
    nlayer = 1  # Layer number

    line_polygons1 = create_line(start_point1, end_point1, line_thickness, nlayer)
    line_polygons2 = create_line(start_point2, end_point2, line_thickness, nlayer)

    # Add both lines to the chip
    chip.add(line_polygons1)
    chip.add(line_polygons2)

    # Create text labels
    text_height = line_thickness * 10  # Set the text height to match the line thickness
    text_layer = nlayer  # Use the same layer as the lines
    left_text = create_text("Left", (-2, 4.5), line_thickness, text_layer, text_height)
    right_text = create_text("Right", (7, 4.5), line_thickness, text_layer, text_height)

    # Add text labels to the chip
    chip.add(left_text)
    chip.add(right_text)

    # Save to a gds file with the updated file name
    output_file = os.path.join(curr_path, "ShahramM", fname + ".gds")
    lib.write_gds(output_file)
    print("GDS file saved as:", output_file)
