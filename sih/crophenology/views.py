from django.urls import reverse_lazy
from django.views import generic
from django.shortcuts import get_object_or_404, render,redirect
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

import rasterio
from rasterio import plot
import matplotlib.pyplot as plt
import numpy as np
import os

def dashboard(request):
    if request.user.is_authenticated:
        username=request.user.username
        return render(request, 'dashboard.html', {'username':username,})
    else:
        error="not signed in"
        return render(request, 'myprofile.html', {'error':error,})

def upload_data(request):
    if request.method == "POST":
        folder_path = request.POST.get('textfield', None)
        preprocess(folder_path)
        return HttpResponseRedirect('/user/dashboard')
    else:
        return render(request,'upload.html')

def preprocess(folder_path):

# def fun(impath):
  os.chdir(folder_path)
  filenames = []
  for root, dirs, files in os.walk("."):
      for filename in files:
          filenames.append(filename)
  #import bands as separate 1 band raster
  filenames.sort()
  print(filenames)
  results_kharif = []
  results_zaid = []
  results_rabi = []
  results_kharife = []
  results_zaide = []
  results_rabie = []

  time = []
  from matplotlib import colors

  for i in range(0,47,2):
    pixels_kharif = 0
    pixels_zaid = 0
    pixels_rabi = 0
    pixels_kharif2 = 0
    pixels_zaid2 = 0
    pixels_rabi2 = 0
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
    #generate nir and red objects as arrays in float64 format
    red = band4.read(1).astype('float64')
    nir = band5.read(1).astype('float64')
    #ndvi calculation, empty cells or nodata cells are reported as 0
    ndvi=np.where(
        (nir+red)==0., 
        0, 
        (nir-red)/(nir+red))
    #ndvi[:5,:5]
    shape = ndvi.shape
    for ii in range(0,shape[0]):
        for j in range(0,shape[1]):
            if(ndvi[ii][j]<0.2 or ndvi[i][j] > 0.6):
                ndvi[ii][j]=-1
            if((ndvi[ii][j]>=0.43 and ndvi[i][j] <= 0.66)):
              pixels_kharif += 1
            if((ndvi[ii][j]>=0.23 and ndvi[i][j] <= 0.42)):
              pixels_rabi += 1
            if((ndvi[ii][j]>=0.32 and ndvi[i][j] <= 0.57)):
              pixels_zaid += 1
    
    results_kharif.append(pixels_kharif)
    results_rabi.append(pixels_rabi)
    results_zaid.append(pixels_zaid)
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
    results_kharife.append(pixels_kharif2)
    results_rabie.append(pixels_rabi2)
    results_zaide.append(pixels_zaid2)
    
    #export ndvi image
    ndviImage = rasterio.open('../ndviImage'+str(i) +'.tiff','w',driver='Gtiff',
                              width=band4.width, 
                              height = band4.height, 
                              count=1, crs=band4.crs, 
                              transform=band4.transform, 
                              dtype='float64')
    ndviImage.write(ndvi,1)
    ndviImage.close()
    #plot ndvi
    
    ndvi = rasterio.open('../ndviImage'+str(i) +'.tiff')
    
      # let's visualize
    #plt.show()
    # fig = plt.figure(figsize=(18,12))
    # plot.show(ndvi)
  os.chdir('../')  
  print (str(os.path.dirname(os.path.realpath(__file__))))
  
  plt.plot(time, results_kharif, label="NDVI_kharif")  
  plt.plot(time, results_rabi, label="NDVI_rabi")
  plt.plot(time, results_zaid, label="NDVI_zaid")
  plt.legend(loc=2)
  plt.savefig('ndvicomp.png',dpi=300)
  plt.plot(time, results_kharife, label="EVI2_kharif")
  plt.plot(time, results_rabie, label="EVI2_rabi")
  plt.plot(time, results_zaide, label="EVI2_zaid")
  plt.legend(loc=2)
  plt.savefig('evicomp.png',dpi=300)

  return str(os.path.dirname(os.path.realpath(__file__)))
  


