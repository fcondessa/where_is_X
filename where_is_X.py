import json
from collections import defaultdict
import matplotlib.pyplot as plt
import numpy as np
from scipy.ndimage import convolve
path_location_dir = 'loc_dir.json'
path_location_list = 'locs.json'

with open(path_location_dir) as f:
	locations_dictionary = json.load(f)

with open(path_location_list) as f:
	locations_list= json.load(f)

def to_map(list_locations,resolution=1):
	coord = np.array(list_locations)
	orig_coordinates = (np.round(np.array(coord) / float(resolution)))
	len_coor = orig_coordinates.shape[0]
	val = 1.0
	x = int(360 / resolution)
	y = int(180 / resolution)
	xoffset = int(180 / resolution)
	yoffset = int(90 / resolution)
	matr = np.zeros((x,y))
	for elem in orig_coordinates:
		# matr[int(np.mod(elem[0],x)),int(np.mod(elem[1],y))]+=val
		matr[int(elem[1] + xoffset), int(elem[0] + yoffset)] += val
	return matr



target_list = ['pennsylvania','pa','pittsburgh','philadelphia','california','new york']
for target_id in range(len(target_list)):
	target = target_list[target_id]
	val_limits_pa = [47,52,99,107]
	resolution = .1
	matr = to_map(locations_dictionary[target],resolution)
	#val_limits = [40,70,52 ,115]
	val_limits = val_limits_pa
	val_limits = [int(elem/resolution) for elem in val_limits]
	val = matr.T[::-1,:]
	val = val[val_limits[0]:val_limits[1],val_limits[2]:val_limits[3]]
	val = convolve(1.0*(val),np.ones((2,2)))
	plt.subplot(2,3,1+target_id)
	plt.imshow(np.log(val),cmap='plasma')
	plt.title(target)

