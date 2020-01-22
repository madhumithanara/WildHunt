import cv2
import numpy as np
from google.colab.patches import cv2_imshow
from google.colab import drive
drive.mount('/content/drive')

import os
os.chdir('/content/drive/My Drive/SIH_2020/Clipped_NDVI')
filenames = []
for root, dirs, files in os.walk("."):
    for filename in files:
        filenames.append(filename)

print(len(filenames))



#import required libraries
import rasterio
from rasterio import plot
import matplotlib.pyplot as plt
import numpy as np

#%matplotlib inline

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
  
  #generate nir and red objects as arrays in float64 format
  red = band4.read(1).astype('float64')
  nir = band5.read(1).astype('float64')
  #evi2 calculation, empty cells or nodata cells are reported as 0
  evi2=np.where(
      (nir+red)==0., 
      0, 
      2.5*((nir-red)/(nir+2.4*red+1)))
  evi2[:5,:5]
  shape = evi2.shape
  for ii in range(0,shape[0]):
      for j in range(0,shape[1]):
          # if(evi2[ii][j]<0.2 or evi2[ii][j] > 0.6):
          #     evi2[ii][j]=-1
          if((evi2[ii][j]>=0.84 and evi2[ii][j] <= 1.25)):
            pixels_kharif += 1
          if((evi2[ii][j]>=0.45 and evi2[ii][j] <= 0.72)):
            pixels_rabi += 1
          if((evi2[ii][j]>=0.55 and evi2[ii][j] <= 0.96)):
            pixels_zaid += 1
  results_kharif.append(pixels_kharif)
  results_rabi.append(pixels_rabi)
  results_zaid.append(pixels_zaid)
  
  # export evi2 image
  evi2Image = rasterio.open('evi2Image'+str(i) +'.tiff','w',driver='Gtiff',
                            width=band4.width, 
                            height = band4.height, 
                            count=1, crs=band4.crs, 
                            transform=band4.transform, 
                            dtype='float64')
  evi2Image.write(evi2,1)
  evi2Image.close()
  #plot evi2

  evi2 = rasterio.open('evi2Image'+str(i) +'.tiff')
  # plot.show(evi2)
  print("image",i,"done")
plt.plot(time, results_kharif, label="EVI2_kharif")
plt.plot(time, results_rabi, label="EVI2_rabi")
plt.plot(time, results_zaid, label="EVI2_zaid")
plt.legend(loc=2)
plt.show()