from signal_propogation import *

def optimization(drones, min_signal_strength, buildings, frequency, grid_size):
    def heuristic(hub_location):
        total_strength = 0
        for drone in drones:
            strength = calculate_signal_strength(hub_location, drone, frequency, buildings)
            if strength < min_signal_strength:
                return float('-inf')
            total_strength += strength
        return total_strength

    # Start at the centroid of drones
    current_location = np.mean(drones, axis=0)
    step_size = 1  # Adjust the step size as needed
    improvement = True

    while improvement:
        improvement = False
        best_heuristic = heuristic(current_location)

        for dx in [-step_size, 0, step_size]:
            for dy in [-step_size, 0, step_size]:
                for dz in [-step_size, 0, step_size]:
                    if dx == 0 and dy == 0 and dz == 0:
                        continue
                    neighbor = current_location + np.array([dx, dy, dz])
                    if 0 <= neighbor[0] < grid_size[0] and 0 <= neighbor[1] < grid_size[1] and 0 <= neighbor[2] < grid_size[2]:
                        neighbor_heuristic = heuristic(neighbor)
                        if neighbor_heuristic > best_heuristic:
                            best_heuristic = neighbor_heuristic
                            current_location = neighbor
                            improvement = True

    return current_location

# Example usage
#optimal_hub_location = custom_optimization(drone_positions, min_signal_strength, buildings, additional_loss_per_obstacle, frequency, (100, 100, 100))
