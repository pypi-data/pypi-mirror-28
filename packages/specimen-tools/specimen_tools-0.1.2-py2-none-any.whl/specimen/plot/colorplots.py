# Copyright 2018 Jose Cambronero and Phillip Stanley-Marbell
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject
# to the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR
# ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF
# CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


import os

from colormath.color_objects import sRGBColor, XYZColor
from colormath.color_conversions import convert_color
from colorsys import hsv_to_rgb
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
import numpy as np


def color_pairs_plot(*args, **kwargs):
    """
    Plot swatches of color
    :param args: separate rgb channels, 2 lists of rgb tuples, or a list of tuples of rgb tuples
    :param kwargs: groups (in order to plot multiple columns of swatchs)
    :return:
    """
    if len(args) == 6:
        return _color_pairs_plot_rgb(*args, **kwargs)
    elif len(args) == 2:
        return _color_pairs_plot_sep(*args, **kwargs)
    else:
        return _color_pairs_plot_tupled(*args, **kwargs)

def _color_pairs_plot_rgb(r1, g1, b1, r2, g2, b2, **kwargs):
    return _color_pairs_plot_sep(zip(r1, g1, b1), zip(r2, g2, b2), **kwargs)

def _color_pairs_plot_sep(color1, color2, **kwargs):
    return _color_pairs_plot_tupled(zip(color1, color2), **kwargs)

def _color_pairs_plot_tupled(rgb_pairs, **kwargs):
    groups = kwargs.get('groups', 1)
    normalize = kwargs.get('normalize', False)
    # check if we should still normalize values
    if not normalize:
        normalize = max([v > 1 for color1, color2 in rgb_pairs for v in list(color1) + list(color2)])
    nrows = len(rgb_pairs)
    pairs_per_group = nrows / groups
    if 'ax' in kwargs:
      ax = kwargs['ax']
      fig = ax.get_figure()
    else:
      fig, ax = plt.subplots()
    # dimension info
    bbox = ax.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
    width, height = bbox.width, bbox.height
    X = width * fig.get_dpi()
    Y = height * fig.get_dpi()
    # space between swatches: arbitrary
    swatch_space = 60
    # make groups distinguishable
    group_space = 0.5 * swatch_space
    # we can define X = group_space * (groups - 1) + (swatch_space + 2 * swatch_width) * groups
    swatch_width = (X - group_space * (groups - 1) - swatch_space * groups) / (2 * groups)
    # offset between groups must consider swatch space etc
    group_offset = 2 * swatch_width + swatch_space + group_space
    # swatch height
    h = Y / (pairs_per_group + 1)
    for i, pair in enumerate(rgb_pairs):
        # location for this pair on y axis
        y = Y - (h * (i % pairs_per_group)) - h
        # horizontal offset multipler based on group
        group_id = i / pairs_per_group
        for j, color in enumerate(pair):
            # normalize rgb color to 0.0 to 1.0
            if normalize:
                color = [ channel / 255.0 for channel in color ]
            # left/right swatch
            is_second = j % 2
            # starting point for this group
            xmin = group_id * group_offset
            # if it is the second swatch, we move a bit to the right
            xmin += is_second * (swatch_width + swatch_space)
            # max is simply the swatch width added to the start of the swatch
            xmax = xmin + swatch_width
            ax.hlines(y=y + h * 0.1, xmin= xmin, xmax=xmax, color=color, linewidth=h * 0.6)
            # add an arrow
            if j == 0:
                ax.arrow(xmax + 10, y + h * 0.1, swatch_space * 0.5, 0, head_width = 8, width = 4, shape = 'full')
    ax.set_axis_off()
    return ax

def smash(x, min_v = 0.0, max_v = 1.0):
    if x < min_v:
        return min_v
    elif x > max_v:
        return max_v
    else:
        return x

