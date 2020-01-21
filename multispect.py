# from osgeo import gdal
import numpy as np
import sys
import rasterio
from matplotlib import pyplot as plt
import cv2 

img1 = rasterio.open("awifs_ndvi_201701_15_2_clipped.tif") #nir
img2 = rasterio.open("awifs_ndvi_201701_15_1_clipped.tif") #red

array1 = img1.read(1)
array2 = img2.read(1) 


print(array2.shape)

numr = np.subtract(array1,array2)
denr = np.add(array1,array2)

ndvi = np.divide(numr,denr)


# cv2.imshow('NDVI Visualization',ndvi)
# cv2.waitKey(0)

greaterthanone = 0
lessthanminusone = 0

for i in range(len(ndvi)):
	for j in range(len(ndvi[0])):
		if ndvi[i][j] > 10:
			greaterthanone+=1
		elif ndvi[i][j] < -1:
			lessthanminusone += 1

print("Greater than one ",greaterthanone)
print("Less than minus one",lessthanminusone)