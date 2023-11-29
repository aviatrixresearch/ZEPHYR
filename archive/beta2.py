import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize

# Set random seed for reproducibility
np.random.seed(42)

# Number of drones
num_drones = 10

# Define the operational area (100m x 100m for example)
area_size = 100

# Randomly generate drone positions within the operational area
drones_positions = area_size * np.random.rand(num_drones, 2)

# Objective function to minimize (sum of distances from tower to drones)
def objective(tower_location):
    distances = np.sqrt(np.sum((drones_positions - tower_location) ** 2, axis=1))
    return np.sum(distances)

# Initial guess for tower location (center of the area)
initial_guess = [area_size / 2, area_size / 2]

# Run the optimization
result = minimize(objective, initial_guess, bounds=[(0, area_size), (0, area_size)])

# Optimal tower location
optimal_location = result.x
print("Optimal Tower Location:", optimal_location)

# Plot the results
plt.figure(figsize=(10, 10))
plt.scatter(drones_positions[:, 0], drones_positions[:, 1], c='blue', label='Drones')
plt.scatter(optimal_location[0], optimal_location[1], c='red', label='Cellular Tower')
plt.xlim(0, area_size)
plt.ylim(0, area_size)
plt.title('Optimal Cellular Tower Location for Drone Swarm')
plt.xlabel('X Coordinate')
plt.ylabel('Y Coordinate')
plt.grid(True)
plt.legend()
plt.show()
