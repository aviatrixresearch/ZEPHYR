import numpy as np
from geometry import astar_3d, is_line_intersect_building

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


def calculate_signal_strength(hub_position, drone_position, frequency, buildings):
    # Calculate FSPL
    distance = np.linalg.norm(np.array(drone_position) - np.array(hub_position))
    fspl = 20 * np.log10(distance) + 20 * np.log10(frequency) + 20 * np.log10((4 * np.pi) / (3 * 10**8))

    # Add obstacle loss
    obstacle_loss = fspl*0.1
    for building in buildings:
        if is_line_intersect_building(hub_position, drone_position, building):
            return fspl + obstacle_loss

    return fspl + obstacle_loss
        