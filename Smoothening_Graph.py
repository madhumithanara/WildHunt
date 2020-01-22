#import required libraries
import rasterio
from rasterio import plot
import matplotlib.pyplot as plt
import numpy as np
#%matplotlib inline
import os
print (os.listdir('../'))
os.chdir('/content/drive/My Drive/Clipped_NDVI/')
filenames = []
for root, dirs, files in os.walk("."):
    for filename in files:
        filenames.append(filename)
print(len(filenames))
#import bands as separate 1 band raster
counts = []
avg_zaid = []
avg_kharif = []
avg_rabi = []

a_zaid = []
a_kharif = []
a_rabi = []
for i in range(0,len(filenames)-1,2):
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
  count_rabi = 0
  rabi = 0
  
  count_kharif = 0
  kharif  = 0
  
  count_zaid = 0
  zaid = 0
  

  for i1 in range(0,shape[0]):
      
      for j in range(0,shape[1]):
          if(ndvi[i1][j]<0.2 or ndvi[i1][j]>0.7):
              ndvi[i1][j]=-1
          else:
            if ndvi[i1][j]>=0.45 and ndvi[i1][j]<=0.65:
              count_kharif += 1
              kharif += ndvi[i1][j]
            if ndvi[i1][j] >= 0.25 and ndvi[i1][j]<=0.40:
              count_rabi += 1
              rabi += ndvi[i1][j]
            if ndvi[i1][j]>=0.35 and ndvi[i1][j]<=0.55:
              count_zaid += 1
              zaid += ndvi[i1][j]
  if(count_kharif>0):
    avg_kharif.append((kharif/count_kharif)/5)
    a_kharif.append(kharif/count_kharif)
  else:
    avg_kharif.append(0)
    a_kharif.append(0)

  if(count_kharif>0):
    a_rabi.append(rabi/count_rabi)
    avg_rabi.append((rabi/count_rabi)/3)
  else:
    avg_rabi.append(0)
    a_rabi.append(0)

  if(count_kharif>0):
    avg_zaid.append((zaid/count_zaid)/4)
    a_zaid.append(zaid/count_zaid)
  else:
    avg_zaid.append(0)
    a_zaid.append(0)

  
  

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


for i in range (0,len(avg_kharif)):
  if(avg_kharif[i]>avg_rabi[i]):
    if(avg_kharif[i]>avg_zaid[i]):
      counts.append(a_kharif[i])
    else:
      counts.append(a_zaid[i])
  else:
    if(avg_rabi[i]>avg_zaid[i]):
      counts.append(a_rabi[i])
    else:
      counts.append(a_zaid[i])


import matplotlib.pyplot as plt

xcord = []

for i in range(0,len(counts)):
    xcord.append(i+1)

plt.plot(xcord,counts)


from matplotlib import pyplot as mp
import numpy as np
from scipy.stats import norm

s = np.std(counts)
m = np.mean(counts)
plt.plot(norm.pdf(counts,m,s))

data =counts

# Fit a normal distribution to the data:
mu, std = norm.fit(data)

# Plot the histogram.
plt.hist(data, bins=1, density=True, alpha=0.6, color='w')

# plt.show()

# Plot the PDF.
xmin, xmax = plt.xlim()
x = np.linspace(xmin, xmax, 30)
p = norm.pdf(x, mu, std)
plt.plot(x, p, 'k', linewidth=2)
title = "Fit results: mu = %.2f,  std = %.2f" % (mu, std)
plt.title(title)

plt.show()