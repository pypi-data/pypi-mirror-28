# -*- coding: utf-8 -*-

# Copyright (c) 2016-2017 by University of Kassel and Fraunhofer Institute for Wind Energy and
# Energy System Technology (IWES), Kassel. All rights reserved. Use of this source code is governed
# by a BSD-style license that can be found in the LICENSE file.

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.collections import LineCollection, PatchCollection
from matplotlib.patches import Circle, Ellipse, Rectangle, RegularPolygon, Arc
from matplotlib.transforms import Affine2D

try:
    import pplog as logging
except ImportError:
    import logging

logger = logging.getLogger(__name__)


def _rotate_dim2(arr, ang):
    """
    :param arr: array with 2 dimensions
    :param ang: angle [rad]
    """
    return np.dot(np.array([[np.cos(ang), np.sin(ang)], [-np.sin(ang), np.cos(ang)]]), arr)


def create_bus_symbol_collection(coords, buses=None, size=5, marker="o", patch_type="circle",
                                 colors=None, z=None, cmap=None, norm=None, infofunc=None,
                                 picker=False, net=None, cbar_title="Bus Voltage [pu]", **kwargs):
    infos = []

    if 'height' in kwargs and 'width' in kwargs:
        height, width = kwargs['height'], kwargs['width']
    else:
        height, width = size, size

    def figmaker(x, y, i):
        if patch_type == "circle":
            if colors:
                fig = Circle((x, y), size, color=colors[i], **kwargs)
            else:
                fig = Circle((x, y), size, **kwargs)
        elif patch_type == 'ellipse':
            angle = kwargs['angle'] if 'angle' in kwargs else 0
            if colors:
                fig = Ellipse((x, y), width=width, height=height, color=colors[i], **kwargs)
            else:
                fig = Ellipse((x, y), width=width, height=height, angle=angle, **kwargs)
        elif patch_type == "rect":
            if colors:
                fig = Rectangle([x - width, y - height], 2 * width, 2 * height, color=colors[i],
                                **kwargs)
            else:
                fig = Rectangle([x - width, y - height], 2 * width, 2 * height, **kwargs)
        elif patch_type.startswith("poly"):
            edges = int(patch_type[4:])
            if colors:
                fig = RegularPolygon([x, y], numVertices=edges, radius=size, color=colors[i],
                                     **kwargs)
            else:
                fig = RegularPolygon([x, y], numVertices=edges, radius=size, **kwargs)
        else:
            logger.error("Wrong patchtype. Please choose a correct patch type.")
        if infofunc:
            infos.append(infofunc(buses[i]))
        return fig

    patches = [figmaker(x, y, i)
               for i, (x, y) in enumerate(coords)
               if x != np.nan]
    pc = PatchCollection(patches, match_original=True, picker=picker)
    pc.bus_indices = np.array(buses)
    if cmap:
        pc.set_cmap(cmap)
        pc.set_norm(norm)
        if z is None and net:
            z = net.res_bus.vm_pu.loc[buses]
        else:
            logger.warning("z is None and no net is provided")
        pc.set_array(np.array(z))
        pc.has_colormap = True
        pc.cbar_title = cbar_title

    pc.patch_type = patch_type
    pc.size = size
    if 'orientation' in kwargs:
        pc.orientation = kwargs['orientation']
    if "zorder" in kwargs:
        pc.set_zorder(kwargs["zorder"])
    pc.info = infos
    return pc


