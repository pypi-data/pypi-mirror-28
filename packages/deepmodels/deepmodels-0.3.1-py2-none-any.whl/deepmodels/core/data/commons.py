"""Definition of dataset class.
"""

import abc
import json


class InfoKeyBase(object):
  """Data info key name.
  """
  NAME = "name"
  SAVE_DIR = "save_dir"
  ENGINE = "engine"
  IMG_FORMAT = "img_format"
  # metadata file for dataset.
  TRAIN_META_FN = "train_meta_fn"
  TEST_META_FN = "test_meta_fn"
  # actual data file for dataset.
  # type varies depend on library.
  TRAIN_DATA_FN = "train_data_fn"
  TEST_DATA_FN = "test_data_fn"
  LABELS = "labels"
  TRAIN_SAMPLE_COUNT = "train_sample_count"
  TEST_SAMPLE_COUNT = "test_sample_count"
  # dict name mapping name to id.
  LABEL_NAME_TO_ID = "nametoid"
  # dict name mapping id to name.
  LABEL_ID_TO_NAME = "idtoname"


class BoundingBox(object):
  """Class for bounding box in detection.
  """
  box_xmin = 0
  box_ymin = 0
  box_width = 0
  box_height = 0
  img_width = 0
  img_height = 0

  def __init__(self, xmin, ymin, width, height):
    self.box_xmin = xmin
    self.box_ymin = ymin
    self.box_width = width
    self.box_height = height

  def get_box_tuple(self):
    return (self.box_xmin, self.box_ymin, self.box_width, self.box_height)


class DataInfoBase(object):
  """Base class for dataset information.
  """
  __metaclass__ = abc.ABCMeta

  # path to the file with metadata regarding the dataset, e.g. class labels, data file path.
  _info_fn = ""
  # object of dataset info.
  _ds_info = None

  def __init__(self, info_fn=None):
    self._info_fn = info_fn

  def save_info(self):
    """Save dataset info to a file
    """
    with open(self._info_fn, "w") as f:
      json.dump(self._ds_info, f)
    print "dataset info saved to file {}".format(self._info_fn)

  def load_info(self):
    """Load dataset info from a file.
    """
    with open(self._info_fn, "r") as f:
      self._ds_info = json.load(f)
    print "[DataInfoBase] dataset info loaded from file {}".format(
        self._info_fn)

  def get_value(self, key_name):
    """Retrieve info value from structure.
    """
    if key_name in [
        InfoKeyBase.NAME, InfoKeyBase.ENGINE, InfoKeyBase.IMG_FORMAT,
        InfoKeyBase.SAVE_DIR, InfoKeyBase.LABELS, InfoKeyBase.TRAIN_META_FN,
        InfoKeyBase.TEST_META_FN, InfoKeyBase.TRAIN_DATA_FN,
        InfoKeyBase.TEST_DATA_FN, InfoKeyBase.TRAIN_SAMPLE_COUNT,
        InfoKeyBase.TEST_SAMPLE_COUNT
    ]:
      return self._ds_info[key_name]

  def set_value(self, key_name, val):
    """Set data info value.
    """
    if key_name in [
        InfoKeyBase.NAME, InfoKeyBase.ENGINE, InfoKeyBase.IMG_FORMAT,
        InfoKeyBase.SAVE_DIR, InfoKeyBase.LABELS, InfoKeyBase.TRAIN_META_FN,
        InfoKeyBase.TEST_META_FN, InfoKeyBase.TRAIN_DATA_FN,
        InfoKeyBase.TEST_DATA_FN, InfoKeyBase.TRAIN_SAMPLE_COUNT,
        InfoKeyBase.TEST_SAMPLE_COUNT
    ]:
      self._ds_info[key_name] = val

  def get_label_name(self, label_id):
    label_id = str(label_id)
    return self.get_value(InfoKeyBase.LABEL_ID_TO_NAME)[label_id]

  def get_label_id(self, label_name):
    return self.get_value(InfoKeyBase.LABEL_NAME_TO_ID)[label_name]


class DatasetBase(object):
  """Base class representing a generic dataset.
  """
  __metaclass__ = abc.ABCMeta

  def download(self):
    """Download data to local storage.
    """
    pass

  # @abc.abstractmethod
  def create_base_data(self):
    """Create a basic structure of the data to work with.

    Examples like loading image data and labels to array
    before specific format for later use.
    For internal use.
    """
    pass
