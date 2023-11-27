from signal_propogation import *

def objective_with_signal_propagation(tower_location, positions):
    total_signal_strength = 0
    for drone_position in positions:
        path_blocked = any(line_intersects_circle(drone_position, tower_location, obstacle) for obstacle in obstacles)
        total_signal_strength += signal_strength(tower_location, drone_position, not path_blocked)
    return total_signal_strength