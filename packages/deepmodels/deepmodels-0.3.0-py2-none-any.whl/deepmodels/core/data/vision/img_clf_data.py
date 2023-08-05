"""Class interface for image classification dataset.

A dataset is usually made of three parts.
1) datainfo: general info about the dataset, saved in json.
2) metadata: a generic format for listing dataset entries in csv.
3) data file: binary data files on disk to store actual data.
"""

import abc
import csv
import json
import math
import os
import random

from deepmodels.core import commons, tools
from deepmodels.core.data.commons import InfoKeyBase, DataInfoBase, DatasetBase


class InfoKey(InfoKeyBase):
  """Data info key name.
  """
  MULTI_LABEL = "multi_label"


class ImgClfDataInfo(DataInfoBase):
  """Info class for image classification dataset.
  """
  data_save_dir = None

  def __init__(self, ds_name, save_dir, multi_label=False):
    # basic structure of info.
    self._ds_info = {
        InfoKey.NAME: ds_name,
        InfoKey.SAVE_DIR: save_dir,
        InfoKey.ENGINE: None,
        InfoKey.IMG_FORMAT: "",
        # if has multiple label type or not.
        InfoKey.MULTI_LABEL: multi_label,
        InfoKey.TRAIN_META_FN: "",
        InfoKey.TEST_META_FN: "",
        InfoKey.TRAIN_DATA_FN: "",
        InfoKey.TEST_DATA_FN: "",
        # when extend to multiple labels, it will be a list.
        InfoKey.LABELS: {
            InfoKey.LABEL_ID_TO_NAME: {},
            InfoKey.LABEL_NAME_TO_ID: {}
        },
        InfoKey.TRAIN_SAMPLE_COUNT: 0,
        InfoKey.TEST_SAMPLE_COUNT: 0
    }
    assert ds_name is not None and save_dir is not None
    self.data_save_dir = save_dir
    info_fn = os.path.join(save_dir, "{}__info.json".format(ds_name))
    super(ImgClfDataInfo, self).__init__(info_fn)
    if os.path.exists(info_fn):
      self.load_info()

  def get_value(self, key_name):
    if key_name in [InfoKey.LABEL_ID_TO_NAME, InfoKey.LABEL_NAME_TO_ID]:
      return self._ds_info[InfoKey.LABELS][key_name]
    return super(ImgClfDataInfo, self).get_value(key_name)

  def set_value(self, key_name, val):
    if key_name in [InfoKey.LABEL_ID_TO_NAME, InfoKey.LABEL_NAME_TO_ID]:
      self._ds_info[InfoKey.LABELS][key_name] = val
    super(ImgClfDataInfo, self).set_value(key_name, val)


