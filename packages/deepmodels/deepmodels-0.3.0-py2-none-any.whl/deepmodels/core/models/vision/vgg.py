"""DeepModels version of VGG16.
"""

import abc
import os

from deepmodels.core import commons
from deepmodels.core.models import commons as model_common


class DMVGG(model_common.DMModel):
  """Interface for VGG model family.
  """
  # not using now.
  vggm_params = commons.ModelParams(
      model_name=commons.ModelType.model_names[commons.ModelType.VGG_M],
      model_type=commons.ModelType.VGG_M,
      input_img_width=224,
      input_img_height=224,
      cls_num=1000)
  vgg16_params = commons.ModelParams(
      model_name=commons.ModelType.model_names[commons.ModelType.VGG16],
      model_type=commons.ModelType.VGG16,
      input_img_width=224,
      input_img_height=224,
      cls_num=1000)
  vgg19_params = commons.ModelParams(
      model_name=commons.ModelType.model_names[commons.ModelType.VGG19],
      model_type=commons.ModelType.VGG19,
      input_img_width=224,
      input_img_height=224,
      cls_num=1000)

  @abc.abstractmethod
  def __init__(self, model_type=commons.ModelType.VGG16):
    super(DMVGG, self).__init__(None)
    assert model_type in [commons.ModelType.VGG16, commons.ModelType.VGG19]
    if model_type == commons.ModelType.VGG16:
      self.model_params = self.vgg16_params
    if model_type == commons.ModelType.VGG19:
      self.model_params = self.vgg19_params

  def get_input_shape(self):
    return (None, self.model_params.input_img_height,
            self.model_params.input_img_width, 3)
