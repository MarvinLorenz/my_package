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

#plotting.py

def plot_transect(var_to_display, bathy, h, path, filename, labels, xaxis=None, cont=None, cmap = 'jet',fig_x=10,fig_y=5,fs=20, title=None, vmin=None,vmax=None):
	
	#label = [x, y, pcolor, cont]
	if np.shape(var_to_display) != np.shape(h):
		sys.exit('var and h dont have the same dimensions')
	if cont != None:
		if np.shape(var_to_display) != np.shape(h) or np.shape(var_to_display) != np.shape(cont):
			sys.exit('var, h and cont dont have the same dimensions')
	bathy_array = []
	i=0
	while i < np.shape(h)[0]:
		bathy_array.append(bathy)
		i+=1
	z_axis = bathy_array - np.cumsum(h,axis=0)
	
	if xaxis==None:
		x_axis = np.zeros(shape=np.shape(var_to_display))
		i=0
		while i < np.shape(x_axis)[0]:
			x_axis[i,:] = np.arange(np.shape(h)[1])
			i+=1
	else:
		x_axis = np.zeros(shape=np.shape(var_to_display))
		i=0
		while i < np.shape(x_axis)[0]:
			x_axis[i,:] = xaxis
			i+=1
	plt.figure(figsize=(fig_x,fig_y))
	if title != None:
		plt.title(title)
	ax = plt.subplot(111)
	plt.gca().invert_yaxis()
	if vmin==None:
		vmin=int(np.min(var_to_display))
	if vmax==None:
		vmax=int(np.max(var_to_display))+1
	pcol=ax.pcolor(x_axis,z_axis,var_to_display, cmap = cmap, vmin = vmin, vmax = vmax)
	cbar = plt.colorbar(pcol)
	cbar.set_label(labels[2], fontsize = fs)
	if cont != None:
		#print(np.shape(x_axis), np.shape(z_axis), np.shape(cont))
		levels = np.linspace(-np.max(cont),np.max(cont),9)
		cont = ax.contour(x_axis, z_axis, cont, levels=levels,colors='k')
		plt.clabel(cont, inline=1, fontsize=fs-8, fmt='%1.2f')
	plt.xlabel(labels[0], fontsize = fs)
	plt.xticks(fontsize = fs)
	plt.ylabel(labels[1], fontsize = fs)
	plt.yticks(fontsize = fs)
	plt.gcf().subplots_adjust(bottom=0.15)
	plt.xlim([x_axis[0,0],x_axis[0,-1]])
	plt.ylim([np.max(bathy)+10,10])
	plt.savefig(path+filename,format = 'png',bbox_inches='tight')
	plt.close()
	plt.clf()
	return('done')


def plot_pcolor(var,x,y,path,filename,labels,cont=None,contN=10,cont_min_max=None,coastline=None,title=None,\
fig_x=10,fig_y=5,vmin=None,vmax=None,cmap='jet',fs=20,xlim=None,ylim=None,quiver=None,quiver_step=10,qk_pos=[0.2,0.2]):
	
	#convert x and y so cont can be plotted as well
	if cont != None or coastline != None or quiver != None:
		x_n = np.zeros(shape=np.shape(var))
		y_n = np.zeros(shape=np.shape(var))
		i=0
		while i < np.shape(x_n)[0]:
			x_n[i,:] = x
			i+=1
		j=0
		while j < np.shape(y_n)[1]:
			y_n[:,j] = y
			j+=1
	plt.figure(figsize=(fig_x,fig_y))
	if title != None:
		plt.title(title)
	ax = plt.subplot(111)
	#plt.gca().invert_yaxis()
	if vmin==None:
		vmin=int(np.min(var))
	if vmax==None:
		vmax=int(np.max(var))+1
	pcol=ax.pcolor(x,y,var, cmap = cmap, vmin = vmin, vmax = vmax)
	cbar = plt.colorbar(pcol)
	cbar.set_label(labels[2], fontsize = fs)
	if cont != None:
		#print(np.shape(x_axis), np.shape(z_axis), np.shape(cont))
		if cont_min_max == None:
			levels = np.linspace(np.min(cont),np.max(cont),contN)
		else:
			levels = np.linspace(cont_min_max[0],cont_min_max[1],contN)
		cont = ax.contour(x_n, y_n, cont, levels=levels,colors='k')
		plt.clabel(cont, inline=1, fontsize=fs-8, fmt='%1.2f')
	if coastline != None:
		coastline = np.ma.getdata(coastline)
		coastline[coastline >10000] = -10.0
		level = [-10]
		plt.rcParams['contour.negative_linestyle'] = 'solid'
		cont = ax.contour(x_n, y_n, coastline, levels=level, colors = 'black',linewidths=1.0)
	if quiver != None:
		#Colors=np.sqrt(np.abs(quiver[0][::quiver_step,::quiver_step]**2+quiver[1][::quiver_step,::quiver_step]**2))
		qui = ax.quiver(x_n[::quiver_step,::quiver_step], y_n[::quiver_step,::quiver_step], quiver[0][::quiver_step,::quiver_step]\
		,quiver[1][::quiver_step,::quiver_step], units='width', pivot = 'middle', scale = 5)
		plt.quiverkey(qui, qk_pos[0], qk_pos[1], 0.1, r'0.1 m/s', labelpos='E',coordinates='figure')
	plt.xlabel(labels[0], fontsize = fs)
	plt.xticks(fontsize = fs)
	plt.ylabel(labels[1], fontsize = fs)
	plt.yticks(fontsize = fs)
	plt.gcf().subplots_adjust(bottom=0.15)
	if xlim==None:
		plt.xlim([x[0],x[-1]])
	else:
		plt.xlim(xlim)
	if ylim == None:
		plt.ylim([y[0],y[-1]])
	else:
		plt.ylim(ylim)
	plt.savefig(path+filename,format = 'png',bbox_inches='tight')
	plt.close()
	plt.clf()
	
	return('done')		
	