class ImgClfDataset(DatasetBase):
  """Image classification dataset.

  Each image can have one or more labels.

  Metadata file format:
  The first row (header) describes the meaning of each column.
  Each row contains: image file path or url, value for each label type in following columns.
  """
  __metadata__ = abc.ABCMeta

  ds_info = None

  def __init__(self, ds_name=None, save_dir=None, ds_info_=None):
    """Initialization.

    Args:
      ds_name: dataset name.
      save_dir: directory to save dataset related data.
      Good for intermediate data.
    """
    if ds_info_ is None:
      assert ds_name is not None and save_dir is not None
      self.ds_info = ImgClfDataInfo(ds_name, save_dir)
    else:
      self.ds_info = ds_info_

  """ Dataset labels and metadata. """

  def get_label_name(self, label_id):
    """Map id to name.
    """
    return self.ds_info.get_label_name(label_id)

  def get_label_id(self, label_name):
    """Map name to id.
    """
    return self.ds_info.get_label_id(label_name)

  def is_multi_label(self):
    return self.ds_info.get_value(InfoKey.MULTI_LABEL)

  """ Build dataset. """

  def gen_metadata_from_folder(self, img_dir, save_fn_prefix, train_ratio=0.8):
    """Generate csv files for training and testing data.

    The images are organized by categories in separate folder.
    Three csv files will be generated: train metadata, test metadata
    and label names.
    Each metadata file has format: <img_path, img_label>.

    Args:
      img_dir: root directory. Each subfolder is a category.
      save_fn_prefix: prefix for saved files. train and test.
      files will have corresponding suffix appended.
      train_ratio: ratio between train and test data.

    Returns:
      train meta fn, test meta fn, label id to name mapper, label name to id mapper.
    """
    assert not self.is_multi_label()
    # list all category directories.
    cat_dirs = os.listdir(img_dir)
    cat_dirs = [os.path.join(img_dir, x) for x in cat_dirs]
    cat_dirs = [x for x in cat_dirs if os.path.isdir(x)]
    img_exts = ["*.png", "*.jpg", "*.bmp", "*.jpeg"]
    all_data = [("img_fn", "category")]
    # generate over all metadata.
    for cat_id, cur_cat_dir in enumerate(cat_dirs):
      cur_cat_name = os.path.basename(cur_cat_dir.strip("/"))
      cur_fns = tools.list_files(cur_cat_dir, img_exts)
      print "{} has image: {}".format(cur_cat_dir, len(cur_fns))
      all_cat_names = [cur_cat_name] * len(cur_fns)
      all_data.extend(zip(cur_fns, all_cat_names))
    meta_fn = save_fn_prefix + "__all.csv"
    target_dir = os.path.dirname(meta_fn)
    if not os.path.exists(target_dir):
      os.makedirs(target_dir)
    with open(meta_fn, "w") as f:
      writer = csv.writer(f)
      writer.writerows(all_data)
      print "all metadata has been written to file: {}".format(meta_fn)
    # split data.
    return self.split_metadata(meta_fn, train_ratio)

  def split_metadata(self, meta_fn, train_ratio=0.7, target_label_col=1):
    """Split metadata into train and test files.

    Returns:
      train meta fn, test meta fn, label id to name mapper, label name to id mapper.
    """
    assert not self.is_multi_label()
    # read metadata.
    cls_ids = {}
    label_names = {}
    label_ids = {}
    train_rows = []
    test_rows = []
    all_rows = []
    col_num = 0
    print "split data from {}".format(meta_fn)
    with open(meta_fn, "r") as f:
      reader = csv.reader(f)
      next(reader)
      cnt = 0
      for row in reader:
        col_num = len(row)
        all_rows.append(row)
        cur_label = row[int(target_label_col)]
        if cur_label not in cls_ids.keys():
          cur_id = len(label_names)
          label_ids[cur_label] = cur_id
          label_names[cur_id] = cur_label
          cls_ids[cur_label] = []
        cls_ids[cur_label].append(cnt)
        cnt += 1
    # shuffle and split.
    for label, ids in cls_ids.iteritems():
      random.shuffle(ids)
      train_sz = int(len(ids) * train_ratio)
      train_ids = ids[:train_sz]
      test_ids = ids[train_sz:]
      train_rows.extend([all_rows[x] for x in train_ids])
      test_rows.extend([all_rows[x] for x in test_ids])
    # save to separate metadata fn.
    # training data.
    meta_prefix = os.path.splitext(meta_fn)[0]
    train_meta_fn = tools.gen_data_filename(
        meta_prefix, commons.DataFileType.METADATA, commons.DataType.TRAIN)
    self.ds_info.set_value(InfoKey.TRAIN_META_FN, train_meta_fn)
    with open(train_meta_fn, "w") as f:
      writer = csv.writer(f)
      writer.writerow(tuple(["header"] * col_num))
      writer.writerows(train_rows)
      print "train metadata has been written to file: {}".format(train_meta_fn)
      self.ds_info.set_value(InfoKey.TRAIN_SAMPLE_COUNT, len(train_rows))
    # testing data.
    test_meta_fn = tools.gen_data_filename(
        meta_prefix, commons.DataFileType.METADATA, commons.DataType.TEST)
    self.ds_info.set_value(InfoKey.TEST_META_FN, test_meta_fn)
    with open(test_meta_fn, "w") as f:
      writer = csv.writer(f)
      writer.writerow(tuple(["header"] * col_num))
      writer.writerows(test_rows)
      print "test metadata has been written to file: {}".format(test_meta_fn)
      self.ds_info.set_value(InfoKey.TEST_SAMPLE_COUNT, len(test_rows))
    self.ds_info.save_info()
    return train_meta_fn, test_meta_fn, label_names, label_ids

  @abc.abstractmethod
  def build_from_metadata(self, meta_fn, data_type, save_fn_prefix):
    """Load dataset from metadata file and convert it to compact data format.

    The data format depends on the library of selection.

    Args:
      meta_fn: metadata file.
      data_type: train or test.
      save_fn_prefix: prefix for saved data file.
    """
    pass

  @abc.abstractmethod
  def build_from_folder(self, data_folder):
    """Create data from a given folder which has a set of category subfolders.
    """
    pass

  """ Fetch data from dataset. """

  @abc.abstractmethod
  def gen_batch_data(self,
                     data_type=commons.DataType.TRAIN,
                     batch_size=32,
                     target_img_height=128,
                     target_img_width=128,
                     preprocess_fn=None):
    """Create batch data for classification use.

    The data is not exposed to external but used in learner.
    """
    pass