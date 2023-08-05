#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `prainsa` package."""


import unittest, os, prainsa

from prainsa import loader


class test_prainsa(unittest.TestCase):
    """Tests for `prainsa` package."""

    def setUp(self):
        """Set up test fixtures, if any."""
        self.mat_v73 = os.path.dirname(os.path.abspath(prainsa.__file__)) + '/data/matlab_array_v73.mat'
        self.mat_v6 = os.path.dirname(os.path.abspath(prainsa.__file__)) + '/data/matlab_array_v6.mat'
        self.numpy_array = os.path.dirname(os.path.abspath(prainsa.__file__)) + '/data/numpy_array.npy'
        self.zipped_numpy_array = os.path.dirname(os.path.abspath(prainsa.__file__)) + '/data/zipped_numpy_array.npz'
        self.prainsa_object = os.path.dirname(os.path.abspath(prainsa.__file__)) + '/data/prainsa_object'

    def tearDown(self):
        """Tear down test fixtures, if any."""
        pass

    def test_loading_v73_mat_file(self):
        loader(self.mat_v73, None, 'example_data', 15, 100, 1)

    def test_loading_v6_mat_file(self):
        loader(self.mat_v6, None, 'example_data', 15, 100, 1)

    def test_loading_numpy_array_file(self):
        loader(self.numpy_array, None, 'example_data', 15, 100, 1)

    def test_loading_zipped_numpy_array_file(self):
        loader(self.zipped_numpy_array, None, 'example_data', 15, 100, 1)

    def test_loading_prainsa_object(self):
        loader(self.prainsa_object)

    def test_confirm_mat_file_numpy_file(self):
        v73 = loader(self.mat_v73, None, 'example_data', 15, 100, 1)
        np_array = loader(self.numpy_array, None, 'example_data', 15, 100, 1)
        assert(sum(sum(v73.dataset == np_array.dataset)) == (15 * 5000))

    def test_confirm_mat_file_zipped_numpy_file(self):
        v73 = loader(self.mat_v73, None, 'example_data', 15, 100, 1)
        zipped_np_array = loader(self.numpy_array, None, 'example_data', 15, 100, 1)
        assert(sum(sum(v73.dataset == zipped_np_array.dataset)) == (15 * 5000))

    def test_confirm_mat_file_prainsa_object(self):
        v73 = loader(self.mat_v73, None, 'example_data', 15, 100, 1)
        prainsa_object = loader(self.prainsa_object)
        assert(sum(sum(v73.dataset == prainsa_object.dataset)) == (15 * 5000))

    def test_confirm_mat_file_older_version(self):
        v73 = loader(self.mat_v73, None, 'example_data', 15, 100, 1)
        v6 = loader(self.mat_v6, None, 'example_data', 15, 100, 1)
        assert(sum(sum(v73.dataset == v6.dataset)) == (15 * 5000))