def create_bus_collection(net, buses=None, size=5, marker="o", patch_type="circle", colors=None,
                          z=None, cmap=None, norm=None, infofunc=None, picker=False,
                          bus_geodata=None, cbar_title="Bus Voltage [pu]", **kwargs):
    """
    Creates a matplotlib patch collection of pandapower buses.

    Input:
        **net** (pandapowerNet) - The pandapower network

    OPTIONAL:
        **buses** (list, None) - The buses for which the collections are created.
        If None, all buses in the network are considered.

        **size** (int, 5) - patch size

        **marker** (str, "o") - patch marker

        **patch_type** (str, "circle") - patch type, can be

                - "circle" for a circle
                - "rect" for a rectangle
                - "poly<n>" for a polygon with n edges

        **infofunc** (function, None) - infofunction for the patch element

        **colors** (list, None) - list of colors for every element

        **cmap** - colormap for the patch colors

        **bus_geodata** (DataFrame, None) - coordinates to use for plotting
        If None, net["bus_geodata"] is used

        **picker** - picker argument passed to the patch collection

        **kwargs - key word arguments are passed to the patch function

    OUTPUT:
        **pc** - patch collection
    """
    buses = net.bus.index.tolist() if buses is None else list(buses)
    if len(buses) == 0:
        return None
    if bus_geodata is None:
        bus_geodata = net["bus_geodata"]

    coords = zip(bus_geodata.loc[buses, "x"].values, bus_geodata.loc[buses, "y"].values)

    pc = create_bus_symbol_collection(coords=coords, buses=buses, size=size, marker=marker,
                                      patch_type=patch_type, colors=colors, z=z, cmap=cmap,
                                      norm=norm, infofunc=infofunc, picker=picker, net=net,
                                      cbar_title=cbar_title, **kwargs)
    return pc


def create_line_collection(net, lines=None, line_geodata=None, use_bus_geodata=False, infofunc=None,
                           cmap=None, norm=None, picker=False, z=None,
                           cbar_title="Line Loading [%]", clim=None, **kwargs):
    """
    Creates a matplotlib line collection of pandapower lines.

    Input:
        **net** (pandapowerNet) - The pandapower network

    OPTIONAL:
        **lines** (list, None) - The lines for which the collections are created. If None, all lines
            in the network are considered.

        **line_geodata** (DataFrame, None) - coordinates to use for plotting If None,
            net["line_geodata"] is used

         **infofunc** (function, None) - infofunction for the patch element

        **kwargs - key word arguments are passed to the patch function

    OUTPUT:
        **lc** - line collection
    """
    lines = net.line.index.tolist() if lines is None else list(lines)
    if len(lines) == 0:
        return None
    if line_geodata is None:
        line_geodata = net["line_geodata"]
    if len(lines) == 0:
        return None

    if use_bus_geodata:
        data = [([(net.bus_geodata.at[a, "x"], net.bus_geodata.at[a, "y"]),
                  (net.bus_geodata.at[b, "x"], net.bus_geodata.at[b, "y"])],
                 infofunc(line) if infofunc else [])
                for line, (a, b) in net.line.loc[lines, ["from_bus", "to_bus"]].iterrows()
                if a in net.bus_geodata.index.values
                and b in net.bus_geodata.index.values]
    else:
        data = [(line_geodata.loc[line, "coords"],
                 infofunc(line) if infofunc else [])
                for line in lines if line in line_geodata.index.values]

    if len(data) == 0:
        return None

    data, info = list(zip(*data))

    # This would be done anyways by matplotlib - doing it explicitly makes it a) clear and
    # b) prevents unexpected behavior when observing colors being "none"
    lc = LineCollection(data, picker=picker, **kwargs)
    lc.line_indices = np.array(lines)
    if cmap:
        if z is None:
            z = net.res_line.loading_percent.loc[lines]
        lc.set_cmap(cmap)
        lc.set_norm(norm)
        if clim is not None:
            lc.set_clim(clim)
        lc.set_array(np.array(z))
        lc.has_colormap = True
        lc.cbar_title = cbar_title
    lc.info = info
    return lc


def create_trafo_connection_collection(net, trafos=None, bus_geodata=None, infofunc=None, **kwargs):
    """
    Creates a matplotlib line collection of pandapower transformers.

    Input:
        **net** (pandapowerNet) - The pandapower network

    OPTIONAL:
        **trafos** (list, None) - The transformers for which the collections are created.
            If None, all transformers in the network are considered.

        **kwargs - key word arguments are passed to the patch function

    OUTPUT:
        **lc** - line collection
    """
    trafos = net.trafo if trafos is None else net.trafo.loc[trafos]

    if bus_geodata is None:
        bus_geodata = net["bus_geodata"]

    hv_geo = list(zip(bus_geodata.loc[trafos["hv_bus"], "x"].values,
                      bus_geodata.loc[trafos["hv_bus"], "y"].values))
    lv_geo = list(zip(bus_geodata.loc[trafos["lv_bus"], "x"].values,
                      bus_geodata.loc[trafos["lv_bus"], "y"].values))

    tg = list(zip(hv_geo, lv_geo))

    info = [infofunc(tr) if infofunc else [] for tr in trafos.index.values]

    lc = LineCollection([(tgd[0], tgd[1]) for tgd in tg], **kwargs)
    lc.info = info

    return lc


