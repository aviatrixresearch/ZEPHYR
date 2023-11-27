from generate_env import generate_env
import matplotlib.pyplot as plt
import random
from shapely.geometry import Point

NUM_DRONES = 10

def main():
    ax, buildings, grid, positions = generate_env('map.osm', NUM_DRONES)
    
    plt.show()

if __name__ == '__main__':
    main()





#print('\n')
#print(buildings)
#plt.show()
