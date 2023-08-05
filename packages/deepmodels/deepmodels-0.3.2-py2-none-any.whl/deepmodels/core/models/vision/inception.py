"""Inception models.
"""

import abc

from deepmodels.core import commons
from deepmodels.core.models import commons as model_common


class DMInception(model_common.DMModel):
  """Inception model family.
  """
  inception_v3_params = commons.ModelParams(
      model_name=commons.ModelType.model_names[commons.ModelType.INCEPTION_V3],
      model_type=commons.ModelType.INCEPTION_V3,
      input_img_width=299,
      input_img_height=299,
      cls_num=1000)

  inception_v4_params = commons.ModelParams(
      model_name=commons.ModelType.model_names[commons.ModelType.INCEPTION_V4],
      model_type=commons.ModelType.INCEPTION_V4,
      input_img_width=299,
      input_img_height=299,
      cls_num=1000)

  @abc.abstractmethod
  def __init__(self, model_type=commons.ModelType.INCEPTION_V3):
    assert model_type == commons.ModelType.INCEPTION_V3
    self.model_params = self.inception_v3_params

  def get_input_shape(self):
    return (None, self.model_params.input_img_height,
            self.model_params.input_img_width, 3)
