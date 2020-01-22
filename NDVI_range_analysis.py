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

!pip install rasterio
#import required libraries
import rasterio
from rasterio import plot
import matplotlib.pyplot as plt
import numpy as np

#%matplotlib inline

#import bands as separate 1 band raster
for k in range(0,8):
  results_kharif = []
  results_zaid = []
  results_rabi = []

  time = []

  for i in range(0,47,2):
    pixels_kharif = 0
    pixels_zaid = 0
    pixels_rabi = 0
    time.append(i//2)
    # print(filenames[i])
    # print(filenames[i+1])
    band4 = rasterio.open(filenames[i]) #red
    band5 = rasterio.open(filenames[i+1]) #nir
    
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
    for ii in range(0,shape[0]):
        for j in range(0,shape[1]):
            if(ndvi[ii][j]<(k/10+0.05) or ndvi[ii][j] >(k/10+ 0.15)):
                ndvi[ii][j]=-1
            else:
                pixels_rabi += 1
    print(i//2,"num of pixels",pixels_rabi)
    # results_kharif.append(pixels_kharif)
    results_rabi.append(pixels_rabi)

  lbl = "NDVI_"+str(k/10+0.05)+"-"+str(k/10+0.15)
  save_name = "NDVI_"+str(k/10+0.05)+"-"+str(k/10+0.15)+".png"
  # plt.plot(time, results_kharif, label="NDVI_kharif")
  plt.plot(time, results_rabi, label=lbl)
  # plt.plot(time, results_zaid, label="NDVI_zaid")
  plt.savefig(save_name, dpi=300)
  plt.legend(loc=2)
  plt.show()