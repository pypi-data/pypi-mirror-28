import errno
import os
from os.path import isdir as dir_exist
from os.path import isfile as file_exist
from os.path import basename

from .prainsa_loader import prainsa_loader
from .numpy_loader import numpy_loader
from .matlab_loader import matlab_loader

def main_loader(path, dataset_name=None, variable_name=None, num_channels=None, sampling_rate=None, epoch_length=1, mapping=True):
	if dir_exist(path):
		# get files only
		files = [file for file in os.listdir(path) if '.' in file]

		# look for metadata files
		for file in files:
			file_name, ext = file.split('.')
			if file_name == 'metadata' and ext == 'dat':
				return prainsa_loader(path, mapping).create_Prainsa()

		# look for Matlab files
		for file in files:
			file_name, ext = file.split('.')
			if ext == 'mat':
				return matlab_loader(file.path, dataset_name, variable_name, num_channels, sampling_rate, epoch_length).create_Prainsa()

		# look for NumPy files
		for file in files:
			file_name, ext = file.split('.')
			if ext == 'npy' or ext == 'npz':
				return numpy_loader(file.path, dataset_name, variable_name, num_channels, sampling_rate, epoch_length).create_Prainsa()

	elif file_exist(path):
		file_name, ext = os.path.splitext(path)
		if ext not in ['.mat', '.npz', '.npy']:
			raise Exception('File type is not recognized. Must be a ".mat", ".npz", or ".npy" file!')
		elif ext == '.mat':
			return matlab_loader(path, dataset_name, variable_name, num_channels, sampling_rate, epoch_length).create_Prainsa()
		else:
			return numpy_loader(path, dataset_name, variable_name, num_channels, sampling_rate, epoch_length).create_Prainsa()
	
	else:
		raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), '{}'.format(path))
