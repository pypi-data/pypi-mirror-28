"""Vision related common definition.
"""

import abc

from deepmodels.core import commons
from deepmodels.core.models import commons as model_common


class DMImgModel(model_common.DMModel):
  """DeepModels image model base class.
  """
  pass


class DMGANModel(model_common.DMModel):
  """Generative Adversarial Networks base class.

  Now specific to image inputs.

  Attributes:
    generator: generator model.
    discriminator: discriminator model.
    img_shape: target image shape (height, width, channels).
  """
  generator = None
  discriminator = None
  img_shape = None

  def __init__(self, model_params_):
    self.model_params = model_params_
    self.img_shape = (self.model_params.input_img_height,
                      self.model_params.input_img_width, 3)

  @abc.abstractmethod
  def build_generator(self, inputs=None):
    """Build generator network.

    Args:
      inputs: input variable (optional if using random noise).

    Returns:
      generated image.
    """
    pass

  @abc.abstractmethod
  def build_discriminator(self, inputs=None):
    """Build discriminator model.

    Args:
      inputs: input variable (use built in).

    Returns:
      prediction output.
    """
    pass

  @abc.abstractmethod
  def build_model(self, inputs=None):
    pass

  def get_input_shape(self):
    return self.img_shape

  def save_model(self, model_fn):
    self.generator.save(model_fn)

  def load_model(self, model_fn):
    self.generator.save(model_fn)
