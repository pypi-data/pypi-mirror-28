from time import time
from os.path import isfile as file_exist

import numpy as np

from ..prainsa import Prainsa
from ..utilities import fancy_print, printList

class prainsa_loader(object):
	def __init__(self, dir_path, mapping=None):
		self.path = dir_path
		self.mapping = 'r+' if mapping else None
		self.name = None
		self.dataset = None
		self.sampling_rate = None
		self.num_channels = None
		self.epoch_length = None
		self.loading_time = 0
		self.load_metadata()
		self.load_dataset()
		self.prainsa_object = Prainsa(self.dataset, self.name, self.sampling_rate, self.num_channels, self.epoch_length)
		self.load_bands()
		self.load_xcorr()
		self.load_lags()
		self.minutes = int(self.loading_time / 60)
		self.seconds = int(self.loading_time % 60)
		self.ms = int(self.loading_time * 1000 % 1000)
		fancy_print('Finished loading a Prainsa object.\nLoading time: {} minute(s), {} second(s), and {} millisecond(s)'.format(self.minutes, self.seconds, self.ms))

	def load_metadata(self):
		start = time()
		if not file_exist('{}/metadata.dat'.format(self.path)):
			raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), '{}/metadata.dat'.format(self.path))
		with open('{}/metadata.dat'.format(self.path),'r') as metadata:
			for line in metadata:
				parameter, value = line.split('=')
				if parameter == 'name':
					self.__dict__[parameter] = value[:-1]
				else:
					self.__dict__[parameter] = int(value)
		end = time()
		self.loading_time += end - start

	def load_dataset(self):
		start = time()
		if not file_exist('{}/dataset.npz'.format(self.path)):
			raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), '{}/dataset.npz'.format(self.path))
		self.dataset = np.load('{}/dataset.npz'.format(self.path), mmap_mode=self.mapping)
		self.dataset = self.dataset['dataset']
		end = time()
		self.loading_time += end - start

	def load_bands(self):
		start = time()
		if file_exist('{}/bands.npz'.format(self.path)):
			bands_dict = np.load('{}/bands.npz'.format(self.path), mmap_mode=self.mapping)
			available_keys = [k for k in bands_dict.keys() if k in ['delta','theta','alpha','beta','gamma']]
			for key in available_keys:
				self.prainsa_object.__dict__[key] = bands_dict[key]
		end = time()
		self.loading_time += end - start

	def load_xcorr(self):
		start = time()
		if file_exist('{}/xcorr.npz'.format(self.path)):
			xcorr_dict = np.load('{}/xcorr.npz'.format(self.path), mmap_mode=self.mapping)
			for key in [k for k in xcorr_dict.keys()]:
				self.prainsa_object.xcorr_dict[key] = xcorr_dict[key]
		end = time()
		self.loading_time += end - start

	def load_lags(self):
		start = time()
		if file_exist('{}/lags.npz'.format(self.path)):
			lags_dict = np.load('{}/lags.npz'.format(self.path), mmap_mode=self.mapping)
			for key in [k for k in lags_dict.keys()]:
				self.prainsa_object.lags_dict[key] = lags_dict[key]
		end = time()
		self.loading_time += end - start

	def create_Prainsa(self):
		return self.prainsa_object
