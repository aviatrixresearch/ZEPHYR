import osmium as osm
import shapely.wkb as wkblib
from shapely.geometry import Polygon, MultiPolygon
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import osmnx as ox
from pyproj import Proj, transform
import xml.etree.ElementTree as ET
import random
from shapely.geometry import Point

class BuildingHandler(osm.SimpleHandler):
    def __init__(self):
        osm.SimpleHandler.__init__(self)
        self.buildings = []

    def area(self, a):
        wkbfab = osm.geom.WKBFactory()
        if 'building' in a.tags:
            wkb = wkbfab.create_multipolygon(a)
            poly = wkblib.loads(wkb, hex=True)
            # Retrieve levels as a string and convert to an integer
            levels_str = a.tags.get('building:levels', '1')  # Default to '1' level if not specified
            levels = int(levels_str)  # Convert to integer
            self.buildings.append((poly, levels))

def plot_building_walls(ax, x, y, height):
    # Number of points forming the polygon
    num_points = len(x)

    # Plot each wall of the building
    for i in range(num_points - 1):
        # Coordinates of the wall
        wall_x = [x[i], x[i], x[i+1], x[i+1]]
        wall_y = [y[i], y[i], y[i+1], y[i+1]]
        wall_z = [0, height, height, 0]

        # Draw the wall as a quadrilateral
        ax.add_collection3d(Poly3DCollection([list(zip(wall_x, wall_y, wall_z))], color='gray', alpha=0.7))

def generate_drone_positions_3d(buildings_with_height, num_drones, grid, min_altitude=2, max_altitude=30):
    """
    Generates 3D drone positions that are not inside buildings.
    
    :param buildings_with_height: List of tuples (building_polygon, height).
    :param num_drones: Number of drone positions to generate.
    :param grid_size: Tuple (width, height) representing the size of the grid.
    :param min_altitude: Minimum flying altitude for drones.
    :param max_altitude: Maximum flying altitude for drones.
    :return: List of drone positions (x, y, z).
    """
    drone_positions = []

    while len(drone_positions) < num_drones:
        x = random.uniform(grid[0], grid[1])
        y = random.uniform(grid[2], grid[3])
        z = random.uniform(min_altitude, max_altitude)
        point = Point(x, y)

        # Check if the point is above all buildings
        if all(z > building_height or not building.contains(point) for building, building_height in buildings_with_height):
            drone_positions.append((x, y, z))

    return drone_positions

def generate_env(map_file, num_drones):

    def get_osm_bounds(osm_file_path):
        # Parse the OSM XML file
        tree = ET.parse(osm_file_path)
        root = tree.getroot()

        # Find the 'bounds' element
        bounds = root.find('bounds')
        if bounds is not None:
            minlat = float(bounds.get('minlat'))
            minlon = float(bounds.get('minlon'))
            maxlat = float(bounds.get('maxlat'))
            maxlon = float(bounds.get('maxlon'))
            return minlon, minlat, maxlon, maxlat
        else:
            return None

    def latlon_to_meters(lat, lon):
        # Define projections
        proj_latlon = Proj(proj='latlong', datum='WGS84')
        proj_meter = Proj(proj='utm', zone=33, datum='WGS84')

        # Convert
        x, y = transform(proj_latlon, proj_meter, lon, lat)
        return x, y

    handler = BuildingHandler()
    handler.apply_file(map_file)
    grid = get_osm_bounds(map_file)

    # Assuming 3 meters per level
    buildings_with_height = [(shape, levels * 3) for shape, levels in handler.buildings]

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    for building, height in buildings_with_height:
        if isinstance(building, Polygon):
            x, y = building.exterior.xy
            ax.plot_trisurf(x, y, [height]*len(x), alpha=0.7, color='tan')
            plot_building_walls(ax, x, y, height)
        elif isinstance(building, MultiPolygon):
            for poly in building.geoms:
                x, y = poly.exterior.xy
                ax.plot_trisurf(x, y, [height]*len(x), alpha=0.7, color='tan')
                plot_building_walls(ax, x, y, height)

    drone_positions = generate_drone_positions_3d(buildings_with_height, num_drones, grid)
    #for x, y, z in drone_positions:
    #    ax.scatter(x, y, z, color='blue', marker='o')

    ax.set_xlabel('Longitude')
    ax.set_ylabel('Latitude')
    ax.set_zlabel('Height (m)')

    minx, miny = latlon_to_meters(grid[0], grid[1])
    maxx, maxy = latlon_to_meters(grid[2], grid[3])

    #print(minx, miny)
    #print(maxx, maxy)

    grid_size = (abs(maxx-minx), abs(maxy-miny))

    return ax, buildings_with_height, grid_size, drone_positions

