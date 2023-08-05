"""Keras implementation of image generation dataset.
"""

import csv
import h5py
import math
import os
import random
import sys
import time

from tqdm import tqdm
import numpy as np

import cv2

from deepmodels.core import commons, tools
from deepmodels.core.data.vision.img_gen_data import InfoKey, ImgGenDataset


class ImgGenDatasetKeras(ImgGenDataset):
  """Keras implementation.
  """

  def __init__(self, ds_name=None, save_dir=None, ds_info=None):
    super(ImgGenDatasetKeras, self).__init__(ds_name, save_dir, ds_info)
    self.ds_info.set_value(InfoKey.ENGINE, "keras")

  def build_from_metadata(self,
                          meta_fn,
                          data_type,
                          save_fn_prefix,
                          target_img_shape=(256, 256, 3),
                          overwrite=True):
    """Convert dataset meta file to data file.
    """
    # set data filenames.
    assert data_type in [commons.DataType.TRAIN, commons.DataType.TEST]
    data_fn = tools.gen_data_filename(save_fn_prefix,
                                      commons.DataFileType.HDF5, data_type)
    if data_type == commons.DataType.TRAIN:
      self.ds_info.set_value(InfoKey.TRAIN_DATA_FN, data_fn)
    else:
      self.ds_info.set_value(InfoKey.TEST_DATA_FN, data_fn)
    if overwrite or not os.path.exists(data_fn):
      print("converting {}".format(meta_fn))
      img_fns = []
      # read all metadata.
      with open(meta_fn, "r") as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
          assert len(row) >= 1
          img_fns.append(row[0])
      # read image and convert to file.
      if os.path.exists(data_fn):
        os.remove(data_fn)
      with h5py.File(data_fn) as f:
        img_dset = f.create_dataset(
            "images",
            shape=(0, ) + target_img_shape,
            dtype=np.uint8,
            maxshape=(None, ) + target_img_shape)
        for img_id, img_fn in enumerate(tqdm(img_fns)):
          img_data = tools.read_img_data(
              img_fn, target_img_shape, use_arr=True)
          if img_data is not None:
            if len(img_data.shape) == 2:
              img_data = np.expand_dims(img_data, axis=2)
            img_dset.resize(img_dset.len() + 1, axis=0)
            img_dset[-1] = img_data
        print("metadata {} has been converted to data file: {}".format(
            meta_fn, data_fn))
        if data_type == commons.DataType.TRAIN:
          self.ds_info.set_value(InfoKey.TRAIN_SAMPLE_COUNT, img_dset.len())
        else:
          self.ds_info.set_value(InfoKey.TEST_SAMPLE_COUNT, img_dset.len())
        self.ds_info.save_info()

  def build_from_folder(self,
                        data_folder,
                        match_patterns=["*.jpg", "*.png"],
                        target_img_shape=(256, 256, 3),
                        overwrite=True):
    # create metadata.
    meta_prefix = os.path.join(data_folder,
                               self.ds_info.get_value(InfoKey.NAME))
    meta_fn = self.gen_metadata_from_folder(data_folder, match_patterns,
                                            meta_prefix)
    self.ds_info.set_value(InfoKey.TRAIN_META_FN, meta_fn)
    # convert to hdf5.
    self.build_from_metadata(
        self.ds_info.get_value(InfoKey.TRAIN_META_FN), commons.DataType.TRAIN,
        meta_prefix, target_img_shape, overwrite)

  def gen_batch_data(self,
                     data_type=commons.DataType.TRAIN,
                     batch_size=32,
                     target_img_height=128,
                     target_img_width=128,
                     preprocess_fn=None):
    """Create batch image generator for keras model.
    """
    # init random.
    random.seed(time.time())
    data_fn = None
    samp_count = 0
    if data_type == commons.DataType.TRAIN:
      data_fn = self.ds_info.get_value(InfoKey.TRAIN_DATA_FN)
      samp_count = self.ds_info.get_value(InfoKey.TRAIN_SAMPLE_COUNT)
    print("reading from data file: {}".format(data_fn))
    print("sample count: {}".format(samp_count))
    while True:
      assert os.path.exists(data_fn), "{} not exist".format(data_fn)
      print("start fetching data for new epoch...")
      with h5py.File(data_fn, "r") as f:
        img_dset = f["images"]
        samp_ids = range(samp_count)
        random.shuffle(samp_ids)
        num_batches = int(math.ceil(len(samp_ids) * 1.0 / batch_size))
        print("number of batches: {}".format(num_batches))
        for idx in xrange(num_batches):
          startt = time.time()
          if idx == num_batches - 1:
            batch_indice = samp_ids[idx * batch_size:]
          else:
            batch_indice = samp_ids[idx * batch_size:idx * batch_size +
                                    batch_size]
          batch_indice = sorted(batch_indice)
          img_batch = img_dset[batch_indice]
          # resizing.
          if img_batch.shape[1] != target_img_height or img_batch.shape[
              2] != target_img_width:
            new_batch = np.zeros((img_batch.shape[0], target_img_height,
                                  target_img_width, img_batch.shape[3]))
            for img_id, img_arr in enumerate(img_batch):
              new_arr = cv2.resize(img_arr,
                                   (target_img_width, target_img_height))
              new_batch[img_id] = new_arr
            img_batch = new_batch
          # preprocessing.
          if preprocess_fn is not None:
            new_batch = np.zeros(img_batch.shape)
            for img_id, img_arr in enumerate(img_batch):
              new_arr = preprocess_fn(img_arr)
              new_batch[img_id] = new_arr
            img_batch = new_batch
          # convert type.
          img_batch = img_batch.astype(np.float32)
          yield img_batch
