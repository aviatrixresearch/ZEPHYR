import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import distance

# Define the operational area (1000m x 1000m)
operational_area = (1000, 1000)

# Define the positions of the drones (as an example, we use a grid of 10x10 drones)
num_drones = 100
drone_positions = np.column_stack((
    np.repeat(np.linspace(100, 900, 10), 10),
    np.tile(np.linspace(100, 900, 10), 10)
))

# Define the PSO parameters
num_particles = 30
max_iter = 100
w = 0.5         # inertia weight
c1 = 1.5        # personal best weight
c2 = 1.5        # global best weight

# Initialize the particles (tower locations) randomly within the operational area
particles = np.random.rand(num_particles, 2) * operational_area
velocities = np.random.rand(num_particles, 2) - 0.5

# Initialize the personal best positions and values
personal_best_positions = np.copy(particles)
personal_best_values = np.full(num_particles, float('inf'))

# Initialize the global best position and value
global_best_position = None
global_best_value = float('inf')

# Define the objective function (minimize the maximum distance from any drone to the tower)
def objective_function(tower_position):
    distances = distance.cdist([tower_position], drone_positions).flatten()
    return np.max(distances)

# Run the PSO algorithm
for iter in range(max_iter):
    for i in range(num_particles):
        # Evaluate the current particle
        current_value = objective_function(particles[i])
        
        # Update the personal best position and value if needed
        if current_value < personal_best_values[i]:
            personal_best_positions[i] = particles[i]
            personal_best_values[i] = current_value
        
        # Update the global best position and value if needed
        if current_value < global_best_value:
            global_best_position = particles[i]
            global_best_value = current_value
    
    # Update the particles' velocities and positions
    for i in range(num_particles):
        velocities[i] = (
            w * velocities[i] +
            c1 * np.random.rand() * (personal_best_positions[i] - particles[i]) +
            c2 * np.random.rand() * (global_best_position - particles[i])
        )
        particles[i] += velocities[i]
        
        # Ensure the particles stay within the operational area
        particles[i] = np.clip(particles[i], 0, operational_area)
        
    print(f'Iteration {iter+1}/{max_iter}, Global Best Value: {global_best_value:.2f}')

# Plot the results
plt.figure(figsize=(10, 10))
plt.scatter(drone_positions[:, 0], drone_positions[:, 1], label='Drones', c='blue')
plt.scatter(*global_best_position, label='Optimal Tower Location', c='red')
plt.title('Optimal Cellular Tower Location for Drone Communication')
plt.xlabel('X Position (m)')
plt.ylabel('Y Position (m)')
plt.legend()
plt.grid(True)
plt.show()
