#import required libraries
import rasterio
from rasterio import plot
import matplotlib.pyplot as plt
import numpy as np
#%matplotlib inline
import os
print (os.listdir('../'))
os.chdir('../sih/Clipped_NDVI/')
filenames = []
for root, dirs, files in os.walk("."):
    for filename in files:
        filenames.append(filename)
#import bands as separate 1 band raster
for i in range(0,len(filenames),2):
  # print(filenames[i])
  # print(filenames[i+1])
  band4 = rasterio.open(filenames[i]) #red
  band5 = rasterio.open(filenames[i+1]) #nir
  #number of raster rows
  band4.height
  #number of raster columns
  band4.width
  #plot band 
  # plot.show(band4)
  #type of raster byte
  band4.dtypes[0]
  #raster sytem of reference
  band4.crs
  #raster transform parameters
  band4.transform
  #raster values as matrix array
  band4.read(1)
  #multiple band representation
  # fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
  # plot.show(band4, ax=ax1, cmap='Blues') #red
  # plot.show(band5, ax=ax2, cmap='Blues') #nir
  # fig.tight_layout()
  #generate nir and red objects as arrays in float64 format
  red = band4.read(1).astype('float64')
  nir = band5.read(1).astype('float64')
  #ndvi calculation, empty cells or nodata cells are reported as 0
  ndvi=np.where(
      (nir+red)==0., 
      0, 
      (nir-red)/(nir+red))
  ndvi[:5,:5]
  shape = ndvi.shape
  for i in range(0,shape[0]):
      for j in range(0,shape[1]):
          if(ndvi[i][j]<0.2):
              ndvi[i][j]=-1

  #export ndvi image
  ndviImage = rasterio.open('ndviImage'+str(i) +'.tiff','w',driver='Gtiff',
                            width=band4.width, 
                            height = band4.height, 
                            count=1, crs=band4.crs, 
                            transform=band4.transform, 
                            dtype='float64')
  ndviImage.write(ndvi,1)
  ndviImage.close()
  #plot ndvi

  ndvi = rasterio.open('ndviImage'+str(i) +'.tiff')
  fig = plt.figure(figsize=(18,12))
  plot.show(ndvi)