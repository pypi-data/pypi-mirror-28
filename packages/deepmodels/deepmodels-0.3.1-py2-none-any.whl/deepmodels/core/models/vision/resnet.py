"""DeepModels definition of ResNet.
"""

import abc

from deepmodels.core import commons
from deepmodels.core.models import commons as model_common


class DMResNet(model_common.DMModel):
  """Interface for ResNet model family.
  """
  resnet50_params = commons.ModelParams(
      model_name=commons.ModelType.model_names[commons.ModelType.RESNET_50],
      model_type=commons.ModelType.RESNET_50,
      input_img_width=224,
      input_img_height=224,
      cls_num=1000)
  # not supported now.
  resnet101_params = commons.ModelParams(
      model_name=commons.ModelType.model_names[commons.ModelType.RESNET_101],
      model_type=commons.ModelType.RESNET_101,
      input_img_width=224,
      input_img_height=224,
      cls_num=1000)

  @abc.abstractmethod
  def __init__(self, model_type=commons.ModelType.RESNET_50):
    assert model_type == commons.ModelType.RESNET_50
    self.model_params = self.resnet50_params

  def get_input_shape(self):
    return (None, self.model_params.input_img_height,
            self.model_params.input_img_width, 3)
