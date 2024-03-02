######################################################################
#                                                                    #
#  Copyright 2009 Lucas Heitzmann Gabrielli.                         #
#  This file is part of gdspy, distributed under the terms of the    #
#  Boost Software License - Version 1.0.  See the accompanying       #
#  LICENSE file or <http://www.boost.org/LICENSE_1_0.txt>            #
#                                                                    #
######################################################################
# import sys
import numpy as np
import gdspy
import math
# import datetime   
import os

curr_path = os.path.dirname(os.path.abspath(__file__))

if __name__ == "__main__":
    #fname = sys.argv[0].split(".")[0] # get script name
    fname = "metasurface" # get script name
    # Examples
    lib = gdspy.GdsLibrary(unit=1e-9, precision=1e-9)
    #------------------------------------
    chip_h = 25e6
    chip_w = 75e6
    #load cells
    # libLig = gdspy.GdsLibrary(infile=loadlibname)

    #---------------------
    #cell for the chip size and chip facets
    # chip = lib.new_cell("NChip")

    #---------------------
    #cell for the antennas
    ant = lib.new_cell("Antenna")

    #---------------------
    #function for the L shaped antennas
    def Lshape(len1, width1, len2, width2, x0, y0, nlayer):
        path1 = gdspy.Path(width1, (x0, y0+len1-width2/2))
        path1.segment(len1,'-y', layer=nlayer)
        #bend right and up
        path2 = gdspy.Path(width2, (x0+width1/2, y0))
        path2.segment(len2-width1,'+x', layer=nlayer)
        #add to cell
        ant.add(path1)
        ant.add(path2)
    #---------------------
    #function for the L shaped antennas
    def Lshape2(len1, width1, len2, width2, x0, y0, nlayer):
        y1 = y0 + len1
        x2 = x0 + width1
        y3 = y0 + width2
        x4 = x0 + len2
        vertices = [(x0, y0), (x0, y1), (x2, y1), (x2, y3), (x4, y3), (x4, y0)]
        poly = gdspy.Polygon(vertices, layer=nlayer)
    
        #add to cell
        ant.add(poly)
    
    #---------------------
    #function for the L shaped proximity correction
    def prox_corr_L(len1, width1, len2, width2, sqr_l, x0, y0, nlayer):
        y1 = y0 + len1
        x2 = x0 + width1
        y3 = y0 + width2 + sqr_l/2
        x4 = x2 - sqr_l/2
        y5 = y3 - sqr_l
        x6 = x4 + sqr_l
        y7 = y0 + width2
        x8 = x0 + len2
        vertices = [(x0, y0), (x0, y1), (x2, y1), (x2, y3), (x4, y3), (x4, y5), (x6, y5), (x6, y7), (x8, y7), (x8, y0)]
        poly = gdspy.Polygon(vertices, layer=nlayer)
        square1 = gdspy.Rectangle((x0-sqr_l/2, y0-sqr_l/2), (x0+sqr_l/2, y0+sqr_l/2), layer=nlayer)
        square2 = gdspy.Rectangle((x0-sqr_l/2, y1-sqr_l/2), (x0+sqr_l/2, y1+sqr_l/2), layer=nlayer)
        square3 = gdspy.Rectangle((x2-sqr_l/2, y1-sqr_l/2), (x2+sqr_l/2, y1+sqr_l/2), layer=nlayer)
        square4 = gdspy.Rectangle((x8-sqr_l/2, y7-sqr_l/2), (x8+sqr_l/2, y7+sqr_l/2), layer=nlayer)
        square5 = gdspy.Rectangle((x8-sqr_l/2, y0-sqr_l/2), (x8+sqr_l/2, y0+sqr_l/2), layer=nlayer)
        #add to cell
        ant.add(poly)
        ant.add(square1)
        ant.add(square2)
        ant.add(square3)
        ant.add(square4)
        ant.add(square5)

    #---------------------
    #function for coordinate rotation
    def rotate(angle, x, y):
        rot_x = x * math.cos(angle) - y * math.sin(angle)
        rot_y = x * math.sin(angle) + y * math.cos(angle)
    
        return rot_x, rot_y

    #---------------------
    #function for the U shape
    def Ushape(height1, width1, height2, width2, x0, y0, nlayer):
        y1 = y0 + height1
        x2 = x0 + width1
        y3 = y0 + height2
        x4 = x0 + width2 - width1
        x6 = x0 + width2
        
        vertices = [(x0, y0), (x0, y1), (x2, y1), (x2, y3), (x4, y3), (x4, y1), (x6, y1), (x6, y0)]
        poly = gdspy.Polygon(vertices, layer=nlayer)

        #add to cell
        ant.add(poly)

       #---------------------
    #function for the U shaped proximity correction
    def prox_corr_U(height1, width1, height2, width2, sqr_l, x0, y0, nlayer):
        y1 = y0 + height1
        x2 = x0 + width1
        y3 = y0 + height2 + sqr_l/2
        x4 = x2 - sqr_l/2
        y5 = y3 - sqr_l
        x6 = x4 + sqr_l
        y7 = y0 + height2
        x8 = x0 + width2 - width1 - sqr_l/2
        x10 = x8 + sqr_l
        x12 = x10 - sqr_l/2
        x14 = x0 + width2
        vertices = [(x0, y0), (x0, y1), (x2, y1), (x2, y3), (x4, y3), (x4, y5), (x6, y5), (x6, y7), (x8, y7), (x8, y5), (x10, y5), (x10, y3), (x12, y3), (x12, y1), (x14, y1), (x14, y0)]
        poly = gdspy.Polygon(vertices, layer=nlayer)
        square1 = gdspy.Rectangle((x0-sqr_l/2, y0-sqr_l/2), (x0+sqr_l/2, y0+sqr_l/2), layer=nlayer)
        square2 = gdspy.Rectangle((x0-sqr_l/2, y1-sqr_l/2), (x0+sqr_l/2, y1+sqr_l/2), layer=nlayer)
        square3 = gdspy.Rectangle((x2-sqr_l/2, y1-sqr_l/2), (x2+sqr_l/2, y1+sqr_l/2), layer=nlayer)
        square4 = gdspy.Rectangle((x12-sqr_l/2, y1-sqr_l/2), (x12+sqr_l/2, y1+sqr_l/2), layer=nlayer)
        square5 = gdspy.Rectangle((x14-sqr_l/2, y1-sqr_l/2), (x14+sqr_l/2, y1+sqr_l/2), layer=nlayer)
        square6 = gdspy.Rectangle((x14-sqr_l/2, y0-sqr_l/2), (x14+sqr_l/2, y0+sqr_l/2), layer=nlayer)
        #add to cell
        ant.add(poly)
        ant.add(square1)
        ant.add(square2)
        ant.add(square3)
        ant.add(square4)
        ant.add(square5)
        ant.add(square6)

    #---------------------
    #function for the alignment marks
    def AlMk(x0, y0, len, width, side, nlayer):
        
        mark1 = Lshape2(len, width, len, width, x0, y0, nlayer)
        
        poly2 = Lshape2(len, width, len, width, 0, 0, nlayer)
        poly2.rotate(math.pi)
        mark2 = poly2.translate(x0+side, y0+side)

        poly3 = Lshape2(len, width, len, width, 0, 0, nlayer)
        poly3.rotate(math.pi/2)
        mark3 = poly3.translate(x0+side, y0)

        poly4 = Lshape2(len, width, len, width, 0, 0, nlayer)
        poly4.rotate(3*math.pi/2)
        mark4 = poly4.translate(x0, y0+side)

        ant.add(mark1)
        ant.add(mark2)
        ant.add(mark3)
        ant.add(mark4)

    #---------------------
    # Positive resist case
    delta_x_V = 700 # horizonal offset between antennas
    delta_y_V = 700 # vertical offset between antennas
    delta_x_U = 1500 # horizonal offset between antennas
    delta_y_U = 1500 # vertical offset between antennas
    n_x = 400 # number of antennas in x direction
    n_y = 400 # number of antennas in y direction
    offset = 100 # margin
    sqr_l = 20 #length of square for proximity correction
    #---------------------
    # antenna parameters
    l1V = 200
    w1V = 100
    l2V = 190
    w2V = 100

    h1U = 80
    w1U = 60
    h2U = 50
    w2U = 160

    len_mark_g = 40e3
    width_mark_g = 20e3
    side_mark_g = 500e3

    # for i in range(n_x):
    #     for j in range(n_y):

    #         Lshape2(l1V, w1V, l2V, w2V, offset+i*delta_x_V, offset+j*delta_y_V, 1)

    # for i in range(n_x):
    #     for j in range(n_y):
    #         rot_x0, rot_y0 = rotate(math.pi/4, offset+i*delta_x_V, offset+j*delta_y_V)
    #         Lshape2(l1V, w1V, l2V, w2V, rot_x0, rot_y0, 2)
    # AlMk(0, 0, len_mark_g, width_mark_g, side_mark_g, 1)

    for i in range(n_x):
        for j in range(n_y):
            rot_x0, rot_y0 = rotate(math.pi/4, offset+i*delta_x_V, offset+j*delta_y_V)
            margin_x = math.cos(math.pi/4) * delta_y_V * n_y
            prox_corr_L(l1V, w1V, l2V, w2V, sqr_l, rot_x0 + margin_x, rot_y0, 1)
   
    # for i in range(n_x):
    #     for j in range(n_y):

    #         Ushape(h1U, w1U, h2U, w2U, offset+i*delta_x_U, offset+j*delta_y_U, 4)
    
    # for i in range(2):
    #     for j in range(2):
    #         rot_x0, rot_y0 = rotate(math.pi/4, offset+i*delta_x_V, offset+j*delta_y_V)
    #         margin_x = math.cos(math.pi/4) * delta_y_V * n_y
    #         prox_corr_U(h1U, w1U, h2U, w2U, sqr_l, rot_x0 + margin_x, rot_y0, 4)

    # chip_facet1 = gdspy.Rectangle((0, cut_y), (chip_w, chip_h - cut_y))
    # chip_facet1 = gdspy.Rectangle((0, 0), (chip_w, chip_h), layer=0)
    # ant.add(chip_facet1)

    

    # Save to a gds file and check out the output
    print(os.path.join(curr_path,"gdsii",fname+".gds"))
    lib.write_gds(os.path.join(curr_path,"gdsii",fname+".gds"))