def create_trafo_collection(net, trafos=None, picker=False, size=None,
                                   infofunc=None, **kwargs):
    """
    Creates a matplotlib line collection of pandapower transformers.

    Input:
        **net** (pandapowerNet) - The pandapower network

    OPTIONAL:
        **trafos** (list, None) - The transformers for which the collections are created.
            If None, all transformers in the network are considered.

        **kwargs - key word arguments are passed to the patch function

    OUTPUT:
        **lc** - line collection

        **pc** - patch collection
    """
    trafo_table = net.trafo if trafos is None else net.trafo.loc[trafos]
    lines = []
    circles = []
    infos = []
    color = kwargs.pop("color", "k")
    linewidths = kwargs.pop("linewidths", 2.)
    for i, trafo in trafo_table.iterrows():
        p1 = net.bus_geodata[["x", "y"]].loc[trafo.hv_bus].values
        p2 = net.bus_geodata[["x", "y"]].loc[trafo.lv_bus].values
        if np.all(p1 == p2):
            continue
        d = np.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)
        if size is None:
            size_this = np.sqrt(d) / 5
        else:
            size_this = size
        off = size_this * 0.35
        circ1 = (0.5 - off / d) * (p1 - p2) + p2
        circ2 = (0.5 + off / d) * (p1 - p2) + p2
        circles.append(Circle(circ1, size_this, fc=(1, 0, 0, 0), ec=color))
        circles.append(Circle(circ2, size_this, fc=(1, 0, 0, 0), ec=color))

        lp1 = (0.5 - off / d - size_this / d) * (p2 - p1) + p1
        lp2 = (0.5 - off / d - size_this / d) * (p1 - p2) + p2
        lines.append([p1, lp1])
        lines.append([p2, lp2])
        if infofunc is not None:
            infos.append(infofunc(i))
            infos.append(infofunc(i))
    if len(circles) == 0:
        return None, None
    lc = LineCollection((lines), color=color, picker=picker, linewidths=linewidths, **kwargs)
    lc.info = infos
    pc = PatchCollection(circles, match_original=True, picker=picker, linewidth=linewidths, **kwargs)
    pc.info = infos
    return lc, pc


def create_trafo3w_collection(net, trafo3ws=None, picker=False, size=None,
                                     infofunc=None, **kwargs):
    """
    Creates a matplotlib line collection of pandapower transformers.

    Input:
        **net** (pandapowerNet) - The pandapower network

    OPTIONAL:
        **trafo3ws** (list, None) - The three winding transformers for which the collections are
            created. If None, all three winding transformers in the network are considered.

        **kwargs - key word arguments are passed to the patch function

    OUTPUT:
        **lc** - line collection

        **pc** - patch collection
    """
    trafo3w_table = net.trafo3w if trafo3ws is None else net.trafo3w.loc[trafo3ws]
    lines = []
    circles = []
    infos = []
    color = kwargs.pop("color", "k")
    linewidth = kwargs.pop("linewidths", 2.)
    for i, trafo3w in trafo3w_table.iterrows():
        # get bus geodata
        p1 = net.bus_geodata[["x", "y"]].loc[trafo3w.hv_bus].values
        p2 = net.bus_geodata[["x", "y"]].loc[trafo3w.mv_bus].values
        p3 = net.bus_geodata[["x", "y"]].loc[trafo3w.lv_bus].values
        if np.all(p1 == p2) and np.all(p1 == p3):
            continue
        p = np.array([p1, p2, p3])
        # determine center of buses and minimum distance center-buses
        center = sum(p)/3
        d = np.linalg.norm(p-center, axis=1)
        r = d.min()/3
        # determine closest bus to center and vector from center to circle midpoint in closest
        # direction
        closest = d.argmin()
        to_closest = (p[closest] - center)/d[closest] * 2*r/3
        # determine vectors from center to circle midpoint
        order = list(range(closest, 3)) + list(range(closest))
        cm = np.empty((3, 2))
        cm[order.pop(0)] = to_closest
        ang = 2*np.pi/3  # 120 degree
        cm[order.pop(0)] = _rotate_dim2(to_closest, ang)
        cm[order.pop(0)] = _rotate_dim2(to_closest, -ang)
        # determine midpoints of circles
        m = center + cm
        # determine endpoints of circles
        e = (center - p) * (1 - 5*r/3/d).reshape(3, 1) + p
        # save circle and line collection data
        for i in range(3):
            circles.append(Circle(m[i], r, fc=(1, 0, 0, 0), ec=color))
            lines.append([p[i], e[i]])

        if infofunc is not None:
            infos.append(infofunc(i))
            infos.append(infofunc(i))
    if len(circles) == 0:
        return None, None
    lc = LineCollection((lines), color=color, picker=picker, linewidths=linewidth, **kwargs)
    lc.info = infos
    pc = PatchCollection(circles, match_original=True, picker=picker, linewidth=linewidth, **kwargs)
    pc.info = infos
    return lc, pc


