from generate_env import generate_env, generate_env_simple
import matplotlib.pyplot as plt
import random
from shapely.geometry import Point
from argparse import ArgumentParser
from optimizer import optimization

NUM_DRONES = 10

parser = ArgumentParser()
parser.add_argument('--simple', action='store_true', help='Run program with simple interface')
args = parser.parse_args()


def main():
    if args.simple:
        ax, buildings, grid, positions = generate_env_simple()
        optimal_hub_location = optimization(positions, 100, buildings, 2.8e9, (100, 100, 100))
        ax.scatter(*optimal_hub_location, c='green', marker='^', s=100)
    else:
        ax, buildings, grid, positions = generate_env('map.osm', NUM_DRONES)
    plt.show()

if __name__ == '__main__':
    main()





#print('\n')
#print(buildings)
#plt.show()
