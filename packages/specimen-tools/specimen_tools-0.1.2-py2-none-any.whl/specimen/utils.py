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

import colorsys
from itertools import combinations

from colormath.color_objects import LabColor, sRGBColor
from colormath.color_conversions import convert_color
import numpy as np
import pycountry


def is_iterable(x):
    """ Check if a value is iterable """
    try:
        iter(x)
        return True
    except:
        return False

def flatten_list(l):
    if l and is_iterable(l) and is_iterable(l[0]) and not (isinstance(l[0], str) or isinstance(l[0], unicode)):
        return [item for sublist in l for item in sublist]
    else:
        return l


munsell_hue_labels = np.array(['R', 'YR', 'Y', 'GY', 'G', 'BG', 'B', 'PB', 'P', 'RP'])

def munsell_buckets(hues, labels = False, color = 'right', normalizer = 100.0):
    """
    Returns corresponding color in munsell bucket
    Source http://www.farbkarten-shop.de/media/products/0944505001412681032.pdf
    :param hues: hues to discretize
    :param labels: if true returns string name rather than bucket
    :param normalizer: divisor constant to normalize if values not already between 0.0 and 1.0
    :return: representative hue (and optionally) the label for the bucket
    """
    if not is_iterable(hues):
        raise ValueError("hues must be iterable")
    if not color in ['left', 'mid', 'right']:
        raise ValueError("color must be one of 'left', 'mid', 'right'")
    munsell_bounds = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
    # bring to 0.0 to 1.0 if necessary
    hues = np.array(hues)
    if max(hues) > 1.0:
        hues = hues / normalizer
    bucketed = np.digitize(hues, bins = munsell_bounds)
    # make zero indexed
    bucketed -= 1
    # reassign values of 1 to the first bucket
    bucketed[np.where(hues == 1.0)] = 0
    if not labels:
        return bucketed
    else:
        return bucketed, munsell_hue_labels[bucketed]

def _get_hue_pair_map():
  """ Order agnostic mapping to munsell hues ( e.g R-P, P-R both map to same value )"""
  pairs = list(combinations(munsell_hue_labels, 2))
  # self maps
  pairs += [(h, h) for h in munsell_hue_labels]
  pairs = {p:p for p in pairs}
  # reverses pairs
  pairs.update({(h2, h1):mapped for (h1, h2), mapped in pairs.iteritems()})
  return pairs

munsell_pair_map = _get_hue_pair_map()

def get_full_country_name(iso_code, override = None):
    """
    Get country name for 2 letter iso country code used in specimen data as unicode
    :param iso_code:
    :param override: we may prefer some mappings, or some may be old and not in the countries data, so try override first
    :return:
    """
    if not override is None and iso_code in override:
        return unicode(override[iso_code])
    else:
        return unicode(pycountry.countries.get(alpha_2 = iso_code).name)

def rgb_to_lab(r, g, b):
    rgb = sRGBColor(r, g, b)
    lab = convert_color(rgb, LabColor)
    # scale to fit Mathematica scale
    return tuple(val / 100.0 for val in lab.get_value_tuple())

def lab_to_rgb(l, a, b):
    # undo the / 100.0 shown above
    lab = LabColor(l * 100.0, a * 100.0, b * 100.0)
    rgb = convert_color(lab, sRGBColor)
    # scale to fit Mathematica scale
    return tuple(rgb.get_value_tuple())

def df_rgb_to_lab(df):
  rgb = list('rgb')
  df = df[rgb]
  f_star = lambda x: list(rgb_to_lab(*x))
  return df.apply(f_star, axis=1).rename(columns=dict(zip(rgb, 'lab')))

def mat_rgb_to_lab(mat):
  f_star = lambda x: list(rgb_to_lab(*x))
  return np.apply_along_axis(f_star, 1, mat)
  
def mat_lab_to_rgb(mat):
  f_star = lambda x: list(lab_to_rgb(*x))
  return np.apply_along_axis(f_star, 1, mat)

def prefix(p, l):
  return ['%s%s' % (p, e) for e in l]
  
def to_csv_str(vals):
    return ','.join(map(str, vals))
