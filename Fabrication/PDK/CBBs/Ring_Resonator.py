import gdsfactory as gf
import json
import argparse

def main(args):
    # Parameters of Device
    w = args.width
    rad = args.radius
    l_str = rad
    l_coupler = args.couplerlength
    gap = args.couplergap

    if args.FullRing:
        c = gf.Component(name="RingResonator_Full")

        a = gf.Component("wg_in")
        a.add_polygon([(0, l_str, l_str, 0), (0, 0, w, w)], layer=(1,0))
        a.add_port(name="o1", center=[l_str-l_str, w/2], width = w, orientation=180, layer=(1,0), port_type='optical')
        a.add_port(name="o2", center=[l_str, w/2], width = w, orientation=0, layer=(1,0), port_type='optical')
        b = gf.Component("wg_thru")
        b.add_polygon([(l_str+l_coupler, l_str+l_coupler+l_str, l_str+l_coupler+l_str, l_str+l_coupler), (0, 0, w, w)], layer=(1,0))
        b.add_port(name="o1", center=[l_str+l_coupler, w/2], width = w, orientation=180, layer=(1,0), port_type='optical')
        b.add_port(name="o2", center=[l_str+l_coupler+l_str, w/2], width = w, orientation=0, layer=(1,0), port_type='optical')
        d = gf.Component("wg_drop")
        d.add_polygon([(0, l_str, l_str, 0), (w-w-gap-(2*rad)-w-gap, w-w-gap-(2*rad)-w-gap, w-w-gap-(2*rad)-w-gap-w, w-w-gap-(2*rad)-w-gap-w)], layer=(1,0))
        d.add_port(name="o1", center=[l_str-l_str, w-w-gap-(2*rad)-w-gap-(w/2)], width = w, orientation=180, layer=(1,0), port_type='optical')
        d.add_port(name="o2", center=[l_str, w-w-gap-(2*rad)-w-gap-(w/2)], width = w, orientation=0, layer=(1,0), port_type='optical')
        e = gf.Component("wg_add")
        e.add_polygon([(l_str+l_coupler, l_str+l_coupler+l_str, l_str+l_coupler+l_str, l_str+l_coupler), (w-w-gap-(2*rad)-w-gap, w-w-gap-(2*rad)-w-gap, w-w-gap-(2*rad)-w-gap-w, w-w-gap-(2*rad)-w-gap-w)], layer=(1,0))
        e.add_port(name="o1", center=[l_str+l_coupler, w-w-gap-(2*rad)-w-gap-(w/2)], width = w, orientation=180, layer=(1,0), port_type='optical')
        e.add_port(name="o2", center=[l_str+l_coupler+l_str, w-w-gap-(2*rad)-w-gap-(w/2)], width = w, orientation=0, layer=(1,0), port_type='optical')
        f = gf.Component("coupler_top")
        f.add_polygon([(l_str, l_str+l_coupler, l_str+l_coupler, l_str), (0, 0, w, w)], layer=(1,0))
        f.add_port(name="o1", center=[l_str, w/2], width = w, orientation=180, layer=(1,0), port_type='optical')
        f.add_port(name="o2", center=[l_str+l_coupler, w/2], width = w, orientation=0, layer=(1,0), port_type='optical')
        g = gf.Component("coupler_bottom")
        g.add_polygon([(l_str, l_str+l_coupler, l_str+l_coupler, l_str), (w-w-gap-(2*rad)-w-gap, w-w-gap-(2*rad)-w-gap, w-w-gap-(2*rad)-w-gap-w, w-w-gap-(2*rad)-w-gap-w)], layer=(1,0))
        g.add_port(name="o1", center=[l_str, w-w-gap-(2*rad)-w-gap-(w/2)], width = w, orientation=180, layer=(1,0), port_type='optical')
        g.add_port(name="o2", center=[l_str+l_coupler, w-w-gap-(2*rad)-w-gap-(w/2)], width = w, orientation=0, layer=(1,0), port_type='optical')

        # Ring
        xs1 = gf.cross_section.cross_section(width=w, offset=0, layer=(1,0))
        p1 = gf.path.straight(length=l_coupler, npoints=2)
        p2 = gf.path.arc(radius=rad, angle=90, npoints=101, start_angle=-90)
        p3 = gf.path.arc(radius=rad, angle=90, npoints=101, start_angle=-90)
        p4 = gf.path.straight(length=l_coupler, npoints=2)
        p5 = gf.path.arc(radius=rad, angle=90, npoints=101, start_angle=-90)
        p6 = gf.path.arc(radius=rad, angle=90, npoints=101, start_angle=-90)
        p = p1+p2+p3+p4+p5+p6
        total_p = p.extrude(xs1)
        wg_in = c << a
        wg_thru = c << b
        wg_drop = c << d
        wg_add = c << e
        wg_coup_top = c << f
        wg_coup_bottom = c << g
        ring = c << total_p
        ring.move(origin=(0,0), destination=(l_str, w-w-gap-(2*rad)-(w/2)))
        c.add_port("opt1", port=wg_in.ports["o1"])
        c.add_port("opt2", port=wg_thru.ports["o2"])
        c.add_port("opt3", port=wg_drop.ports["o1"])
        c.add_port("opt4", port=wg_add.ports["o2"])

        c.write_gds("RingResonatorFull.gds", with_metadata=True)

    if args.HalfRing:
        c = gf.Component(name="RingResonator_Half")

        a = gf.Component("wg_in")
        a.add_polygon([(0, l_str, l_str, 0), (0, 0, w, w)], layer=(1,0))
        a.add_port(name="o1", center=[l_str-l_str, w/2], width = w, orientation=180, layer=(1,0), port_type='optical')
        a.add_port(name="o2", center=[l_str, w/2], width = w, orientation=0, layer=(1,0), port_type='optical')
        b = gf.Component("wg_thru")
        b.add_polygon([(l_str+l_coupler, l_str+l_coupler+l_str, l_str+l_coupler+l_str, l_str+l_coupler), (0, 0, w, w)], layer=(1,0))
        b.add_port(name="o1", center=[l_str+l_coupler, w/2], width = w, orientation=180, layer=(1,0), port_type='optical')
        b.add_port(name="o2", center=[l_str+l_coupler+l_str, w/2], width = w, orientation=0, layer=(1,0), port_type='optical')
        f = gf.Component("coupler_top")
        f.add_polygon([(l_str, l_str+l_coupler, l_str+l_coupler, l_str), (0, 0, w, w)], layer=(1,0))
        f.add_port(name="o1", center=[l_str, w/2], width = w, orientation=180, layer=(1,0), port_type='optical')
        f.add_port(name="o2", center=[l_str+l_coupler, w/2], width = w, orientation=0, layer=(1,0), port_type='optical')

        # Ring
        xs1 = gf.cross_section.cross_section(width=w, offset=0, layer=(1,0))
        p1 = gf.path.arc(radius=rad, angle=90, npoints=101, start_angle=-90)
        p2= gf.path.arc(radius=rad, angle=90, npoints=101, start_angle=-90)
        p3 = gf.path.straight(length=l_coupler, npoints=2)
        p = p1+p3+p2
        total_p = p.extrude(xs1)
        wg_in = c << a
        wg_thru = c << b
        wg_coup_top = c << f
        ring = c << total_p
        ring.move(origin=(0,0), destination=(l_str+l_coupler+l_str, w-w-gap-rad)).rotate(angle=90, center=(l_str+l_coupler+l_str, w-w-gap-rad-(w/2)))
        c.add_port("opt1", port=wg_in.ports["o1"])
        c.add_port("opt2", port=wg_thru.ports["o2"])
        c.add_port("opt3", port=ring.ports["o2"])
        c.add_port("opt4", port=ring.ports["o1"])

        c.show()
        c.write_gds("RingResonatorHalf.gds", with_metadata=True)
        # elems=c.get_netlist()
        # instances=[]
        # for e1 in elems['instances']:
        #     instances.append(e1)
        #     print(instances)
        #     ports = []
        #     for e2 in elems['ports']:
        #         ports.append(e2)
        #         print(ports)

    
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--HalfRing', action='store_true', default=True, help='Set True to Activate (default: False)')
    parser.add_argument('--FullRing', action='store_true', default=True, help='Set True to Activate (default: False)')
    parser.add_argument('-width', type=float, default=1, help='Width of the Waveguide (default: 1 um)')
    parser.add_argument('-radius', type=float, default=10, help='Radius of the Ring Resonator (default: 50 um)')
    parser.add_argument('-couplerlength', type=float, default=50, help='Coupling Length of Directional Coupler (default: 10 um)')
    parser.add_argument('-couplergap', type=float, default=0.5, help='Directional Coupler Gap (default: 0.5 um)')
    args = parser.parse_args()
    main(args)

