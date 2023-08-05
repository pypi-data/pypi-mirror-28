"""Keras compatible image classification dataset.
"""

import csv
import h5py
import math
import os
import random
import time
import PIL.Image

import cv2

import numpy as np
from tqdm import tqdm

from keras.utils import to_categorical

from deepmodels.core import commons, tools
from deepmodels.core.data.vision.img_clf_data import InfoKey, ImgClfDataset


class ImgClfDatasetKeras(ImgClfDataset):
  """Keras implementation of image classification dataset.
  """

  def __init__(self, ds_name=None, save_dir=None, ds_info=None):
    """Init for keras dataset.
    """
    super(ImgClfDatasetKeras, self).__init__(ds_name, save_dir, ds_info)
    self.ds_info.set_value(InfoKey.ENGINE, "keras")

  def build_from_metadata_single_label(self, meta_fn, data_type,
                                       save_fn_prefix):
    """Build single label data.
    """
    # set data filenames.
    assert data_type in [commons.DataType.TRAIN, commons.DataType.TEST]
    data_fn = tools.gen_data_filename(save_fn_prefix,
                                      commons.DataFileType.HDF5, data_type)
    if data_type == commons.DataType.TRAIN:
      self.ds_info.set_value(InfoKey.TRAIN_DATA_FN, data_fn)
    else:
      self.ds_info.set_value(InfoKey.TEST_DATA_FN, data_fn)
    if not os.path.exists(data_fn):
      # convert metadata to data file.
      # read all metadata.
      label_names = {}
      label_ids = {}
      img_fns = []
      labels = []
      print("converting {}".format(meta_fn))
      with open(meta_fn, "r") as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
          assert len(row) == 2
          img_fns.append(row[0])
          if row[1] not in label_ids:
            cur_label_id = len(label_ids)
            label_ids[row[1]] = cur_label_id
            label_names[cur_label_id] = row[1]
          labels.append(label_ids[row[1]])
      self.ds_info.set_value(InfoKey.LABEL_ID_TO_NAME, label_names)
      self.ds_info.set_value(InfoKey.LABEL_NAME_TO_ID, label_ids)
      # read image and convert to file.
      with h5py.File(data_fn) as f:
        img_dset = f.create_dataset(
            "images",
            shape=(0, 256, 256, 3),
            dtype=np.uint8,
            maxshape=(None, 256, 256, 3))
        label_dset = f.create_dataset(
            "labels", shape=(0, ), dtype=np.int16, maxshape=(None, ))
        for img_id, img_fn in enumerate(tqdm(img_fns)):
          img_data = tools.read_img_data(img_fn, use_arr=True)
          if img_data is not None:
            # make (height, weight, channel)
            img_data = np.swapaxes(img_data, 0, 1)
            img_dset.resize(img_dset.len() + 1, axis=0)
            img_dset[-1] = img_data
            label_dset.resize(label_dset.len() + 1, axis=0)
            label_dset[-1] = labels[img_id]
        print("metadata {} has been converted to data file: {}".format(
            meta_fn, data_fn))
        if data_type == commons.DataType.TRAIN:
          self.ds_info.set_value(InfoKey.TRAIN_SAMPLE_COUNT, img_dset.len())
        else:
          self.ds_info.set_value(InfoKey.TEST_SAMPLE_COUNT, img_dset.len())
        self.ds_info.save_info()

  def build_from_metadata_multi_label(self, meta_fn, data_type,
                                      save_fn_prefix):
    """Build multi-label data.

    Format: img_fn, label_val1, label_val2, ...
    """
    # set data filenames.
    assert data_type in [commons.DataType.TRAIN, commons.DataType.TEST]
    data_fn = tools.gen_data_filename(save_fn_prefix,
                                      commons.DataFileType.HDF5, data_type)
    if data_type == commons.DataType.TRAIN:
      self.ds_info.set_value(InfoKey.TRAIN_DATA_FN, data_fn)
    else:
      self.ds_info.set_value(InfoKey.TEST_DATA_FN, data_fn)
    if not os.path.exists(data_fn):
      # read all metadata.
      label_names = {}
      label_ids = {}
      img_fns = []
      labels = []  # two dimension list.
      print("converting {}".format(meta_fn))
      with open(meta_fn, "r") as f:
        reader = csv.reader(f)
        # ignore title.
        next(reader)
        for row in reader:
          labels.append([])
          img_fns.append(row[0])
          for cur_label_name in row[1:]:
            if cur_label_name not in label_ids:
              cur_label_id = len(label_ids)
              label_ids[cur_label_name] = cur_label_id
              label_names[cur_label_id] = cur_label_name
            labels[-1].append(cur_label_id)
      self.ds_info.set_value(InfoKey.LABEL_ID_TO_NAME, label_names)
      self.ds_info.set_value(InfoKey.LABEL_NAME_TO_ID, label_ids)
      # read image and convert to file.
      with h5py.File(data_fn) as f:
        # create dataset.
        img_dset = f.create_dataset(
            "images",
            shape=(0, 256, 256, 3),
            dtype=np.uint8,
            maxshape=(None, 256, 256, 3))
        # binary matrix, each label id will be set to 1.
        label_dset = f.create_dataset(
            "labels",
            shape=(0, len(label_ids)),
            dtype=np.uint8,
            maxshape=(None, len(label_ids)))
        # fill datasets.
        for img_id, img_fn in enumerate(tqdm(img_fns)):
          img_data = tools.read_img_data(img_fn, use_arr=True)
          if img_data is not None:
            # make (height, weight, channel)
            img_data = np.swapaxes(img_data, 0, 1)
            img_dset.resize(img_dset.len() + 1, axis=0)
            img_dset[-1] = img_data
            # form label vector.
            label_dset.resize(label_dset.len() + 1, axis=0)
            cur_label_vec = np.zeros(len(label_ids), dtype=np.uint8)
            for cur_sublabel in labels[img_id]:
              cur_label_vec[cur_sublabel] = 1
            label_dset[-1] = cur_label_vec
        print("metadata {} has been converted to data file: {}".format(
            meta_fn, data_fn))
        if data_type == commons.DataType.TRAIN:
          self.ds_info.set_value(InfoKey.TRAIN_SAMPLE_COUNT, img_dset.len())
        else:
          self.ds_info.set_value(InfoKey.TEST_SAMPLE_COUNT, img_dset.len())
        self.ds_info.save_info()

  def build_from_metadata(self, meta_fn, data_type, save_fn_prefix):
    """Convert dataset meta file to data file.
    """
    if self.is_multi_label():
      self.build_from_metadata_multi_label(meta_fn, data_type, save_fn_prefix)
    else:
      self.build_from_metadata_single_label(meta_fn, data_type, save_fn_prefix)

  def build_from_folder(self, data_folder, train_ratio=0.8):
    assert not self.is_multi_label(
    ), "build from folder only supports single label."
    # create metadata.
    meta_prefix = os.path.join(self.ds_info.data_save_dir,
                               self.ds_info.get_value(InfoKey.NAME))
    vals = self.gen_metadata_from_folder(
        data_folder, meta_prefix, train_ratio=train_ratio)
    self.ds_info.set_value(InfoKey.TRAIN_META_FN, vals[0])
    self.ds_info.set_value(InfoKey.TEST_META_FN, vals[1])
    self.ds_info.set_value(InfoKey.LABEL_ID_TO_NAME, vals[2])
    self.ds_info.set_value(InfoKey.LABEL_NAME_TO_ID, vals[3])
    # convert to hdf5.
    self.build_from_metadata(
        self.ds_info.get_value(InfoKey.TRAIN_META_FN), commons.DataType.TRAIN,
        meta_prefix)
    self.build_from_metadata(
        self.ds_info.get_value(InfoKey.TEST_META_FN), commons.DataType.TEST,
        meta_prefix)

  def gen_batch_data(self,
                     data_type=commons.DataType.TRAIN,
                     batch_size=32,
                     target_img_height=128,
                     target_img_width=128,
                     preprocess_fn=None):
    """Create batch image generator for keras model.

    Used as a data generator.

    Returns:
      a batch data generator.
    """
    # init random.
    random.seed(time.time())
    data_fn = None
    samp_count = 0
    if data_type == commons.DataType.TRAIN:
      data_fn = self.ds_info.get_value(InfoKey.TRAIN_DATA_FN)
      samp_count = self.ds_info.get_value(InfoKey.TRAIN_SAMPLE_COUNT)
    else:
      data_fn = self.ds_info.get_value(InfoKey.TEST_DATA_FN)
      samp_count = self.ds_info.get_value(InfoKey.TEST_SAMPLE_COUNT)
    print "\nreading from data file: {}".format(data_fn)
    print "sample count: {}".format(samp_count)
    while True:
      assert os.path.exists(data_fn)
      print("\nstart data file for new epoch...")
      with h5py.File(data_fn, "r") as f:
        img_dset = f["images"]
        label_dset = f["labels"]
        samp_ids = range(samp_count)
        random.shuffle(samp_ids)
        num_batches = int(math.ceil(samp_count * 1.0 / batch_size))
        print "number of batches: {}".format(num_batches)
        for idx in xrange(num_batches):
          startt = time.time()
          # select current batch.
          if idx == num_batches - 1:
            batch_indice = samp_ids[idx * batch_size:]
          else:
            batch_indice = samp_ids[idx * batch_size:idx * batch_size +
                                    batch_size]
          batch_indice = sorted(batch_indice)
          img_batch = img_dset[batch_indice]
          label_batch = label_dset[batch_indice]
          # preprocessing.
          if preprocess_fn is not None:
            new_batch = []
            for img_id, img_arr in enumerate(img_batch):
              new_arr = preprocess_fn(img_arr)
              new_batch.append(new_arr)
            img_batch = np.array(new_batch)
          # convert type.
          img_batch = img_batch.astype(np.float32)
          if not self.is_multi_label():
            label_batch = to_categorical(
                label_batch,
                len(self.ds_info.get_value(InfoKey.LABEL_NAME_TO_ID)))
          # print "label batch shape: {}".format(label_batch.shape)
          yield (img_batch, label_batch)
