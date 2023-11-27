import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import numpy as np
from scipy.optimize import minimize

# Initialize global variables
drones_positions = np.random.rand(2, 2) * 100  # 10 drones in a 100x100 area
obstacles = [(50, 50, 10), (80, 80, 5), (25, 25, 8), (25, 80, 15)]  # Define obstacles
area_size = 100

# Function to check if a line intersects with a circle (simple obstacle)
def line_intersects_circle(p1, p2, circle):
    # vector d
    d = p2 - p1
    # vector f
    f = p1 - circle[:2]
    r = circle[2]
    
    a = np.dot(d, d)
    b = 2 * np.dot(f, d)
    c = np.dot(f, f) - r**2
    
    discriminant = b**2 - 4 * a * c
    if discriminant < 0:
        return False
    else:
        discriminant = np.sqrt(discriminant)
        t1 = (-b - discriminant) / (2 * a)
        t2 = (-b + discriminant) / (2 * a)
        if 0 <= t1 <= 1 or 0 <= t2 <= 1:
            return True
        return False


# Modified objective function to account for obstacles
def objective_with_obstacles(tower_location):
    total_distance = 0
    for drone_position in drones_positions:
        path_blocked = any(line_intersects_circle(drone_position, tower_location, obstacle) for obstacle in obstacles)
        distance = np.linalg.norm(drone_position - tower_location)
        #if path_blocked:
        #    distance *= 1.5  # Increase "distance" if path is blocked
        total_distance += distance
    return total_distance


def signal_strength(tower_location, drone_position, is_LoS):
    frequency = 5e9
    speed_of_light = 2.99e8
    
    # Basic Free Space Path Loss (FSPL) model
    distance = np.linalg.norm(drone_position - tower_location)
    fspl = 20 * np.log10(distance) + 20 * np.log10(frequency) + 20 * np.log10((4 * np.pi) / speed_of_light)
    nlos_additional_loss = 10*fspl

    # Adjustments for LoS and NLoS
    if is_LoS:
        loss = fspl
    else:
        # Additional loss for NLoS
        loss = fspl + nlos_additional_loss

    return -loss  # Negative because we want to maximize signal strength


def objective_with_signal_propagation(tower_location):
    total_signal_strength = 0
    for drone_position in drones_positions:
        path_blocked = any(line_intersects_circle(drone_position, tower_location, obstacle) for obstacle in obstacles)
        total_signal_strength += signal_strength(tower_location, drone_position, not path_blocked)
    return total_signal_strength


def update_plot():
    plt.gca().clear()
    plt.scatter(drones_positions[:, 0], drones_positions[:, 1], c='blue', label='Drones')
    for obstacle in obstacles:
        circle = Circle(obstacle[:2], obstacle[2], color='green', alpha=0.3)
        plt.gca().add_patch(circle)
    result = minimize(objective_with_signal_propagation, np.mean(drones_positions, axis=0), bounds=[(0, area_size), (0, area_size)], method='L-BFGS-B')
    optimal_location = result.x
    plt.scatter(optimal_location[0], optimal_location[1], c='red', label='Cellular Tower')
    plt.xlim(0, area_size)
    plt.ylim(0, area_size)
    plt.legend()
    plt.draw()

def on_click(event):
    global current_drone
    if event.xdata is None or event.ydata is None:  # Click outside axes
        return
    distances = np.linalg.norm(drones_positions - np.array([event.xdata, event.ydata]), axis=1)
    closest_drone = np.argmin(distances)
    if distances[closest_drone] < 5:  # Threshold to select a drone
        current_drone = closest_drone

def on_release(event):
    global current_drone
    current_drone = None  # Release the drone

def on_motion(event):
    try:
        if current_drone is None:
            return
        if event.xdata is None or event.ydata is None:
            return
        drones_positions[current_drone] = [event.xdata, event.ydata]
        update_plot()
    except:
        return

fig, ax = plt.subplots()
fig.canvas.mpl_connect('button_press_event', on_click)
fig.canvas.mpl_connect('button_release_event', on_release)
fig.canvas.mpl_connect('motion_notify_event', on_motion)
update_plot()
plt.show()
