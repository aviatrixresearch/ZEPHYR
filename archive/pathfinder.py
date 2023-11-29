import numpy as np

grid_size = 100  # Size of the grid
resolution = 1  # Each grid cell represents 1x1 unit area

# Create a grid initialized to free space
grid = np.zeros((grid_size, grid_size), dtype=int)

# Mark buildings on the grid
for building, _ in buildings_with_height:
    x, y = building.exterior.xy
    for xi, yi in zip(x, y):
        grid[int(xi//resolution)][int(yi//resolution)] = 1  # Mark as obstacle

import heapq

def heuristic(a, b):
    return np.sqrt((b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2)

def astar(grid, start, goal):
    neighbors = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # 4-way movement
    close_set = set()
    came_from = {}
    gscore = {start: 0}
    fscore = {start: heuristic(start, goal)}
    oheap = []

    heapq.heappush(oheap, (fscore[start], start))
    
    while oheap:
        current = heapq.heappop(oheap)[1]

        if current == goal:
            data = []
            while current in came_from:
                data.append(current)
                current = came_from[current]
            return data

        close_set.add(current)
        for i, j in neighbors:
            neighbor = current[0] + i, current[1] + j            
            tentative_g_score = gscore[current] + heuristic(current, neighbor)
            if 0 <= neighbor[0] < grid.shape[0]:
                if 0 <= neighbor[1] < grid.shape[1]:                
                    if grid[neighbor[0]][neighbor[1]] == 1:
                        continue
                else:
                    # array bound y walls
                    continue
            else:
                # array bound x walls
                continue
                
            if neighbor in close_set and tentative_g_score >= gscore.get(neighbor, 0):
                continue
                
            if  tentative_g_score < gscore.get(neighbor, 0) or neighbor not in [i[1]for i in oheap]:
                came_from[neighbor] = current
                gscore[neighbor] = tentative_g_score
                fscore[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                heapq.heappush(oheap, (fscore[neighbor], neighbor))
                
    return False

def move_drone_astar(drone_pos, target_pos, grid):
    path = astar(grid, (int(drone_pos[0]), int(drone_pos[1])), (int(target_pos[0]), int(target_pos[1])))
    # Return the next position on the path or current position if no path is found
    return path[-2] if path else drone_pos

# Animation update function
def update(frame):
    for i, drone_plot in enumerate(drone_plots):
        target_pos = [...]  # Define the target position for each drone
        new_pos = move_drone_astar(drones_positions[i], target_pos, grid)
        drones_positions[i] = new_pos
        drone_plot.set_data(new_pos[0], new_pos[1])
