"""DeepModels version of AlexNet.
"""

from deepmodels.core import commons
from deepmodels.core.models import commons as model_common


class DMAlexNet(model_common.DMModel):
  """DeepModels version of AlexNet.
  """
  v2_params = commons.ModelParams(
      model_name=commons.ModelType.model_names[commons.ModelType.ALEX_V2],
      model_type=commons.ModelType.ALEX_V2,
      input_img_width=224,
      input_img_height=224,
      cls_num=1000)

  def __init__(self):
    super(AlexNetDM, self).__init__(None)
    self.net_params = self.v2_params
    self.net_graph_fn = ""
    self.net_weight_fn = model_common.get_builtin_net_weights_fn(
        self.net_params.model_type)
    if self.download_pretrained_model and not os.path.exists(
        self.net_weight_fn):
      net_downloader_tf.download_net(self.net_params.model_type)

  def get_label_names(self):
    pass