def create_load_collection(net, size=1., infofunc=None, orientation=np.pi, **kwargs):
    lines = []
    polys = []
    infos = []
    off = 2.
    ang = orientation if hasattr(orientation, '__iter__') else [orientation]*net.load.shape[0]
    for i, load in net.load.iterrows():
        p1 = net.bus_geodata[["x", "y"]].loc[load.bus]
        p2 = p1 + _rotate_dim2(np.array([0, size * off]), ang[i])
        p3 = p1 + _rotate_dim2(np.array([0, size * (off-0.5)]), ang[i])
        polys.append(RegularPolygon(p2, numVertices=3, radius=size, orientation=-ang[i]))
        lines.append((p1, p3))
        if infofunc is not None:
            infos.append(infofunc(i))
    load1 = PatchCollection(polys, facecolor="w", edgecolor="k", **kwargs)
    load2 = LineCollection(lines, color="k", **kwargs)
    load1.info = infos
    load2.info = infos
    return load1, load2


def create_gen_collection(net, size=1., infofunc=None, **kwargs):
    lines = []
    polys = []
    infos = []
    off = 1.7
    for i, gen in net.gen.iterrows():
        p1 = net.bus_geodata[["x", "y"]].loc[gen.bus]
        p2 = p1 - np.array([0, size * off])
        polys.append(Circle(p2, size))
        polys.append(
            Arc(p2 + np.array([-size / 6.2, -size / 2.6]), size / 2, size, theta1=45, theta2=135))
        polys.append(
            Arc(p2 + np.array([size / 6.2, size / 2.6]), size / 2, size, theta1=225, theta2=315))
        lines.append((p1, p2 + np.array([0, size])))
        if infofunc is not None:
            infos.append(infofunc(i))
    gen1 = PatchCollection(polys, facecolor="w", edgecolor="k", **kwargs)
    gen2 = LineCollection(lines, color="k", **kwargs)
    gen1.info = infos
    gen2.info = infos
    return gen1, gen2


def create_sgen_collection(net, size=1., infofunc=None, orientation=np.pi, **kwargs):
    lines = []
    polys = []
    infos = []
    off = 1.7
    r_triangle = size*0.4
    ang = orientation if hasattr(orientation, '__iter__') else [orientation]*net.sgen.shape[0]
    for i, sgen in net.sgen.iterrows():
        bus_geo = net.bus_geodata[["x", "y"]].loc[sgen.bus]
        mp_circ = bus_geo + _rotate_dim2(np.array([0, size * off]), ang[i])  # mp means midpoint
        circ_edge = bus_geo + _rotate_dim2(np.array([0, size * (off-1)]), ang[i])
        mp_tri1 = mp_circ + _rotate_dim2(np.array([r_triangle, -r_triangle/4]), ang[i])
        mp_tri2 = mp_circ + _rotate_dim2(np.array([-r_triangle, r_triangle/4]), ang[i])
        perp_foot1 = mp_tri1 + _rotate_dim2(np.array([0, -r_triangle/2]), ang[i])  # dropped perpendicular foot of triangle1
        line_end1 = perp_foot1 + + _rotate_dim2(np.array([-2.5*r_triangle, 0]), ang[i])
        perp_foot2 = mp_tri2 + _rotate_dim2(np.array([0, r_triangle/2]), ang[i])
        line_end2 = perp_foot2 + + _rotate_dim2(np.array([2.5*r_triangle, 0]), ang[i])
        polys.append(Circle(mp_circ, size))
        polys.append(RegularPolygon(mp_tri1, numVertices=3, radius=r_triangle, orientation=-ang[i]))
        polys.append(RegularPolygon(mp_tri2, numVertices=3, radius=r_triangle,
                                    orientation=np.pi-ang[i]))
        lines.append((bus_geo, circ_edge))
        lines.append((perp_foot1, line_end1))
        lines.append((perp_foot2, line_end2))
        if infofunc is not None:
            infos.append(infofunc(i))
    sgen1 = PatchCollection(polys, facecolor="w", edgecolor="k", **kwargs)
    sgen2 = LineCollection(lines, color="k", **kwargs)
    sgen1.info = infos
    sgen2.info = infos
    return sgen1, sgen2


