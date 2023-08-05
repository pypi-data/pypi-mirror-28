"""Inception Resnet models.
"""

import os

from deepmodels.tf.core import commons
from deepmodels.tf.core.dm_models import common as model_common
from deepmodels.shared.tools import data_manager
from deepmodels.tf.models import net_downloader_tf


class InceptionResNetDM(model_common.NetworkDM):
  """Inception resnet model, only v2 now.
  """

  def __init__(self):
    super(InceptionResNetDM, self).__init__(None)
    net_type = commons.ModelType.INCEPTION_RESNET_V2
    self.net_params = commons.ModelParams(
        model_name=commons.ModelType.model_names[net_type],
        model_type=net_type,
        input_img_width=224,
        input_img_height=224,
        cls_num=1001)
    self.net_graph_fn = ""
    self.net_weight_fn = model_common.get_builtin_net_weights_fn(
        self.net_params.model_type)
    if not os.path.exists(self.net_weight_fn):
      net_downloader_tf.download_net(self.net_params.model_type)

  def get_label_names(self):
    proj_dir = data_manager.get_project_dir()
    label_fn = os.path.join(proj_dir, "models/inception/inception_labels.txt")
    label_name_dict = {}
    with open(label_fn, "r") as f:
      label_str = f.read()
      label_name_dict = eval(label_str)
    return label_name_dict
