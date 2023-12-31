# Environment Simulation

## Project Overview

This project is focused on creating a realistic simulation environment for drone operations using data extracted from OpenStreetMap (OSM). It includes the generation of a 3D model representing buildings as obstacles and a pathfinding algorithm for drones to navigate through urban landscapes. The primary goal is to optimize drone paths in real-world scenarios, considering factors like building interference and signal propagation.

## Features

- **3D Environmental Modeling:** Generates a 3D representation of an urban area with buildings as obstacles, based on OSM or random data.

![Complex Environment Model](assets/tuscaloosa.PNG)

- **Node Pathfinding:** Implements a 3D A* pathfinding algorithm to navigate drones (nodes) around obstacles.
- **Signal Strength Calculation:** Estimates the signal strength between drones and a central communication hub, considering obstacles and distance.
- **Interactive Visualization:** Provides a real-time 3D visualization of drone movements and building structures. (This functionality is archived and still in progress. Run /archive/beta2.py to see the idea)

![Simulation with Simple Environment Model](/assets/isometric.PNG)

## Getting Started

### Prerequisites

Ensure you have the following installed:

- Python 3
- Libraries: `numpy`, `matplotlib`, `osmium`, `shapely`, `osmnx`, `pyproj`, `rasterio`, `requests`, `scipy`

You can install these libraries using pip:

```bash
pip install -r requirements.txt
```
### Installation
Clone repository
```bash
git clone https://github.com/aviatrixresearch/ZEPHYR
```
Naviate to repository
```bash
cd ZEPHYR
```

### Execute Simulation
```bash
python main.py --simple
```

## Contact
Jonathan Stuecker (jpstuecker@crimson.ua.edu)