def create_ext_grid_collection(net, size=1., orientation=0, infofunc=None, picker=False, **kwargs):
    lines = []
    polys = []
    infos = []
    for i, ext_grid in net.ext_grid.iterrows():
        p1 = net.bus_geodata[["x", "y"]].loc[ext_grid.bus]
        p2 = p1 + _rotate_dim2(np.array([0, size]), orientation)
        polys.append(Rectangle([p2[0] - size / 2, p2[1] - size / 2], size, size))
        lines.append((p1, p2 - _rotate_dim2(np.array([0, size / 2]), orientation)))
        if infofunc is not None:
            infos.append(infofunc(i))
    ext_grid1 = PatchCollection(polys, facecolor=(1, 0, 0, 0), edgecolor=(0, 0, 0, 1),
                                hatch="XXX", picker=picker, **kwargs)
    ext_grid2 = LineCollection(lines, color="k", picker=picker, **kwargs)
    ext_grid1.info = infos
    ext_grid2.info = infos
    return ext_grid1, ext_grid2


def create_line_switch_collection(net, size=1, distance_to_bus=3, use_line_geodata=False, **kwargs):
    """
    Creates a matplotlib patch collection of pandapower switches.

    INPUT:
        **net** (pandapowerNet) - The pandapower network

    OPTIONAL:

        **size** (float, 1) - Size of the switch patches

        **distance_to_bus** (float, 3) - Distance of the switch patch from the bus patch

        **use_line_geodata** (bool, False) - If True, line coordinates are used to identify the
                                             switch position

        **kwargs - Key word arguments are passed to the patch function

    """
    lbs_switches = net.switch.index[net.switch.et == "l"]

    color = kwargs.pop("color", "k")

    switch_patches = []
    for switch in lbs_switches:
        sb = net.switch.bus.loc[switch]
        line = net.line.loc[net.switch.element.loc[switch]]
        fb = line.from_bus
        tb = line.to_bus

        line_buses = set([fb, tb])
        target_bus = list(line_buses - set([sb]))[0]

        if sb not in net.bus_geodata.index or target_bus not in net.bus_geodata.index:
            logger.warning("Bus coordinates for switch %s not found, skipped switch!" % switch)
            continue

        # switch bus and target coordinates
        pos_sb = net.bus_geodata.loc[sb, ["x", "y"]].values
        pos_ta = np.zeros(2)

        use_bus_geodata = False

        if use_line_geodata:
            if line.name in net.line_geodata.index:
                line_coords = net.line_geodata.coords.loc[line.name]
                # check, which end of the line is nearer to the switch bus
                if len(line_coords) > 2:
                    if abs(line_coords[0][0] - pos_sb[0]) < 0.01 and \
                            abs(line_coords[0][1] - pos_sb[1]) < 0.01:
                        pos_ta = np.array([line_coords[1][0], line_coords[1][1]])
                    else:
                        pos_ta = np.array([line_coords[-2][0], line_coords[-2][1]])
                else:
                    use_bus_geodata = True
            else:
                use_bus_geodata = True

        if not use_line_geodata or use_bus_geodata:
            pos_ta = net.bus_geodata.loc[target_bus, ["x", "y"]]

        # position of switch symbol
        vec = pos_ta - pos_sb
        mag = np.linalg.norm(vec)
        pos_sw = pos_sb + vec / mag * distance_to_bus

        # rotation of switch symbol
        angle = np.arctan2(vec[1], vec[0])
        rotation = Affine2D().rotate_around(pos_sw[0], pos_sw[1], angle)

        # color switch by state
        col = color if net.switch.closed.loc[switch] else "white"

        # create switch patch (switch size is respected to center the switch on the line)
        patch = Rectangle((pos_sw[0] - size/2, pos_sw[1] - size/2), size, size, facecolor=col,
                          edgecolor=color)
        # apply rotation
        patch.set_transform(rotation)

        switch_patches.append(patch)

    switches = PatchCollection(switch_patches, match_original=True, **kwargs)
    return switches


