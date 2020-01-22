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

results_rabi = []

time = ["jan17","feb17","mar17","apr17","may17","jun17","jul17","aug17","sep17","oct17","nov17","dec17","jan18","feb18","mar18","apr18","may18","jun18","jul18","aug18","sep18","oct18","nov18","dec18"]
time2 = ["jan17","feb17","mar17","apr17","may17","jun17","jul17","aug17","sep17","oct17","nov17","dec17","jan18","feb18","mar18","apr18","may18","jun18","jul18","aug18","sep18","oct18","nov18"]
for i in range(0,47,2):
  pixels_kharif = 0
  pixels_zaid = 0
  pixels_rabi = 0
  # time.append(i//2)
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
          if(ndvi[ii][j]<0.2 or ndvi[ii][j] > 0.6):
              ndvi[ii][j]=-1
          else:
            pixels_rabi += 1
  results_rabi.append(pixels_rabi)

  print("Image",i//2,"done")

plt.plot(time, results_rabi, label="NDVI")
plt.xticks(rotation=90)
plt.legend(loc=2)
plt.show()
z=0
diff=[]
threshold = 250000
for i in range(0,len(results_rabi)-1):
  diff.append(results_rabi[i+1]-results_rabi[i])
  if(diff[i]>threshold):
    print("Date of sowing:", time[i])
    z=z+1
  elif(-1*diff[i]>threshold):
    print("Date of harvesting:", time[i])

print("number of harvests:",z)

plt.plot(time2, diff, label="change_in_NDVI")
plt.xticks(rotation=80)
plt.legend(loc=2)
plt.show()