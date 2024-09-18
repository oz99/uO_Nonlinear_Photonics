#num_gratings = 110;  # Number of grating elements
#initial_period = 0.4e-6;  # Initial period of the grating (e.g., 700 nm)
#final_period = 0.267e-6;  # Final period of the grating (e.g., 300 nm)
#initial_width = 0.2e-6;  # Initial width of the grating element (e.g., 350 nm)
#final_width = 0.17e-6;  # Final width of the grating element (e.g., 150 nm)
#initial_duty_cycle = 0.5;  # Initial duty cycle (50% of the period)
#final_duty_cycle = 0.6;  # Final duty cycle (80% of the period)
#tapering_length = 35e-6;  # Length over which tapering occurs (e.g., 10 microns)
#initial_y_span = 0.2e-6;  # Initial height of the grating element (e.g., 450 nm)
#final_y_span = 0.45e-6;  # Final height of the grating element (e.g., 250 nm)

# Loop to create tapered grating elements
for (i = 0:num_gratings-(num_gratings*0.1)) {
    xpos = i * initial_period;  # Positioning each grating element based on the initial period

    # Calculate the taper ratio based on the manual tapering length
    #if (xpos <= tapering_length) {
        #taper_ratio = xpos / tapering_length;  # Ratio within the tapering length
    #} else {
        #taper_ratio = 1;  # Beyond tapering length, keep the property constant
    #}
    
    # Calculate the taper ratio based on the position
    taper_ratio = i / (num_gratings-1);
    
    # Taper the period
    current_period = initial_period * (1 - taper_ratio) + final_period * taper_ratio;
    
    # Taper the duty cycle
    current_duty_cycle = initial_duty_cycle * (1 - taper_ratio) + final_duty_cycle * taper_ratio;
    
    # Calculate the width of the current grating element
    current_width = current_duty_cycle * current_period;

    # Taper the grating width independently of the duty cycle
    actual_width = initial_width * (1 - taper_ratio) + final_width * taper_ratio;
    
    # Taper the y span (height)
    current_y_span = initial_y_span * (1 - taper_ratio) + final_y_span * taper_ratio;
    
    # Calculate the gap between this segment and the next
    current_gap = current_period - current_width;
    
        # Create the rectangular grating element
    addrect;
    set("x", xpos + current_width / 2);  # Position the element
    set("x span", current_width);  # Apply the actual width
    set("y", 0);
    set("y span", current_y_span);  # Apply the tapered height (y span)
    set("z", 0);
    set("z span", height);
    
 }
 
#####################################################################
# Linear taper
# This object makes a linear taper with angled sidewalls.  
# 
# Input properties
# thickness:         waveguide height
# base angle:        sidewall angle of the waveguide
# width_l & width_r: the left and right width of the taper
# len:               length of the taper
# hfrac_ref:         the reference height at where the widths are specified, 0 =< hfrac_ref =< 1.  This is relative to the height of the trapeziod (waveguide cross section) 
#		The most common cases:
#		1   : top width
#		0.5 : middle width
#		0   : bottom width
#
# Tags: integrated optics waveguide linear taper
#
# Copyright 2018 Lumerical Solutions Inc
#####################################################################
grating_span = num_gratings*(initial_period);
taper_fraction = %taper fraction%;
delta_w = 2*height*tan((90-angle_side)*pi/180);
width_r = final_y_span;

?"width_l = " + num2str(width_l);
?"width_r = " + num2str(width_r) + endl;

width_top_l = width_l - (1-hfrac_ref)*delta_w;
width_top_r = width_r - (1-hfrac_ref)*delta_w;
?"width_top_l = " + num2str(width_top_l);
?"width_top_r = " + num2str(width_top_r) + endl;

width_bot_l = width_l + hfrac_ref*delta_w;
width_bot_r = width_r + hfrac_ref*delta_w;
?"width_bot_l = " + num2str(width_bot_l);
?"width_bot_r = " + num2str(width_bot_r) + endl;

# Error checking:

if ((hfrac_ref>1) or (hfrac_ref<0)){
    ?"Error: hfrac_ref must be between 0 and 1.";
    break;
}

if ((width_top_l<0) or (width_top_r<0) or (width_bot_l<0) or (width_bot_r<0)){
    ?"Error: width and angle values are not correct.";
    break;
}

zmin = -height/2;
zmax = height/2;


xmin = grating_span*taper_fraction;
xmax = grating_span;


ymin_bot_l = -width_bot_l/2;
ymax_bot_l = width_bot_l/2;


ymin_bot_r = -width_bot_r/2;
ymax_bot_r = width_bot_r/2;


ymin_top_l = -width_top_l/2;
ymax_top_l = width_top_l/2;


ymin_top_r = -width_top_r/2;
ymax_top_r = width_top_r/2;




vtx=    [xmin,ymin_bot_l,zmin;    #1
        xmax,ymin_bot_r,zmin;     #2
        xmax,ymax_bot_r,zmin;     #3
        xmin,ymax_bot_l,zmin;     #4  
        xmin,ymin_top_l,zmax;     #5
        xmax,ymin_top_r,zmax;     #6
        xmax,ymax_top_r,zmax;     #7  
        xmin,ymax_top_l,zmax];    #8


a = cell(6);
for(i = 1:6){
    a{i} = cell(1);
}        


#facets:


a{1}{1} = [1,4,3,2]; #bottom facet
a{2}{1} = [1,2,6,5];
a{3}{1} = [2,3,7,6];
a{4}{1} = [3,4,8,7];
a{5}{1} = [1,5,8,4];
a{6}{1} = [5,6,7,8]; #top facet


addplanarsolid(vtx,a);

##############################################################
# Straight waveguide 
# This object makes a straight waveguide with angled sidewalls.  
# 
# Input properties
# base angle: sidewall angle of the waveguide
# base height: height of the waveguide
# base width: width of the waveguide base
# x span: x span of the waveguide
# y span: y span of the waveguide
#
# Tags: integrated optics waveguide straight ridge
#
# Copyright 2015 Lumerical Solutions Inc
##############################################################

addrect;
    set("x", grating_span+%x span%/2);  # Position the element
    set("x span", %x span%);  # Apply the actual width
    set("y", 0);
    set("y span", final_y_span);  # Apply the tapered height (y span)
    set("z", 0);
    set("z span", height);

selectall;
set("material",material); 
if(get("material")=="<Object defined dielectric>") 
  { set("index",index); } 
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--length', type=float, default=5, help='Length of the y-spliter')


    parser.add_argument('--NetlistNew', action='store_true', default=True, help='Set True to Activate (default: False)')
    args = parser.parse_args()
    main(args)