def add_collections_to_axes(ax, collections, plot_colorbars=True):
    for c in collections:
        if c:
            ax.add_collection(c)
            if plot_colorbars and hasattr(c, "has_colormap") and c.has_colormap:
                extend = c.extend if hasattr(c, "extend") else "neither"
                cbar_load = plt.colorbar(c, extend=extend, ax=ax)
                if hasattr(c, "cbar_title"):
                    cbar_load.ax.set_ylabel(c.cbar_title)


def draw_collections(collections, figsize=(10, 8), ax=None, plot_colorbars=True, set_aspect=True,
                     axes_visible=(False, False)):
    """
    Draws matplotlib collections which can be created with the create collection functions.

    Input:
        **collections** (list) - iterable of collection objects

    OPTIONAL:
        **figsize** (tuple, (10,8)) - figsize of the matplotlib figure

        **ax** (axis, None) - matplotlib axis object to plot into, new axis is created if None
    """

    if not ax:
        plt.figure(facecolor="white", figsize=figsize)
        plt.subplots_adjust(left=0.01, right=0.99, top=0.99, bottom=0.05,
                            wspace=0.02, hspace=0.04)
    ax = ax or plt.gca()

    add_collections_to_axes(ax, collections, plot_colorbars=plot_colorbars)

    try:
        ax.set_facecolor("white")
    except:
        ax.set_axis_bgcolor("white")
    ax.xaxis.set_visible(axes_visible[0])
    ax.yaxis.set_visible(axes_visible[1])
    if set_aspect:
        ax.set_aspect('equal', 'datalim')
    ax.autoscale_view(True, True, True)
    ax.margins(.02)
    plt.draw()
    return ax


if __name__ == "__main__":
    if 0:
        import pandapower as pp

        net = pp.create_empty_network()
        b1 = pp.create_bus(net, 10, geodata=(5, 10))
        b2 = pp.create_bus(net, 0.4, geodata=(5, 15))
        b3 = pp.create_bus(net, 0.4, geodata=(0, 22))
        b4 = pp.create_bus(net, 0.4, geodata=(8, 20))
        pp.create_gen(net, b1, p_kw=100)
        pp.create_load(net, b3, p_kw=100)
        pp.create_ext_grid(net, b4)

        pp.create_line(net, b2, b3, 2.0, std_type="NAYY 4x50 SE")
        pp.create_line(net, b2, b4, 2.0, std_type="NAYY 4x50 SE")
        pp.create_transformer(net, b1, b2, std_type="0.63 MVA 10/0.4 kV")
        pp.create_transformer(net, b3, b4, std_type="0.63 MVA 10/0.4 kV")

        bc = create_bus_collection(net, size=0.2, color="k")
        lc = create_line_collection(net, use_line_geodata=False, color="k", linewidth=3.)
        lt, bt = create_trafo_collection(net, size=2, linewidth=3.)
        load1, load2 = create_load_collection(net, linewidth=2.,
                                                     infofunc=lambda x: ("load", x))
        gen1, gen2 = create_gen_collection(net, linewidth=2.,
                                                  infofunc=lambda x: ("gen", x))
        eg1, eg2 = create_ext_grid_collection(net, size=2.,
                                                     infofunc=lambda x: ("ext_grid", x))

        draw_collections([bc, lc, load1, load2, gen1, gen2, lt, bt, eg1, eg2])
    else:
        pass