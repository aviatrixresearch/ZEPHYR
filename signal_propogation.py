import numpy as np
from geometry import astar_3d, segment_intersects_obstacle

def nLoS_loss(value):
    return 10*value

def calculate_fspl(distance, frequency):
    """
    Calculate the Free Space Path Loss (FSPL).
    :param distance: Distance between two points (meters).
    :param frequency: Frequency of the signal (Hz).
    :return: FSPL in dB.
    """
    c = 2.99e8  # Speed of light in m/s
    fspl = 20 * np.log10(distance) + 20 * np.log10(frequency) + 20 * np.log10((4 * np.pi) / c)
    return fspl

def adjust_signal_for_obstructions(path, obstacles, additional_loss_per_obstacle):
    """
    Adjust the signal strength based on obstructions in the path.
    :param path: The path as a list of 3D points.
    :param obstacles: List of obstacles.
    :param additional_loss_per_obstacle: Additional signal loss per obstacle (dB).
    :return: Total additional loss due to obstructions (dB).
    """
    total_additional_loss = 0
    for segment_start, segment_end in zip(path, path[1:]):
        if segment_intersects_obstacle(segment_start, segment_end, obstacles):
            total_additional_loss += additional_loss_per_obstacle
    return total_additional_loss

def calculate_signal_strength(start, end, frequency, obstacles, additional_loss_per_obstacle):
    distance = np.linalg.norm(np.array(end) - np.array(start))
    fspl = calculate_fspl(distance, frequency)
    path = astar_3d(obstacles, start, end, grid_size, resolution)
    obstruction_loss = adjust_signal_for_obstructions(path, obstacles, additional_loss_per_obstacle)
    total_signal_loss = fspl + obstruction_loss
    return total_signal_loss
        