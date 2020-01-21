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

results_kharif = []
results_zaid = []
results_rabi = []

time = []

for i in range(0,47,2):
  pixels_kharif = 0
  pixels_zaid = 0
  pixels_rabi = 0
  time.append(i//2)
  print(filenames[i])
  print(filenames[i+1])
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
          if(ndvi[i][j]<0.2 or ndvi[i][j] > 0.6):
              ndvi[i][j]=-1
          if((ndvi[i][j]>=0.43 and ndvi[i][j] <= 0.66)):
            pixels_kharif += 1
          if((ndvi[i][j]>=0.23 and ndvi[i][j] <= 0.42)):
            pixels_rabi += 1
          if((ndvi[i][j]>=0.32 and ndvi[i][j] <= 0.57)):
            pixels_zaid += 1
  results_kharif.append(pixels_kharif)
  results_rabi.append(pixels_rabi)
  results_zaid.append(pixels_zaid)
  
  export ndvi image
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
plt.plot(time, results_kharif, label="NDVI_kharif")
plt.plot(time, results_rabi, label="NDVI_rabi")
plt.plot(time, results_zaid, label="NDVI_zaid")
plt.legend(loc=2)
plt.show()