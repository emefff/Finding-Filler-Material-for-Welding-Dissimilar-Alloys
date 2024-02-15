#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 12 11:28:34 2024

@author: mario
"""

import matplotlib.pyplot as plt
import math

#image_name = "/home/mario/pythonProjects/Schaefflerdiagramm/Schaeffler_cut.jpg"
# image_size = [1854, 1440] # we need the physical_size, we have to transform coordinates
# def x_transform(Cr_equivalent):
#     return image_size[0] / 36 *Cr_equivalent
# def y_transform(Ni_equivalent):
#     return image_size[1] / 28 * (28 - Ni_equivalent) # we have to flip the axis!

# in the background we will show a Schaeffler diagram with its axes in the jpg
image_name = "/home/mario/pythonProjects/Schaefflerdiagramm/Schaeffler_cut2.jpg"


def x_transform2(Cr_equivalent):
    """
    Transform the Cr-equivalent to x-coordinates of the image we plot on.
    Only works with Schaeffler_cut2.jpg. For a new diagram, offsets and slopes
    must be adapted.

    Parameters
    ----------
    Cr_equivalent : TYPE float
        DESCRIPTION. a value between 0-36%

    Returns
    -------
    TYPE int
        DESCRIPTION. x-coordinate of the jpg background we plot on.

    """
    # with the original axis in the image (Schaeffler_cut2.jpg), we have to do a little more
    return int(157.3333 + (2010.6667 - 157.33333) / 36 * Cr_equivalent)


def y_transform2(Ni_equivalent):
    """
    Transform the Ni-equivalent to y-coordinates of the image we plot on.
    Only works with Schaeffler_cut2.jpg. For a new diagram, offsets and slopes
    must be adapted.

    Parameters
    ----------
    Ni_equivalent : TYPE float
        DESCRIPTION. a value between 0-36%

    Returns
    -------
    TYPE int
        DESCRIPTION. y-coordinate of the jpg background we plot on.

    """
    # with the original axis in the image (Schaeffler_cut2.jpg), we have to do a little more
    return int(1468 - (1468 - 30.66667) / 28 *   Ni_equivalent )


def get_value(metal_dict, key):
    """
    Only returns the value to a key of a metal_dict. Kind of useless, but hey.

    Parameters
    ----------
    metal_dict : TYPE dict
        DESCRIPTION. contains the volume percentages of elements of the metal
    key : TYPE string
        DESCRIPTION. An element that is a key in the dict, for example:
                     "Si", "C", "Mn", ...  and the other important alloying elements.

    Returns
    -------
    TYPE float
        DESCRIPTION. the volume percentage in our metal_dict

    """
    return metal_dict[key]


def Cr_equivalent(metal_dict):
    """
    Calculates the Cr-equivalent from a metal_dict.

    Parameters
    ----------
    metal_dict : TYPE dict
        DESCRIPTION. contains the volume percentages of elements of the metal

    Returns
    -------
    TYPE float
        DESCRIPTION. the Cr-equivalent is returned.

    """
    try:
        Cr = get_value(metal_dict, "Cr")
    except KeyError:
        Cr = 0.0
    try:
        Mo = get_value(metal_dict, "Mo")
    except KeyError:
        Mo = 0.0
    try:
        Si = get_value(metal_dict, "Si")
    except KeyError:
        Si = 0.0
    try:
        Nb = get_value(metal_dict, "Nb")
    except KeyError:
        Nb = 0.0
    return Cr + Mo + 1.5 * Si + 0.5 * Nb


def Ni_equivalent(metal_dict):
    """
    Calculates the Ni-equivalent from a metal_dict.

    Parameters
    ----------
    metal_dict : TYPE dict
        DESCRIPTION. contains the volume percentages of elements of the metal

    Returns
    -------
    TYPE
        DESCRIPTION. the Ni-equivalent is returned.


    """
    try:
        Ni = get_value(metal_dict, "Ni")
    except KeyError:
        Ni = 0.0
    try:
        C = get_value(metal_dict, "C")
    except KeyError:
        C = 0.0
    try:
        Mn = get_value(metal_dict, "Mn")
    except KeyError:
        Mn = 0.0
    return Ni + 30 * C + 0.5 * Mn


def plot_background(alpha):
    """
    Plots the background of the Schaeffler diagram we want to plot on.
    Takes an alpha as input

    Parameters
    ----------
    alpha : TYPE float
        DESCRIPTION. can be 0<=alpha<=1

    Returns
    -------
    None.

    """
    plt.figure(figsize=(15,9))
    im = plt.imread(image_name)
    implot = plt.imshow(im, alpha=alpha)
    plt.axis('off')
    plt.tight_layout()
 
    
def plot_metal_dict(metal_dict, text):
    """
    Plots a single point in the Schaeffler diagram. Takes a metal_dict as input.

    Parameters
    ----------
    metal_dict : TYPE dict
        DESCRIPTION. contains the volume percentages of elements of the metal
    text : TYPE string
        DESCRIPTION. you may enter a text here, it is written next to the point
                     in the plot.

    Returns
    -------
    None.

    """
    Cr_equi = Cr_equivalent(metal_dict)
    Ni_equi = Ni_equivalent(metal_dict)
    x_coord = x_transform2(Cr_equi)
    y_coord = y_transform2(Ni_equi)
    plt.scatter(x_coord, y_coord, s=200)
    plt.text(int(x_coord+10), int(y_coord), text)

    
def plot_mix_dicts(metal_dict1, metal_dict2, mix_percentage):
    """
    Calculates a "mixture" between two points in the Schaeffler diagram and plots
    this value.
    If the mixture is 20% between the two points, it means that 20% of point_2 and 80% of point_1
    are in the mixture.  
    It takes two metal_dicts as input.

    Parameters
    ----------
    metal_dict1 : TYPE dict
        DESCRIPTION. contains the volume percentages of elements of the first metal
    metal_dict2 : TYPE dict
        DESCRIPTION. contains the volume percentages of elements the second metal
        mix_percentage : TYPE float or int
        DESCRIPTION. percentage of dilution with respect to point_2

    Returns
    -------
    None.

    """
    # plot distance in mix percent from metaldict_1 to metaldict_2
    Cr_equi1 = Cr_equivalent(metal_dict1)
    Ni_equi1 = Ni_equivalent(metal_dict1)
    Cr_equi2 = Cr_equivalent(metal_dict2)
    Ni_equi2 = Ni_equivalent(metal_dict2)
    
    Cr_mix = Cr_equi2 + abs(Cr_equi1 - Cr_equi2) * mix_percentage/100
    Ni_mix = Ni_equi2 + abs(Ni_equi1 - Ni_equi2) * mix_percentage/100
    
    x_coord = x_transform2(Cr_mix)
    y_coord = y_transform2(Ni_mix)
    plt.scatter(x_coord, y_coord, marker="D", s=150)
 
    
def mix_dicts(metal_dict1, metal_dict2, mix_percentage):
    """
    Calculates a "mixture" between two points in the Schaeffler diagram. If the mixture 
    is 20% between the two points, it means that 20% of point_2 and 80% of point_1
    are in the mixture. Be careful to choose the order of points and percentage 
    correctly, for a reversing of the direction, one can enter a negative percentage
    and switch the points (or enter 100-percentage as mix_percentage). 
    It takes two metal_dicts as input.

    Parameters
    ----------
    metal_dict1 : TYPE dict
        DESCRIPTION. contains the volume percentages of elements of the first metal
    metal_dict2 : TYPE dict
        DESCRIPTION. contains the volume percentages of elements the second metal
        mix_percentage : TYPE float or int
        DESCRIPTION. percentage of dilution with respect to point_2

    Returns
    -------
    list 
        DESCRIPTION. coordinates of the mixure point in the Schaeffler diagram

    """
    Cr_equi1 = Cr_equivalent(metal_dict1)
    Ni_equi1 = Ni_equivalent(metal_dict1)
    Cr_equi2 = Cr_equivalent(metal_dict2)
    Ni_equi2 = Ni_equivalent(metal_dict2)
    
    Cr_mix = Cr_equi2 + abs(Cr_equi1 - Cr_equi2) * mix_percentage / 100
    Ni_mix = Ni_equi2 + abs(Ni_equi1 - Ni_equi2) * mix_percentage / 100
    return [Cr_mix, Ni_mix]


def plot_metal_point(metal_point, text):
    """
    Plots a single point in the Schaeffler diagram. Takes  a point as input.

    Parameters
    ----------
    metal_point : TYPE list
        DESCRIPTION. point, x is chromium equivalent and second is Ni-equivalent
    text : TYPE string
        DESCRIPTION. you may enter a text here, it is written next to the point
                     in the plot.

    Returns
    -------
    None.

    """
    x_coord = x_transform2(metal_point[0])
    y_coord = y_transform2(metal_point[1])
    plt.scatter(x_coord, y_coord, marker="^", s=250)
    plt.text(int(x_coord+10), int(y_coord), text)


def mix_points(metal_point1, metal_point2, mix_percentage):
    """
    Calculates a "mixture" between two points in the Schaeffler diagram. If the mixture 
    is 20% between the two points, it means that 20% of point_2 and 80% of point_1
    are in the mixture. Be careful to choose the order of points and percentage 
    correctly, for a reversing of the direction, one can enter a negative percentage
    and switch the points (or enter 100-percentage as mix_percentage).
    It takes two metal_points as input.

    Parameters
    ----------
    metal_point1 : TYPE list
        DESCRIPTION. first point, x is chromium equivalent and second is Ni-equivalent
    metal_point2 : TYPE list
        DESCRIPTION. second point, x is chromium equivalent and second is Ni-equivalent
    mix_percentage : TYPE float or int
        DESCRIPTION. percentage of dilution with respect to point_2

    Returns
    -------
    list
        DESCRIPTION.

    """
    Cr_equi1 = metal_point1[0]
    Ni_equi1 = metal_point1[1]
    Cr_equi2 = metal_point2[0]
    Ni_equi2 = metal_point2[1]
    
    Cr_mix = Cr_equi2 + (Cr_equi1 - Cr_equi2) * mix_percentage / 100
    Ni_mix = Ni_equi2 + (Ni_equi1 - Ni_equi2) * mix_percentage / 100
    return [Cr_mix, Ni_mix]


def plot_line_points(metal_point1, metal_point2, style, markersize):
    """
    Plots a line between two points in the Schaeffler diagram.

    Parameters
    ----------
    metal_point1 : TYPE list
        DESCRIPTION. first point, x is chromium equivalent and second is Ni-equivalent
    metal_point2 : TYPE list
        DESCRIPTION. second point, x is chromium equivalent and second is Ni-equivalent
    style : TYPE string
        DESCRIPTION. the usual matplotlib-strings for styles like "ro" for red
                     circles

    Returns
    -------
    None.

    """
    x_coord1 = x_transform2(metal_point1[0])
    y_coord1 = y_transform2(metal_point1[1])
    
    x_coord2 = x_transform2(metal_point2[0])
    y_coord2 = y_transform2(metal_point2[1])
    plt.plot([x_coord1,x_coord2], [y_coord1,y_coord2], style, markersize=markersize)


def plot_line_dicts(metal_dict1, metal_dict2, style):
    """
    Plots a line between to metal dicts in the Schaeffler diagram

    Parameters
    ----------
    metal_dict1 : TYPE dict
        DESCRIPTION. contains the volume percentages of elements of the first metal
    metal_dict2 : TYPE dict
        DESCRIPTION. contains the volume percentages of elements the second metal
    style : TYPE string
        DESCRIPTION. the usual matplotlib-strings for styles like "ro" for red
                     circles

    Returns
    -------
    None.

    """
    Cr_equi1 = Cr_equivalent(metal_dict1)
    Ni_equi1 = Ni_equivalent(metal_dict1)
    Cr_equi2 = Cr_equivalent(metal_dict2)
    Ni_equi2 = Ni_equivalent(metal_dict2)
        
    x_coord1 = x_transform2(Cr_equi1)
    y_coord1 = y_transform2(Ni_equi1)
    
    x_coord2 = x_transform2(Cr_equi2)
    y_coord2 = y_transform2(Ni_equi2)
    plt.plot([x_coord1,x_coord2], [y_coord1,y_coord2], style)


def weld_steels_rod(metal_dict1, metal_dict2, rod_dict):
    """
    Performs the usual graphical calculation that we do when we want to weld 
    two steels with a certain rod

    Parameters
    ----------
    metal_dict1 : TYPE dict
        DESCRIPTION. contains the volume percentages of elements of the first metal
    metal_dict2 : TYPE dict
        DESCRIPTION. contains the volume percentages of elements the second metal
    rod_dict : TYPE dict
        DESCRIPTION. contains the volume percentages of elements the rod material

    Returns
    -------
    None.

    """
    results_points_list = []
    
    plot_mix_dicts(metal_dict1, metal_dict2, 50)
    mix50_steels_point = mix_dicts(metal_dict1, metal_dict2, 50)
    weldrod_point = [Cr_equivalent(rod_dict), Ni_equivalent(rod_dict)]
    results_points_list.append(weldrod_point) # the first point will be the rod material itself
    mix10_weldrod_mix50steels_point = mix_points(mix50_steels_point, weldrod_point, 10)
    mix20_weldrod_mix50steels_point = mix_points(mix50_steels_point, weldrod_point, 20)
    mix25_weldrod_mix50steels_point = mix_points(mix50_steels_point, weldrod_point, 25)
    mix30_weldrod_mix50steels_point = mix_points(mix50_steels_point, weldrod_point, 30)
    mix35_weldrod_mix50steels_point = mix_points(mix50_steels_point, weldrod_point, 35)
    mix40_weldrod_mix50steels_point = mix_points(mix50_steels_point, weldrod_point, 40)
    mix50_weldrod_mix50steels_point = mix_points(mix50_steels_point, weldrod_point, 50)
    # we add above dilution points
    results_points_list.append(mix10_weldrod_mix50steels_point) # the add the 10% point
    results_points_list.append(mix20_weldrod_mix50steels_point) # the add the 20% point
    results_points_list.append(mix25_weldrod_mix50steels_point) # the add the 25% point
    results_points_list.append(mix30_weldrod_mix50steels_point) # the add the 30% point
    results_points_list.append(mix35_weldrod_mix50steels_point) # the add the 35% point
    results_points_list.append(mix40_weldrod_mix50steels_point) # the add the 40% point
    results_points_list.append(mix50_weldrod_mix50steels_point) # the add the 50% point
    plot_metal_point(mix10_weldrod_mix50steels_point, "10% dilution")
    plot_metal_point(mix20_weldrod_mix50steels_point, "20% dilution")
    plot_metal_point(mix25_weldrod_mix50steels_point, "25% dilution")
    plot_metal_point(mix30_weldrod_mix50steels_point, "30% dilution")
    plot_metal_point(mix35_weldrod_mix50steels_point, "35% dilution")
    plot_metal_point(mix40_weldrod_mix50steels_point, "40% dilution")
    plot_metal_point(mix50_weldrod_mix50steels_point, "50% dilution")
    plot_line_points(mix50_steels_point, weldrod_point, "b--", 10)
    return results_points_list
    

def find_distance_points(metal_point1, metal_point2):
    point1_x = metal_point1[0]
    point1_y = metal_point1[1]
    point2_x = metal_point2[0]
    point2_y = metal_point2[1]
    distance = math.sqrt(abs( (point2_x-point1_x)**2 + (point2_y-point1_y)**2))
    return distance


def find_min_distance_points_on_curves(curve1, curve2):
    # create some dummy values 
    points_list = [[1000000000000, 1000000000000], [1000000000000, 1000000000000]]
    distance = 100000000
    
    for i,point1 in enumerate(curve1):
        for j,point2 in enumerate(curve2):
            distance_new = find_distance_points(point1, point2)
            if distance_new<distance:
                distance = distance_new
                del(points_list)
                points_list = [point1, point2, distance]
    # print(f"{points_list = }")
    return points_list
                
def find_min_distance_point_to_curve(curve, point):
    # create some dummy values 
    points_list = [[1000000000000, 1000000000000], [1000000000000, 1000000000000]]
    distance = 100000000
    
    for i,point_curve in enumerate(curve):
        distance_new = find_distance_points(point_curve, point)
        if distance_new<distance:
            distance = distance_new
            del(points_list)
            points_list = [point, point_curve, distance]
    # print(f"{points_list = }")
    return points_list


def find_best_rod(results_dict, curve, dilution):
    """
    Finds the best rod in a results_dict with a given dilution. It does not make
    sense to just search for the nearest distances, searching for the nearest
    points and a chosen dilution is much more useful.

    Parameters
    ----------
    results_dict : TYPE dict
        DESCRIPTION. A dictionary of results from weld_steels_rod, that 
                     consists of dilution points for 0%-50% and a rod name for 
                     the key.
    curve: TYPE list of lists
        DESCRIPTION. A curve (list of points) which we will use for measuring 
                     a distance to. The question is, which curve we want to use. 
                     Do we want our x%-dilution point near the center of the 
                     S-curve or near to one of the border curves of the S-curve?
                                          
    dilution : TYPE int
        DESCRIPTION. number that denotes the dilution of rod and welding steels. 
                     Currently, we only have 0, 10, 20, 25, 30, 35, 40, and 50. If the
                     user enters a different number, we round to the nearest
                     of these values
 
    Returns
    -------
    best_key : TYPE string
        DESCRIPTION. The name of the best rod
    result : TYPE list
        DESCRIPTION. A list that contains a result given by find_min_distance_point_to_curve.
                     The list[0] is the point with dilution% of the best rod
                     list[1] is the nearest point on the s-curve and
                     list[2] is their distance in the Schaeffler diagram.

    """
    dilutions_list = [0, 10, 20, 25, 30, 35, 40, 50]
    closest_value = min(dilutions_list, key = lambda x: abs(x-dilution))
    # print(dilution, closest_value)
    dilution = closest_value
    
    result = 100000000
    distance = 100000000
    best_key = "best key"
    
    # idx = dilution / 10 # in the results_dict, points are stored in order of dilution 0, 10, 20, 30, 40%
    idx = dilutions_list.index(closest_value)
        
    for i,key in enumerate(results_dict):
        distance_result_new = find_min_distance_point_to_curve(curve, results_dict[key][idx]) # we need a list otherwise error in find_distance_points
        # print("***** ", distance_result_new)
        if distance_result_new[2] <= distance:
            distance = distance_result_new[2]
            best_key = key
            result = distance_result_new
    return best_key, result


def plot_curve_points_list(points_list, style):
    """
    Plots a curve from a points_list. Segments are just straight lines.

    Parameters
    ----------
    points_list : TYPE list
        DESCRIPTION. List of coordinates in the S-diagram
    style : TYPE string
        DESCRIPTION. the usual matplotlib-strings for styles like "ro" for red
                     circles

    Returns
    -------
    None.

    """
    len_points_list = len(points_list)
    for i,point in enumerate(points_list):
        if i < len_points_list-1:
            plot_line_points(points_list[i], points_list[i+1], style, 6)
        else:
            break


######################### LET'S DEFINE SOME STEELS ############################
# steels etc...
steel_14723_avg_dict = {"name":"1.4723","C":0.12,  "Si":0.75, "Mn":1.0, 
                        "Cr":7.0, "Al":0.75}
steel_14021_avg_dict = {"name":"1.4021","C":0.205, "Si":0.5, "Mn":0.75, 
                        "Cr":13.0, "Al":0.0}
steel_A508_avg_dict = {"name":"A508","C":0.3, "Si":0.4, "Mn":1.35,  
                        "Cr":0.0, "Mo": 0.1, "Ni": 0.4, "Al":0.0}
steel_A304L_avg_dict = {"name":"A304L","C":0.03, "Si":1.0, "Mn":2.0,  
                        "Cr":18.5, "Mo": 0.0, "Ni": 11.0, "Nb":0.01, "Al":0.0}


# welding rods etc
bohler_Thermanit2509CuT_avg_dict = {"name":"Thermanit2509CuT","C":0.02, 
                                    "Si":0.35, "Mn":0.9, "Cr":25.5, "Ni":9.5,
                                    "Mo":3.8, "W":0.6}
bohler_ThermanitJE308LSi_dict = {"name":"ThermanitJE308LSi","C":0.02, "Si":0.9,
                                 "Mn":1.7, "Cr":20, "Ni":10}
bohler_FOXCN2312MoA_dict = {"name":"FOXCN2312MoA","C":0.02, "Si":0.7, "Mn":0.8,
                            "Cr":23.0, "Ni":12.5, "Mo":2.7}
bohler_EMK8_dict = {"name":"EMK8","C":0.1, "Si":1.0, "Mn":1.7}
bohler_UnionIMoMn_dict = {"name":"UnionIMoMn","C":0.09, "Si":0.65, "Mn":1.8, 
                          "Mo":0.52}
bohler_UnionICrMo910_dict = {"name":"UnionICrMo910","C":0.07, "Si":0.60, "Mn":1.0, 
                          "Cr": 2.55, "Mo":1.0}
bohler_Thermanit1605Mo_dict = {"name":"Thermanit1605Mo","C":0.02, "Si":0.35, 
                               "Mn":1.3, "Cr": 16, "Ni": 5.5, "Mo": 1.0}
bohler_CAT430LCbIG_dict = {"name":"CAT430LCbIG","C":0.02, "Si":0.5, "Mn":0.5, 
                          "Cr": 18, "Nb": 0.24}
bohler_ThermanitGE316LCryo_dict = {"name":"ThermanitGE316LCryo","C":0.02, 
                                   "Si":0.35, "Mn":1.8, "Cr": 18.5, "Ni": 12.3,
                                   "Mo": 2.8}
filler_308L_dict = {"name":"308L","C":0.04, "Si":1.0, "Mn":1.25, "Cr":19.5, 
                    "Mo": 0.75, "Ni": 10.5, "Nb":0.0, "Al":0.0}

# first we show the background, then we add points etc.
plot_background(0.25)

# we add some points
plot_metal_dict(steel_14021_avg_dict, get_value(steel_14021_avg_dict, "name"))
plot_metal_dict(steel_14723_avg_dict, get_value(steel_14723_avg_dict, "name"))
plot_metal_dict(bohler_Thermanit2509CuT_avg_dict, get_value(bohler_Thermanit2509CuT_avg_dict, "name"))
plot_metal_dict(bohler_ThermanitJE308LSi_dict, get_value(bohler_ThermanitJE308LSi_dict, "name"))
plot_metal_dict(bohler_FOXCN2312MoA_dict, get_value(bohler_FOXCN2312MoA_dict, "name"))
plot_metal_dict(bohler_EMK8_dict, get_value(bohler_EMK8_dict, "name"))
plot_metal_dict(bohler_UnionIMoMn_dict, get_value(bohler_UnionIMoMn_dict, "name"))
#plot_metal_dict(bohler_UnionICrMo910_dict, get_value(bohler_UnionICrMo910_dict, "name"))
plot_metal_dict(bohler_Thermanit1605Mo_dict, get_value(bohler_Thermanit1605Mo_dict, "name"))
plot_metal_dict(bohler_CAT430LCbIG_dict, get_value(bohler_CAT430LCbIG_dict, "name"))
plot_metal_dict(bohler_ThermanitGE316LCryo_dict, get_value(bohler_ThermanitGE316LCryo_dict, "name"))
# plot_metal_dict(steel_A508_avg_dict, get_value(steel_A508_avg_dict, "name"))
# plot_metal_dict(steel_A304L_avg_dict, get_value(steel_A304L_avg_dict, "name"))
# plot_metal_dict(filler_308L_dict, get_value(filler_308L_dict, "name"))


# we plot a line between our two metals we want to weld
plot_line_dicts(steel_14021_avg_dict, steel_14723_avg_dict, "r-")
# plot_line_dicts(steel_A508_avg_dict, steel_A304L_avg_dict, "r-")

# we zoom into an interesting area of the diagram
# maxima are Cr:0-36 and Ni= 0-28
Cr_lower_lim = 0
Cr_upper_lim = 36
Ni_lower_lim = 0
Ni_upper_lim = 28
x_canvas = 100
y_canvas = 150
x_lower = x_transform2(Cr_lower_lim) - x_canvas
x_upper = x_transform2(Cr_upper_lim)
y_lower = y_transform2(Ni_lower_lim)+ y_canvas
y_upper = y_transform2(Ni_upper_lim)
plt.xlim([x_lower,x_upper])
plt.ylim([y_lower,y_upper])


# we want to store results in a list of lists
results_points_dict = {}

# let's try the first rod
result = weld_steels_rod(steel_14021_avg_dict, steel_14723_avg_dict, bohler_Thermanit2509CuT_avg_dict)
results_points_dict[get_value(bohler_Thermanit2509CuT_avg_dict, "name")] = result

# let's try another rod bohler_ThermanitJE308LSi
result = weld_steels_rod(steel_14021_avg_dict, steel_14723_avg_dict, bohler_ThermanitJE308LSi_dict)
results_points_dict[get_value(bohler_ThermanitJE308LSi_dict, "name")] = result

# let's try another rod bohler_UnionIMoMn
result = weld_steels_rod(steel_14021_avg_dict, steel_14723_avg_dict, bohler_UnionIMoMn_dict)
results_points_dict[get_value(bohler_UnionIMoMn_dict, "name")] = result

# let's try another rod bohler_EMK8
result = weld_steels_rod(steel_14021_avg_dict, steel_14723_avg_dict, bohler_EMK8_dict)
results_points_dict[get_value(bohler_EMK8_dict, "name")] = result

# let's try another rod bohler_Thermanit1605Mo
result = weld_steels_rod(steel_14021_avg_dict, steel_14723_avg_dict, bohler_Thermanit1605Mo_dict)
results_points_dict[get_value(bohler_Thermanit1605Mo_dict, "name")] = result

# let's try another rod bohler_CAT430LCbIG
result = weld_steels_rod(steel_14021_avg_dict, steel_14723_avg_dict, bohler_CAT430LCbIG_dict)
results_points_dict[get_value(bohler_CAT430LCbIG_dict, "name")] = result

# let's try another rod bohler_ThermanitGE316LCryo
result = weld_steels_rod(steel_14021_avg_dict, steel_14723_avg_dict, bohler_ThermanitGE316LCryo_dict)
results_points_dict[get_value(bohler_ThermanitGE316LCryo_dict, "name")] = result

# one last try
result = weld_steels_rod(steel_14021_avg_dict, steel_14723_avg_dict, bohler_FOXCN2312MoA_dict)
results_points_dict[get_value(bohler_FOXCN2312MoA_dict, "name")] = result



# # first pass
# result1 = weld_steels_rod(steel_A304L_avg_dict, steel_A508_avg_dict, filler_308L_dict) # mind the order!!!
# results_points_dict[get_value(filler_308L_dict, "name")] = result1
# # second pass
# result2 = weld_steels_rod(steel_A304L_avg_dict, steel_A304L_avg_dict, filler_308L_dict) # mind the order!!!
# results_points_dict[get_value(filler_308L_dict, "name")] = result2
# # third pass
# result3 = weld_steels_rod(steel_A508_avg_dict, steel_A508_avg_dict, filler_308L_dict) # mind the order!!!
# results_points_dict[get_value(filler_308L_dict, "name")] = result3
# # fourth pass
# result3 = weld_steels_rod(steel_A304L_avg_dict, steel_A508_avg_dict, filler_308L_dict) # mind the order!!!
# results_points_dict[get_value(filler_308L_dict, "name")] = result3


# we want to find an average curve in the center of the "S"
# one point for every 0.5% of Ni-equivalent
s_curve_center = [[13.2,0],[14.3,0.5],[15.4,1],[16.6,1.5],[17.9,2],[19.2,2.5],
                [20.3,3],[21.6,3.5],[22.7,4],[23.6,4.5],[24.05,4.75],[24.2,5],
                [24.21,5.25],[24.1,5.5],[23.8,6],[23.3,6.5],[22.8,7],
                [22.25,7.5],[21.75,8],[21.3,8.5],[20.9,9],[20.6,9.5],[20.4,10],
                [20.35,10.5],[20.3,11],[20.3,11.5],[20.3,12],[20.3,12.5],
                [20.3,13]]
plot_curve_points_list(s_curve_center, "rX-")

s_curve_left_border = [[11.9,0],[12.9,0.5],[13.95,1],[15.0,1.5],[16.05,2],[17.2,2.5],
                [18.2,3],[19.3,3.5],[20.2,4],[21.05,4.5],[21.5,4.75],[21.9,5],
                [22.25,5.25],[22.55,5.5],[22.75,5.75],[22.8,6],[22.7,6.25],
                [22.5,6.5],[22.0,7],[21.45,7.5],[20.85,8],[20.25,8.5],[19.65,9],
                [19.0,9.5],[18.4,10],[17.85,10.4],[18.4,11],[18.9,11.5],
                [19.35,12.0],[19.85,12.5],[20.3,13.0],[20.8,13.5],[21.25,14.0],
                [21.75,14.5],[22.2,15.0],[22.7,15.5],[23.3,16.1]]
plot_curve_points_list(s_curve_left_border, "bX-")

s_curve_right_border = [[14.7,0],[16.0,0.5],[17.4,1],[18.6,1.5],[20.0,2],[21.35,2.5],
                [22.6,3],[23.95,3.5],[25.25,4],[26.85,4.6],[26.7,4.75],[26.35,5],
                [26.0,5.25],[25.65,5.5],[25.32,5.75],[24.95,6],[24.3,6.5],[23.65,7],
                [23.05,7.5],[22.45,8],[22.05,8.5],[21.9,9],[21.82,9.5],[21.82,10],
                [21.85,10.4],[21.96,11],[22.05,11.5],[22.18,12.0],[22.32,12.5],
                [22.45,13.0],[22.6,13.5],[22.75,14.0],[22.9,14.5],[23.05,15.0],
                [23.2,15.5],[23.3,16.1]]
plot_curve_points_list(s_curve_right_border, "cX-")

# let's create the ferrite 0% line, as it is a straight line this is easier:
ferrite_0_percent_line = []
for i in range (43):
    x_ferrite0 = 14.4 + i * 0.5
    y_ferrite0 = 8.25 + i * 0.523
    ferrite_0_percent_line.append([x_ferrite0, y_ferrite0])
plot_curve_points_list(ferrite_0_percent_line, "b-")

# let's create the ferrite 5% line:
ferrite_5_percent_line = []
for i in range (43):
    x_ferrite5 = 15.1 + i * 0.5
    y_ferrite5 = 7.7 + i * 0.488
    ferrite_5_percent_line.append([x_ferrite5, y_ferrite5])
plot_curve_points_list(ferrite_5_percent_line, "r-")

# let's create the ferrite 10% line:
ferrite_10_percent_line = []
for i in range (43):
    x_ferrite10 = 15.85 + i * 0.5
    y_ferrite10 = 7.1 + i * 0.433
    ferrite_10_percent_line.append([x_ferrite10, y_ferrite10])
plot_curve_points_list(ferrite_10_percent_line, "g-")

# let's create the ferrite 20% line:
ferrite_20_percent_line = []
for i in range (43):
    x_ferrite20 = 16.85 + i * 0.5
    y_ferrite20 = 6.3 + i * 0.362
    ferrite_20_percent_line.append([x_ferrite20, y_ferrite20])
plot_curve_points_list(ferrite_20_percent_line, "c-")

# let's create the ferrite 40% line:
ferrite_40_percent_line = []
for i in range (38):
    x_ferrite40 = 17.9 + i * 0.5
    y_ferrite40 = 5.5 + i * 0.322
    ferrite_40_percent_line.append([x_ferrite40, y_ferrite40])
plot_curve_points_list(ferrite_40_percent_line, "y-")

# let's create the ferrite 7.5% line from the 5% and 10% line:
ferrite_075_percent_line = []
for i in range (43):
    x_ferrite075 =  15.5 + i * 0.5
    y_ferrite075 = (ferrite_5_percent_line[i][1] + ferrite_10_percent_line[i][1])/2
    ferrite_075_percent_line.append([x_ferrite075, y_ferrite075])
plot_curve_points_list(ferrite_075_percent_line, "k--")

# let's create the ferrite 2.5% line from the 0% and 5% line:
ferrite_025_percent_line = []
for i in range (43):
    x_ferrite025 =  14.8 + i * 0.5
    y_ferrite025 = (ferrite_0_percent_line[i][1] + ferrite_5_percent_line[i][1])/2 - 0.02
    ferrite_025_percent_line.append([x_ferrite025, y_ferrite025])
plot_curve_points_list(ferrite_025_percent_line, "k--")

# let's create the ferrite 15.0% line from the 10% and 20% line:
ferrite_15_percent_line = []
for i in range (43):
    x_ferrite15 =  16.35 + i * 0.5
    y_ferrite15 = (ferrite_10_percent_line[i][1] + ferrite_20_percent_line[i][1])/2 - 0.0
    ferrite_15_percent_line.append([x_ferrite15, y_ferrite15])
plot_curve_points_list(ferrite_15_percent_line, "k--")


# let's find the best rod in our ensemble of rods for the two steels
dilution = 25
ferrite = 10
line = ferrite_10_percent_line
best_rod, result = find_best_rod(results_points_dict, line, dilution)
plot_line_points(result[0], result[1], "kD-", 15)
print(f"ferrite_percentage = {ferrite}, {dilution = }, {best_rod = }")

dilution = 30
ferrite = 10
line = ferrite_10_percent_line
best_rod, result = find_best_rod(results_points_dict, line, dilution)
plot_line_points(result[0], result[1], "kD-", 15)
print(f"ferrite_percentage = {ferrite}, {dilution = }, {best_rod = }")

dilution = 25
ferrite = 7.5
line = ferrite_075_percent_line
best_rod, result = find_best_rod(results_points_dict, line, dilution)
plot_line_points(result[0], result[1], "kD-", 15)
print(f"ferrite_percentage = {ferrite}, {dilution = }, {best_rod = }")

dilution = 30
ferrite = 7.5
line = ferrite_075_percent_line
best_rod, result = find_best_rod(results_points_dict, line, dilution)
plot_line_points(result[0], result[1], "kD-", 15)
print(f"ferrite_percentage = {ferrite}, {dilution = }, {best_rod = }")

dilution = 25
ferrite = 5
line = ferrite_5_percent_line
best_rod, result = find_best_rod(results_points_dict, line, dilution)
plot_line_points(result[0], result[1], "kD-", 15)
print(f"ferrite_percentage = {ferrite}, {dilution = }, {best_rod = }")

dilution = 30
ferrite = 5
line = ferrite_5_percent_line
best_rod, result = find_best_rod(results_points_dict, line, dilution)
plot_line_points(result[0], result[1], "kD-", 15)
print(f"ferrite_percentage = {ferrite}, {dilution = }, {best_rod = }")