def plot_along_hue(hues, y, ax = None, normalize = False, **kwargs):
    # normalize x coordinates
    if normalize or max(map(lambda x: x > 1.0, hues)):
        hues = [h / 360.0 for h in hues]
    # create "fake" HSV color with full saturation and value, but same hue as point
    hsv_colors = [(h, 1, 1) for h in hues]
    # convert color to rgb to actually color points in graph
    rgb_colors = [hsv_to_rgb(*col) for col in hsv_colors]
    # there may be some smudge, so anything outside of range gets put back into range
    rgb_colors = [(smash(r), smash(g), smash(b)) for r, g, b in rgb_colors]
    if ax is None:
        fig, ax = plt.subplots()
    ax.scatter(x = hues, y = y, c = rgb_colors, alpha = 1.0, s = 100, **kwargs)
    return ax



# plots the spectral locus and then overlays colors as points by projecting into x,y
def chromaticity_scatter(colors, cs = None, marker = '*', converter = lambda x: convert_color(sRGBColor(*x), XYZColor), ax = None, **kwargs):
    # plot basic background if not provided
    if ax == None:
        ax = _spectral_locus()
    # convert every color to XYZ
    XYZ = map(converter, colors)
    # now convert every XYZ to x,y pairs
    # check if we can iterate over points
    try:
        map(lambda x: x, XYZ[0])
    except:
        XYZ = map(lambda x: x.get_value_tuple(), XYZ)
    xyz = [map(lambda x: x / sum(pt), pt) for pt in XYZ]
    xs,ys,_ = zip(*xyz)
    # create group colors if provided else sets to red
    if not cs:
        cs = 'red'
        cmap = None
    else:
        cmap = plt.get_cmap('jet', len(cs))
        cmap.set_under('gray')
    ax.scatter(x = xs, y = ys, s = 100, c = cs, marker = marker, cmap = cmap, **kwargs)
    return ax

def _spectral_locus():
    # TODO  we should just pickle xs, ys below
    locus_pts_file = os.path.join(os.path.dirname(__file__), '../resources/spectral-locus.csv')
    xs = []
    ys = []
    for line in open(locus_pts_file, "r"):
        _, Xstr, Ystr, Zstr = line.split(",")
        # convert from XYZ to x,y
        XYZ = [ float(coord) for coord in [Xstr, Ystr, Zstr]]
        denom = sum(XYZ)
        xs.append(XYZ[0] / denom)
        ys.append(XYZ[1] / denom)
    fig, ax = plt.subplots()
    poly = Polygon(np.array(zip(xs, ys)), fill = False, closed= True)
    ax.add_patch(poly)
    return ax

def plot_svd(m, xdim = 0, ydim = 1, colors = None, ax = None, title = "SVD plot", pct_var = True):
    """
    Compute the SVD of a matrix and plot in 2-d as a scatter plot
    :param m: matrix to decompose
    :param xdim: vector of U to use as x axis
    :param ydim: vector of U to use as y axis
    :param colors: optional color mapping for each point
    :param ax: optional existing axes
    :param title: optional title
    :param pct_var: if true returns the % of variance explained by the eigenvalues associated with xdim and ydim
    :return: scatter plot and potentially % of variance explained by dimensions used
    """
    if xdim < 0 or ydim < 0 or xdim == ydim:
        raise ValueError("Must be valid 2-d for plotting")
    u, s, v = np.linalg.svd(m)
    if colors is None:
        cmap = plt.get_cmap('jet')
    else:
        colors = np.array(colors)
        cmap = plt.get_cmap('jet', len(colors))

    cmap.set_under('gray')
    if ax is None:
        ax = plt.subplot()
    ax.scatter(x=u[:, 0], y=u[:, 1], c = colors, cmap = cmap, label = "Group %s" )
    ax.set_xlabel("U[:][%d]" % xdim)
    ax.set_ylabel("U[:][%d]" % ydim)
    ax.legend(loc = 'best')
    ax.set_title(title)
    if pct_var:
        return ax, sum(s[[xdim, ydim]]) / sum(s)
    else:
        return ax
