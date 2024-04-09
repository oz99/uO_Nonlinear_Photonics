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
    fname = "DoseTest" # get script name
    # Examples
    lib = gdspy.GdsLibrary(unit=1e-6, precision=1e-9)
    #------------------------------------
    chip_h = 18e6/1000
    chip_w = 18e6/1000
    wf_l = 100e3/1000
    #load cells
    # libLig = gdspy.GdsLibrary(infile=loadlibname)

    #---------------------
    #cell for the chip size and chip facets
    #chip = lib.new_cell("NChip")

    #---------------------
    #cell for the write field
    #wf = lib.new_cell("WF")

    #---------------------
    #cell for the antennas
    ant = lib.new_cell("Dose_Antenna")

    # wf.add(gdspy.Rectangle((0, 0), (wf_l, wf_l), layer=0))

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
    
        return poly
    
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

    

    
    n_x = 2 # number of antennas in x direction
    n_y = 11 # number of antennas in y direction
    offset_x = 2.5e3/1000 # horizontal margin
    offset_y = 2.5e3/1000 # vertical margin
    sqr_l = 20/1000 # length of square for proximity correction
    #---------------------
    # antenna parameters
    l1V = 170/1000
    w1V = 80/1000
    l2V = 160/1000
    w2V = 80/1000
    delta_x_V = 450/1000 # horizonal offset between V-shape antennas
    delta_y_V = 900/1000 # vertical offset between V-shape antennas

    h1U = 160/1000
    w1U = 120/1000
    h2U = 100/1000
    w2U = 320/1000
    delta_x_U = 1500/1000 # horizonal offset between U-shape antennas
    delta_y_U = 1500/1000 # vertical offset between U-shape antennas

    #---------------------
    # alignment mark parameters
    len_mark_s = 2e3/1000
    width_mark_s = 500/1000
    side_mark_s = 20e3/1000

    len_mark_g = 40e3/1000
    width_mark_g = 20e3/1000
    side_mark_g = 100e3/1000

    #---------------------
    #function for the dose test building block
    def DoseTest(x0, y0):
    
        AlMk(x0, y0, len_mark_s, width_mark_s, side_mark_s, 2)

        # Vertical dose label with height 1.5
        for i, v in enumerate("ABCDEFGHIJK"):
            label = gdspy.Text(v, 1, (2.4e3/1000 + x0, 2.1e3/1000+i*delta_y_U + y0), horizontal=False, layer=1)
            ant.add(label)

        for i in range(n_x):
            for j in range(n_y):
                ant.add(Lshape2(l1V, w1V, l2V, w2V, offset_x+(i+1)*delta_x_U + x0, offset_y+j*delta_y_U + y0, 1))

        for i in range(n_x):
            for j in range(n_y):
                prox_corr_L(l1V, w1V, l2V, w2V, sqr_l, offset_x+(i-1+2*n_x)*delta_x_U + x0, offset_y+j*delta_y_U + y0, 1)

        for i in range(n_x):
            for j in range(n_y):
                vShape = Lshape2(l1V, w1V, l2V, w2V, 0, 0, 1).rotate(math.pi/4)
                vShape.translate(offset_x+(i-1+3*n_x)*delta_x_U + x0, offset_y+j*delta_y_U + y0)
                ant.add(vShape)

        for i in range(n_x):
            for j in range(n_y):
                Ushape(h1U, w1U, h2U, w2U, offset_x+(i-1+4*n_x)*delta_x_U + x0, offset_y+j*delta_y_U + y0, 1)

        for i in range(n_x):
            for j in range(n_y):
                prox_corr_U(h1U, w1U, h2U, w2U, sqr_l, offset_x+(i-1+5*n_x)*delta_x_U + x0, offset_y+j*delta_y_U + y0, 1)

    AlMk(-3*width_mark_g, -3*width_mark_g, len_mark_g, width_mark_g, side_mark_g+6*width_mark_g, 2)

    for i in range(2):
            for j in range(2):
                DoseTest(i*4*side_mark_s, j*4*side_mark_s)
    DoseTest(wf_l/2 - side_mark_s/2, wf_l/2 - side_mark_s/2)

    rad = 150/1000
    pitch = 5*rad
    for i in range(17):
        ant.add(gdspy.Round((wf_l/2, offset_y+i*(pitch+rad)), rad, tolerance=0.01))
        ant.add(gdspy.Round((wf_l/2, offset_y+4*side_mark_s+i*(pitch+rad)), rad, tolerance=0.01))
        ant.add(gdspy.Round((offset_x+i*(pitch+rad), 2.5*side_mark_s), rad, tolerance=0.01))
        ant.add(gdspy.Round((offset_x+4*side_mark_s+i*(pitch+rad), 2.5*side_mark_s), rad, tolerance=0.01))


    # chip_facet1 = gdspy.Rectangle((0, cut_y), (chip_w, chip_h - cut_y))
    # chip_facet1 = gdspy.Rectangle((0, 0), (chip_w, chip_h), layer=0)
    # ant.add(chip_facet1)

    # Save to a gds file and check out the output
    print(os.path.join(curr_path,"gdsii",fname+".gds"))
    lib.write_gds(os.path.join(curr_path,"gdsii",fname+".gds"))