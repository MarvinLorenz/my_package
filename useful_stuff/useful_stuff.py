# -*- coding: utf-8 -*-
"""
Created on Mon Mar 19 11:26:27 2018

@author: lorenz
"""
import numpy as np
import sys
sys.path.append('/fast/lorenz/Programs/seawater')
import gsw as gsw
from scipy import interpolate
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter
from matplotlib.ticker import ScalarFormatter
import netCDF4

def h_weighted_mean(var,weight):
	var_weight = var*weight
	out = np.sum(var_weight,axis=0)/np.sum(weight, axis=0)
	return(out)

def interpolate_on_grid(lat,lon,data,grid_lat,grid_lon):
	
	#note that the used np.interp uses the values under a mask, too. That will destroy the values at the borders and are masked in the last line of code
	#This should be therefore used only for plots or comparisons!
	
	if np.shape(data)[0] != len(lat) or np.shape(data)[1] != len(lon):
		print(np.shape(data),len(lat),len(lon))
		sys.exit('x and y dont match data')
	data_grid = np.zeros(shape=(np.shape(grid_lat)[0],np.shape(grid_lon)[0])) #the data that will be returned
	data_x = np.zeros(shape=(np.shape(lat)[0],np.shape(grid_lon)[0]))
	#interp to grid_x
	j=0
	while j < np.shape(data_x)[0]:
		data_x[j,:] = np.interp(grid_lon,lon,data[j,:])
		j+=1
	print(np.shape(data_grid))
	#interp to grid_y
	i=0
	while i < np.shape(data_grid)[1]:
		data_grid[:,i] = np.interp(grid_lat,lat,data_x[:,i])
		i+=1
	#create a mask
	mask_val = np.ma.getdata(data)[0,0]
	if mask_val < 0:
		data_grid = np.ma.masked_where(data_grid < np.min(data), data_grid)
	elif mask_val > 0:
		data_grid = np.ma.masked_where(data_grid > np.max(data), data_grid)
	return(data_grid)

def useful_fucntion():
	
	return()