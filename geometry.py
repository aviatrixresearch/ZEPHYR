import numpy as np
import heapq
from shapely.geometry import LineString

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
    
def heuristic(a, b):
    return np.sqrt((b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2 + (b[2] - a[2]) ** 2)

def astar_3d(obstacles, start, goal, grid_size, resolution=1):
    """
    A* pathfinding in 3D space.
    :param obstacles: List of obstacles (buildings) with their 3D coordinates and dimensions.
    :param start: 3D start coordinate (x, y, z).
    :param goal: 3D goal coordinate (x, y, z).
    :param grid_size: Size of the grid for each dimension (x, y, z).
    :param resolution: Grid resolution.
    :return: Path as a list of 3D points (if a path exists), otherwise False.
    """
    neighbors = [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]  # 6-way movement

    close_set = set()
    came_from = {}
    gscore = {start: 0}
    fscore = {start: heuristic(start, goal)}
    oheap = []

    heapq.heappush(oheap, (fscore[start], start))
    
    while oheap:
        current = heapq.heappop(oheap)[1]

        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            return path[::-1]

        close_set.add(current)
        for i, j, k in neighbors:
            neighbor = current[0] + i, current[1] + j, current[2] + k
            tentative_g_score = gscore[current] + heuristic(current, neighbor)

            if 0 <= neighbor[0] < grid_size[0] and 0 <= neighbor[1] < grid_size[1] and 0 <= neighbor[2] < grid_size[2]:
                if is_collision_3d(neighbor, obstacles, resolution):
                    continue
            else:
                continue

            if neighbor in close_set and tentative_g_score >= gscore.get(neighbor, 0):
                continue

            if tentative_g_score < gscore.get(neighbor, 0) or neighbor not in [i[1] for i in oheap]:
                came_from[neighbor] = current
                gscore[neighbor] = tentative_g_score
                fscore[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                heapq.heappush(oheap, (fscore[neighbor], neighbor))

    return False

def is_collision_3d(point, obstacles, resolution):
    """
    Check if a point collides with any obstacle.
    :param point: The 3D point to check.
    :param obstacles: List of obstacles.
    :param resolution: Grid resolution.
    :return: True if there is a collision, False otherwise.
    """
    px, py, pz = point
    for obstacle in obstacles:
        ox, oy, oz, dx, dy, dz = obstacle  # Obstacle position and dimensions
        if ox <= px <= ox + dx and oy <= py <= oy + dy and oz <= pz <= oz + dz:
            return True
    return False

def is_line_intersect_building(hub_position, drone_position, building):
    """
    Check if the line segment between the hub and a drone intersects a building in 3D space.

    :param hub_position: Tuple (x, y, z) representing the position of the hub.
    :param drone_position: Tuple (x, y, z) representing the position of the drone.
    :param building: Shapely Polygon representing the building footprint.
    :param building_height: Height of the building.
    :return: True if the line intersects the building in 3D, False otherwise.
    """
    building_height = building[1]
    # Create a 2D line segment from the hub to the drone
    line_2d = LineString([hub_position[:2], drone_position[:2]])  # Only use x, y coordinates

    # Check for 2D intersection with the building footprint
    if line_2d.intersects(building[0]):
        # Check if the drone's altitude is within the building's height
        min_altitude = min(hub_position[2], drone_position[2])
        max_altitude = max(hub_position[2], drone_position[2])
        if min_altitude < building_height < max_altitude or min_altitude < building_height < max_altitude:
            return True

    return False
