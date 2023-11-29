import rasterio
from matplotlib import pyplot as plt

# Load the topographic data
with rasterio.open('sample.tif') as dataset:
    # Read the dataset
    topographic_data = dataset.read(1)

# Plot the data
plt.imshow(topographic_data, cmap='terrain')
plt.colorbar(label='Elevation (meters)')
plt.title('Topographic Map')
plt.show()