def plot_simple(x,y,path,filename,labels_axes,title=None,fig_x=10,fig_y=5,fs=20,xlim=None,ylim=None,invert_y='No',labels_graphs=None,labelpos='upper right'):
	
	plt.figure(figsize=(fig_x,fig_y))
	if title != None:
		plt.title(title)
	ax = plt.subplot(111)
	if invert_y == 'Yes':
		plt.gca().invert_yaxis()
	if len(np.shape(y))!=1 and len(np.shape(x))!=1:
		print(np.shape(y)[0], 'graphs')
		i=0
		while i < np.shape(y)[0]:
			ax.plot(x[i],y[i],label = labels_graphs[i])
			i+=1
	else:
		print('only one graph')
		ax.plot(x,y,label=labels_graphs)
	plt.xlabel(labels_axes[0], fontsize = fs)
	plt.xticks(fontsize = fs)
	plt.ylabel(labels_axes[1], fontsize = fs)
	plt.yticks(fontsize = fs)
	plt.gcf().subplots_adjust(bottom=0.15)
	if labels_graphs != None:
		plt.legend(loc=labelpos)		
	if xlim==None and len(np.shape(x))==1 :
		plt.xlim([x[0],x[-1]])
	elif xlim==None and len(np.shape(x))!=1 :
		plt.xlim([np.min(x),np.max(x)])
	else:
		plt.xlim(xlim)
	if ylim == None:
		plt.ylim([np.min(y),np.max(y)])
	else:
		plt.ylim(ylim)
	plt.savefig(path+filename,format = 'png',bbox_inches='tight')
	plt.close()
	plt.clf()
	
	return('done')
	
def plot_n_pcolor(var,x,y,path,filename,labels,ax_shape,coastline=None,title=None,fig_x=10,fig_y=10,vmin=None,vmax=None,cmap='jet',\
fs=20,xlim=None,ylim=None,ax_title=None,ax_title_pos=[0.8,0.8]):
	
	print(np.shape(var))
	print(ax_shape)
	
	if coastline != None:
		x_n = np.zeros(shape=np.shape(var[0]))
		y_n = np.zeros(shape=np.shape(var[0]))
		i=0
		while i < np.shape(x_n)[0]:
			x_n[i,:] = x
			i+=1
		j=0
		while j < np.shape(y_n)[1]:
			y_n[:,j] = y
			j+=1	
	
	fig, ax = plt.subplots(nrows=ax_shape[0], ncols=ax_shape[1], sharex=True, sharey=True)
	fig.set_size_inches(fig_x,fig_y)

	if title != None:
		plt.title(title)
	#plt.gca().invert_yaxis()
	if vmin==None:
		vmin=int(np.min(var))
	if vmax==None:
		vmax=int(np.max(var))+1
	
	k=0
	i=0
	while i < np.shape(ax)[0]:
		j=0
		while j < np.shape(ax)[1]:
			if k < np.shape(var)[0]:
				pcol=ax[i][j].pcolor(x,y,var[k], cmap = cmap, vmin = vmin, vmax = vmax)
				if coastline != None:
					coastline = np.ma.getdata(coastline)
					coastline[coastline >10000] = -10.0
					level = [-10]
					plt.rcParams['contour.negative_linestyle'] = 'solid'
					ax[i][j].contour(x_n, y_n, coastline, levels=level, colors = 'black',linewidths=1.0)
				if ax_title != None:
					ax[i][j].text(ax_title_pos[0],ax_title_pos[1], ax_title[k],transform = ax[i][j].transAxes, fontsize=fs)
			ax[i][j].tick_params(axis = 'both', length = 4, labelsize = fs-2, which = 'both', direction = 'inout', labelcolor='black', top='on', bottom='on', left='on', right='on')
			if i == 0:
				ax[i][j].tick_params(labeltop= True)
			if j == np.shape(ax)[1]-1:
				ax[i][j].tick_params(labelright= True)
			if xlim==None:
				plt.xlim([x[0],x[-1]])
			else:
				plt.xlim(xlim)
			if ylim == None:
				plt.ylim([y[0],y[-1]])
			else:
				plt.ylim(ylim)
			j+=1
			k+=1
		i+=1

	
	fig.add_subplot(111, frameon=False)
	# hide tick and tick label of the big axes
	plt.tick_params(labelcolor='none', top='off', bottom='off', left='off', right='off')
	plt.xlabel(labels[0], fontsize = fs, labelpad=20)
	plt.ylabel(labels[1] , fontsize = fs, labelpad=20)
	
	cbaxes = fig.add_axes([1.0, 0.15, 0.03, 0.75]) 
	cbar = plt.colorbar(pcol, cax=cbaxes)
	cbar.set_label(labels[2], fontsize = fs)	
	cbar.ax.tick_params(labelsize=fs)
	
	fig.subplots_adjust(hspace=0)
	fig.subplots_adjust(wspace=0)
	plt.gcf().subplots_adjust(bottom=0.15)
	plt.savefig(path+filename,format = 'png',bbox_inches='tight')
	plt.close()
	plt.clf()
	
	return('done')	

