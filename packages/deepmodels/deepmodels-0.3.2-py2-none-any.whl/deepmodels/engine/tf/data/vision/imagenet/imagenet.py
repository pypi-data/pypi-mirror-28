"""ImageNet dataset.
"""

import json
import os

from deepmodels.core.data.vision.img_clf_data import InfoKey, ImgClfDataInfo
from deepmodels.engine.tf.data.vision.img_clf_data import ImgClfDatasetTF


class ImageNetInfoTFVGG(ImgClfDataInfo):
  def load_info(self):
    label_fn = os.path.join(os.path.dirname(__file__), "vgg_16_labels.txt")
    with open(label_fn, "r") as f:
      label_str = f.read()
      label_name_dict = eval(label_str)
    self.set_value(InfoKey.LABEL_ID_TO_NAME, label_name_dict)


class ImageNetTFVGG(ImgClfDatasetTF):
  """ImageNet for tf using vgg compatible labels.
  """
  def __init__(self, ds_name=None, save_dir=None, ds_info=None):
    data_info = ImageNetInfoTFVGG()
    super(ImageNetTFVGG, self).__init__(ds_info=data_info)