#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np

def apply_mirror_boundary_conditions(coord, dim):
    """
    Return the correct coordinate according to mirror boundary conditions
        coord: a coordinate (x or y) in the image
        dim: the length of the axis of said coordinate
    """
    # If the coordinate is outside of the bounds of the axis, take its reflection inside the image
    if coord < 0:
        coord = -coord
    elif coord >= dim:
        coord =  2*(dim-1) - coord % (2*(dim-1))
    # Else, do nothing
    return coord


def get_pixel(image, i, j):
    """
    Return the value of the pixel (i,j) in image, with mirror boundary conditions
    Note that (i,j) = (y,x) in pixel coordinate (assuming image conventions)
    Input:
        image: the image array; size:(width, height, num_channel)
        i: the row-coordinate of the pixel
        j: the col-ccordinate of the pixel
    Output:
        the value of the pixel; size:(num_channel,)
    """
    width = image.shape[0]
    height = image.shape[1]
    if i < 0:
        i = -i
    if i >= height:
        i = 2*height - 2 - (i % (2*height-2))
    if j < 0:
        j = -j
    if j >= width:
        j = 2*width - 2 - (j % (2*width-2))
    return image[int(i),int(j),:]


def get_window(image, window_size, centre_coordinates):
    """
    Get a window in image taking into account boundary conditions
        image: a numpy array representing our image
        window_size: an odd number specifying the size of the window
        centre_coordinates: a list containing the x-y coordinates of the window's central pixel
    """
    # Get convenient variables
    window_radius = (window_size - 1)/2
    i_centre, j_centre = (centre_coordinates[0], centre_coordinates[1])
    nrows, ncols = image.shape
    window = np.zeros((window_size, window_size))
    # Fill in the window array with pixels of the image
    for i in range(window_size):
        # Apply mirror boundary conditions on the x-coordinate
        i_mirrored = apply_mirror_boundary_conditions(i_centre + i - window_radius, nrows)
        for j in range(window_size):
            # Same for the y-coordinate
            j_mirrored = apply_mirror_boundary_conditions(j_centre + j - window_radius, ncols)
            # Fill in the window with the corresponding pixel
            window[i, j] = image[i_mirrored, j_mirrored]
    return window


def shift_to_the_right(image, window, centre_coordinates):
    nrows, ncols = image.shape
    window_size = len(window)
    window_radius = (window_size - 1)/2
    j_mirrored = apply_mirror_boundary_conditions(centre_coordinates[1] + 1 + window_radius, nrows)
    shifted = np.roll(window, -1, axis=0)
    for i in range(window_size):
        i_mirrored = apply_mirror_boundary_conditions(i_centre + i - window_radius, nrows)
        shifted[i, -1] = window[i_mirrored, j_mirrored]
    return shifted


def shift_to_the_bottom(image, window, centre_coordinates):
    nrows, ncols = image.shape
    window_size = len(window)
    window_radius = (window_size - 1)/2
    i_mirrored = apply_mirror_boundary_conditions(centre_coordinates[0] + 1 + window_radius, nrows)
    shifted = np.roll(window, -1, axis=1)
    for j in range(window_size):
        j_mirrored = apply_mirror_boundary_conditions(j_centre + j - window_radius, ncols)
        shifted[-1, j] = window[i_mirrored, j_mirrored]
    return shifted


def sliding_window(image, window_size):
    """
    Construct a list of sliding windows of given size on an image.
    The windows will slide from left to right and from up to down.
        image: a numpy array representing our image
        window_size: an odd number specifying the size of the window
    """
    nrows, ncols = image.shape
    windows = []
    for i in range(nrows):
        for j in range(ncols):
            # TODO: do not rebuild the entire window at each loop, some values do not move.
            window = get_window(image, window_size, [i, j])