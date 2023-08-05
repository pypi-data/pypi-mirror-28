"""Tools for tensorflow deepmodels.
"""

import numpy as np
import tensorflow as tf

from deepmodels.core.commons import DataType, DataFileType


def conv_feat_map_tensor_max(conv_fmap_tensor):
  """Compute maximum activation of conv feature maps.
  """
  tf.assert_equal(tf.rank(conv_fmap_tensor), 4)
  new_conv_tensor = tf.reduce_max(conv_fmap_tensor, axis=3)
  return new_conv_tensor


def conv_feat_map_tensor_avg(conv_fmap_tensor):
  """Compute average activation of conv feature maps.
  """
  tf.assert_equal(tf.rank(conv_fmap_tensor), 4)
  new_conv_tensor = tf.reduce_mean(conv_fmap_tensor, axis=3)
  return new_conv_tensor


def conv_feat_map_sum(conv_fmap_tensor):
  """Compute maximum activation of conv feature maps.
  """
  tf.assert_equal(tf.rank(conv_fmap_tensor), 4)
  new_conv_tensor = tf.reduce_sum(conv_fmap_tensor, axis=3)
  return new_conv_tensor


def conv_feat_map_tensor_gram(conv_fmap_tensor):
  """Compute Gram matrix of conv feature maps.

  Used in style transfer.
  """
  tf.assert_equal(tf.rank(conv_fmap_tensor), 4)
  shape = tf.shape(conv_fmap_tensor)
  num_images = shape[0]
  width = shape[1]
  height = shape[2]
  num_filters = shape[3]
  filters = tf.reshape(conv_fmap_tensor,
                       tf.stack([num_images, -1, num_filters]))
  grams = tf.matmul(
      filters, filters,
      transpose_a=True) / tf.to_float(width * height * num_filters)
  return grams


def conv_feat_map_arr_gram(conv_fmap_arr):
  """Numpy version.
  """
  assert conv_fmap_arr.ndim == 4, "conv feature map must have dim 4"
  shape = conv_fmap_arr.shape
  num_images = shape[0]
  width = shape[1]
  height = shape[2]
  num_filters = shape[3]
  filters = np.reshape(conv_fmap_arr, [num_images, -1, num_filters])
  grams = np.matmul(np.swapaxes(filters, 1, 2), filters) / (width * height *
                                                            num_filters)
  return grams


def conv_feat_map_arr_mean_var(conv_fmap_arr):
  """Compute spatial mean and variance for input feature maps.
  """
  assert conv_fmap_arr.ndim == 4, "conv feature map must have dim 4"
  shape = conv_fmap_arr.shape
  num_images = shape[0]
  width = shape[1]
  height = shape[2]
  num_filters = shape[3]
  filters = np.reshape(conv_fmap_arr, [num_images, -1, num_filters])
  layer_means = np.mean(filters, axis=1)
  layer_vars = np.var(filters, axis=1)
  return layer_means, layer_vars
