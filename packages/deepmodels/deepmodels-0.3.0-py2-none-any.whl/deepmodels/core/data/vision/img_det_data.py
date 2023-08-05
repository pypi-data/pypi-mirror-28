"""Object detection in image data source.
"""

import abc
import csv

from deepmodels.core.data.commons import InfoKeyBase, DataInfoBase, DatasetBase


class InfoKey(InfoKeyBase):
  """Object detection info key.
  """
  BBOX = "bounding_boxes"
  # bounding box cooridnates.
  BBOX_XMIN = "box_xmin"
  BBOX_YMIN = "box_ymin"
  BBOX_WIDTH = "box_width"
  BBOX_HEIGHT = "box_height"


class ImgDetDataInfo(DataInfoBase):
  """Info class for image detection dataset.
  """

  def __init__(self, ds_name, save_dir):
    # basic structure of info.
    self._ds_info = {
        InfoKey.NAME: ds_name,
        InfoKey.SAVE_DIR: save_dir,
        InfoKey.ENGINE: None,
        InfoKey.IMG_FORMAT: "",
        InfoKey.TRAIN_META_FN: "",
        InfoKey.TEST_META_FN: "",
        InfoKey.TRAIN_DATA_FN: "",
        InfoKey.TEST_DATA_FN: "",
        InfoKey.LABELS: {
            InfoKey.LABEL_ID_TO_NAME: {},
            InfoKey.LABEL_NAME_TO_ID: {}
        },
        InfoKey.TRAIN_SAMPLE_COUNT: 0,
        InfoKey.TEST_SAMPLE_COUNT: 0,
        # each box is ((box), label_id)
        InfoKey.BBOX: []
    }
    assert ds_name is not None and save_dir is not None
    info_fn = os.path.join(save_dir, "{}__info.json".format(ds_name))
    super(ImgDetDataInfo, self).__init__(info_fn)
    if os.path.exists(info_fn):
      self.load_info()


class ImgDetDataset(DatasetBase):
  """Image object detection dataset.

  Metadata file format:
  The first row (header) describes the meaning of each column.
  Each row contains: image file path or url, box coordinates, label_name.
  If an image has more than one box annotation, use separate record.
  """
  __metadata__ = abc.ABCMeta

  ds_info = None

  def __init__(self, ds_name=None, save_dir=None, ds_info=None):
    if ds_info is None:
      assert ds_name is not None and save_dir is not None
      self.ds_info = ImgDetDataInfo(ds_name, save_dir)
    else:
      self.ds_info = ds_info

  """ Dataset labels and metadata """

  def get_label_name(self, label_id):
    """Map id to name.
    """
    return self.ds_info.get_label_name(label_id)

  def get_label_id(self, label_name):
    """Map name to id.
    """
    return self.ds_info.get_label_id(label_name)

  """ Build dataset """

  def add_to_metadata(self, meta_fn, records):
    """Add a labeled record to metadata.

    Args:
      records: list of tuples. each tuple is: (img_path, bbox, label_name).
      bbox is (xmin, ymin, width, height).
    """
    new_content = []
    if not os.path.exists(meta_fn):
      new_content.append(
          ("img_path", "xmin", "ymin", "width", "height", "label"))
    with open(meta_fn, "wa") as f:
      writer = csv.writer(f)
      new_content.extend(records)
      writer.writerows(new_content)
      print "{} records written to {}".format(len(records), meta_fn)

  def split_metadata(self, meta_fn, train_ratio=0.7):
    """Split metadata into train and test based on labels.
    """
    pass

  @abc.abstractmethod
  def build_from_metadata(self, meta_fn, data_type, save_fn_prefix):
    pass

  """ Fetch data from dataset """

  @abc.abstractmethod
  def gen_batch_data(self):
    pass
