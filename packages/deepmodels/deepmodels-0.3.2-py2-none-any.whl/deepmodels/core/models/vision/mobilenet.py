"""MobileNet interface.
"""

import abc

from deepmodels.core import commons
from deepmodels.core.models import commons as model_commons


class DMMobileNet(model_commons.DMModel):
  """MobileNet class interface.
  """
  mobilenet_params = commons.ModelParams(
      model_name=commons.ModelType.model_names[commons.ModelType.MOBILENET],
      model_type=commons.ModelType.MOBILENET,
      input_img_width=224,
      input_img_height=244,
      cls_num=1000)

  @abc.abstractmethod
  def __init__(self):
    self.model_params = self.mobilenet_params

  def get_input_shape(self):
    return (None, self.model_params.input_img_height,
            self.model_params.input_img_width, 3)
