from os.path import isfile as file_exist
from os.path import basename
from time import time

import numpy as np

from ..prainsa import Prainsa
from ..utilities import fancy_print, printList, array_reshape_by_column

class numpy_loader(object):
	def __init__(self, path, dataset_name=None, variable_name=None, num_channels=None, sampling_rate=None, epoch_length=1):
		self.path = path
		self.name = dataset_name
		self.variable_name = variable_name
		self.channels = num_channels
		self.dataset = None
		self.numpy_object = None
		self.sampling_rate = sampling_rate
		self.epoch_length = epoch_length
		self.loading_time = 0
		self.check_path()
		self.load_numpy_object()
		self.get_dataset()
		self.check_dimensions()
		self.check_sampling_rate()
		self.generate_dataset_name()
		self.minutes = int(self.loading_time / 60)
		self.seconds = int(self.loading_time % 60)
		self.ms = int(self.loading_time * 1000 % 1000)
		fancy_print('Finished loading a matlab file.\nLoading time: {} minute(s), {} second(s), and {} millisecond(s)'.format(self.minutes, self.seconds, self.ms))

	def check_path(self):
		if not file_exist(self.path):
			raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), self.path)

	def create_Prainsa(self):
		return Prainsa(self.dataset, self.name, self.sampling_rate, self.channels, self.epoch_length)

	def load_numpy_object(self):
		start = time()
		if self.path.split('.')[-1] == 'npz':
			self.numpy_object = np.load(self.path)
		elif self.path.split('.')[-1] == 'npy':
			pass
		else:
			raise Exception('Unrecognized file type. Must be "npy" or "npz" !')
		end = time()
		self.loading_time += end - start

	def get_dataset(self):
		start = time()
		if self.numpy_object == None:
			self.dataset = np.load(self.path)
			end = time()
			self.loading_time += end - start
		else:
			start = time()
			variables_list = [key for key in self.numpy_object.keys()]
			if self.variable_name in variables_list:
				self.dataset = self.numpy_object[self.variable_name]
				end = time()
				self.loading_time += end - start
			else:
				if not self.variable_name is None:
					fancy_print('The variable name \"{}\" does not exist in the npz file.'.format(self.variable_name))
				if len(variables_list) < 1:
					raise KeyError(errno.ENOKEY, os.strerror(errno.ENOKEY), 'there are no variables in the npz file!')
				ans = 0
				while ans < 1 or ans > len(variables_list):
					fancy_print('The variables available in this dataset are:')
					printList(variables_list)
					fancy_print('Please enter the number that corresponds to the variable name:')
					ans = int(input())
				self.variable_name = variables_list[ans-1]
				self.dataset = np.array(self.matlab_object[self.variable_name], dtype=np.float32)
				end = time()
				self.loading_time += end - start
		
	def check_dimensions(self):	
		if not self.channels in self.dataset.shape:
			if not self.channels is None:
				fancy_print('The number of channels, {}, provided is not one of the dataset\'s dimensions'.format(self.channels))
			ans = 0
			while ans < 1 or ans > len(self.dataset.shape):
				fancy_print('The dimensions of this dataset are:')
				printList(self.dataset.shape)
				fancy_print('Please enter the number that corresponds to the number of channels:')
				ans = int(input())
			self.channels = self.dataset.shape[ans - 1]
		channels_index = self.dataset.shape.index(self.channels)
		if channels_index == 1 and len(self.dataset.shape) == 2:
			pass
		else:
			start = time()
			reshaped_dataset = array_reshape_by_column(self.dataset, channels_index)
			if self.dataset.shape[channels_index] != reshaped_dataset.shape[1]:
				self.dataset = array_reshape_by_column(reshaped_dataset, 1)
			else:
				self.dataset = reshaped_dataset
			end = time()
			self.loading_time += end - start

	def check_sampling_rate(self):
		if (self.sampling_rate is None) or (self.dataset.shape[0] % self.sampling_rate != 0):
			self.sampling_rate = float('nan')
			while self.dataset.shape[0] % self.sampling_rate != 0:
				fancy_print('[Warning] the number of observations in the dataset is not a multiple of the sampling rate.')
				fancy_print('Please specify the sampling rate: ')
				self.sampling_rate = int(input())

	def generate_dataset_name(self):
		if self.name is None:
			self.name = basename(self.path).split('.')[0]
			self.name = '{}_{}_{}spe_{}ch_{}Hz'.format(self.name, self.variable_name, self.epoch_length, self.channels, self.sampling_rate)