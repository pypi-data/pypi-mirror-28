"""Class interface for image generation dataset.
"""

import abc
import csv
import glob
import json
import os

from deepmodels.core import commons, tools
from deepmodels.core.data.commons import DatasetBase, DataInfoBase


class InfoKey(object):
  """Dataset info key name.
  """
  NAME = "name"
  SAVE_DIR = "save_dir"
  ENGINE = "engine"
  TRAIN_META_FN = "train_meta_fn"
  TRAIN_DATA_FN = "train_data_fn"
  TRAIN_SAMPLE_COUNT = "train_sample_count"


class ImgGenDataInfo(DataInfoBase):
  """Info class for image generation dataset.
  """

  def __init__(self, ds_name, save_dir):
    self._ds_info = {
        InfoKey.NAME: ds_name,
        InfoKey.SAVE_DIR: save_dir,
        InfoKey.ENGINE: None,
        InfoKey.TRAIN_META_FN: "",
        InfoKey.TRAIN_DATA_FN: "",
        InfoKey.TRAIN_SAMPLE_COUNT: 0
    }
    assert ds_name is not None and save_dir is not None
    info_fn = os.path.join(save_dir, "{}__info.json".format(ds_name))
    super(ImgGenDataInfo, self).__init__(info_fn)
    if os.path.exists(info_fn):
      self.load_info()

  def get_value(self, key_name):
    """Retrieve value of a key.
    """
    return self._ds_info[key_name]

  def set_value(self, key_name, val):
    """Set a key value.
    """
    self._ds_info[key_name] = val


class ImgGenDataset(DatasetBase):
  """Class for image generation dataset.
  """
  ds_info = None

  def __init__(self, ds_name=None, save_dir=None, ds_info_=None):
    if ds_info_ == None:
      assert ds_name is not None and save_dir is not None
      self.ds_info = ImgGenDataInfo(ds_name, save_dir)
    else:
      self.ds_info = ds_info_

  def gen_metadata_from_folder(self,
                               img_dir,
                               match_patterns,
                               save_fn_prefix,
                               overwrite=True):
    """Generate csv files for training and testing.

    Due to the unsupervised nature, currently only image info is saved.

    Returns:
      metadata file name.
    """
    all_data = [("img_fn")]
    # get all image files.
    for fn_pattern in match_patterns:
      cur_img_fns = glob.glob(os.path.join(img_dir, fn_pattern))
      all_data.extend(zip(cur_img_fns))
    meta_fn = save_fn_prefix + ".csv"
    if overwrite or not os.path.exists(meta_fn):
      with open(meta_fn, "w") as f:
        writer = csv.writer(f)
        writer.writerows(all_data)
        print("all metadata has been written to file: {}".format(meta_fn))
    self.ds_info.set_value(InfoKey.TRAIN_META_FN, meta_fn)
    self.ds_info.save_info()
    return meta_fn

  @abc.abstractmethod
  def build_from_metadata(self,
                          meta_fn,
                          data_type,
                          save_fn_prefix,
                          target_img_shape=(256, 256, 3),
                          overwrite=True):
    """Convert metadata to compact data format.
    """
    pass

  @abc.abstractmethod
  def build_from_folder(self,
                        data_folder,
                        match_patterns=["*.jpg", "*.png"],
                        target_img_shape=(256, 256, 3),
                        overwrite=True):
    """Create data from folder of images.
    """
    pass

  @abc.abstractmethod
  def gen_batch_data(self,
                     data_type=commons.DataType.TRAIN,
                     batch_size=32,
                     target_img_height=128,
                     target_img_width=128,
                     preprocess_fn=None):
    pass


if __name__ == "__main__":
  pass
  # testing code.
  dm_data = ImgGenDataset("test_gen_data", "tmp/")
  dm_data.gen_metadata_from_folder(
      "/media/jiefeng/DataHouse/Recognition/flower/flower_photos/daisy/",
      "tmp/gen_meta")
